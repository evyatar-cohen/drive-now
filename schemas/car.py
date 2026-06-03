from typing import Optional

from pydantic import BaseModel, field_validator

from models.car import CarStatus

# Duplicating the model validator on CarCreate and CarUpdate instead of using a the pydantic's mixin.
# A mixin without fields needs check_fields=False to bypass Pydantic's field check,
# which is awkward and goes against how Pydantic works. Duplication is cleaner here.


class CarCreate(BaseModel):
    model: str
    year: int

    @field_validator("model")
    @classmethod
    def model_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("model must not be blank")
        return v.strip()


class CarUpdate(BaseModel):
    model: Optional[str] = None
    year: Optional[int] = None
    status: Optional[CarStatus] = None

    @field_validator("model")
    @classmethod
    def model_not_blank(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("model must not be blank")
        return v.strip() if v is not None else v


class CarResponse(BaseModel):
    id: int
    model: str
    year: int
    status: CarStatus

    model_config = {"from_attributes": True}