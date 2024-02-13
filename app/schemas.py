from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from pydantic.dataclasses import dataclass

app = FastAPI()


class UserSchema(BaseModel):
    username: str | None = None


class UserWithPasswordSchema(BaseModel):
    username: str | None = None
    password: str | None = None


class ProductSchema(BaseModel):
    name: str | None = None
    price: float | None = None
    quantity: int | None = None


class Payment(BaseModel):
    type: str
    amount: float


class ReceiptSchema(BaseModel):
    products: List[ProductSchema]
    payment: Payment
    total: float
    rest: float
    created_at: datetime
