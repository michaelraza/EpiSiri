from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from classes import models, schemas, database1
import utilities


router = APIRouter(prefix='/Customers', tags=['Customers'])

@router.post('', response_model=schemas.Customer_response, status_code= status.HTTP_201_CREATED)
async def create_Customer(
    payload: schemas.Customer_POST_Body, 
    cursor: Session = Depends(database1.get_cursor),
    ):
    try: 
        hashed_password = utilities.hash_password(payload.CustomerPassword)
        new_Customer= models.Customers(password=hashed_password, email= payload.CustomerEmail)
        cursor.add(new_Customer)
        cursor.commit()
        cursor.refresh(new_Customer)
        # return {'message':f'The Customer has been created with the id: {new_Customer.id}'}
        return new_Customer
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Customer already exists" 
        )
        
@router.get('', response_model=List[schemas.Customer_response])
async def get_all_Customers(cursor: Session = Depends(database1.get_cursor)):
    all_Customers = cursor.query(models.Customers).all()
    return all_Customers

@router.get('/{Customer_id}', response_model=schemas.Customer_response)
async def get_Customer_by_id(Customer_id:int, cursor: Session = Depends(database1.get_cursor)):
    corresponding_Customer = cursor.query(models.Customers).filter(models.Customers.id == Customer_id).first()
    if(corresponding_Customer):
        return corresponding_Customer
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No Customer with id:{Customer_id}'
        )