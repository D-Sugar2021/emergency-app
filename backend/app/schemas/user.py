from pydantic import BaseModel, EmailStr

# Shared properties
class UserBase(BaseModel):
    email: EmailStr | None = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str

# Properties stored in DB
class UserInDBBase(UserBase):
    id: int
    is_active: bool
    hashed_password: str

    class Config:
        from_attributes = True

# Properties to return to client
class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
