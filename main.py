from fastapi import FastAPI
from Authentication import models
from Authentication.database import engine
from Authentication.routers import user,admin,authentication


## -------------------------------- Database connection initialization --------------------------------
models.Base.metadata.create_all(bind=engine)

## -------------------------------- App initialization --------------------------------
app = FastAPI()


## -------------------------------- Register Route for {Authentication} -------------------------------
app.include_router(authentication.router)
## -------------------------------- Register Route for {Admin} -------------------------------
app.include_router(admin.router)
## -------------------------------- Register Route for {User} -------------------------------
app.include_router(user.router)

## uvicorn main:app --reload