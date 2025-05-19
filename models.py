from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class UserSignUp(BaseModel):
    first_name: str
    last_name: str
    gender: Literal["Male", "Female"]
    mobile_no: str
    email: EmailStr
    country: str
    password: str
    confirm_password: str

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "gender": "Male",
                "mobile_no": "0771234567",
                "email": "john.doe@example.com",
                "country": "Sri Lanka",
                "password": "secret123",
                "confirm_password": "secret123"
            }
        }

class UserLogin(BaseModel):
    email: EmailStr
    password: str