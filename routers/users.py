"""
Router for Users
"""
from fastapi import status, HTTPException, APIRouter

from models.database import User, Movie, UserReview
from schemas.schemas import UserResponseModel, UserRequestModel

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.post(
    "/",
    summary="Create Users",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseModel
)
async def create_user(user: UserRequestModel):
    """CREAR USUARIO EN BD

    :param user:

    :return:
    """
    if User.select().where(User.username == user.username).exists():
        raise HTTPException(
            status_code=409,
            detail="El username ya se encuentra en uso."
        )

    if User.select().where(User.email == user.email).exists():
        raise HTTPException(
            status_code=409,
            detail="El email ya se encuentra en uso."
        )

    hash_pass: str = User.create_password(user.password)

    user = User.create(
        username=user.username,
        password=hash_pass,
        email=user.email
    )

    return user

