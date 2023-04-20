from typing import Union, Annotated
import logging

from fastapi import FastAPI, HTTPException, status, Path
from fastapi.responses import JSONResponse
from database import db_cnx

from database import User
from database import Movie
from database import UserReview
from schemas import UserRequestModel
from schemas import UserResponseModel
from schemas import MoviesResponseModel
from schemas import MoviesRequestModel
from schemas import UserReviewRequestModel
from schemas import UserReviewResponseModel
from schemas import UserReviewRequestPutModel



logger = logging.getLogger(__name__)  # Set up a logger object
handler = logging.StreamHandler()  # Add a stream handler to the logger object
logger.addHandler(handler)
# Set the logging level
logger.setLevel(logging.INFO)


app = FastAPI(
    # root_path="/api/v1",
    openapi_url="/api/v1/openapi.json",
    title="My App",
    version="0.0.1",
    description="My description",
    contact={"name": "mack", "url": "http://mack.host"},
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


@app.on_event("startup")
def startup():
    if db_cnx.is_closed():
        db_cnx.connect()
        print("connecting...")
        logger.info(f"db_cnx ---> {dir(db_cnx)}")

    db_cnx.create_tables([User, Movie, UserReview])


@app.on_event("shutdown")
def shutdown():
    if not db_cnx.is_closed():
        logger.info(f"db_cnx ---> {db_cnx}")
        print("closing...")
        db_cnx.close()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post(
    "/users",
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


@app.post(
    "/movies",
    summary="Create movies",
    status_code=status.HTTP_200_OK,
    response_model=MoviesResponseModel
)
async def create_movie(movie: MoviesRequestModel):
    """CREAR PELÍCULA

    :param movie:

    :return:
    """
    if Movie.select().where(Movie.title == movie.title).exists():
        raise HTTPException(
            status_code=409,
            detail="La película ya existe."
        )

    movie = Movie.create(
        title=movie.title
    )

    return movie


@app.post(
    "/reviews",
    summary="Create reviews for the movies by users.",
    status_code=status.HTTP_200_OK,
    response_model=UserReviewResponseModel
)
async def create_movie(user_review: UserReviewRequestModel):
    """CREAR REVIEW DE PELÍCULAS

    :param user_review:

    :return:
    """
    # VERIFICAR SI EL USUARIO EXISTE
    if User.select().where(User.id == user_review.user_id).first() is None:
        raise HTTPException(
            status_code=404,
            detail="User not fount."
        )

    if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not fount."
        )

    user_review = UserReview.create(
        user_id=user_review.user_id,
        movie_id=user_review.movie_id,
        review=user_review.review,
        score=user_review.score
    )

    return user_review


@app.get(
    "/reviews",
    response_model=list[UserReviewResponseModel],
    status_code=status.HTTP_200_OK,
    summary="Get all reviews by the users of the movies."
)
async def get_reviews(page: int = 1, limit: int = 10):
    """LISTAR LA TABLA -UserReview-

    :return:
    """
    reviews = UserReview.select().paginate(page, limit)  # SELECT * FROM user_reviews

    return [user_review for user_review in reviews]


@app.get(
    "/reviews/{review_id}",
    response_model=UserReviewResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Get the review by ID."
)
async def get_review(
    review_id: Annotated[int, Path(
        gt=0,
        title="The ID of the review.",
        description="This is the ID user review. It's required.",
        example=1
    )]
):
    """LISTAR LA TABLA -UserReview- MEDIANTE UN PARÁMETRO

    :return:
    """
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not fount."
        )
    return user_review


@app.put(
    "/reviews/{review_id}",
    response_model=UserReviewResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Put the user movie review by ID"
)
async def update_review(
    review_id: Annotated[int, Path(
        gt=0,
        title="The ID of the review.",
        description="This is the ID user review. It's required.",
        example=1
    )],
    review_request: UserReviewRequestPutModel
):
    """ACTUALIZAR -UserReview- MEDIANTE PARÁMETRO

    :return:
    """
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not fount."
        )

    user_review.review = review_request.review
    user_review.score = review_request.score

    user_review.save()

    return user_review


@app.delete(
    "/reviews/{review_id}",
    response_model=UserReviewResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Delete the user movie review by ID"
)
async def update_review(
    review_id: Annotated[int, Path(
        gt=0,
        title="The ID of the review.",
        description="This is the ID user review. It's required.",
        example=1
    )]
):
    """Eliminar -UserReview- MEDIANTE PARÁMETRO

    :return:
    """
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not fount."
        )

    user_review.delete_instance()

    return user_review














