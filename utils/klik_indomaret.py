import re
import hashlib
import secrets
from typing import Optional

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone format"""
    # Accept format: 62812xxxx or 0812xxxx
    pattern = r'^(62|0)[0-9]{9,}$'
    return re.match(pattern, phone) is not None

def hash_password(password: str) -> str:
    """Hash password with salt"""
    salt = secrets.token_hex(32)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return salt + pwd_hash.hex()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    salt = hashed[:64]
    stored_hash = hashed[64:]
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return pwd_hash.hex() == stored_hash

def generate_otp() -> str:
    """Generate random 6-digit OTP"""
    return str(secrets.randbelow(1000000)).zfill(6)

async def login_to_klikindomaret(email: str, password: str) -> dict:
    """
    Login ke KlikIndomaret
    TODO: Implement actual API call
    """
    # Placeholder untuk API call ke KlikIndomaret
    # Contoh menggunakan requests atau aiohttp
    pass

async def send_otp(phone: str, otp: str) -> bool:
    """
    Send OTP to phone number
    TODO: Implement actual SMS gateway
    """
    # Placeholder untuk SMS gateway (Twilio, AWS SNS, dll)
    pass
