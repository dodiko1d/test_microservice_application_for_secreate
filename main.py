from fastapi import FastAPI

# Application separated routers.
from product.router import router as product_router
from products_group.router import router as products_group_router

# Database models.
import product.model as product_model
import products_group.model as products_group_model

# Database settings.
from database import engine
from database import SessionLocal


# Creating models.
product_model.Base.metadata.create_all(bind=engine)
products_group_model.Base.metadata.create_all(bind=engine)

# Application instance.
app = FastAPI()


# Connecting separated routers.
app.include_router(
    product_router,
    prefix='/product',
    tags=['Product'],
    responses={404: {'description': 'Not found'}}
)

app.include_router(
    products_group_router,
    prefix='/products_group',
    tags=['Products group'],
    responses={404: {'description': 'Not found'}}
)