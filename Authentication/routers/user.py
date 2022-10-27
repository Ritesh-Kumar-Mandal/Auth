from fastapi import APIRouter, Depends, HTTPException, status, Response
from Authentication import schemas,database,auth
from sqlalchemy.orm import Session
from typing import List
from Authentication.repository import user
from Authentication.role_checker import RoleChecker

allow_create_resource = RoleChecker(["user","admin"])

router = APIRouter(
    prefix="/user",
    tags=['User'],
    dependencies=[Depends(allow_create_resource), Depends(database.get_db), Depends(auth.get_current_active_user)]
)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.User, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    return user.update(id, request, db)

@router.get('/{id}', status_code=200, response_model=schemas.ShowUser)
def get(id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    return user.get(id, db)




