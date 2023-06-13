from fastapi import FastAPI, Body, HTTPException, Response, status
from typing import Optional, Union
from pydantic import BaseModel

app = FastAPI()

# Data models

class Articles(BaseModel):
    itemId: int
    itemName: str
    itemPrice: float
    availability: bool = True
    rating: Optional[int]

class ProductRouter:
    articles = [
        {"itemId": "item_id", "itemName": "item_name", "itemPrice": "item_price"},
        {"itemId": "item_id1", "itemName": "item_name1", "itemPrice": "item_price1"},
        {"itemId": "item_id2", "itemName": "item_name2", "itemPrice": "item_price2"},
        {"itemId": "item_id3", "itemName": "item_name3", "itemPrice": "item_price3"}
    ]

    @app.get("/products")
    async def get_articles():
        return {
            "articles": ProductRouter.articles,
            "limit": 10,
            "total": len(ProductRouter.articles),
            "skip": 0
        }

    @app.get("/products/{itemId}")
    async def get_item(itemId: int, response: Response):
        try:
            corresponding_product = ProductRouter.articles[itemId - 1]
            return corresponding_product
        except IndexError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )

    @app.post("/products")
    async def create_article(payload: Articles, response: Response):
        ProductRouter.articles.append(payload.dict())
        response.status_code = status.HTTP_201_CREATED
        return {
            "message": f"{payload.itemName} added successfully"
        }

    @app.delete("/products/{itemId}")
    async def delete_item(itemId: int, response: Response):
        try:
            ProductRouter.articles.pop(itemId - 1)
            response.status_code = status.HTTP_204_NO_CONTENT
        except IndexError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )

    @app.put("/products/{itemId}")
    async def replace_item(itemId: int, payload: Articles, response: Response):
        try:
            ProductRouter.articles[itemId - 1] = payload.dict()
            return {"message": f"Item successfully updated: {payload.itemName}"}
        except IndexError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
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

    @app.get("/users")
    async def get_users():
        return {"users": UserRouter.users}

    @app.get("/users/{userId}")
    async def get_user_by_id(userId: int, response: Response):
        try:
            corresponding_user = UserRouter.users[userId - 1]
            return corresponding_user
        except IndexError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

    @app.post("/users")
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

    @app.get("/transactions")
    async def get_transactions():
        return {"transactions": TransactionRouter.transactions}

    @app.get("/transactions/{transactionId}")
    async def get_transaction(transactionId: int, response: Response):
        try:
            corresponding_transaction = TransactionRouter.transactions[transactionId - 1]
            return corresponding_transaction
        except IndexError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )

    @app.post("/transactions")
    async def create_transaction(payload: Transactions, response: Response):
        TransactionRouter.transactions.append(payload.dict())
        response.status_code = status.HTTP_201_CREATED   
