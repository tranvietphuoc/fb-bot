import os
import secrets

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = True
    TESTING = False
    SECRET_KEY = str(secrets.token_hex(16))
