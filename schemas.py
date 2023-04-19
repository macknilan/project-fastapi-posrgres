"""
FILE FOR THE SCHEMAS/TYPE VALIDATIONS OF MODELS IN DATA BASE
"""
from pydantic import BaseModel, EmailStr, Field, validator


class UserBaseModel(BaseModel):
    """
    CLASE PARA VALIDAR -User- CAMPOS OBLIGATORIOS
    """
    password: str = Field(
        title="Password",
        description="Password user",
        min_length=8,
        max_length=128,
        example="contrasenas"
    )
    username: str = Field(
        title="User name",
        description="User name",
        min_length=8,
        max_length=150,
        example="jhon_doe"
    )
    email: EmailStr = Field(
        example="johndoe@mail.com",
        title="Email",
        description="Email user"
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
        if 8 >= len(v) <= 255:
            raise ValueError("Email must be at least of 8 characters and max 255 characters")
        return v
