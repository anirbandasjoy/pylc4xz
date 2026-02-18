#!/usr/bin/env python3
"""
Database Migration Script (Sync Version)

This script drops all tables and recreates them with the latest schema.
WARNING: This will DELETE ALL DATA in the database!

Usage:
    python migrate_db.py --drop    # Drop all tables (DELETES ALL DATA!)
    python migrate_db.py --create  # Create tables only
    python migrate_db.py --check   # Check current schema
"""

import argparse
from sqlmodel import SQLModel
from app.core.database import sync_engine


def drop_all_tables():
    """Drop all tables in the database"""
    print("\n⚠️  Dropping all tables...")
    print("=" * 60)

    SQLModel.metadata.drop_all(sync_engine)
    print("✅ All tables dropped successfully!")

    return True


def create_all_tables():
    """Create all tables in the database"""
    print("\n🔄 Creating tables...")

    # Import all models to ensure they're registered with metadata
    from app.models.user import User

    SQLModel.metadata.create_all(sync_engine)
    print("✅ All tables created successfully!")

    return True


def check_schema():
    """Check current database schema"""
    print("\n🔍 Checking current database schema...")
    print("=" * 60)

    from sqlalchemy import inspect
    inspector = inspect(sync_engine)

    tables = inspector.get_table_names()

    if not tables:
        print("   No tables found in database")
    else:
        print(f"\n   Found {len(tables)} table(s):")
        for table in tables:
            print(f"   → {table}")

            # Get columns
            columns = inspector.get_columns(table)
            print(f"      Columns: {', '.join([col['name'] for col in columns])}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Database migration script for FastAPI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --drop              Drop all tables (DELETES ALL DATA!)
  %(prog)s --drop --create     Drop and recreate all tables
  %(prog)s --create            Create tables without dropping
  %(prog)s --check             Check current database schema
        """
    )

    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop all tables (WARNING: deletes all data)"
    )

    parser.add_argument(
        "--create",
        action="store_true",
        help="Create all tables"
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help="Check current database schema"
    )

    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("🗄️  Database Migration Tool")
    print("=" * 60)

    # Check schema mode
    if args.check:
        check_schema()
        print("\n" + "=" * 60 + "\n")
        return

    # Create only mode
    if args.create and not args.drop:
        create_all_tables()
        print("\n✅ Tables created successfully!")
        print("=" * 60 + "\n")
        return

    # Drop and create mode
    if args.drop:
        print("\n⚠️  WARNING: This will DELETE ALL DATA!")
        confirm = input("   Type 'YES' to confirm: ")

        if confirm != "YES":
            print("\n❌ Migration cancelled!")
            print("=" * 60 + "\n")
            return

        drop_all_tables()

        if args.create:
            create_all_tables()
            print("\n✅ Migration completed successfully!")
            print("   Database is now fresh and ready!")
            print("\n💡 Next steps:")
            print("   1. Start your FastAPI server: python main.py")
            print("   2. Register first user (will become admin automatically)")
        else:
            print("\n✅ Tables dropped successfully!")
            print("   Run with --create to recreate tables")

        print("=" * 60 + "\n")
        return

    # No action specified
    print("\n❌ No action specified!")
    print("   Use --help to see available options")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
