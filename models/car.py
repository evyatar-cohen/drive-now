import enum

from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from core.db import Base


class CarStatus(enum.Enum):
    available = "available"
    in_use = "in_use"
    maintenance = "maintenance"


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[CarStatus] = mapped_column(Enum(CarStatus), nullable=False, default=CarStatus.available)