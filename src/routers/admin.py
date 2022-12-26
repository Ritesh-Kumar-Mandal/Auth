from fastapi import APIRouter, Depends, HTTPException, status, Response
from src import schemas
from typing import List
from sqlalchemy.orm import Session
from src.repository import user
from src.utils import dbUtil,jwtUtil
from src.utils.roleCheckerUtil import RoleChecker

allow_create_resource = RoleChecker(["admin"])

router = APIRouter(
    prefix="/admin",
    tags=['Admin'],
    dependencies=[Depends(allow_create_resource), Depends(dbUtil.get_db), Depends(jwtUtil.get_current_active_user)]
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create(request: schemas.CreateUserAdmin, db: Session = Depends(dbUtil.get_db), current_user: schemas.User = Depends(jwtUtil.get_current_active_user)):
    return user.create(request, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(dbUtil.get_db), current_user: schemas.User = Depends(jwtUtil.get_current_active_user)):
    return user.delete(id, db)


@router.patch('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.UpdateUserBasicInfo, db: Session = Depends(dbUtil.get_db), current_user: schemas.User = Depends(jwtUtil.get_current_active_user)):
    return user.update(id, request, db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def reset_password(id: int, request: schemas.ResetPassword, db: Session = Depends(dbUtil.get_db), current_user: schemas.User = Depends(jwtUtil.get_current_active_user)):
    return user.reset_password(id, request, db)

@router.get('/{id}', status_code=200, response_model=schemas.ShowUser)
def get(id: int, db: Session = Depends(dbUtil.get_db), current_user: schemas.User = Depends(jwtUtil.get_current_active_user)):
    return user.get_user_profile(id, db)

@router.get('/', response_model=List[schemas.ShowUser])
def all(db: Session = Depends(dbUtil.get_db), current_user: schemas.User = Depends(jwtUtil.get_current_active_user)):
    return user.get_all_user_profile(db)