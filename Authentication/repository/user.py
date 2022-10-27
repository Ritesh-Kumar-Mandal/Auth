from fastapi import HTTPException, status
from Authentication import models,schemas,auth
from typing import Optional, List
from sqlalchemy.orm import Session


def create(request: schemas.User, db: Session):

    new_user = models.User(username=request.username,
                            full_name=request.full_name,
                            email=request.email,
                            password=auth.bcrypt(request.password),
                            role='user'
                            )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def get(id: int,  db: Session):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found !")
    return user

def update(id: int, request: schemas.UpdateUser, db: Session):

    user = db.query(models.User).filter(models.User.id == id)
    
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")
    
    user_data = request.dict(exclude_unset=True)

    for key, value in user_data.items():
        if key.lower()=='password':
            user_data[key] = auth.bcrypt(value)
        elif key.lower()=='role':
            user_data[key] = 'user'
           
        setattr(user, key, value)

    user.update(user_data)
    db.commit()
    
    return {"Message": f"User with id {id} updated successfully"}