from fastapi import HTTPException, status
import bcrypt

from .models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from .schemas import CreateUserPayload


class UserService:

    async def get_user_by_username(self, username: str, session: AsyncSession) -> User:
        statement = select(User).where(User.username == username)
        try:
            result = await session.exec(statement)
            user = result.first()
        except Exception as e:
            raise Exception(str(e))
        return user

    async def get_user_by_email(self, email: str, session: AsyncSession) -> User:
        statement = select(User).where(User.email == email)
        try:
            result = await session.exec(statement)
            user = result.first()
        except Exception as e:
            raise Exception(str(e))
        return user

    async def create_user(
        self, payload: CreateUserPayload, session: AsyncSession
    ) -> User:
        try:
            get_user = await self.get_user_by_username(payload.username, session)
        except Exception:
            raise
        if get_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this username already exists",
            )
        else:
            try:
                get_user_email = await self.get_user_by_email(payload.email, session)
            except Exception:
                raise
            if get_user_email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with this email already exists",
                )
        user = User(
            username=payload.username,
            email=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
        )
        user.password_hash = bcrypt.hashpw(
            payload.password.encode("utf-8"), bcrypt.gensalt()
        )

        try:
            session.add(user)
            await session.commit()
            await session.refresh(user)
        except Exception as e:
            await session.rollback()
            raise Exception(str(e))
        return user
