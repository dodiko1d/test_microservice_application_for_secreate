from typing import Optional
from pydantic import BaseModel


class ProductCreation(BaseModel):
    stock_keeping_unit: int
    name: str
    group_id: int
    stock_balance: int
    description: Optional[str] = ''
