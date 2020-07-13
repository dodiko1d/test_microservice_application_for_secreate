from sqlalchemy.orm import Session
from sqlalchemy import literal

from . import model, schemas


def __get_product_instance_by_id(db: Session, product_id: int):
    return db.query(model.Product).filter(model.Product.id == product_id).first()


def create_product(db: Session, product: schemas.ProductCreation):
    db_product = model.Product(
        id=product.id,
        name=product.name,
        group_id=product.group_id,
        stock_balance=product.stock_balance,
        description=product.description,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def remove_product(db: Session, product_id: int):
    product = __get_product_instance_by_id(db=db, product_id=product_id)
    db.delete(product)
    db.commit()


def change_product_property(db: Session, product_id: int, property_name: str, new_property_value):
    db_product_json = __get_product_instance_by_id(db=db, product_id=product_id).json()
    property_type = type(db_product_json[property_name])
    if property_type != type(new_property_value):
        try:
            new_property_value = db_product_json[property_name].__class__(new_property_value)
        except ValueError:
            return {'404': 'Incorrect property type'}
    db_product_json[property_name] = new_property_value
    db_product = model.Product(**db_product_json)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def __find_product_instances_by_name_part(db: Session, name_part: str, limit: int = 5):
    result = db.query(model.Product).filter(literal(name_part).contains(model.Product.name))
    return result.limit(limit).all()


def __find_product_instances_by_description_part(db: Session, description_part: str, limit: int = 5):
    result = db.query(model.Product).filter(literal(description_part).contains(model.Product.description))
    return result.limit(limit).all()


def get_product_data_by_id(db: Session, product_id: int):
    product = __get_product_instance_by_id(db=db, product_id=product_id)
    if not product:
        return False
    return {
        'id': product.id,
        'name': product.name,
        'group_id': product.group_id,
        'stock_balance': product.stock_balance,
        'description': product.description,
    }
