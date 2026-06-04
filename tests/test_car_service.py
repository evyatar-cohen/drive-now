import pytest
from unittest.mock import MagicMock

from services.exceptions import CarHasActiveRentalsError, CarNotFoundError
from schemas.car import CarCreate, CarUpdate
from services.car_service import CarService
from models.car import CarStatus


def make_service(car_repo=None, rental_repo=None):
    return CarService(car_repo or MagicMock(), rental_repo or MagicMock())


# --- CarCreate validator ---

def test_car_create_strips_whitespace():
    car = CarCreate(model="  Toyota  ", year=2020)
    assert car.model == "Toyota"


def test_car_create_blank_model_raises():
    with pytest.raises(ValueError, match="must not be blank"):
        CarCreate(model="   ", year=2020)


# --- CarUpdate validator ---

def test_car_update_none_model_is_allowed():
    update = CarUpdate(status=CarStatus.available)
    assert update.model is None


def test_car_update_blank_model_raises():
    with pytest.raises(ValueError, match="must not be blank"):
        CarUpdate(model="   ")


# --- update_car: only provided fields reach the repo ---

def test_update_car_only_sends_set_fields():
    car_repo = MagicMock()
    service = make_service(car_repo=car_repo)

    service.update_car(1, CarUpdate(status=CarStatus.maintenance))

    car_repo.update.assert_called_once_with(1, {"status": CarStatus.maintenance})


def test_update_car_raises_when_not_found():
    car_repo = MagicMock()
    car_repo.get_by_id.return_value = None
    service = make_service(car_repo=car_repo)

    with pytest.raises(CarNotFoundError):
        service.update_car(99, CarUpdate(year=2021))


# --- active rentals guard ---

def test_update_car_to_available_blocked_when_active_rentals():
    rental_repo = MagicMock()
    rental_repo.has_active_rentals.return_value = True
    service = make_service(rental_repo=rental_repo)

    with pytest.raises(CarHasActiveRentalsError):
        service.update_car(1, CarUpdate(status=CarStatus.available))


def test_delete_car_blocked_when_active_rentals():
    rental_repo = MagicMock()
    rental_repo.has_active_rentals.return_value = True
    service = make_service(rental_repo=rental_repo)

    with pytest.raises(CarHasActiveRentalsError):
        service.delete_car(1)