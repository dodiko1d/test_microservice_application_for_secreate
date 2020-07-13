from sqlalchemy.orm import Session
from product import controller as ProductController

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


def __get_products_group_instance_by_id(db: Session, products_group_id: int):
    group = db.query(model.ProductsGroup).filter(model.ProductsGroup.id == products_group_id).first()
    if not group:
        return False
    return group


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


def __get_last_products_instances_of_products_group(db:Session, products_group_id: int, limit: int):
    products_group = __get_products_group_instance_by_id(db=db, products_group_id=products_group_id)
    return products_group.products_of_group.limit(limit).all()


def get_products_of_group_ids_list(db: Session, products_group_id: int, limit: int):
    last_products = __get_last_products_instances_of_products_group(
        db=db,
        products_group_id=products_group_id,
        limit=limit
    )
    return [*map(lambda product: product.stock_keeping_unit, last_products)]


def get_last_products_of_group_data_list(db: Session, products_group_id: int, limit: int):
    last_products_ids_list = get_products_of_group_ids_list(db=db, products_group_id=products_group_id, limit=limit)
    return [*map(lambda product_id: ProductController.get_product_data_by_id(product_id), last_products_ids_list)]
