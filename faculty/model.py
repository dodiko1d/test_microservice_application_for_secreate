""" Database Products Group Model. """

from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship


class ProductsGroup(Base):
    __tablename__ = 'products_group'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

    products_of_group = relationship('Product', back_populates='group')
