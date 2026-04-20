from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: int
    firebase_uid: str
    email: EmailStr
    display_name: str | None = None
    role: str
    locale: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    display_name: str | None = None
    locale: str | None = None


class RoleChange(BaseModel):
    role: str
