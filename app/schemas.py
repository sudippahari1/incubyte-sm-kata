from pydantic import BaseModel, Field
from typing import Optional


class EmployeeCreate(BaseModel):
    full_name: str
    job_title: str
    country: str
    salary: float = Field(gt=0)


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    job_title: Optional[str] = None
    country: Optional[str] = None
    salary: Optional[float] = Field(default=None, gt=0)


class EmployeeResponse(BaseModel):
    id: int
    full_name: str
    job_title: str
    country: str
    salary: float

    model_config = {"from_attributes": True}
