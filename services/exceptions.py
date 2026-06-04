class CarNotFoundError(Exception):
    def __init__(self, car_id: int):
        self.car_id = car_id
        super().__init__(f"Car not found: id={car_id}")


class RentalNotFoundError(Exception):
    def __init__(self, rental_id: int):
        self.rental_id = rental_id
        super().__init__(f"Rental not found: id={rental_id}")


class CarNotAvailableError(Exception):
    def __init__(self, car_id: int):
        self.car_id = car_id
        super().__init__(f"Car is not available: id={car_id}")


class RentalAlreadyEndedError(Exception):
    def __init__(self, rental_id: int):
        self.rental_id = rental_id
        super().__init__(f"Rental already ended: id={rental_id}")


class CarHasActiveRentalsError(Exception):
    def __init__(self, car_id: int):
        self.car_id = car_id
        super().__init__(f"Car has active rentals: id={car_id}")