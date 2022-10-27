from fastapi import APIRouter, Depends, HTTPException, status
from Authentication import models,schemas,database
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from .. auth import authenticate_user,verify,create_access_token


router = APIRouter(
    tags=['Authentication']
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post('/token')
def login_for_access_token(request: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(database.get_db)):
    
    ## To see if username/email exsist in Database
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Creadentials. !")
    
    if not verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect Password. !")

    ## Generate and return JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}