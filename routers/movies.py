"""
Router for Movies
"""
from fastapi import APIRouter, status, HTTPException

from models.database import Movie
from schemas.schemas import MoviesResponseModel, MoviesRequestModel

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.post(
    "/",
    summary="Create movies",
    status_code=status.HTTP_200_OK,
    response_model=MoviesResponseModel,
)
async def create_movie(movie: MoviesRequestModel):
    """CREAR PELÍCULA

    :param movie:

    :return:
    """
    if Movie.select().where(Movie.title == movie.title).exists():
        raise HTTPException(status_code=409, detail="La película ya existe.")

    movie = Movie.create(title=movie.title)

    return movie
