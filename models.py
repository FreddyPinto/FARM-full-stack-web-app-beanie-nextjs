from datetime import datetime
from os import name
from typing import List, Optional
from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel, Field


class User(Document):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=22)
    email: str = Field(min_length=6, max_length=50)
    created_at: datetime = Field(default_factory=datetime.now)

    class settings:
        name = "user"

    class Config:
        json_schema_extra = {
            "example": {
                "username": "Jhon",
                "password": "password",
                "email": "jhon@mail.com",
            }
        }


class RegisterUser(BaseModel):
    username: str
    password: str
    email: str


class LoginUser(BaseModel):
    username: str
    password: str


class CurrentUser(BaseModel):
    id: PydanticObjectId
    username: str
    email: str


class Car(Document):
    brand: str
    make: str
    year: int
    cm3: int
    price: float
    description: Optional[str] = None
    picture_url: Optional[str] = None
    pros: List[str] = []
    cons: List[str] = []
    created_at: datetime = Field(default_factory=datetime.now)
    owner: Link[User] = None

    class Settings:
        name = "car"

class UpdateCar(BaseModel):
    brand: Optional[str] = None
    make: Optional[str] = None
    year: Optional[int] = None
    cm3: Optional[int] = None
    price: Optional[float] = None
    description: Optional[str] = None
    picture_url: Optional[str] = None
    pros: Optional[List[str]] = []
    cons: Optional[List[str]] = []