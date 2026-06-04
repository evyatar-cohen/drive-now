from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.config import settings
from core.db import get_db
from messaging.redis_broker import RedisBroker
from repositories.sql.car_repository import CarSQLRepository
from repositories.sql.rental_repository import RentalSQLRepository
from schemas.rental import RentalCreate, RentalResponse
from services.rental_service import RentalService

router = APIRouter(prefix="/rentals", tags=["rentals"])

broker = RedisBroker(settings.redis_url)


def get_service(db: Session = Depends(get_db)) -> RentalService:
    return RentalService(RentalSQLRepository(db), CarSQLRepository(db), broker)


@router.post("/", response_model=RentalResponse, status_code=status.HTTP_201_CREATED)
def start_rental(data: RentalCreate, service: RentalService = Depends(get_service)):
    return service.start_rental(data)


@router.get("/", response_model=list[RentalResponse])
def list_rentals(car_id: int | None = None, service: RentalService = Depends(get_service)):
    return service.get_rentals(car_id=car_id)


@router.get("/{rental_id}", response_model=RentalResponse)
def get_rental(rental_id: int, service: RentalService = Depends(get_service)):
    return service.get_rental(rental_id)


@router.patch("/{rental_id}/end", response_model=RentalResponse)
def end_rental(rental_id: int, service: RentalService = Depends(get_service)):
    return service.end_rental(rental_id)