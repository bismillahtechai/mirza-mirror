"""
Database module for Mirza Mirror.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.utils.logger import log_info, log_error

# Load environment variables
load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./mirza_mirror.db")

# Fix for Render PostgreSQL URLs (postgres:// -> postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

def get_db():
    """
    Get database session.
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize database.
    """
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        log_info("Database initialized successfully")
        
        # Execute schema.sql if it exists
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        if os.path.exists(schema_path):
            with open(schema_path, "r") as f:
                schema_sql = f.read()
            
            with engine.connect() as conn:
                conn.execute(schema_sql)
            
            log_info("Database schema applied successfully")
    except Exception as e:
        log_error(f"Error initializing database: {str(e)}")
        raise
