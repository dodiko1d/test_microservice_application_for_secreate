from sqlalchemy.orm import Session
from sqlalchemy import literal
from products_group import controller as products_group_controller

from . import model, schemas


def __get_product_instance_by_id(db: Session, product_id: int):
    return db.query(model.Product).filter(model.Product.id == product_id).first()


def __check_reserved_number_smaller_or_equal_stock_balance(reserved_number: int, stock_balance: int):
    if reserved_number > stock_balance:
        return True
    return False


def create_product(db: Session, product: schemas.ProductCreation):
    if __check_reserved_number_smaller_or_equal_stock_balance(reserved_number=product.reserved_number,
                                                              stock_balance=product.stock_balance):
        return {'404': 'Reserved number should be less or equal stock balance.'}

    db_product = model.Product(
        id=product.id,
        name=product.name,
        group_id=product.group_id,
        stock_balance=product.stock_balance,
        description=product.description,
        reserved_number=product.reserved_number,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def remove_product(db: Session, product_id: int):
    product = __get_product_instance_by_id(db=db, product_id=product_id)
    db.delete(product)
    db.commit()
    return {'200': 'Product has been removed.'}


def increase_stock_balance(db: Session, product_id: int, increasing_value: int):
    product = __get_product_instance_by_id(db=db, product_id=product_id)
    product.stock_balance += increasing_value
    db.commit()
    db.refresh(product)
    return product


def reduce_stock_balance(db: Session, product_id: int, reducing_value: int):
    product = __get_product_instance_by_id(db=db, product_id=product_id)
    if product.stock_balance - reducing_value < product.reserved_number:
        return {'404': 'Stock balance can\'t be less than 0 or reserved number.'}
    product.stock_balance -= reducing_value
    db.commit()
    db.refresh(product)
    return product


def get_rest_not_reserved_product(db: Session, product_id: int):
    product = __get_product_instance_by_id(db=db, product_id=product_id)
    return product.stock_balance - product.reserved_number


def increase_reserved_product(db: Session, product_id: int, increasing_value: int):
    product = __get_product_instance_by_id(db=db, product_id=product_id)
    if increasing_value > get_rest_not_reserved_product(db=db, product_id=product_id):
        return {'404': 'Reserved number can\'t be greater than stock balance.'}
    product.reserved_number += increasing_value
    db.commit()
    db.refresh(product)
    return product


def reduce_reserved_product(db: Session, product_id: int, reducing_value: int):
    product = __get_product_instance_by_id(db=db, product_id=product_id)
    if product.reserved_number - reducing_value < 0:
        return {'404': 'Reserved number can\'t be less than 0.'}
    product.reserved_number -= reducing_value
    db.commit()
    db.refresh(product)
    return product


def change_product_group(db: Session, product_id: int, new_group_id: int):
    product = __get_product_instance_by_id(db=db, product_id=product_id)
    group = products_group_controller.__get_products_group_instance_by_id(db=db, products_group_id=new_group_id)
    if not group:
        return 'There is not group with such ID'
    product.group_id = new_group_id
    product.group = group
    db.commit()
    db.refresh(product)
    return product



def change_product_property(db: Session, product_id: int, property_name: str, new_property_value):
    db_product_json = __get_product_instance_by_id(db=db, product_id=product_id).json()
    property_type = type(db_product_json[property_name])

    if property_name in ['stock_balance', 'reserved_number']:
        return {'404': 'There are unique methods for properties stock balance, reserved_number and group.'}

    if property_type != type(new_property_value):
        try:
            new_property_value = db_product_json[property_name].__class__(new_property_value)
        except ValueError:
            return {'404': 'Incorrect property type.'}

    db_product_json[property_name] = new_property_value
    remove_product(db=db, product_id=product_id)

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
