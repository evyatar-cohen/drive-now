from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from core.exceptions import DatabaseError
from models.car import Car, CarStatus
from repositories.base import CarRepositoryBase


class CarSQLRepository(CarRepositoryBase):

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, car_id: int) -> Car | None:
        try:
            return self.db.get(Car, car_id)
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to fetch car id={car_id}") from e

    def get_all(self, status: CarStatus | None = None) -> list[Car]:
        try:
            query = select(Car)
            if status is not None:
                query = query.where(Car.status == status)
            return list(self.db.execute(query).scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseError("Failed to fetch cars") from e

    def add(self, car: Car) -> Car:
        try:
            self.db.add(car)
            self.db.commit()
            self.db.refresh(car)
            return car
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError("Failed to add car") from e

    def update(self, car_id: int, data: dict) -> Car | None:
        try:
            car = self.db.get(Car, car_id)
            if car is None:
                return None
            for field, value in data.items():
                setattr(car, field, value)
            self.db.commit()
            self.db.refresh(car)
            return car
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to update car id={car_id}") from e

    def delete(self, car_id: int) -> bool:
        try:
            car = self.db.get(Car, car_id)
            if car is None:
                return False
            self.db.delete(car)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to delete car id={car_id}") from e