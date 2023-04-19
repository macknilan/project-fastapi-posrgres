from typing import Union
import logging

from fastapi import FastAPI
from database import db_cnx

from database import User
from database import Movie
from database import UserReview
from schemas import UserBaseModel


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


@app.post("/users")
async def create_user(user: UserBaseModel):
    """CREAR USUARIO EN BD

    :param user:

    :return: int
    """
    hash_pass: str = User.create_password(user.password)

    user = User.create(
        username=user.username,
        password=hash_pass,
        email=user.email
    )

    return user.id
