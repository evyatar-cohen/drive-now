from datetime import date
from typing import Optional

from pydantic import BaseModel, field_validator


class RentalCreate(BaseModel):
    car_id: int
    customer_name: str

    @field_validator("customer_name")
    @classmethod
    def customer_name_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("customer_name must not be blank")
        return v.strip()


class RentalResponse(BaseModel):
    id: int
    car_id: int
    customer_name: str
    start_date: date
    end_date: Optional[date] = None

    model_config = {"from_attributes": True}