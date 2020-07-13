from sqlalchemy.orm import Session

from . import model, schemas


def create_product(db: Session, product: schemas.ProductCreation):
    db_product = model.Product(
        stock_keeping_unit=product.stock_keeping_unit,
        name=product.name,
        group_id=product.group_id,
        stock_balance=product.stock_balance,
        description=product.description,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product_by_stock_keeping_unit(db: Session, product: schemas.ProductCreation):
    return False
