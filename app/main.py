from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI JWT Auth")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
