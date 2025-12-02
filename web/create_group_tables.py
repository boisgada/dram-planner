#!/usr/bin/env python3
"""
Script to create group tables directly in the database.
This bypasses Alembic migrations to fix the immediate issue.
"""
import os
import sys
from sqlalchemy import create_engine, text

# Get database URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://dramplanner:dramplanner@db:5432/dramplanner')

# SQL statements to create tables
SQL_STATEMENTS = [
    # Master Beverage Catalog
    """
    CREATE TABLE IF NOT EXISTS master_beverages (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        brand VARCHAR(255),
        category VARCHAR(50) NOT NULL,
        subcategory VARCHAR(100),
        abv FLOAT,
        region VARCHAR(100),
        country VARCHAR(100),
        description TEXT,
        tasting_notes TEXT,
        image_url VARCHAR(500),
        external_id VARCHAR(100),
        source VARCHAR(50),
        verified BOOLEAN,
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS ix_master_beverages_name ON master_beverages(name);
    """,
    """
    CREATE INDEX IF NOT EXISTS ix_master_beverages_category ON master_beverages(category);
    """,
    """
    CREATE INDEX IF NOT EXISTS ix_master_beverages_brand ON master_beverages(brand);
    """,
    
    # User Groups
    """
    CREATE TABLE IF NOT EXISTS user_groups (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        is_private BOOLEAN,
        created_by_id INTEGER NOT NULL REFERENCES users(id),
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    );
    """,
    
    # Group Memberships
    """
    CREATE TABLE IF NOT EXISTS group_memberships (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id),
        group_id INTEGER NOT NULL REFERENCES user_groups(id),
        role VARCHAR(20),
        joined_at TIMESTAMP,
        UNIQUE(user_id, group_id)
    );
    """,
    
    # Group Schedules
    """
    CREATE TABLE IF NOT EXISTS group_schedules (
        id SERIAL PRIMARY KEY,
        group_id INTEGER NOT NULL REFERENCES user_groups(id),
        name VARCHAR(200) NOT NULL,
        description TEXT,
        start_date DATE NOT NULL,
        weeks INTEGER NOT NULL,
        is_active BOOLEAN,
        created_by_id INTEGER NOT NULL REFERENCES users(id),
        created_at TIMESTAMP
    );
    """,
    
    # Group Schedule Items
    """
    CREATE TABLE IF NOT EXISTS group_schedule_items (
        id SERIAL PRIMARY KEY,
        schedule_id INTEGER NOT NULL REFERENCES group_schedules(id),
        week INTEGER NOT NULL,
        tasting_date DATE NOT NULL,
        bottle_name VARCHAR(255) NOT NULL,
        category VARCHAR(50),
        notes TEXT,
        completed BOOLEAN,
        completed_by_id INTEGER REFERENCES users(id),
        completed_at TIMESTAMP
    );
    """
]

def main():
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            for sql in SQL_STATEMENTS:
                try:
                    conn.execute(text(sql))
                    conn.commit()
                    print(f"✓ Executed: {sql[:50]}...")
                except Exception as e:
                    # Ignore "already exists" errors
                    if 'already exists' in str(e).lower() or 'duplicate' in str(e).lower():
                        print(f"⊘ Skipped (already exists): {sql[:50]}...")
                    else:
                        print(f"✗ Error: {e}")
                        print(f"  SQL: {sql[:100]}...")
        print("\n✓ All tables created successfully!")
        return 0
    except Exception as e:
        print(f"✗ Fatal error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())

