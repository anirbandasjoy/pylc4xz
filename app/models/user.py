from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """User roles enum"""
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"


class UserBase(SQLModel):
    """Base User model"""
    email: str = Field(index=True, unique=True, max_length=255)
    username: str = Field(max_length=100)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    role: UserRole = Field(default=UserRole.USER)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)


class User(UserBase, table=True):
    """User table model"""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = Field(default=None)


class UserCreate(SQLModel):
    """User registration schema"""
    email: str = Field(max_length=255)
    username: str = Field(max_length=100)
    password: str = Field(min_length=6, max_length=72, description="Password must be between 6 and 72 characters")
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)


class UserUpdate(SQLModel):
    """User update schema"""
    email: Optional[str] = Field(default=None, max_length=255)
    username: Optional[str] = Field(default=None, max_length=100)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


class UserUpdatePassword(SQLModel):
    """User password update schema"""
    old_password: str
    new_password: str = Field(min_length=6, max_length=72, description="Password must be between 6 and 72 characters")


class UserRead(UserBase):
    """User response schema"""
    id: int
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None


class UserLogin(SQLModel):
    """User login schema"""
    username: str
    password: str


class Token(SQLModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(SQLModel):
    """Token data schema"""
    username: Optional[str] = None
    user_id: Optional[int] = None
