"""
Script de FastAPI
In Python 3.10
Run:
    uvicorn main:app --reload
"""
import logging

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from models.database import Movie, User, UserReview, db_cnx
from routers import movies, reviews, users
from shared import common

logger = logging.getLogger(__name__)  # Set up a logger object
handler = logging.StreamHandler()  # Add a stream handler to the logger object
logger.addHandler(handler)
# Set the logging level
logger.setLevel(logging.INFO)


app = FastAPI(
    openapi_url="/api/v1/openapi.json",
    title="FastApi Test",
    version="0.1",
    description="My description",
    contact={"name": "mack", "url": "http://mack.host"},
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

api_vx = APIRouter(prefix="/api/v1")

# ROUTERS
api_vx.include_router(users.router)
api_vx.include_router(movies.router)
api_vx.include_router(reviews.router)


@api_vx.post(
    "/auth",
    summary="Servicio para OAuth2",
    status_code=status.HTTP_200_OK
)
async def auth(data: OAuth2PasswordRequestForm = Depends()):
    """
    FUNCIÓN PARA AUTENTICAR AOUTH2 EN EL PROYECTO

    `:param data:`

    `:return:`
    """
    user = User.authenticate(data.username, data.password)

    if user:
        return {
            "access_token": common.create_access_token(user),
            "token_type": "eBearer"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User or Password wrong",
            headers={"www-Authenticate": "Bearer"}
        )


app.include_router(api_vx)


@app.on_event("startup")
def startup():
    """
    FUNCIÓN DE INICIO BD POSTGRES
    """
    if db_cnx.is_closed():
        db_cnx.connect()
        print("connecting...")
        logger.info(f"db_cnx ---> {dir(db_cnx)}")

    db_cnx.create_tables([User, Movie, UserReview])


@app.on_event("shutdown")
def shutdown():
    """
    FUNCIÓN PARA CERRAR CONEXIONES CON BD
    :return:
    """
    if not db_cnx.is_closed():
        logger.info(f"db_cnx ---> {db_cnx}")
        print("closing...")
        db_cnx.close()
