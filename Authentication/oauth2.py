from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from Lifeopedia import token, database, models
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(_token_: str = Depends(oauth2_scheme)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = token.verify_token(_token_, credentials_exception)

    user = get_user(email=token_data.email)

    if user is None:
        raise credentials_exception
    return user

def get_user(email: str):
    return Session.query(models.User).filter(models.User.email == email).first()