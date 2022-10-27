from fastapi import APIRouter, Depends, HTTPException, status, Response
from Authentication import schemas,database, auth
from typing import List
from sqlalchemy.orm import Session
from Authentication.repository import admin,user
from Authentication.role_checker import RoleChecker

allow_create_resource = RoleChecker(["admin"])

router = APIRouter(
    prefix="/admin",
    tags=['Admin'],
    dependencies=[Depends(allow_create_resource), Depends(database.get_db), Depends(auth.get_current_active_user)]
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create(request: schemas.User, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    return user.create(request, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    return admin.delete(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.User, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    return admin.update(id, request, db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowUser)
def get(id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    return user.get(id, db)

@router.get('/', response_model=List[schemas.ShowUser])
def all(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    return admin.get_all(db)