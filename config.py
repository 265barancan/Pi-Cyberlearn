import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-cyberlearn-pi'
    DATABASE_URI = os.path.join(basedir, 'cyberlearn.db')
    
    # Flask optimizations
    TEMPLATES_AUTO_RELOAD = os.environ.get('FLASK_ENV') == 'development'
    SEND_FILE_MAX_AGE_DEFAULT = 86400  # 1 day cache
    
    # Gemini Optimization
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
