from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.routes.cars import router as cars_router
from api.routes.rentals import router as rentals_router
from core.db import Base, engine
from core.exceptions import DatabaseError
from services.exceptions import CarHasActiveRentalsError, CarNotAvailableError, CarNotFoundError, RentalAlreadyEndedError, RentalNotFoundError
from core.logging import get_logger

logger = get_logger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DriveNow")

app.include_router(cars_router)
app.include_router(rentals_router)



# exceptions handlers - each exception and its own error code

# the specific car couldn't be found
@app.exception_handler(CarNotFoundError)
def car_not_found_handler(request: Request, exc: CarNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(RentalNotFoundError)
def rental_not_found_handler(request: Request, exc: RentalNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(CarNotAvailableError)
def car_not_available_handler(request: Request, exc: CarNotAvailableError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(RentalAlreadyEndedError)
def rental_already_ended_handler(request: Request, exc: RentalAlreadyEndedError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(CarHasActiveRentalsError)
def car_has_active_rentals_handler(request: Request, exc: CarHasActiveRentalsError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

# database error
@app.exception_handler(DatabaseError)
def database_error_handler(request: Request, exc: DatabaseError):
    logger.error("Database error: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "A database error occurred"})

# general error will return 500
@app.exception_handler(Exception)
def unexpected_error_handler(request: Request, exc: Exception):
    logger.error("Unexpected error: %s", exc, exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "An unexpected error occurred"})