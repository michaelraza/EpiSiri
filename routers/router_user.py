from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from classes import models, schemas, database1
import utilities


router = APIRouter(prefix='/users', tags=['Users'])