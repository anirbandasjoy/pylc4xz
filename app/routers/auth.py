from datetime import timedelta
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from sqlalchemy import func
from pydantic import BaseModel
import bcrypt

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_password_hash,
)
from app.core.config import settings
from app.core.auth_dependencies import get_current_user
from app.core.builders import ExceptionBuilder
from app.models.user import (
    User,
    UserCreate,
    UserRead,
    UserLogin,
    Token,
    UserUpdatePassword,
    UserRole,
)
from app.utils.password_generator import password_generator, PasswordGenerator


router = APIRouter(prefix="/auth", tags=["Authentication"])


# Password Generator Schemas
class PasswordGenerateRequest(BaseModel):
    """Password generation request"""
    length: int = Query(default=16, ge=6, le=72, description="Password length")
    use_uppercase: bool = Query(default=True, description="Include uppercase letters")
    use_digits: bool = Query(default=True, description="Include numbers")
    use_special: bool = Query(default=True, description="Include special characters")
    avoid_ambiguous: bool = Query(default=False, description="Avoid ambiguous characters (0OIl1)")


class PasswordCheckRequest(BaseModel):
    """Password strength check request"""
    password: str


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Register a new user

    - **email**: User email address (must be unique)
    - **username**: Username (must be unique)
    - **password**: User password (6-72 bytes)
    - **first_name**: Optional first name
    - **last_name**: Optional last name
    """
    try:
        # Validate password length in BYTES (not characters)
        password_bytes = len(user_data.password.encode('utf-8'))

        if password_bytes > 72:
            return JSONResponse(
                content={
                    "success": False,
                    "message": f"Password too long ({password_bytes} bytes). Maximum 72 bytes allowed.",
                    "error_code": "PASSWORD_TOO_LONG",
                    "password_bytes": password_bytes
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if len(user_data.password) < 6:
            return JSONResponse(
                content={
                    "success": False,
                    "message": "Password must be at least 6 characters",
                    "error_code": "PASSWORD_TOO_SHORT"
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Check if email already exists
        existing_user = db.exec(
            select(User).where(User.email == user_data.email)
        ).first()

        if existing_user:
            return JSONResponse(
                content={
                    "success": False,
                    "message": "Email already registered",
                    "error_code": "EMAIL_EXISTS"
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Check if username already exists
        existing_username = db.exec(
            select(User).where(User.username == user_data.username)
        ).first()

        if existing_username:
            return JSONResponse(
                content={
                    "success": False,
                    "message": "Username already taken",
                    "error_code": "USERNAME_EXISTS"
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Check if this is the first user - make them admin
        user_count = db.exec(select(func.count()).select_from(User)).one()
        is_first_user = user_count == 0

        # Hash password with automatic truncation for bcrypt (max 72 bytes)
        # Convert to bytes and truncate to 72 bytes for bcrypt
        password_bytes = user_data.password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]

        # Use the truncated bytes directly with bcrypt
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')

        new_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role=UserRole.ADMIN if is_first_user else UserRole.USER,  # First user becomes admin
            is_verified=True if is_first_user else False  # First user is auto-verified
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except Exception as e:
        # Handle any unexpected errors
        import traceback
        error_details = traceback.format_exc()

        return JSONResponse(
            content={
                "success": False,
                "message": f"Registration failed: {str(e)}",
                "error_code": "REGISTRATION_ERROR",
                "debug": {
                    "error": str(e),
                    "password_length": len(user_data.password) if user_data.password else 0,
                    "password_bytes": len(user_data.password.encode('utf-8')) if user_data.password else 0
                }
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """
    Login with OAuth2 compatible token

    - **username**: Username or email
    - **password**: User password
    """
    # Try to find user by username or email
    user = db.exec(
        select(User).where(
            (User.username == form_data.username) | (User.email == form_data.username)
        )
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )

    # Update last login
    from datetime import datetime
    user.last_login = datetime.utcnow()
    db.commit()

    # Create tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token(
        data={
            "sub": user.username,
            "user_id": user.id,
            "email": user.email,
            "role": user.role
        },
        expires_delta=access_token_expires
    )

    refresh_token = create_refresh_token(
        data={
            "sub": user.username,
            "user_id": user.id
        },
        expires_delta=refresh_token_expires
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
) -> Any:
    """
    Refresh access token using refresh token

    - **refresh_token**: Valid refresh token
    """
    from app.core.security import verify_token

    payload = verify_token(refresh_token, token_type="refresh")

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user_id = payload.get("user_id")
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )

    # Create new tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token(
        data={
            "sub": user.username,
            "user_id": user.id,
            "email": user.email,
            "role": user.role
        },
        expires_delta=access_token_expires
    )

    new_refresh_token = create_refresh_token(
        data={
            "sub": user.username,
            "user_id": user.id
        },
        expires_delta=refresh_token_expires
    )

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.get("/me", response_model=UserRead)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get current user information

    Requires valid JWT token
    """
    return current_user


