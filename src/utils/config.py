import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

def load_config():
    """Load configuration from environment variables"""
    # Load environment variables from .env file
    load_dotenv()
    
    # Get database URL with fallback to SQLite
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///instance/crawler.db')
    
    # Convert postgres:// to postgresql:// for SQLAlchemy 1.4+
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    # Get port with fallback to 5001
    port = int(os.environ.get('PORT', 5001))
    
    logger.info(f"Configuration loaded: PORT={port}")
    
    return {
        'DATABASE_URL': database_url,
        'PORT': port
    }