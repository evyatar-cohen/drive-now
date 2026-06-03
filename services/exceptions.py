class CarNotFoundError(Exception):
    def __init__(self, car_id: int):
        self.car_id = car_id
        super().__init__(f"Car not found: id={car_id}")