from fastapi import Depends, FastAPI, HTTPException, status
import schematics
from sqlalchemy.orm import Session

import schemas
import models
from database1 import get_cursor, database_engine

import router_products
import router_customers

# Créer les tables si elles ne sont pas présente dans la DB
models.Base.metadata.create_all(bind=database_engine)

app = FastAPI()

app.include_router(router_products.router)
app.include_router(router_customers.router)

