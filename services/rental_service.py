from datetime import date

from core.logging import get_logger
from core.metrics import active_cars, ongoing_rentals
from models.car import CarStatus
from models.rental import Rental
from repositories.base import CarRepositoryBase, RentalRepositoryBase
from schemas.rental import RentalCreate
from services.exceptions import CarNotAvailableError, CarNotFoundError, RentalAlreadyEndedError, RentalNotFoundError

logger = get_logger(__name__)


class RentalService:

    def __init__(self, rental_repository: RentalRepositoryBase, car_repository: CarRepositoryBase):
        self.rental_repository = rental_repository
        self.car_repository = car_repository

    def get_rental(self, rental_id: int) -> Rental:
        rental = self.rental_repository.get_by_id(rental_id)
        if rental is None:
            logger.warning("Rental not found: id=%d", rental_id)
            raise RentalNotFoundError(rental_id)
        return rental

    def get_rentals(self, car_id: int | None = None) -> list[Rental]:
        rentals = self.rental_repository.get_all(car_id=car_id)
        logger.info("Listed %d rentals (car_id=%s)", len(rentals), car_id)
        return rentals

    def start_rental(self, data: RentalCreate) -> Rental:
        car = self.car_repository.get_by_id(data.car_id)
        if car is None:
            logger.warning("Start rental failed, car not found: id=%d", data.car_id)
            raise CarNotFoundError(data.car_id)
        if car.status != CarStatus.available:
            logger.warning("Start rental failed, car not available: id=%d status=%s", car.id, car.status)
            raise CarNotAvailableError(data.car_id)

        rental = Rental(car_id=data.car_id, customer_name=data.customer_name)
        rental = self.rental_repository.add(rental)

        self.car_repository.update(data.car_id, {"status": CarStatus.in_use})
        ongoing_rentals.inc()
        active_cars.dec()
        logger.info("Rental started: id=%d car_id=%d customer=%s", rental.id, rental.car_id, rental.customer_name)
        return rental

    def end_rental(self, rental_id: int) -> Rental:
        rental = self.rental_repository.get_by_id(rental_id)
        if rental is None:
            logger.warning("End rental failed, rental not found: id=%d", rental_id)
            raise RentalNotFoundError(rental_id)
        if rental.end_date is not None:
            logger.warning("End rental failed, rental already ended: id=%d", rental_id)
            raise RentalAlreadyEndedError(rental_id)

        rental = self.rental_repository.end_rental(rental_id, date.today())

        self.car_repository.update(rental.car_id, {"status": CarStatus.available})
        ongoing_rentals.dec()
        active_cars.inc()
        logger.info("Rental ended: id=%d car_id=%d", rental_id, rental.car_id)
        return rental
