"""
Router for Movies Reviews
"""
from typing import Annotated

from fastapi import status, HTTPException, APIRouter, Path

from models.database import User, Movie, UserReview
from schemas.schemas import (
    UserReviewResponseModel,
    UserReviewRequestModel,
    UserReviewRequestPutModel,
)

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post(
    "/",
    summary="Create reviews for the movies by users.",
    status_code=status.HTTP_200_OK,
    response_model=UserReviewResponseModel,
)
async def create_movie(user_review: UserReviewRequestModel):
    """CREAR REVIEW DE PELÍCULAS

    :param user_review:

    :return:
    """
    # VERIFICAR SI EL USUARIO EXISTE
    if User.select().where(User.id == user_review.user_id).first() is None:
        raise HTTPException(status_code=404, detail="User not fount.")

    if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
        raise HTTPException(status_code=404, detail="Movie not fount.")

    user_review = UserReview.create(
        user_id=user_review.user_id,
        movie_id=user_review.movie_id,
        review=user_review.review,
        score=user_review.score,
    )

    return user_review


@router.get(
    "/",
    response_model=list[UserReviewResponseModel],
    status_code=status.HTTP_200_OK,
    summary="Get all reviews by the users of the movies.",
)
async def get_reviews(page: int = 1, limit: int = 10):
    """LISTAR LA TABLA -UserReview-

    :return:
    """
    reviews = UserReview.select().paginate(page, limit)  # SELECT * FROM user_reviews

    return [user_review for user_review in reviews]


@router.get(
    "/{review_id}",
    response_model=UserReviewResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Get the review by ID.",
)
async def get_review(
    review_id: Annotated[
        int,
        Path(
            gt=0,
            title="The ID of the review.",
            description="This is the ID user review. It's required.",
            example=1,
        ),
    ]
):
    """LISTAR LA TABLA -UserReview- MEDIANTE UN PARÁMETRO

    :return:
    """
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not fount."
        )
    return user_review


@router.put(
    "/{review_id}",
    response_model=UserReviewResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Put the user movie review by ID",
)
async def update_review(
    review_id: Annotated[
        int,
        Path(
            gt=0,
            title="The ID of the review.",
            description="This is the ID user review. It's required.",
            example=1,
        ),
    ],
    review_request: UserReviewRequestPutModel,
):
    """ACTUALIZAR -UserReview- MEDIANTE PARÁMETRO

    :return:
    """
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not fount."
        )

    user_review.review = review_request.review
    user_review.score = review_request.score

    user_review.save()

    return user_review


@router.delete(
    "/{review_id}",
    response_model=UserReviewResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Delete the user movie review by ID",
)
async def update_review(
    review_id: Annotated[
        int,
        Path(
            gt=0,
            title="The ID of the review.",
            description="This is the ID user review. It's required.",
            example=1,
        ),
    ]
):
    """Eliminar -UserReview- MEDIANTE PARÁMETRO

    :return:
    """
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not fount."
        )

    user_review.delete_instance()

    return user_review
