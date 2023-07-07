from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from classes import models, schemas, database1
import utilities


router = APIRouter(prefix='/customers', tags=['Customers'])

@router.post('', response_model=schemas.Customer_response, status_code= status.HTTP_201_CREATED)
async def create_customer(
    payload: schemas.Customer_POST_Body, 
    cursor: Session = Depends(database1.get_cursor),
    ):
    try: 
        hashed_password = utilities.hash_password(payload.customerPassword)
        new_customer= models.Customers(password=hashed_password, email= payload.customerEmail)
        cursor.add(new_customer)
        cursor.commit()
        cursor.refresh(new_customer)
        # return {'message':f'The customer has been created with the id: {new_customer.id}'}
        return new_customer
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists" 
        )
        
@router.get('', response_model=List[schemas.Customer_response])
async def get_all_customers(cursor: Session = Depends(database1.get_cursor)):
    all_customers = cursor.query(models.Customers).all()
    return all_customers

@router.get('/{customer_id}', response_model=schemas.Customer_response)
async def get_user_by_id(customer_id:int, cursor: Session = Depends(database1.get_cursor)):
    corresponding_customer = cursor.query(models.Customers).filter(models.Customers.id == customer_id).first()
    if(corresponding_customer):
        return corresponding_customer
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No user with id:{customer_id}'
        )