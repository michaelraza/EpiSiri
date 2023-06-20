#Importation
from fastapi import FastAPI, Body, HTTPException, Response, status
from typing import Optional, Union
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from schematics.models import Model
import connection #MongoDB

import psycopg2 #PostgreSQL
from psycopg2.extras import RealDictCursor
#connexion
connexion = psycopg2.connect(
    host="localhost",
    database="EpiSiri",
    user="postgres",
    password="root",
    cursor_factory=RealDictCursor
)
cursor = connexion.cursor() #todo 





api_description = description = """ 
En 2077, tous les individus sur Terre ont un Iphone, sans exception. Le monde de demain est peut être déja le monde d'aujourd'hui. Payer ne nécéssite plus de contact, que ce soit humain, physique ni même électronique. D'un claquement de voix, les humains pourront payer et récuperer leur affaires, le seul outil que nous auront réellement besoin c'est d'une connexion internet de très haut débit instantané sans ping, ainsi que d'appareils beaucoup trop chère, mais l'avenir a un prix. C'est la qu'EpiSiri entre en scène, avec nos Iphone légèrement onéreux, nous pourrons choisir, commandé avec la voix et récéptionner les colis juste avec nos beaux Iphones. Voila ce qu'est EpiSiri, l'avenir, mais aussi le présent, elle sera toujours a votre écoute (littéralement).
You will be able to do the CRUD :
Create 
Read
Update
Delete

For Products, Users and Transactions
"""
tags_metadata = [
    {
        "name" : "EpiSiri",
        "description": "Welcome To EpiSiri",
        "externalsDocs" : {
            "description": "items external docs",
            "url": "https://fastapi.tiangolo.com/"
        }
    }
]
app = FastAPI(
    title="EpiSiri API",
    description=api_description,
    openapi_tags= tags_metadata
)

#Root de base

@app.get("/",  tags=["Root"])
async def root():
        return { "message" : "Est ce que c'est bon pour vous ? " }

#Class Articles

class Articles(BaseModel):
    
    productName: str
    productPrice: float
    productAvailability: bool = True
    productWeight: float
    
