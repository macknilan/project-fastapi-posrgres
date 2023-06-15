"""
SHARE CLASSES/FUNCTIONS
"""
import os
import jwt
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_DIR = os.path.join(BASE_DIR, ".envs")

load_dotenv(os.path.join(ENV_DIR, ".env"))

print("DEBUGGER")


def create_access_token(user, days=1):
    """
    FUNCIÓN PARA CREAR EL PAYLOAD

    :param user:

    :param days:

    :return:
    """
    encode_payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.utcnow() + timedelta(days=days)
    }

    return jwt.encode(encode_payload, key=os.getenv("SECRET_KEY"), algorithm="HS512")

