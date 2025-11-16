"""
Configuration for User Management API
VULNERABILITY: Contains hardcoded credentials and API keys
"""

# VULNERABILITY: Hardcoded database credentials
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'admin123',  # Weak password!
    'database': 'users.db'
}

# VULNERABILITY: Hardcoded API keys
API_KEYS = {
    'stripe': 'sk_live_51Hxxx...xxx',
    'sendgrid': 'SG.xxx...xxx',
    'aws_access': 'AKIAIOSFODNN7EXAMPLE',
    'aws_secret': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
}

# VULNERABILITY: Debug settings in production
DEBUG = True
TESTING = True

# VULNERABILITY: Weak secret key
SECRET_KEY = "my_secret_key_123"

# VULNERABILITY: CORS allows all origins
CORS_ORIGINS = "*"

# VULNERABILITY: Rate limiting disabled
RATE_LIMIT_ENABLED = False

