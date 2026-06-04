from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.db import get_db
from models.car import CarStatus
from repositories.sql.car_repository import CarSQLRepository
from repositories.sql.rental_repository import RentalSQLRepository
from schemas.car import CarCreate, CarResponse, CarUpdate
from services.car_service import CarService

router = APIRouter(prefix="/cars", tags=["cars"])


def get_service(db: Session = Depends(get_db)) -> CarService:
    return CarService(CarSQLRepository(db), RentalSQLRepository(db))


@router.post("/", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def create_car(data: CarCreate, service: CarService = Depends(get_service)):
    return service.add_car(data)


@router.get("/", response_model=list[CarResponse])
def list_cars(status: CarStatus | None = None, service: CarService = Depends(get_service)):
    return service.get_cars(status=status)


@router.get("/{car_id}", response_model=CarResponse)
def get_car(car_id: int, service: CarService = Depends(get_service)):
    return service.get_car(car_id)


@router.put("/{car_id}", response_model=CarResponse)
def update_car(car_id: int, data: CarUpdate, service: CarService = Depends(get_service)):
    return service.update_car(car_id, data)


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_car(car_id: int, service: CarService = Depends(get_service)):
    service.delete_car(car_id)