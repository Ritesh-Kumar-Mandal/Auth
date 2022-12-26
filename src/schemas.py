from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

##--------------------------------- Pydantic models --------------------------------
##--------------------------------- User
class User(BaseModel):
    id: int
    full_name: str
    email: str
    password: str = 'pswd'
    role: Optional[str] = 'user'
    is_active: Optional[bool] = False
    tfa_enabled: Optional[bool] = False
    tfa_secret: Optional[str]
    created_on: Optional[datetime]
    updated_on: Optional[datetime]

class CreateUser(BaseModel):
    full_name: str
    email: str
    password: str

class CreateUserAdmin(BaseModel):
    full_name: str
    email: str
    password: str
    role:Optional[str] = 'user'
    is_active: Optional[bool] = True
    tfa_enabled: Optional[bool] = False

## Response Models
class ShowUser(BaseModel):
    full_name: str
    email: str
    role: str
    is_active: Optional[bool] = True
    tfa_enabled: bool
    created_on: Optional[datetime] = None

    class Config():
        orm_mode=True

## Update User
class UpdateUserBasicInfo(BaseModel):
    full_name: str

## Update the user creds
class ChangePassword(BaseModel):
    old_password: str = Field(..., example="Old password")
    new_password: str = Field(..., example="New password")
    confirm_password: str = Field(..., example="Confirm password")

## Basic info of the user
class UserBasicInfo(BaseModel):
    id: int
    email: str
    fullname: str
    role: str
    tfa_enabled: bool

## ---------------------------------  Token based login --------------------------------- 
class Token(BaseModel):
    access_token: str
    token_type: str

class Login(BaseModel):
    email: str
    password: str

## ---------------------------------  Password Reset --------------------------------- 
class EmailRequest(BaseModel):
    email: str

class ResetPassword(BaseModel):
    new_password: str
    confirm_password: str

## ---------------------------------  2FA --------------------------------- 
class LoginOTP(BaseModel):
    email: str
    otp: int

class Enable2FA(BaseModel):
    otp: int