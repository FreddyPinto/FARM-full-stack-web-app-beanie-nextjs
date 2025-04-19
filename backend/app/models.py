from datetime import datetime
from typing import List, Optional
from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel, Field


class User(Document):
    username: str = Field(min_length=3, max_length=50)
    password: str
    email: str
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


class Car(Document, extra="allow"):
    brand: str
    make: str
    year: int
    cm3: int
    price: float
    description: Optional[str] = None
    picture_url: Optional[str] = None
    pros: List[str] = []
    cons: List[str] = []
    date: datetime = datetime.now()
    user: Link[User] = None

    class Settings:
        name = "car"

    class Config:
        json_schema_extra = {
            "example": {
                "brand": "BMW",
                "make": "X5",
                "year": 2021,
                "cm3": 3000,
                "price": 100000,
            }
        }


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