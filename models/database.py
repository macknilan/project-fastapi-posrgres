"""
FILE OF DATABASE
"""
import datetime
import logging

from peewee import *
from fastapi import HTTPException
from argon2 import PasswordHasher, exceptions

# CREATE A LOGGER
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# CREATE A HANDLER TO OUTPUT THE LOGS TO THE CONSOLE
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# ADD THE HANDLER TO THE LOGGER
logger.addHandler(console_handler)


db_cnx = PostgresqlDatabase(
    "fast_api_db",
    user="fast_api_user",
    password="fast api 2023 passs",
    host="localhost",
    port=5432,
)


# MODELS

class User(Model):
    """
    USER MODEL
    """

    password = CharField(
        max_length=128,
        verbose_name="password",
        constraints=[Check("length(password) > 0", "password cannot be empty")],
    )
    username = CharField(
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        verbose_name="username",
        unique=True,
        max_length=150,
        constraints=[Check("length(username) > 0", "username cannot be empty")],
    )
    last_login = DateTimeField(null=True, verbose_name="last login")  # NOT REQUIRED
    is_superuser = BooleanField(
        default=False,
        help_text="Designates that this user has all permissions without explicitly assigning them.",
        verbose_name="superuser status",
    )
    first_name = CharField(
        null=True, max_length=150, verbose_name="first_name"  # NOT REQUIRED
    )
    last_name = CharField(
        null=True, max_length=150, verbose_name="last_name"  # NOT REQUIRED
    )
    email = CharField(
        index=True,
        unique=True,
        verbose_name="email address",
        max_length=255,
        help_text="Required. Max 255 characters or fewer.",
    )
    is_staff = BooleanField(
        default=False,
        verbose_name="staff status",
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting "
        "accounts.",
        verbose_name="active",
    )
    date_joined = DateTimeField(
        default=datetime.datetime.now, verbose_name="date joined"
    )

    def __str__(self):
        return self.username

    class Meta:
        database = db_cnx
        table_name = "users"

    @classmethod
    def authenticate(cls, username, password):
        """
        CLASS METHOD PARA AUTENTICAR EL USUARIO

        `:param username:`

        `:param password:`

        `:return:`

        """
        user = cls.select().where(User.username == username).first()
        verif: bool = False
        ph = PasswordHasher()
        try:
            verif = ph.verify(user.password, password)
            # Now that we have the cleartext password,
            # check the hash's parameters and if outdated,
            # rehash the user's password in the database.
            if ph.check_needs_rehash(user.password):
                hash_pass: str = cls.create_password(user.password)
                user = User.create(username=user.username, password=hash_pass, email=user.email)

        except exceptions.VerifyMismatchError as match_error:
            logger.info(f"{match_error}")
            # raise HTTPException(
            #     status_code=404, detail="Except User or Password wrong."
            # )
        except exceptions.VerificationError as verif_error:
            logger.info(f"{verif_error}")
            # raise HTTPException(
            #     status_code=404, detail="Except User or Password wrong."
            # )
        except exceptions.InvalidHash as invalid_error:
            logger.info(f"{invalid_error}")
            # raise HTTPException(
            #     status_code=404, detail="Except User or Password wrong."
            # )

        if user and verif:
            return user

    @classmethod
    def create_password(cls, password: str) -> str:
        """
        CLASS METHOD FOR HASHING PASSWORD WITH -argon2-
        """
        ph = PasswordHasher()
        pass_hash = ph.hash(password)

        return pass_hash


class Movie(Model):
    """
    MOVIE MODEL
    """

    title = CharField(
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        verbose_name="title",
        unique=True,
        max_length=150,
        constraints=[Check("length(title) > 0", "title cannot be empty")],
    )
    created_at = DateTimeField(
        default=datetime.datetime.now,
        verbose_name="created at",
        help_text="when was created",
    )

    def __str__(self):
        return self.title

    class Meta:
        database = db_cnx
        table_name = "movies"


class UserReview(Model):
    """
    MODEL USER REVIEWS
    """

    user = ForeignKeyField(User, backref="reviews")
    movie = ForeignKeyField(Movie, backref="reviews")
    review = TextField(
        verbose_name="reviews",
        help_text="reviews of movie",
        constraints=[Check("length(review) > 0", "reviews cannot be empty")],
    )
    score = IntegerField(verbose_name="reviews", help_text="score of the movie")
    created_at = DateTimeField(
        default=datetime.datetime.now,
        verbose_name="created at",
        help_text="when was created",
    )

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

    class Meta:
        database = db_cnx
        table_name = "user_reviews"
