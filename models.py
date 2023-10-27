from pydantic import BaseModel









class User(BaseModel):
    uname: str
    password: str

class loginRes(BaseModel):
    id: int
    uname: str
    Role: str
    password: str