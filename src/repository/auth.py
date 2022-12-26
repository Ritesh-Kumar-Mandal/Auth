from fastapi import HTTPException, status
from src import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_
from src.utils import cryptoUtil
from datetime import datetime, timedelta

## ---------------------------- Auth CRUD Operations-------------------------------
## To create new token for a password reset
def create_reset_code(request: schemas.EmailRequest, reset_code: str, db: Session):
    
    query=f"""INSERT INTO codes(email,reset_code,status,expired_in) 
                VALUES ('{request.email}','{reset_code}',1,'{(datetime.now()+timedelta(hours=8))}');"""

    db.execute(query)
    db.commit()

    return {"Message": f"Reset Code created successfully for User with email {request.email}."}

## Replacing the old password with the new password for the given email
def reset_password(new_password: str, email: str, db: Session):

    query = f"""UPDATE users SET password='{cryptoUtil.get_hash(new_password)}' WHERE email='{email}';"""

    db.execute(query)
    db.commit()

    return {"Message": f"Password reset successful for User with email {email}."}

## For diabling the reset token for the user after a successfull password reset
def disable_reset_code(reset_password_token: str, email: str, db: Session):

    query = f"""UPDATE codes 
                SET status='0' 
                WHERE 
                    status='1' 
                AND 
                    reset_code='{reset_password_token}'
                OR 
                    email='{email}'
                ;"""
    db.execute(query)
    db.commit()

    return {"Message": f"Reset code successfully disabled for User with email - {email}."}

## Finding if the user with the given email exsists or not
def find_existed_user(email: str, db: Session):

    user = db.query(models.User).filter(and_(models.User.email == email, models.User.is_active == True)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Either user with email {email} not found OR currently in-active !")
    return user

## Checking if the JWT token is used before and the user is no longer active
def find_token_black_lists(token: str, db: Session):
    token = db.query(models.Blacklists).filter(models.Blacklists.token == token).first()
    return True if token else False

## To check if the password reset token is valid or not
def check_reset_password_token(token: str, db: Session):
    query = f"""SELECT email FROM codes
                WHERE
                    status='1'
                AND
                    reset_code='{token}'
                AND
                    expired_in >= CURRENT_TIMESTAMP
                ;"""
    
    resultproxy = db.execute(query)

    #The end result is the list which contains query results in tuple format
    return [rowproxy for rowproxy in resultproxy]