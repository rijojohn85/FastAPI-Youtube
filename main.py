from typing import Optional, Any

from fastapi import FastAPI, Header, status
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def read_root()->dict[str, str]:
    return {"message": "Hello World"}

#path parameter
@app.get('/greet/{name}')
async def greet(name: str)->dict[str, str]:
    return {'message': f'Hello, {name}'}

#query parameter
@app.get('/hello')
async def hello(name: str)->dict[str, str]:
    return {'message': f'Hello, {name}'}

#query and path parameter
@app.get('/greet2/{name}')
async def greet2(name: str, age: int)->dict[str, str]:
    return {'message': f'Hello, {name} age: {age}'}

#optional query parameters
@app.get('/hello2')
async def hello(age:int, name: Optional[str] = "rijo")->dict[str, str]:
    return {'message': f'Hello, {name} age{age}'}

#schema for create book payload
class BookCreatePayload(BaseModel):
    title: str
    author: str
#end point for creating book
@app.post('/create_book')
async def create_book(payload: BookCreatePayload)->dict[str, str]:
    return {
        "title": payload.title,
        "author": payload.author
    }

#end point for request headers
@app.get('/get_headers', status_code=status.HTTP_200_OK)
async def get_headers(
        accept:str = Header(None),
        content_type: Optional[str] = Header(None),
        user_agent: Optional[str] = Header(None),
        host: Optional[str] = Header(None),
)->dict[str, Any]:
    request_headers = {}
    request_headers['Accept'] = accept
    request_headers['Content-Type'] = content_type
    request_headers['User-Agent'] = user_agent
    request_headers['Host'] = host
    return request_headers