class ProductRouter:
    articles = [
        {"itemId": "item_id", "itemName": "item_name", "itemPrice": "item_price"},
        {"itemId": "item_id1", "itemName": "item_name1", "itemPrice": "item_price1"},
        {"itemId": "item_id2", "itemName": "item_name2", "itemPrice": "item_price2"},
        {"itemId": "item_id3", "itemName": "item_name3", "itemPrice": "item_price3"}
    ]
    """Pour récuperer tous les articles
    """
    @app.get("/products", tags=["Products"])
    async def get_articles():
        cursor.execute("SELECT * FROM article")
        dbProducts = cursor.fetchall()    
        return {
            "articles": dbProducts,
            "limit": 10,
            "total": len(dbProducts),
            "skip": 0
        }
    """Pour récuperer tous les articles par ID
    """
    @app.get("/products/{itemId}", tags=["Products"])
    async def get_item(itemId: int, response: Response):
        try:
            cursor.execute(f"SELECT * FROM article WHERE id={itemId}")
            corresponding_product = cursor.fetchall()
            if(corresponding_product):
                return corresponding_product
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Article not found"
                )
        except:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Article not found"
                )
    """Pour ajouter des articles
    """
    @app.post("/products", tags=["Products"])
    async def create_article(payload: Articles, response: Response):
        cursor.execute("INSERT INTO article (name, price_eur, weight_kg) VALUES(%s,%s,%s) RETURNING *;",(payload.productName, payload.productPrice, payload.productWeight))
        connexion.commit()
        response.status_code = status.HTTP_201_CREATED
        return {
            "message": f"{payload.productName} added successfully"
        }

    """Pour supprimer des articles par ID
    """
    @app.delete("/products/{itemId}", tags=["Products"])
    async def delete_item(itemId: int, response: Response):
        cursor.execute(f"DELETE FROM article WHERE id={itemId}")
        connexion.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
        return 
              
    """Pour ramplacer des articles par ID
    """
    @app.put("/products/{itemId}", tags=["Products"])
    async def update_item(itemId: int, payload: Articles):
        try:
            query = "UPDATE article SET name = %s, price_eur = %s, weight_kg = %s WHERE id = %s RETURNING *"
            values = (payload.productName, payload.productPrice, payload.productWeight, itemId)
            cursor.execute(query, values)
            updated_product = cursor.fetchone()
            connexion.commit()
            if updated_product:
                return {
                    "message": f"{payload.productName} updated successfully"
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Article not found"
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
            

            
            
            
            
            

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserRouter:
    users = [
        {"userId": "user_id1"},
        {"userId": "user_id2"},
        {"userId": "user_id3"}
    ]
    """Pour récuperer tous les utilisateurs
    """    
    @app.get("/users", tags=["Users"])
    async def get_users():
        return {"users": UserRouter.users}
    
    """Pour récuperer tous l'utilisateur par ID
    """ 
    
    @app.get("/users/{userId}", tags=["Users"])
    async def get_user_by_id(userId: int, response: Response):
        try:
            corresponding_user = UserRouter.users[userId - 1]
            return corresponding_user
        except IndexError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

    """Pour ajouter des utilisateurs
    """

    @app.post("/users", tags=["Users"])
    async def create_user(payload: User, response: Response):
        UserRouter.users.append(payload.dict())
        response.status_code = status.HTTP_201_CREATED

class Transactions(BaseModel):
    transactionId: int
    itemId: int
    quantity: int
class TransactionRouter:
    transactions = [
        {"transactionId": 1, "itemId": 1, "quantity": 2, "amount": 10.0},
        {"transactionId": 2, "itemId": 2, "quantity": 1, "amount": 5.0},
        {"transactionId": 3, "itemId": 3, "quantity": 3, "amount": 20.0}
    ]

    """Pour récupérer toutes les transactions
    """
    
    @app.get("/transactions", tags=["Transactions"])
    async def get_transactions():
        return {"transactions": TransactionRouter.transactions}

    """Pour récupérer toutes les transactions par ID
    """

    @app.get("/transactions/{transactionId}", tags=["Transactions"])
    async def get_transaction(transactionId: int, response: Response):
        try:
            corresponding_transaction = TransactionRouter.transactions[transactionId - 1]
            return corresponding_transaction
        except IndexError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
            
    """Pour rajouter des transactions
    """
    @app.post("/transactions", tags=["Transactions"])
    async def create_transaction(payload: Transactions, response: Response):
        TransactionRouter.transactions.append(payload.dict())
        response.status_code = status.HTTP_201_CREATED  
#MONGODB
class Customer(Model):
    cust_id = Field(default=lambda: str(ObjectId()))
    cust_email = EmailStr
    cust_name = Field

# An instance of class User
newuser = Customer()

# Fonction pour créer et assigner des valeurs à l'instance de la classe Customer créée
def create_user(email, username):
    newuser = Customer()
    newuser.cust_email = email
    newuser.cust_name = username
    return dict(newuser)



# Endpoint Signup avec la méthode POST
@app.post("/signup/{email}/{username}")
def addUser(email, username: str):
    user_exists = False
    data = create_user(email, username)

    # Convertir les données en dict pour pouvoir les insérer facilement dans MongoDB
    dict_data = dict(data)

    # Vérifie si un utilisateur existe avec l'e-mail donné
    if connection.db.users.find({'cust_email': data['cust_email']}).count() > 0:
        user_exists = True
        print("Customer Exists")
        return {"message": "Customer Exists"}

    # Si l'e-mail n'existe pas, créez l'utilisateur
    elif not user_exists:
        connection.db.users.insert_one(dict_data)
        return {"message": "User Created", "email": dict_data['cust_email'], "name": dict_data['cust_name']} 
