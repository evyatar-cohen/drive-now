import pytest
from datetime import date
from unittest.mock import MagicMock

from services.rental_service import RentalService
from services.exceptions import RentalNotFoundError, RentalAlreadyEndedError
from models.car import CarStatus


def make_service(rental_repo=None, car_repo=None, broker=None):
    return RentalService(rental_repo or MagicMock(), car_repo or MagicMock(), broker or MagicMock())


def test_end_rental_raises_when_already_ended():
    rental_repo = MagicMock()
    rental = MagicMock()
    rental.end_date = date(2026, 1, 1)
    rental_repo.get_by_id.return_value = rental
    service = make_service(rental_repo=rental_repo)

    with pytest.raises(RentalAlreadyEndedError):
        service.end_rental(1)


def test_end_rental_updates_car_status_to_available():
    rental_repo = MagicMock()
    car_repo = MagicMock()
    rental = MagicMock()
    rental.end_date = None
    rental.car_id = 10
    rental_repo.get_by_id.return_value = rental
    rental_repo.end_rental.return_value = rental
    service = make_service(rental_repo=rental_repo, car_repo=car_repo)

    service.end_rental(1)

    car_repo.update.assert_called_once_with(10, {"status": CarStatus.available})