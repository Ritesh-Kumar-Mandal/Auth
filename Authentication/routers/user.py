from fastapi import APIRouter, Depends, HTTPException, status, Response
from Authentication import schemas,database
from sqlalchemy.orm import Session
from typing import List
from Authentication.repository import user

# allow_create_resource = RoleChecker(["user"])

router = APIRouter(
    prefix="/user",
    tags=['User']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create(request: schemas.User, db: Session = Depends(database.get_db)):
    return user.create(request, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.User, db: Session = Depends(database.get_db)):
    return user.update(id, request, db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowUser)
def get(id: int, db: Session = Depends(database.get_db)):
    return user.get(id, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(database.get_db)):
    return user.delete(id, db)

@router.get('/', response_model=List[schemas.ShowUser])
def all(db: Session = Depends(database.get_db)):
    return user.get_all(db)



