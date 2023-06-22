"""
Router for Users
"""
from typing import Annotated, List, Dict, Any

from argon2 import PasswordHasher, exceptions
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from peewee import CharField

from models.database import User
from schemas.schemas import UserRequestModel, UserResponseModel, UserReviewResponseModel
from shared.common import get_current_user

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


@router.post(
    "/login",
    response_model=UserResponseModel,
    summary="Basic Login."
)
async def login(credentials: Annotated[HTTPBasicCredentials, Depends(security)], response: Response):
    """SERVICIO DE BASIC LOGIN

    :param response:

    :param credentials:

    :return:
    """
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

        # TODO: Mejorar por seguridad la forma en guardar la cookie
        response.set_cookie(key="user_id", value=user.id)
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

"""
@router.get(
    "/reviews",
    response_model=List[UserReviewResponseModel],
    summary="For logged user get de reviews of movies by the cookie.",
    status_code=status.HTTP_200_OK
)
async def get_reviews(user_id: int = Cookie(None)):
    SERVICIO PARA OBTENER LAS RESEÑAS DE LAS PELÍCULAS
    SI LA COOKIE ID DEL USUARIO ESTABLECIDA ANTES SE SE ENCUENTRA

    :param user_id:

    :return:
    
    user = User.select().where(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=404, detail="User not found."
        )

    # return list(user.reviews)
    return [user_review for user_review in user.reviews]
"""


@router.get(
    "/reviews",
    response_model=List[UserReviewResponseModel],
    summary="For logged user get de reviews of movies by the token.",
    status_code=status.HTTP_200_OK
)
async def get_reviews(user: Annotated[User, Depends(get_current_user)]) -> dict[str, Any]:
    """SERVICIO PARA OBTENER LAS RESEÑAS DE LAS PELÍCULAS
    POR MEDIO DE UN TOKEN

    :param :

    :return:
    """
    return [user_review for user_review in user.reviews]
