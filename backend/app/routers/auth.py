from fastapi import APIRouter, HTTPException
from uuid import uuid4

from backend.app.utils.dependencies import security
from backend.app.schemas.user import User


auth = APIRouter(
    prefix="/auth",
    tags=["auth", "register", "login"]
)


@auth.post("/register")
async def register():
    pass


@auth.post("/login")
async def login(cred: User):
    if cred.username == "admin" and cred.password == "admin":
        token = security.create_access_token(uid=str(uuid4()))
        return {"access_token": token}

    raise HTTPException(status_code=401, detail="Incorrect username or password")


#@app.post("/registry", response_model=UserOut, status_code=status.HTTP_201_CREATED)
#async def registry(user: UserCreate, db: Session = Depends())