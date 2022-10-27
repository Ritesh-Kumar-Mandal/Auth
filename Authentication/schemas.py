from pydantic import BaseModel
from typing import Optional, List

##--------------------------------- Pydantic models --------------------------------
##--------------------------------- 
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

class Login(BaseModel):
    username: str
    password: str
##--------------------------------- User
class User(BaseModel):
    username: str
    full_name: str
    email: str
    password: str
    role: Optional[str] = 'user'


## Response Models
class ShowUser(User):
    username: str
    full_name: str
    email: str
    role: str

    class Config():
        orm_mode=True
