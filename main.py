import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from sqlalchemy import func, select

from api.routes.cars import router as cars_router
from api.routes.rentals import router as rentals_router
from core.db import Base, SessionLocal, engine
from core.exceptions import DatabaseError
from core.logging import get_logger
from core.metrics import active_cars, ongoing_rentals, request_duration
from models.car import CarStatus
from models.rental import Rental
from repositories.sql.car_repository import CarSQLRepository
from services.exceptions import CarHasActiveRentalsError, CarNotAvailableError, CarNotFoundError, RentalAlreadyEndedError, RentalNotFoundError

logger = get_logger(__name__)

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    db = SessionLocal()
    try:
        available_count = len(CarSQLRepository(db).get_all(status=CarStatus.available))
        active_cars.set(available_count)
        ongoing_count = db.execute(select(func.count()).select_from(Rental).where(Rental.end_date.is_(None))).scalar()
        ongoing_rentals.set(ongoing_count)
    finally:
        db.close()
    yield


app = FastAPI(title="DriveNow", lifespan=lifespan)

app.include_router(cars_router)
app.include_router(rentals_router)


@app.middleware("http")
async def track_request_duration(request: Request, call_next):
    # /metrics endpoint is not something we should track
    if request.url.path == "/metrics":
        return await call_next(request)
    start = time.time()
    response = await call_next(request)
    request_duration.labels(method=request.method, path=request.url.path).observe(time.time() - start)
    return response


# metrics EP
@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


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