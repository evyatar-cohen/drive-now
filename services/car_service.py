from services.exceptions import CarNotFoundError
from core.logging import get_logger
from models.car import Car, CarStatus
from repositories.base import CarRepositoryBase
from schemas.car import CarCreate, CarUpdate

logger = get_logger(__name__)


class CarService:

    def __init__(self, repository: CarRepositoryBase):
        self.repository = repository

    def get_car(self, car_id: int) -> Car:
        car = self.repository.get_by_id(car_id)
        if car is None:
            logger.warning("Car not found: id=%d", car_id)
            raise CarNotFoundError(car_id)
        return car

    def get_cars(self, status: CarStatus | None = None) -> list[Car]:
        cars = self.repository.get_all(status=status)
        logger.info("Listed %d cars (status=%s)", len(cars), status)
        return cars

    def add_car(self, data: CarCreate) -> Car:
        car = Car(
            model=data.model,
            year=data.year,
            status=CarStatus.available,
        )
        car = self.repository.add(car)
        logger.info("Car added: id=%d model=%s year=%d", car.id, car.model, car.year)
        return car

    def update_car(self, car_id: int, data: CarUpdate) -> Car:
        # TODO: from in use to available only if there is no current rentals
        fields = data.model_dump(exclude_unset=True)
        car = self.repository.update(car_id, fields)
        if car is None:
            logger.warning("Update failed, car not found: id=%d", car_id)
            raise CarNotFoundError(car_id)
        logger.info("Car updated: id=%d fields=%s", car_id, list(fields.keys()))
        return car

    def delete_car(self, car_id: int) -> None:
        # TODO: not delete if there are rentals for the cars
        deleted = self.repository.delete(car_id)
        if not deleted:
            logger.warning("Delete failed, car not found: id=%d", car_id)
            raise CarNotFoundError(car_id)
        logger.info("Car deleted: id=%d", car_id)