""" Types Models for data between-components transferring.
I tried to use them less because in this specific situation it was easier
 and more operative-memory-friendly. """

from typing import Optional
from pydantic import BaseModel


class ProductCreation(BaseModel):
    id: int
    name: str
    group_id: int
    stock_balance: int
    reserved_number: int
    description: Optional[str] = ''
