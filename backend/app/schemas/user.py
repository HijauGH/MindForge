from pydantic import BaseModel, EmailStr, SecretStr
from datetime import datetime

class User(BaseModel):
    id: int
    email: EmailStr
    hashed_password: SecretStr
    username: str
    create_at: datetime
