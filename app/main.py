from fastapi import FastAPI
from .router import users_router


app = FastAPI()


app.include_router(users_router)