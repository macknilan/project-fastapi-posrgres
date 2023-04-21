"""
Router for Users
"""
from typing import Annotated
from fastapi import status, HTTPException, APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from argon2 import PasswordHasher, exceptions

from models.database import User, Movie, UserReview
from schemas.schemas import UserResponseModel, UserRequestModel

router = APIRouter(prefix="/users", tags=["Users"])

security = HTTPBasic()

@router.post(
    "/",
    summary="Create Users",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseModel,
)
async def create_user(user: UserRequestModel):
    """CREAR USUARIO EN BD

    :param user:

    :return:
    """
    if User.select().where(User.username == user.username).exists():
        raise HTTPException(
            status_code=409, detail="El username ya se encuentra en uso."
        )

    if User.select().where(User.email == user.email).exists():
        raise HTTPException(status_code=409, detail="El email ya se encuentra en uso.")

    hash_pass: str = User.create_password(user.password)

    user = User.create(username=user.username, password=hash_pass, email=user.email)

    return user


@router.post("/login", response_model=UserResponseModel)
async def login(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):

    user = User.select().where(User.username == credentials.username).first()
    if user is None:
        raise HTTPException(
            status_code=404, detail="User not found."
        )

    ph = PasswordHasher()
    try:
        ph.verify(user.password, credentials.password)

        # Now that we have the cleartext password,
        # check the hash's parameters and if outdated,
        # rehash the user's password in the database.
        if ph.check_needs_rehash(user.password):
            hash_pass: str = User.create_password(user.password)
            user = User.create(username=user.username, password=hash_pass, email=user.email)

        return user
    except exceptions.VerifyMismatchError as match_error:
        raise HTTPException(
            status_code=404, detail=f"{match_error}"
        )
    except exceptions.VerificationError as verif_error:
        raise HTTPException(
            status_code=404, detail=f"{verif_error}"
        )
    except exceptions.InvalidHash as invalid_error:
        raise HTTPException(
            status_code=404, detail=f"{invalid_error}"
        )














