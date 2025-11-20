# dev.py

from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# CORS for local dev
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # your frontend local dev
]
CORS_ALLOW_CREDENTIALS = True

# JWT cookie secure flag for dev
SIMPLE_JWT['AUTH_COOKIE_SECURE'] = False
SIMPLE_JWT['AUTH_COOKIE_SAMESITE'] = 'Lax'