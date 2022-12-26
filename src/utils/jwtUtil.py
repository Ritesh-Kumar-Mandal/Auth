from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import ValidationError
from src.utils import constantUtil,dbUtil
from src.repository import auth
from src import schemas

##---------------------------- oauth2 --------------------------------
## Login for token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_token_user(token: str = Depends(oauth2_scheme)):
    return token

## Creating access token by embedding the user details and the expiration timestamp
def create_access_token(*, subject: str, expires_delta: int):

    to_encode = {"subject":subject, "expiration": (datetime.now() + timedelta(minutes=expires_delta)).strftime("%Y-%m-%d %H:%M:%S")}

    encoded_jwt = jwt.encode(to_encode, constantUtil.SECRET_KEY, algorithm=constantUtil.ALGORITHM)

    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(dbUtil.get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, constantUtil.SECRET_KEY, algorithms=[constantUtil.ALGORITHM])
        username = payload.get("subject")
        expiration = datetime.strptime(payload.get("expiration"), "%Y-%m-%d %H:%M:%S")
        
        if username is None:
            raise credentials_exception
        
        ## To check if the user have logged out or the token has expired
        black_list = auth.find_token_black_lists(token, db)
        if black_list or (expiration<=datetime.now()):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Token Experied! Please login again. ")
        
    except (JWTError, ValidationError):
        raise credentials_exception

    # print("======================================",payload,"======================================",)

    user = auth.find_existed_user(username, db);
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if not bool(current_user.is_active):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
