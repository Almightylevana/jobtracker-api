from pydantic import BaseModel
from typing import Literal
from datetime import date

class ApplicationCreate(BaseModel):
    company: str
    role: str
    status: Literal["applied", "interviewing", "rejected", "offered", "withdrawn"]
    applied_date: date
    notes: str | None = None
    requirements: str | None = None
    location_type: str | None = None
    salary: str | None = None
    deadline: date | None = None
    url: str | None = None

class Application(ApplicationCreate):
    id: int

class ApplicationUpdate(BaseModel):
    company: str | None = None
    role: str | None = None
    status: Literal["applied", "interviewing", "rejected", "offered", "withdrawn"] | None = None
    applied_date: date | None = None
    notes: str | None = None
    requirements: str | None = None
    location_type: str | None = None
    salary: str | None = None
    deadline: date | None = None
    url: str | None = None