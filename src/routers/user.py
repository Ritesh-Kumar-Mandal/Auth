from fastapi import APIRouter, Depends, HTTPException, status, Response
from src import schemas
from sqlalchemy.orm import Session
from src.repository import user
from src.utils import dbUtil,jwtUtil
from src.utils.roleCheckerUtil import RoleChecker

allow_create_resource = RoleChecker(["user","admin"])

router = APIRouter(
    prefix="/user",
    tags=['User'],
    dependencies=[Depends(allow_create_resource), Depends(dbUtil.get_db), Depends(jwtUtil.get_current_active_user)]
)


@router.get('/', status_code=200, response_model=schemas.ShowUser)
def get(db: Session = Depends(dbUtil.get_db), current_user: schemas.User = Depends(jwtUtil.get_current_active_user)):
    return user.get_user_profile(current_user.id, db)

@router.get('/2fa-qr', status_code=200, summary='Get 2FA QR')
def get(db: Session = Depends(dbUtil.get_db), current_user: schemas.User = Depends(jwtUtil.get_current_active_user)):
    return user.get_2fa_qr(current_user.id, db)

@router.patch('/', status_code=status.HTTP_202_ACCEPTED)
def update(request: schemas.UpdateUserBasicInfo, db: Session = Depends(dbUtil.get_db), current_user: schemas.User = Depends(jwtUtil.get_current_active_user)):
    return user.update(current_user.id, request, db)

@router.put('/', status_code=status.HTTP_202_ACCEPTED)
def change_password(request: schemas.ChangePassword, db: Session = Depends(dbUtil.get_db), current_user: schemas.User = Depends(jwtUtil.get_current_active_user)):
    return user.change_password(current_user.email, request, db)

@router.put('/enable-2fa', status_code=status.HTTP_202_ACCEPTED, summary='Enable 2 Factor Authentication')
def enable_2FA(request: schemas.Enable2FA, db: Session = Depends(dbUtil.get_db), current_user: schemas.User = Depends(jwtUtil.get_current_active_user)):
    return user.enable_2fa(current_user.id, request, db)

@router.put("/disable-2fa", status_code=status.HTTP_202_ACCEPTED, summary='Disable 2 Factor Authentication')
def logout(db: Session = Depends(dbUtil.get_db), current_user: schemas.User = Depends(jwtUtil.get_current_active_user)):
    return user.disable_2fa(current_user.id, db)


@router.get("/logout")
def logout(token: str = Depends(jwtUtil.get_token_user), db: Session = Depends(dbUtil.get_db), current_user: schemas.User = Depends(jwtUtil.get_current_active_user)):
    user.set_black_list(token, current_user, db)
    return {"message": "User logged out successfully."}





