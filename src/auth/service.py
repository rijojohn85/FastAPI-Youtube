from datetime import timedelta
from src.utils import logger

from fastapi import HTTPException, status
import bcrypt

from .models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from .schemas import CreateUserPayload, UserLoginPayload
from .utils import verfiy_password_hash, create_access_token
from fastapi.responses import JSONResponse


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
            raise Exception
        return user

    async def login_user(
        self, payload: UserLoginPayload, session: AsyncSession
    ) -> JSONResponse:

        user = await self.get_user_by_username(payload.username, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
        verified = verfiy_password_hash(
            password_hash=user.password_hash, password=payload.password
        )
        if not verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
        userdata = {
            "uid": str(user.uid),
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        access_token = create_access_token(
            data=userdata, expires_delta=timedelta(minutes=2)
        )
        refresh_token = create_access_token(
            data=userdata, expires_delta=timedelta(days=2), refresh=True
        )
        return JSONResponse(
            {
                "message": "login successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user_data": userdata,
            }
        )
