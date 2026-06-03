import pytest
from unittest.mock import MagicMock

from services.exceptions import CarNotFoundError
from schemas.car import CarCreate, CarUpdate
from services.car_service import CarService
from models.car import CarStatus


# --- CarCreate validator ---

def test_car_create_strips_whitespace():
    car = CarCreate(model="  Toyota  ", year=2020)
    assert car.model == "Toyota"


def test_car_create_blank_model_raises():
    with pytest.raises(ValueError, match="must not be blank"):
        CarCreate(model="   ", year=2020)


def test_car_create_empty_model_raises():
    with pytest.raises(ValueError, match="must not be blank"):
        CarCreate(model="", year=2020)


# --- CarUpdate validator ---

def test_car_update_none_model_is_allowed():
    update = CarUpdate(status=CarStatus.available)
    assert update.model is None


def test_car_update_blank_model_raises():
    with pytest.raises(ValueError, match="must not be blank"):
        CarUpdate(model="   ")


def test_car_update_strips_whitespace():
    update = CarUpdate(model="  Honda  ")
    assert update.model == "Honda"


# --- CarService.update_car: only provided fields reach the repo ---

def test_update_car_only_sends_set_fields():
    repo = MagicMock()
    service = CarService(repo)

    service.update_car(1, CarUpdate(status=CarStatus.maintenance))

    repo.update.assert_called_once_with(1, {"status": CarStatus.maintenance})


def test_update_car_sends_all_fields_when_all_provided():
    repo = MagicMock()
    service = CarService(repo)

    service.update_car(1, CarUpdate(model="Ford", year=2022, status=CarStatus.in_use))

    repo.update.assert_called_once_with(
        1, {"model": "Ford", "year": 2022, "status": CarStatus.in_use}
    )


def test_update_car_raises_when_not_found():
    repo = MagicMock()
    repo.update.return_value = None
    service = CarService(repo)

    with pytest.raises(CarNotFoundError):
        service.update_car(99, CarUpdate(year=2021))