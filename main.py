from fastapi import FastAPI
from app.database import engine, Base
from routers import users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI JWT Auth")

app.include_router(users.router)
