from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Numeric, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum

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
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.id", ondelete="RESTRICT"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="RESTRICT"), nullable=False)
    transaction_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default="now()")
    


    