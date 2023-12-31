from datetime import datetime
from pydantic import BaseModel
from enum import Enum
# DTO : Data Transfert Object
# Représente la structure de la données (data type) en entrée ou en sortie de notre API.

class Product_POST_Body (BaseModel):
    productName: str
    productPrice: float
    productWeight: float
    productAvailability: bool
    
class Products_PATCH_Body (BaseModel):
    productName: str
    productPrice: float
    productWeight: float
    productAvailability: bool
    
class Product_GETID_Response(BaseModel): # format de sortie (response)
    id: int
    name: str
    price_eur: str
    weight_kg: float
    availability: bool
    class Config: # Lors des réponses, nous avons souvant à utiliser les données sortie de notre database. La Config ORM nous permet de "choisir" les columnes à montrer. 
        orm_mode= True
    
class Customer_POST_Body (BaseModel):
    CustomerEmail:str
    CustomerPassword: str

class Customer_response (BaseModel):
    id: int
    email:str
    create_at: datetime
    isAdmin: bool
    class Config: # Importante pour la traduction ORM->DTO
        orm_mode= True


