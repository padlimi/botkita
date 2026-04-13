import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/botkita_db')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# KlikIndomaret Configuration
KLIK_INDOMARET_BASE_URL = 'https://klikindomaret.com'
KLIK_INDOMARET_API = 'https://api.klikindomaret.com'

# Session Configuration
SESSION_TIMEOUT = 3600  # 1 hour
MAX_CART_ITEMS = 50

# Logging
LOG_LEVEL = 'INFO'