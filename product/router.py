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


async def check_product_existence(product_id: int, db: Session = Depends(get_db)):
    db_product = controller.get_product_data_by_id(db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=400, detail='Product with this id does not exist.')


@router.post('/create/', summary='Create your product.')
async def create(product: schemas.ProductCreation, db: Session = Depends(get_db)):
    db_product = controller.get_product_data_by_id(db, product_id=product.id)
    if db_product:
        raise HTTPException(status_code=400, detail='Product has been already registered.')
    controller.create_product(db=db, product=product)
    return {'status_code': '200'}


@router.post(
    '/remove/{product_id}',
    summary='Remove a product.',
    dependencies=[Depends(check_product_existence)]
)
async def remove(product_id: int, db: Session = Depends(get_db)):
    controller.remove_product(db=db, product_id=product_id)
    return {'status_code': '200'}


@router.post(
    '/change_property/{product_id}/{property_name}/{new_property_value}',
    summary='Change product property.',
    dependencies=[Depends(check_product_existence)]
)
async def change_product_property(product_id: int, property_name: str, new_property_value, db: Session = Depends(get_db)):
    return controller.change_product_property(db=db, product_id=product_id,
                                              property_name=property_name,
                                              new_property_value=new_property_value)


@router.post(
    '/increase_stock_balance/{product_id}/{increasing_value}',
    summary='Increase product stock balance.',
    dependencies=[Depends(check_product_existence)]
)
def increase_stock_balance(db: Session, product_id: int, increasing_value: int):
    return controller.increase_stock_balance(db=db, product_id=product_id, increasing_value=increasing_value)


@router.post(
    '/reduce_stock_balance/{product_id}/{reducing_value}',
    summary='Reduce product stock balance.',
    dependencies=[Depends(check_product_existence)]
)
def reduce_stock_balance(db: Session, product_id: int, reducing_value: int):
    return controller.reduce_stock_balance(db=db, product_id=product_id, reducing_value=reducing_value)


@router.post(
    '/get_rest_not_reserved_product/{product_id}',
    summary='Get rest not reserved product amount.',
    dependencies=[Depends(check_product_existence)]
)
def get_rest_not_reserved_product(db: Session, product_id: int):
    return controller.get_rest_not_reserved_product(db=db, product_id=product_id)


@router.post(
    '/increase_reserved_product/{product_id}/{increasing_value}',
    summary='Increase reserved product.',
    dependencies=[Depends(check_product_existence)]
)
def increase_reserved_product(db: Session, product_id: int, increasing_value: int):
    controller.increase_reserved_product(db=db, product_id=product_id, increasing_value=increasing_value)


@router.post(
    '/reduce_reserved_product/{product_id}/{reducing_value}',
    summary='Reduce reserved product.',
    dependencies=[Depends(check_product_existence)]
)
def reduce_reserved_product(db: Session, product_id: int, reducing_value: int):
    return controller.reduce_reserved_product(db=db, product_id=product_id, reducing_value=reducing_value)


@router.post(
    '/reduce_reserved_product/{product_id}/{new_group_id}',
    summary='Change product group.',
    dependencies=[Depends(check_product_existence)]
)
def change_product_group(db: Session, product_id: int, new_group_id: int):
    return controller.change_product_group(db=db, product_id=product_id, new_group_id=new_group_id)
