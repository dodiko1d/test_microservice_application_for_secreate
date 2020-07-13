from sqlalchemy.orm import Session
from sqlalchemy import literal

from product import controller as product_controller

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


def remove_products_group(db: Session, products_group_id: int):
    products_group = __get_products_group_instance_by_id(db=db, products_group_id=products_group_id)
    products_of_group = products_group.products_of_group.all()
    map(lambda product: db.delete(product), products_of_group)
    db.delete(products_group)
    db.commit()


def change_products_group_property(db: Session, products_group_id: int, property_name: str, new_property_value):
    db_products_group_json = __get_products_group_instance_by_id(db=db, products_group_id=products_group_id).json()
    property_type = type(db_products_group_json[property_name])

    if property_type != type(new_property_value):
        try:
            new_property_value = db_products_group_json[property_name].__class__(new_property_value)
        except ValueError:
            return {'404': 'Incorrect property type.'}

    db_products_group_json[property_name] = new_property_value
    db_products_group = model.ProductsGroup(**db_products_group_json)
    db.add(db_products_group)
    db.commit()
    db.refresh(db_products_group)
    return db_products_group


def __find_products_groups_instances_by_name_part(db: Session, name_part: str, limit: int = 5):
    result = db.query(model.ProductsGroup).filter(literal(name_part).contains(model.ProductsGroup.name))
    return result.limit(limit).all()


def __find_products_groups_instances_by_description_part(db: Session, description_part: str, limit: int = 5):
    result = db.query(model.ProductsGroup).filter(literal(description_part).contains(model.ProductsGroup.description))
    return result.limit(limit).all()


def __get_products_group_instance_by_id(db: Session, products_group_id: int):
    products_group = db.query(model.ProductsGroup).filter(model.ProductsGroup.id == products_group_id).first()
    if not products_group:
        return False
    return products_group


def get_products_group_data_by_id(db: Session, products_group_id: int):
    group = db.query(model.ProductsGroup).filter(model.ProductsGroup.id == products_group_id).first()
    if not group:
        return False
    return {
        'id': group.id,
        'name': group.name,
        'description': group.description,
    }


def __get_last_products_groups_instances_list(db: Session, limit: int):
    return db.query(model.ProductsGroup).limit(limit).all()


def get_last_products_groups_ids_list(db: Session, limit: int):
    return [*map(lambda product_group: product_group.id, __get_last_products_groups_instances_list(db=db, limit=limit))]


def get_last_products_groups_data(db: Session, limit: int):
    last_product_groups_ids_list = get_last_products_groups_ids_list(db=db, limit=limit)
    return [*map(get_products_group_data_by_id, last_product_groups_ids_list)]


def __get_last_products_instances_of_products_group(db: Session, products_group_id: int, limit: int):
    products_group = __get_products_group_instance_by_id(db=db, products_group_id=products_group_id)
    return products_group.products_of_group.limit(limit).all()


def get_products_of_group_ids_list(db: Session, products_group_id: int, limit: int):
    last_products = __get_last_products_instances_of_products_group(
        db=db,
        products_group_id=products_group_id,
        limit=limit
    )
    return [*map(lambda product: product.id, last_products)]


def get_last_products_of_group_data_list(db: Session, products_group_id: int, limit: int):
    def product_data_getter(product_id):
        return product_controller.get_product_data_by_id(db=db, product_id=product_id)

    last_products_ids_list = get_products_of_group_ids_list(db=db, products_group_id=products_group_id, limit=limit)

    return [*map(product_data_getter, last_products_ids_list)]
