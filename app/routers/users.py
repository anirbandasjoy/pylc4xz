from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select

from app.core.database import get_db
from app.core.auth_dependencies import get_current_user, require_admin, require_moderator_or_admin
from app.models.user import User, UserRead, UserUpdate, UserRole


router = APIRouter(prefix="/users", tags=["User Management"])


@router.get("/", response_model=List[UserRead])
async def get_all_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of users to return"),
    current_user: User = Depends(require_moderator_or_admin),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get all users (Admin/Moderator only)

    - **skip**: Number of users to skip (pagination)
    - **limit**: Maximum number of users to return (pagination)
    """
    users = db.exec(
        select(User)
        .offset(skip)
        .limit(limit)
    ).all()

    return users


@router.get("/me", response_model=UserRead)
async def get_my_profile(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get my profile

    Returns the current user's profile information
    """
    return current_user


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    user_id: int,
    current_user: User = Depends(require_moderator_or_admin),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get user by ID (Admin/Moderator only)

    - **user_id**: The ID of the user to retrieve
    """
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.put("/me", response_model=UserRead)
async def update_my_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Update my profile

    - **email**: New email address
    - **username**: New username
    - **first_name**: New first name
    - **last_name**: New last name
    """
    # Check if email is being changed and if it's already taken
    if user_data.email and user_data.email != current_user.email:
        existing_user = db.exec(
            select(User).where(User.email == user_data.email)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken"
            )
        current_user.email = user_data.email

    # Check if username is being changed and if it's already taken
    if user_data.username and user_data.username != current_user.username:
        existing_user = db.exec(
            select(User).where(User.username == user_data.username)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        current_user.username = user_data.username

    # Update other fields
    if user_data.first_name is not None:
        current_user.first_name = user_data.first_name

    if user_data.last_name is not None:
        current_user.last_name = user_data.last_name

    from datetime import datetime
    current_user.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(current_user)

    return current_user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
) -> Any:
    """
    Update user by ID (Admin only)

    - **user_id**: The ID of the user to update
    - **email**: New email address
    - **username**: New username
    - **first_name**: New first name
    - **last_name**: New last name
    - **role**: New role (admin, user, moderator)
    - **is_active**: Activate/deactivate user
    - **is_verified**: Verify/unverify user
    """
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Prevent admin from deactivating themselves
    if user.id == current_user.id and user_data.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot deactivate yourself"
        )

    # Update fields
    update_data = user_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if hasattr(user, key):
            setattr(user, key, value)

    from datetime import datetime
    user.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(user)

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
) -> None:
    """
    Delete/terminate user by ID (Admin only)

    - **user_id**: The ID of the user to delete
    """
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Prevent admin from deleting themselves
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot delete yourself"
        )

    db.delete(user)
    db.commit()


@router.patch("/{user_id}/activate", response_model=UserRead)
async def activate_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
) -> Any:
    """
    Activate user account (Admin only)

    - **user_id**: The ID of the user to activate
    """
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.is_active = True

    from datetime import datetime
    user.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(user)

    return user


@router.patch("/{user_id}/deactivate", response_model=UserRead)
async def deactivate_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
) -> Any:
    """
    Deactivate user account (Admin only)

    - **user_id**: The ID of the user to deactivate
    """
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Prevent admin from deactivating themselves
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot deactivate yourself"
        )

    user.is_active = False

    from datetime import datetime
    user.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(user)

    return user


@router.patch("/{user_id}/verify", response_model=UserRead)
async def verify_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
) -> Any:
    """
    Verify user email (Admin only)

    - **user_id**: The ID of the user to verify
    """
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.is_verified = True

    from datetime import datetime
    user.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(user)

    return user


@router.get("/stats/count", response_model=dict)
async def get_user_count(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get user statistics (Admin only)

    Returns total, active, and verified user counts
    """
    total_users = db.exec(select(User)).all()

    active_count = sum(1 for user in total_users if user.is_active)
    verified_count = sum(1 for user in total_users if user.is_verified)
    admin_count = sum(1 for user in total_users if user.role == UserRole.ADMIN)

    return {
        "total_users": len(total_users),
        "active_users": active_count,
        "verified_users": verified_count,
        "admin_users": admin_count
    }
