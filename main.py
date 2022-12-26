from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src import models
from src.utils.dbUtil import engine
from src.routers import auth, user,admin
import uvicorn

## -------------------------------- Database connection initialization --------------------------------
models.Base.metadata.create_all(bind=engine)

## -------------------------------- App initialization --------------------------------
app = FastAPI(
    docs_url="/docs",
    redoc_url="/redocs",
    title="CRUD [Python(FastAPI)]",
    description="A FastAPI app which will allow us to perform basic CRUD operation and also include JWT and Two-Factor Authentication based login.",
    version="0.1.0",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## -------------------------------- Register Route for {Authentication} -------------------------------
app.include_router(auth.router)
## -------------------------------- Register Route for {Admin} -------------------------------
app.include_router(admin.router)
## -------------------------------- Register Route for {User} -------------------------------
app.include_router(user.router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
## uvicorn main:app --reload