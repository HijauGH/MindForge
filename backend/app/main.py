from fastapi import FastAPI

from routers.auth import auth
from os import getenv

app = FastAPI(
    title=getenv("TITLE"),
    version=getenv("VERSION"),
    description=getenv("DESCRIPTION")
)

app.include_router(auth)