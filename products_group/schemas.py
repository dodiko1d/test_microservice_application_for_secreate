from typing import Optional
from pydantic import BaseModel


class ProductsGroupCreation(BaseModel):
    id: int
    name: str
    description: Optional[str] = ''
