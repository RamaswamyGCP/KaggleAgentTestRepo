"""
Authentication module for User Management API
WARNING: Contains security vulnerabilities!
"""

import jwt
import datetime


def generate_token(user_id, secret_key):
    """
    Generate JWT token for user
    VULNERABILITY: Token has long expiration time
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365),  # 1 year!
        'iat': datetime.datetime.utcnow()
    }
    
    # VULNERABILITY: Using HS256 algorithm (symmetric)
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    
    return token


def verify_token(token, secret_key):
    """
    Verify JWT token and return user_id
    VULNERABILITY: Minimal error handling
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload.get('user_id')
    except:
        # VULNERABILITY: Catching all exceptions without specific handling
        return None


def hash_password(password):
    """
    Hash password for storage
    VULNERABILITY: This function exists but is never used!
    Passwords are stored in plain text instead.
    """
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, hashed):
    """
    Verify password against hash
    VULNERABILITY: This function is also unused!
    """
    return hash_password(password) == hashed

