"""
FILE FOR THE SCHEMAS/TYPE VALIDATIONS OF MODELS IN DATA BASE
"""
from typing import Any
from peewee import ModelSelect
from pydantic import BaseModel, EmailStr, Field, validator
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    """
    CONVERTIR EL OBJETO MODEL DE PEEWEE A UN DICCIONARIO
    PARA ENVIARLO COMO RESPUESTA AL CLIENTE
    """

    def get(self, key: Any, default: Any = None) -> Any:
        """SE SOBRE ESCRIBE GET"""
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)

        return res


class ResponseModel(BaseModel):
    """
    MODELO PARA HEREDAR LA CLASE A LOS DEMÁS MODELOS
    CONVERTIR DE MODELOS DE PEEWEE A MODELOS DE PYDANTIC
    """
    class Config:
        """
        CONVERTIR DE MODELOS DE PEEWEE A MODELOS DE PYDANTIC
        """
        orm_mode = True
        getter_dict = PeeweeGetterDict


class ReviewValidator():
    """CLASE HEREDABLE PARA VALIDAR EL ATRIBUTO -score- DE LA TABLA -UserReview-"""
    @validator("score")
    def score_is_valid(cls, v):
        if 1 <= v <= 5:
            # if v >= 1 and v <= 5:
            raise ValueError(
                "Score debe de estar en el rango de 1 a 5."
            )
        return v


# USER 👇


class UserRequestModel(BaseModel):
    """
    CLASE PARA VALIDAR REQUEST -User- CAMPOS OBLIGATORIOS
    """

    password: str = Field(
        title="Password",
        description="Password user",
        min_length=8,
        max_length=128,
        example="contrasenas",
    )
    username: str = Field(
        title="User name",
        description="User name",
        min_length=8,
        max_length=150,
        example="jhon_doe",
    )
    email: EmailStr = Field(
        example="johndoe@mail.com", title="Email", description="Email user"
    )
    # first_name: str = Field(
    #     None,
    #     title="First name",
    #     description="First name user",
    #     min_length=8,
    #     max_length=150,
    # )
    # last_name: str = Field(
    #     None,
    #     title="Last name",
    #     description="Last name user",
    #     min_length=8,
    #     max_length=150,
    # )

    @validator("email")
    def email_is_valid(cls, v):
        if 8 <= len(v) <= 255:
            raise ValueError(
                "Email must be at least of 8 characters and max 255 characters"
            )
        return v


class UserResponseModel(ResponseModel):
    """
    MODELO PARA VALIDAR RESPONSE RESPUESTA DE USUARIO
    """
    id: int
    username: str


# MOVIES 👇

class MoviesRequestModel(BaseModel):
    """
    CLASE PARA VALIDAR REQUEST -Movies- CAMPOS OBLIGATORIOS
    """

    title: str = Field(
        title="Title",
        description="Movie title",
        min_length=1,
        max_length=128,
        example="Real Player One",
    )


class MoviesResponseModel(ResponseModel):
    """
    MODELO PARA VALIDAR RESPONSE RESPUESTA DE MOVIES
    """
    id: int
    title: str


# REVIEWS 👇

class UserReviewRequestModel(BaseModel, ReviewValidator):
    """
    CLASE PARA VALIDAR REQUEST -UserReview- CAMPOS OBLIGATORIOS
    """
    user_id: int = Field(
        title="Id user",
        description="ID of the user",
        gt=0,
        le=100,
        example=1
    )
    movie_id: int = Field(
        title="Id Movie",
        description="ID of the movie",
        gt=0,
        le=100,
        example=1
    )
    review: str = Field(
        title="Review",
        description="Movie review",
        min_length=8,
        max_length=128,
        example="Este es una reseña de prueba...",
    )
    score: int = Field(
        title="Score movie",
        description="Score of the movie",
    )


class UserReviewResponseModel(ResponseModel):
    """
    CLASE PARA VALIDAR RESPONSE -UserReview-
    """
    id: int
    user_id: int
    movie: MoviesResponseModel
    review: str
    score: int


class UserReviewRequestPutModel(BaseModel, ReviewValidator):
    """
    CLASE PARA VALIDAR PUT REQUEST -UserReview-
    """
    review: str = Field(
        title="Review",
        description="Movie review",
        min_length=8,
        max_length=128,
        example="Este es una reseña de prueba modificada...",
    )
    score: int = Field(
        title="Score movie",
        description="Score of the movie",
    )










