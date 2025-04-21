import cloudinary
from typing import List
from beanie import PydanticObjectId, WriteRules
from cloudinary import uploader
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, File, status
from app.models import Car, UpdateCar, User
from app.core.authentication import AuthHandler
from app.core.config import BaseConfig

auth_handler = AuthHandler()
router = APIRouter()
settings = BaseConfig()

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_SECRET_KEY,
)


@router.get("/", response_description="List all cars", response_model=List[Car])
async def get_cars():
    cars = await Car.find_all().to_list()
    return cars


@router.get("/{car_id}", response_description="Get car by id", response_model=Car)
async def get_car(car_id: PydanticObjectId):
    car = await Car.get(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@router.post(
    "/",
    response_description="Create a new car",
    response_model=Car,
    status_code=status.HTTP_201_CREATED,
)
async def create_car(
    brand: str = Form("brand"),
    make: str = Form("make"),
    year: int = Form("year"),
    cm3: int = Form("cm3"),
    km: int = Form("km"),
    price: float = Form("price"),
    # description: str = Form(...),
    # pros: List[str] = Form(...),
    # cons: List[str] = Form(...),
    picture: UploadFile = File("picture"),
    user_data=Depends(auth_handler.auth_wrapper),
):
    user_id = user_data["user_id"]
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Upload the image to Cloudinary
    upload_result = uploader.upload(
        picture.file, folder="FARM2", crop="fill", width=800, height=600, gravity="auto"
    )
    picture_url = upload_result["url"]

    car = Car(
        brand=brand,
        make=make,
        year=year,
        cm3=cm3,
        price=price,
        km=km,
        # description=description,
        # pros=pros,
        # cons=cons,
        picture_url=picture_url,
        user=user,
    )

    await car.insert(link_rule=WriteRules.WRITE)

    return car


async def update_car(car_id: PydanticObjectId, cardata: UpdateCar):
    car = await Car.get(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    updated_car = {k: v for k, v in cardata.model_dump().items() if v is not None}
    return await car.set(updated_car)


@router.delete("/{car_id}")
async def delete_car(car_id: PydanticObjectId):
    car = await Car.get(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    await car.delete()
