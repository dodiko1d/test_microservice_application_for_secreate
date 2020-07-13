""" Site paths work control - call necessary controllers. """

from fastapi import APIRouter, Depends, HTTPException
from . import schemas, controller
from sqlalchemy.orm import Session
from database import SessionLocal


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


async def check_products_group_existence(products_group_id: int, db: Session = Depends(get_db)):
    db_products_group = controller.get_products_group_data_by_id(db, products_group_id=products_group_id)
    if not db_products_group:
        raise HTTPException(status_code=400, detail='Products group with this id does not exist.')


@router.get(
    '',
    summary='Get data about last products groups list.',
)
async def get_last_products_groups_data(limit: int = 5, db: Session = Depends(get_db)):
    return controller.get_last_products_groups_data(db=db, limit=limit)


@router.get(
    '/{products_group_id}/',
    summary='Get data about last products groups list.',
)
async def get_products_group_data_by_id(products_group_id: int, db: Session = Depends(get_db)):
    return controller.get_products_group_data_by_id(db=db, products_group_id=products_group_id)


@router.post(
    '/create/',
    summary='Create a products group.',
)
async def create(products_group: schemas.ProductsGroupCreation, db: Session = Depends(get_db)):
    db_products_group = controller.get_products_group_data_by_id(db=db, products_group_id=products_group.id)
    if db_products_group:
        raise HTTPException(status_code=400, detail='Products group is already registered.')
    controller.create_products_group(db=db, products_group=products_group)
    return {'status_code': '200'}


@router.post(
    '/remove/{products_group_id}',
    summary='Remove a products group.',
    dependencies=[Depends(check_products_group_existence)]
)
async def remove(products_group_id: int, db: Session = Depends(get_db)):
    controller.remove_products_group(db=db, products_group_id=products_group_id)
    return {'status_code': '200'}


@router.post(
    '/change_property/{products_group_id}/{property_name}/{new_property_value}',
    summary='Change products group property.',
    dependencies=[Depends(check_products_group_existence)]
)
async def change(products_group_id: int, property_name: str, new_property_value, db: Session = Depends(get_db)):
    return controller.change_products_group_property(db=db, products_group_id=products_group_id,
                                                     property_name=property_name,
                                                     new_property_value=new_property_value)


@router.get(
    '/get_products_ids_list/{products_group_id}',
    summary='Get IDs of all products in group.',
    dependencies=[Depends(check_products_group_existence)],
)
async def get_products_of_group_ids_list(products_group_id: int, limit: int = 5, db: Session = Depends(get_db)):
    return controller.get_products_of_group_ids_list(db=db, products_group_id=products_group_id, limit=limit)


@router.get(
    '/get_products_list/{products_group_id}',
    summary='Get list of last products in group by group ID.',
    dependencies=[Depends(check_products_group_existence)],
)
async def get_last_products_of_group_data_list(products_group_id: int, limit: int = 5, db: Session = Depends(get_db)):
    return controller.get_last_products_of_group_data_list(db=db, products_group_id=products_group_id, limit=limit)
