from fastapi import APIRouter, HTTPException, status, Depends
from classes import schemas, database1, models
from sqlalchemy.orm import Session
import utilities
from jose import jwt
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.security import OAuth2PasswordBearer
# Formulaire de lancement du OAuth /auth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/auth',
    tags=["Auth"]
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

@router.post('/login', status_code=status.HTTP_201_CREATED)
async def auth_Customer(
        payload : OAuth2PasswordRequestForm= Depends(), 
        cursor: Session= Depends(database1.get_cursor)
    ):
    print(payload.__dict__)
    # 1. Recup les crédentials (Customername car il provient du formulaire par default de FastAPI)
    corresponding_Customer = cursor.query(models.Customers).filter(models.Customers.email == payload.username).first()
    # 2. Vérifier dans la DB si Customer exist
    if(not corresponding_Customer):
         raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail='email not good'
         )
    # 3. Vérif sur passwork hashé 
    valid_pwd = utilities.verify_password(
        payload.password,
        corresponding_Customer.password
     )
    if(not valid_pwd):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='password not good' 
        ) 
    # 4. Génération du JWT
    token = utilities.generate_token(corresponding_Customer.password)
    print(token)
    return token


@router.get("/me")
def get_Customer_profile(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
        current_Customer_id = authorize.get_jwt_subject()
        Customer = get_Customer_by_id(current_Customer_id)
        return Customer
    except AuthJWTException:
        raise HTTPException(status_code=401, detail="Invalid access token")


def authenticate_Customer(email: str, password: str):
    # Retrieve Customer from the database based on email
    Customer = database1.get_Customer_by_email(email)
    if Customer and utilities.verify_password(password, Customer.password):
        return Customer
    return None


def get_Customer_by_id(Customer_id: str):
    # Retrieve Customer from the database based on Customer_id
    Customer = database1.get_Customer_by_id(Customer_id)
    return Customer

def get_current_Customer(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "your_secret_key", algorithms=["HS256"])
        Customer_id = payload.get("sub")
        if Customer_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        Customer = ...  # Retrieve the Customer from the database based on Customer_id
        if Customer is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return Customer
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")