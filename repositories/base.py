from abc import ABC, abstractmethod
from datetime import date

from models.car import Car, CarStatus
from models.rental import Rental

# stubs for the repositories


class CarRepositoryBase(ABC):

    @abstractmethod
    def get_by_id(self, car_id: int) -> Car | None: ...

    @abstractmethod
    def get_all(self, status: CarStatus | None = None) -> list[Car]: ...

    @abstractmethod
    def add(self, car: Car) -> Car: ...

    @abstractmethod
    def update(self, car_id: int, data: dict) -> Car | None: ...

    @abstractmethod
    def delete(self, car_id: int) -> bool: ...


class RentalRepositoryBase(ABC):

    @abstractmethod
    def get_by_id(self, rental_id: int) -> Rental | None: ...

    @abstractmethod
    def get_all(self, car_id: int | None = None) -> list[Rental]: ...

    @abstractmethod
    def add(self, rental: Rental) -> Rental: ...

    @abstractmethod
    def end_rental(self, rental_id: int, end_date: date) -> Rental | None: ...

    @abstractmethod
    def has_active_rentals(self, car_id: int) -> bool: ...