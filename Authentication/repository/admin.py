from fastapi import HTTPException, status
from Authentication import models,schemas,auth
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session


def delete(id: int, db: Session):

    user = db.query(models.User).filter(models.User.id == id)
    
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")

    user.delete(synchronize_session=False)
    db.commit()

    return {"Message": f"User with id {id} deleted successfully"}

def update(id: int, request: schemas.User, db: Session):

    user = db.query(models.User).filter(models.User.id == id)
    
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")
    
    user_data = request.dict(exclude_unset=True)

    for key, value in user_data.items():
        if key.lower()=='password':
            user_data[key] = auth.bcrypt(value)
        
        setattr(user, key, value)

    user.update(user_data)
    db.commit()
    
    return {"Message": f"User with id {id} updated successfully"}


def get_all(db: Session):
    users = db.query(models.User).all()
    return users