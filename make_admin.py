#!/usr/bin/env python3
"""
Quick script to make a user admin directly via database
Usage: python3 make_admin.py <username>
"""

import sys
from sqlmodel import Session, select
from app.core.database import sync_engine
from app.models.user import User

def make_user_admin(username: str):
    """Update user role to admin"""
    with Session(sync_engine) as session:
        # Find user by username
        user = session.exec(
            select(User).where(User.username == username)
        ).first()

        if not user:
            print(f"❌ User '{username}' not found!")
            return False

        print(f"\n👤 Found user:")
        print(f"   ID:       {user.id}")
        print(f"   Username: {user.username}")
        print(f"   Email:    {user.email}")
        print(f"   Role:     {user.role}")
        print(f"   Active:   {user.is_active}")
        print(f"   Verified: {user.is_verified}")

        # Update to admin
        user.role = "admin"
        user.is_verified = True
        session.commit()
        session.refresh(user)

        print(f"\n✅ User updated successfully!")
        print(f"   New role: {user.role}")
        print(f"   Verified: {user.is_verified}")
        print(f"\n💡 You can now login and use admin features!")

        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 make_admin.py <username>")
        print("\nExample:")
        print("  python3 make_admin.py admin")
        sys.exit(1)

    username = sys.argv[1]
    make_user_admin(username)
