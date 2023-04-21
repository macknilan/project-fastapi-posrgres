"""
Router for Movies
"""
from typing import List, Annotated

from fastapi import APIRouter, status, HTTPException, Path

from models.database import Movie
from schemas.schemas import MoviesResponseModel, MoviesRequestModel

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get(
    "/",
    summary="Get movies",
    status_code=status.HTTP_200_OK,
    response_model=List[MoviesResponseModel],
)
async def get_movies(page: int = 1, limit: int = 10):
    """LISTAR PELÍCULAS DE LA TABLA -Movie-

    :return:
    """
    movies = Movie.select().paginate(page, limit)

    return [movie for movie in movies]


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


@router.put(
    "/{movie_id}",
    summary="Update movie.",
    status_code=status.HTTP_200_OK,
    response_model=MoviesResponseModel,
)
async def update_movie(
    movie_request: MoviesRequestModel,
    movie_id: Annotated[
        int,
        Path(
            gt=0,
            title="ID of the movie.",
            description="ID movie. It's required.",
            example=1,
        ),
    ]
):
    """ACTUALIZAR PELÍCULA

    :param movie_request:

    :param movie_id:

    :return:
    """
    movie_title = Movie.select().where(Movie.id == movie_id).first()
    if movie_title is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not fount."
        )

    movie_title.title = movie_request.title
    movie_title.save()

    return movie_title


@router.delete(
    "/{movie_id}",
    response_model=MoviesResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Delete the movie by ID",
)
async def delete_movie(
    movie_id: Annotated[
        int,
        Path(
            gt=0,
            title="The ID of the movie.",
            description="This is the ID movie. It's required.",
            example=1,
        ),
    ]
):
    """Eliminar -Movie- MEDIANTE PARÁMETRO

    :return:
    """
    movie = Movie.select().where(Movie.id == movie_id).first()

    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not fount."
        )

    movie.delete_instance()

    return movie
