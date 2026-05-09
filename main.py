import os
from flask import Flask
from application.database import db
from application.resources import api

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not required, fall back to system environment variables

def create_app():
    app = Flask(__name__)

    database_url = os.getenv('DATABASE_URL', '').strip()

    # PostgreSQL Configuration (production)
    # Prefer a full DATABASE_URL from Supabase pooler settings when available.
    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', 'password')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'onlinebooking')
    
    # Use PostgreSQL by default, fallback to SQLite for development
    use_postgres = os.getenv('USE_POSTGRES', 'True').lower() == 'true'
    
    if use_postgres and not database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?sslmode=require'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///onlinebooking.sqlite3'
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', './static/images')

    db.init_app(app)
    api.init_app(app)
    
    # Import controllers after app initialization to avoid context issues
    with app.app_context():
        from application import controllers

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)