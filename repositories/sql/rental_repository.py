from datetime import date

from sqlalchemy import exists, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from core.exceptions import DatabaseError
from models.rental import Rental
from repositories.base import RentalRepositoryBase


class RentalSQLRepository(RentalRepositoryBase):

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, rental_id: int) -> Rental | None:
        try:
            return self.db.get(Rental, rental_id)
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to fetch rental id={rental_id}") from e

    def get_all(self, car_id: int | None = None) -> list[Rental]:
        try:
            query = select(Rental)
            if car_id is not None:
                query = query.where(Rental.car_id == car_id)
            return list(self.db.execute(query).scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseError("Failed to fetch rentals") from e

    def add(self, rental: Rental) -> Rental:
        try:
            self.db.add(rental)
            self.db.flush()
            self.db.refresh(rental)
            return rental
        except SQLAlchemyError as e:
            raise DatabaseError("Failed to add rental") from e

    def end_rental(self, rental_id: int, end_date: date) -> Rental | None:
        try:
            rental = self.db.get(Rental, rental_id)
            if rental is None:
                return None
            rental.end_date = end_date
            self.db.flush()
            self.db.refresh(rental)
            return rental
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to end rental id={rental_id}") from e

    def has_active_rentals(self, car_id: int) -> bool:
        try:
            query = select(exists().where(Rental.car_id == car_id, Rental.end_date.is_(None)))
            return self.db.execute(query).scalar()
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to check active rentals for car id={car_id}") from e