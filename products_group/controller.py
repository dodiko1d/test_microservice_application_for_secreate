from sqlalchemy.orm import Session

from . import model, schemas


def create_products_group(db: Session, products_group: schemas.ProductsGroupCreation):
    db_products_group = model.ProductsGroup(
        id=products_group.id,
        name=products_group.name,
        description=products_group.description,
    )
    db.add(db_products_group)
    db.commit()
    db.refresh(db_products_group)
    return db_products_group


def get_products_group_by_id(db: Session, products_group: schemas.ProductsGroupCreation):
    return False
