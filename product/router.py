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
async def change(product_id: int, property_name: str, new_property_value, db: Session = Depends(get_db)):
    return controller.change_product_property(db=db, product_id=product_id,
                                              property_name=property_name,
                                              new_property_value=new_property_value)