@router.put("/change-password")
async def change_password(
    password_data: UserUpdatePassword,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Change user password

    - **old_password**: Current password
    - **new_password**: New password (6-72 bytes)
    """
    try:
        # Validate new password length in BYTES (not characters)
        password_bytes = len(password_data.new_password.encode('utf-8'))

        if password_bytes > 72:
            return JSONResponse(
                content={
                    "success": False,
                    "message": f"Password too long ({password_bytes} bytes). Maximum 72 bytes allowed.",
                    "error_code": "PASSWORD_TOO_LONG",
                    "password_bytes": password_bytes
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if len(password_data.new_password) < 6:
            return JSONResponse(
                content={
                    "success": False,
                    "message": "Password must be at least 6 characters",
                    "error_code": "PASSWORD_TOO_SHORT"
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if not verify_password(password_data.old_password, current_user.hashed_password):
            return JSONResponse(
                content={
                    "success": False,
                    "message": "Incorrect current password",
                    "error_code": "INVALID_PASSWORD"
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Hash password with truncation for bcrypt
        password_bytes = password_data.new_password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]

        # Use bcrypt directly to hash the password bytes
        current_user.hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
        db.commit()

        return {
            "success": True,
            "message": "Password changed successfully"
        }

    except Exception as e:
        return JSONResponse(
            content={
                "success": False,
                "message": f"Password change failed: {str(e)}",
                "error_code": "PASSWORD_CHANGE_ERROR",
                "debug": {
                    "error": str(e),
                    "password_length": len(password_data.new_password) if password_data.new_password else 0,
                    "password_bytes": len(password_data.new_password.encode('utf-8')) if password_data.new_password else 0
                }
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ==================== Password Generator Endpoints ====================

@router.post("/generate-password")
async def generate_password(
    length: int = Query(default=16, ge=6, le=72, description="Password length"),
    use_uppercase: bool = Query(default=True, description="Include uppercase letters"),
    use_digits: bool = Query(default=True, description="Include numbers"),
    use_special: bool = Query(default=True, description="Include special characters"),
    avoid_ambiguous: bool = Query(default=False, description="Avoid ambiguous characters"),
    strong: bool = Query(default=False, description="Generate strong password with all character types"),
) -> Any:
    """
    Generate a secure random password
    
    - **length**: Password length (6-72 characters)
    - **use_uppercase**: Include uppercase letters
    - **use_digits**: Include numbers
    - **use_special**: Include special characters
    - **avoid_ambiguous**: Avoid ambiguous characters like 0, O, 1, l
    - **strong**: Generate strong password (guarantees all character types)
    """
    try:
        if strong:
            password = password_generator.generate_strong(length=length)
        else:
            password = password_generator.generate(
                length=length,
                use_uppercase=use_uppercase,
                use_digits=use_digits,
                use_special=use_special,
                avoid_ambiguous=avoid_ambiguous
            )
        
        # Check password strength
        strength_info = password_generator.check_strength(password)
        
        return {
            "success": True,
            "password": password,
            "length": len(password),
            "strength": strength_info
        }
    
    except Exception as e:
        return JSONResponse(
            content={
                "success": False,
                "message": f"Password generation failed: {str(e)}",
                "error_code": "PASSWORD_GENERATION_ERROR"
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.post("/generate-passphrase")
async def generate_passphrase(
    word_count: int = Query(default=4, ge=3, le=8, description="Number of words"),
    separator: str = Query(default="-", description="Separator between words")
) -> Any:
    """
    Generate a memorable passphrase using random words
    
    - **word_count**: Number of words (3-8)
    - **separator**: Separator between words (default: "-")
    
    Example output: correct-horse-battery-staple47$
    """
    try:
        passphrase = password_generator.generate_passphrase(
            word_count=word_count,
            separator=separator
        )
        
        # Check passphrase strength
        strength_info = password_generator.check_strength(passphrase)
        
        return {
            "success": True,
            "passphrase": passphrase,
            "word_count": word_count,
            "length": len(passphrase),
            "strength": strength_info
        }
    
    except Exception as e:
        return JSONResponse(
            content={
                "success": False,
                "message": f"Passphrase generation failed: {str(e)}",
                "error_code": "PASSPHRASE_GENERATION_ERROR"
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.post("/check-password-strength")
async def check_password_strength(
    password_data: PasswordCheckRequest
) -> Any:
    """
    Check password strength
    
    - **password**: Password to check
    
    Returns strength score and feedback
    """
    try:
        strength_info = password_generator.check_strength(password_data.password)
        
        return {
            "success": True,
            "password": "*" * len(password_data.password),  # Don't return actual password
            "strength": strength_info
        }
    
    except Exception as e:
        return JSONResponse(
            content={
                "success": False,
                "message": f"Password check failed: {str(e)}",
                "error_code": "PASSWORD_CHECK_ERROR"
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
