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
    email: str
    password: str
##--------------------------------- User
class User(BaseModel):
    username: str
    full_name: str
    email: str
    password: str
    role: Optional[str] = 'user'
    is_active: Optional[bool] = True


## Response Models
class ShowUser(BaseModel):
    username: str
    full_name: str
    email: str
    role: str
    is_active: Optional[bool] = True

    class Config():
        orm_mode=True

## Update User
class UpdateUser(User):
    username: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[int] = None
    password: Optional[str] = None
    role: Optional[str] = 'user'
    is_active: Optional[bool] = True
