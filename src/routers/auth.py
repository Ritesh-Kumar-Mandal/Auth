from fastapi import APIRouter, Depends, HTTPException, status
from src import models,schemas
from src.repository import user, auth
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import uuid
from src.utils import dbUtil,cryptoUtil,jwtUtil,emailUtil,otpUtil,constantUtil


router = APIRouter(
    tags=['Auth']
)

@router.post('/login')
def login_for_access_token(request: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(dbUtil.get_db)):
    
    ## To see if username/email exsist in Database
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Creadentials. !")
    
    if not cryptoUtil.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect Password. !")

    ## Generate and return JWT token
    access_token = jwtUtil.create_access_token(subject=user.email,expires_delta=constantUtil.ACCESS_TOKEN_EXPIRE_MINUTES)

    ## Change the active status of the user -->True(1)
    query=f"""UPDATE users SET is_active={1}, updated_on='{datetime.utcnow()}' WHERE email='{user.email}';"""
    db.execute(query)
    db.commit()

    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_info": {
            "email": user.email,
            "fullname": user.full_name
        }
    }

@router.post('/login-otp')
def login_with_otp_for_access_token(request: schemas.LoginOTP , db: Session = Depends(dbUtil.get_db)):
    
    ## To see if username/email exsist in Database
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Creadentials. !")

    if not otpUtil.verify_otp(user.tfa_secret, request.otp):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"Incorrect OTP. !")

    ## Generate and return JWT token
    access_token = jwtUtil.create_access_token(subject=user.email,expires_delta=constantUtil.ACCESS_TOKEN_EXPIRE_MINUTES)

    ## Change the active status of the user -->True(1)
    query=f"""UPDATE users SET is_active={1}, updated_on='{datetime.utcnow()}' WHERE email='{user.email}';"""
    db.execute(query)
    db.commit()

    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_info": {
            "email": user.email,
            "fullname": user.full_name
        }
    }

@router.post("/register")
def register(request: schemas.CreateUser, db: Session = Depends(dbUtil.get_db)):
    ## To see if username/email exsist in Database
    usr = db.query(models.User).filter(models.User.email == request.email).first()

    if usr:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User already registered. !")

    # Create new user
    return user.create(request, db)

@router.post("/auth/forgot-password")
async def forgot_password(request: schemas.EmailRequest, db: Session = Depends(dbUtil.get_db)):
    
    # Check exited user
    ## To see if username/email exsist in Database
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email {request.email} doesn't exsist !")

    # Create reset code and save it in database
    reset_code = str(uuid.uuid1())
    auth.create_reset_code(request, reset_code, db)

    # Sending email
    subject = "Testing Email For Dev."
    recipient = [request.email]
    message = f"""
    <!DOCTYPE html>
    <html>
    <title>Reset Password</title>
    <body>
    <div style="width:100%;font-family: monospace;">
        <h1>Hello, {request.email}</h1>
        <p>Someone has requested a link to reset your password. If you requested this, you can change your password through the button below.</p>
        <a href="http://127.0.0.1:8000/docs/auth/reset-password?reset_password_token={reset_code}" style="box-sizing:border-box;border-color:#1f8feb;text-decoration:none;background-color:#1f8feb;border:solid 1px #1f8feb;border-radius:4px;color:#ffffff;font-size:16px;font-weight:bold;margin:0;padding:12px 24px;text-transform:capitalize;display:inline-block" target="_blank">Reset Your Password</a>
        <p>If you didn't request this, you can ignore this email.</p>
        <p>Your password won't change until you access the link above and create a new one.</p>
    </div>
    </body>
    </html>
    """
    await emailUtil.send_email(subject, recipient, message)

    return {
        "code": 200,
        "message": "We've sent an email with instructions to reset your password."
    }

@router.post("/auth/reset-password")
def reset_password(reset_password_token: str, request: schemas.ResetPassword, db: Session = Depends(dbUtil.get_db)):
    
    # Check valid reset password token | return list of email
    user_email = auth.check_reset_password_token(reset_password_token, db)
    
    if not user_email:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"Reset password token has expired, please request a new one. !")

    ## Extracting the email from the nested tuple in list structure
    user_email = user_email[0][0]

    # Check both new & confirm password are matched
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"New Password & Confirm Password doesn't match. !")

    # Reset new password
    auth.reset_password(request.new_password, user_email, db)

    # Disable reset code
    auth.disable_reset_code(reset_password_token, user_email, db)

    return {
        "code": 200,
        "message": f"Password has been reset successfully for User with email {user_email}."
    } 