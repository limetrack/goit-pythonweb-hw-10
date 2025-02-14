from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime, date


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: datetime
    additional_info: Optional[str] = None

    @validator("first_name", "last_name")
    def validate_name(cls, value: str):
        if not value.isalpha():
            raise ValueError("Name fields must contain only alphabetic characters.")
        return value

    @validator("phone")
    def validate_phone(cls, value: str):
        if not value.isdigit() or len(value) not in (10, 11):
            raise ValueError("Phone number must contain 10 or 11 digits.")
        return value

    @validator("birthday")
    def validate_birthday(cls, value: datetime):
        if value.date() >= date.today():
            raise ValueError("Birthday must be a date in the past.")
        return value


class ContactCreate(ContactBase):
    pass


class ContactResponse(ContactBase):
    id: int

    class Config:
        orm_mode = True
