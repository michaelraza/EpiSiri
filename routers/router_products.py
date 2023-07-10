from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from classes.database1 import get_cursor
from classes import models, schemas

router = APIRouter(
    prefix='/products',
    tags=['Products']
)

@router.get('')
async def get_products(cursor: Session = Depends(get_cursor)):
    print(cursor.query(models.Products))  # Requète SQL générée
    all_products = cursor.query(models.Products).all()  # Lancement de la requête
    return {
        "products": all_products,
        "limit": 10,
        "total": 2,
        "skip": 0
    }

# Read by id
@router.get('/{product_id}')
async def get_product(product_id: int, cursor: Session = Depends(get_cursor)):
    corresponding_product = cursor.query(models.Products).filter(models.Products.id == product_id).first()
    if corresponding_product:
        return corresponding_product
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No corresponding product found with id: {product_id}"
        )

# CREATE / POST
@router.post('', status_code=status.HTTP_201_CREATED)
async def create_product(payload: schemas.Product_POST_Body, cursor: Session = Depends(get_cursor)):
    new_product = models.Products(name=payload.productName, price_eur=payload.productPrice, weight_kg=payload.productWeight, availability=payload.productAvailability)  # build the insert
    cursor.add(new_product)  # Send the query
    cursor.commit()  # Save the staged change
    cursor.refresh(new_product)
    return {"message": f"New watch {new_product.name} added successfully with id: {new_product.id}"}

# DELETE
@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, cursor: Session = Depends(get_cursor)):
    # Recherche sur le produit existe ?
    corresponding_product = cursor.query(models.Products).filter(models.Products.id == product_id)
    if corresponding_product.first():
        # Continue to delete
        corresponding_product.delete()  # supprime
        cursor.commit()  # commit the stated changes (changement latent)
        return
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No corresponding product with id: {product_id}'
        )

# UPDATE
@router.patch('/{product_id}')
async def update_product(product_id: int, payload: schemas.Products_PATCH_Body, cursor: Session = Depends(get_cursor)):
    # trouver le produit correspondant
    corresponding_product = cursor.query(models.Products).filter(models.Products.id == product_id)
    if corresponding_product.first():
        # mise à jour (quoi avec quelle valeur ?) Body -> DTO
        corresponding_product.update({'availability': payload.availability})
        cursor.commit()
        return corresponding_product.first()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No corresponding product with id: {product_id}'
        )