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
async def auth_customer(
        payload : OAuth2PasswordRequestForm= Depends(), 
        cursor: Session= Depends(database1.get_cursor)
    ):
    print(payload.__dict__)
    # 1. Recup les crédentials (username car il provient du formulaire par default de FastAPI)
    corresponding_customer = cursor.query(models.Customers).filter(models.Customers.email == payload.username).first()
    # 2. Vérifier dans la DB si user exist
    if(not corresponding_customer):
         raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail='email not good'
         )
    # 3. Vérif sur passwork hashé 
    valid_pwd = utilities.verify_password(
        payload.password,
        corresponding_customer.password
     )
    if(not valid_pwd):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='password not good' 
        ) 
    # 4. Génération du JWT
    token = utilities.generate_token(corresponding_customer.id.value)
    print(token)
    return token


@router.get("/me")
def get_user_profile(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
        current_user_id = authorize.get_jwt_subject()
        user = get_user_by_id(current_user_id)
        return user
    except AuthJWTException:
        raise HTTPException(status_code=401, detail="Invalid access token")


def authenticate_user(email: str, password: str):
    # Retrieve user from the database based on email
    user = database1.get_user_by_email(email)
    if user and utilities.verify_password(password, user.password):
        return user
    return None


def get_user_by_id(user_id: str):
    # Retrieve user from the database based on user_id
    user = database1.get_user_by_id(user_id)
    return user

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "your_secret_key", algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = ...  # Retrieve the user from the database based on user_id
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")