from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

# Classe de base pour créer les modèles
Base = declarative_base()

class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price_eur = Column(Numeric, nullable=False)
    weight_kg = Column(Numeric, nullable=False)
    availability = Column(Boolean, nullable=True, server_default='FALSE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')
    
class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')
