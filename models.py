# models.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from sqlalchemy.sql import func # Import func for server-side default
from datetime import datetime

# SQLAlchemy Base class for model definitions
Base = declarative_base()

# SQLAlchemy model for User
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    # Add relationship to the Order model
    orders = relationship("Order", back_populates="user")

# SQLAlchemy model for Order
class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    order_date = Column(DateTime, default=func.now(), server_default=func.now())  # Use DateTime with server-side default

    # Relationship back to the User model
    user = relationship("User", back_populates="orders")

# Pydantic model for creating a User (used for request validation)
class UserCreate(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True  # Tells Pydantic to convert SQLAlchemy models to dict

# Pydantic model for creating an Order (used for request validation)
class OrderCreate(BaseModel):
    user_id: int
    product_name: str
    quantity: int

    class Config:
        orm_mode = True  # Tells Pydantic to convert SQLAlchemy models to dict

# Pydantic model for reading a User (used for response serialization)
class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True  # Tells Pydantic to convert SQLAlchemy models to dict

# Pydantic model for reading an Order (used for response serialization)
class OrderOut(BaseModel):
    id: int
    user_id: int
    product_name: str
    quantity: int
    order_date: datetime  # datetime will be serialized correctly to ISO format string

    class Config:
        orm_mode = True 
#####################################
class OrderRequest(BaseModel):
    user_id: int
    raw_description: str
