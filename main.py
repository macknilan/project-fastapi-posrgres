from typing import Annotated
import logging

from fastapi import FastAPI
from models.database import db_cnx

from models.database import User
from models.database import Movie
from models.database import UserReview

from routers import movies, users, reviews

logger = logging.getLogger(__name__)  # Set up a logger object
handler = logging.StreamHandler()  # Add a stream handler to the logger object
logger.addHandler(handler)
# Set the logging level
logger.setLevel(logging.INFO)


app = FastAPI(
    # root_path="/api/v1",
    openapi_url="/api/v1/openapi.json",
    title="FastApi Test",
    version="0.0.1",
    description="My description",
    contact={"name": "mack", "url": "http://mack.host"},
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


app.include_router(users.router)
app.include_router(movies.router)
app.include_router(reviews.router)


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

