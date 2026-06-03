from abc import ABC, abstractmethod
from models.car import Car, CarStatus


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