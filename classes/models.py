from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

# Classe de base pour créer les modèles
Base = declarative_base()

class Products(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price_eur = Column(Numeric, nullable=False)
    weight_kg = Column(Numeric, nullable=False)
    availability = Column(Boolean, nullable=True, server_default='FALSE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')
    
class Customers(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')

class Transactions(Base):
    __tablename__="transaction"
    id= Column(Integer, primary_key=True, nullable=False)
    customer_id= Column(Integer, ForeignKey("customer.id", ondelete="RESTRICT"), nullable=False)  # Les Foreign Keys sont basés sur les clé principales des autres tables mais ce n'est pas obligatoire
    product_id = Column(Integer, ForeignKey("product.id", ondelete="RESTRICT"), nullable=False) # ondelete permet de choisir la cascade d'action suite à la suppression (supprimer une transation, doit-elle suppimer le customer ou le produit?)
    transaction_date=Column(TIMESTAMP(timezone=True), nullable=False, server_default="now()")