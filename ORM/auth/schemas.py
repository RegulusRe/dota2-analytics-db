from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Схема для створення користувача"""
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Схема для входу користувача"""
    username: str
    password: str


class UserResponse(BaseModel):
    """Схема для відповіді з даними користувача"""
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Схема для JWT токену"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Схема для даних з токену"""
    username: str | None = None
