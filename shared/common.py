"""
SHARE CLASSES/FUNCTIONS
"""
import os
import logging
from typing import Annotated

import jwt
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from models.database import User

logger = logging.getLogger(__name__)  # Set up a logger object
handler = logging.StreamHandler()  # Add a stream handler to the logger object
logger.addHandler(handler)
# Set the logging level
logger.setLevel(logging.INFO)

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_DIR = os.path.join(BASE_DIR, ".envs")

load_dotenv(os.path.join(ENV_DIR, ".env"))

# This parameter contains the URL that the client (the frontend running in the user's browser)
# will use to send the username and password in order to get a token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth")


def create_access_token(user, days=1):
    """
    FUNCIÓN PARA ENCODE/CREAR EL PAYLOAD

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


def decode_access_token(token: str):
    """
    FUNCIÓN PARA DECODE/SABER EL PAYLOAD
    :param token:
    :return dict[str, Union[int, str]]:
    """
    try:
        return jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms=["HS512"])
    except Exception as decode_err:
        logger.exception(decode_err)
        return None


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    data = decode_access_token(token)
    if data:
        return User.select().where(User.id == data["user_id"]).first()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Token no valido",
            headers={"www-Authenticate": "Bearer"}
        )
