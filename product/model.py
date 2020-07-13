""" Database Product Model. """

from sqlalchemy import Column, ForeignKey, Integer, String, CheckConstraint
from database import Base
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey('products_group.id'))
    stock_balance = Column(Integer)
    description = Column(String)
    reserved_number = Column(Integer)

    group = relationship('ProductGroup', back_populates='products_of_group')

    __table_args__ = (
        CheckConstraint(0 <= stock_balance, name='check_stock_balance_positive'),
        CheckConstraint(0 <= reserved_number, name='check_reserved_product'),
    )
