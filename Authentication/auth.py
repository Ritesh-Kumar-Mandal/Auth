from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from Authentication import models,schemas,database
from sqlalchemy.orm import Session
from passlib.context import CryptContext


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
##---------------------------- oauth2 --------------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

## ---------------------------- Current user ---------------------------
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token, credentials_exception)

    user = get_user(db, email=token_data.email)

    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if not bool(current_user.is_active):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

##---------------------------- token --------------------------------
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

        return schemas.TokenData(email=email)

    except JWTError:
        raise credentials_exception

## ---------------------------- Hashing --------------------------------
## For password encryption and verfications
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def bcrypt(password: str):
        return pwd_cxt.hash(password)

def verify(hashed_password, plain_password):
    return pwd_cxt.verify(plain_password, hashed_password)

## ---------------------------- Authenticate -------------------------------
def get_user(db:Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with email {email} not found !")
    return user

def authenticate_user(db:Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify(password, user.hashed_password):
        return False
    return user