from fastapi import Depends, HTTPException, status, Response
from src import schemas
from typing import List
from src.utils import jwtUtil

class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: schemas.User = Depends(jwtUtil.get_current_user)):
        if user.role.lower() not in self.allowed_roles:
            # logger.debug(f"User with role {user.role} not in {self.allowed_roles}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")