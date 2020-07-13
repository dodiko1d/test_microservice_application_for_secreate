from sqlalchemy import Column, ForeignKey, Integer, String, CheckConstraint
from database import Base


class Product(Base):
    __tablename__ = 'product'

    stock_keeping_unit = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey('products_group.id'))
    stock_balance = Column(Integer)
    description = Column(String)

    __table_args__ = (
        CheckConstraint(stock_balance >= 0, name='check_stock_balance_positive'),
        {})
