import os

class Config:
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'TALL'

    # Additional config settings could go here
    # For example, database configurations or environment settings
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'