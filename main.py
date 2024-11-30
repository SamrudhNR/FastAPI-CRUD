from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User, Order, UserCreate, OrderCreate, UserOut, OrderOut
from database import engine, SessionLocal
from pydantic import BaseModel
from typing import List
from datetime import datetime
import logging
from services.openap_service import process_with_openai
from services.local_modelservice import process_with_local_model
from models import OrderRequest
import json
# import asyncio
from config import OPENAI_API_KEY

# from openai_utils import process_with_openai


app = FastAPI()

async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

@app.post("/users/", response_model=UserOut)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    new_user = User(name=user.name, email=user.email)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

@app.get("/users/{user_id}", response_model=UserOut)
async def read_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user: UserCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).filter(User.id == user_id))
    existing_user = result.scalar_one_or_none()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_user.name = user.name
    existing_user.email = user.email
    
    await session.commit()
    return existing_user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).filter(User.id == user_id))
    existing_user = result.scalar_one_or_none()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Await the delete operation
    await session.delete(existing_user)
    await session.commit()  # Ensure commit happens after delete
    
    return {"message": "User deleted successfully"}

@app.get("/")
def read_root():
    return {"Hello": "World"}

##########
@app.post("/orders/", response_model=OrderOut)
async def create_order(order: OrderCreate, session: AsyncSession = Depends(get_session)):
    new_order = Order(**order.dict())  # Creating the new order
    session.add(new_order)
    await session.commit()
    await session.refresh(new_order)
    return new_order  # Returning Pydantic model by using orm_mode

@app.get("/orders/{order_id}", response_model=OrderOut)
async def read_order(order_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Order).filter(Order.id == order_id))
    order = result.scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order  # Returning Pydantic model by using orm_mode

@app.put("/orders/{order_id}", response_model=OrderOut)
async def update_order(order_id: int, order: OrderCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Order).filter(Order.id == order_id))
    existing_order = result.scalar_one_or_none()
    if existing_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    existing_order.product_name = order.product_name
    existing_order.quantity = order.quantity
    
    await session.commit()
    return existing_order  # Returning Pydantic model by using orm_mode

@app.delete("/orders/{order_id}")
async def delete_order(order_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Order).filter(Order.id == order_id))
    existing_order = result.scalar_one_or_none()
    if existing_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    await session.delete(existing_order)
    await session.commit()
    return {"message": "Order deleted successfully"}


#############################################################333
@app.post("/orders/ai", response_model=OrderOut)
async def create_order_with_ai(
    order_request: OrderRequest, 
    use_local_model: bool = False,  # Option to switch between OpenAI and local model
    session: AsyncSession = Depends(get_session)
):
    # Prepare OpenAI prompt
    prompt = f"""
    Extract structured data from this description:
    "{order_request.raw_description}"

    Expected output format:
    {{
        "product_name": "string",
        "quantity": integer
    }}
    """
    
    # Call OpenAI API
    try:
        response = await process_with_openai(prompt)
        extracted_data = json.loads(response)  # Use json.loads to convert response to dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing data with OpenAI: {str(e)}")

    # Validate extracted data
    if "product_name" not in extracted_data or "quantity" not in extracted_data:
        raise HTTPException(status_code=400, detail="Invalid data from OpenAI")

    # Create a new order
    new_order = Order(
        user_id=order_request.user_id,
        product_name=extracted_data["product_name"],
        quantity=extracted_data["quantity"],
    )
    session.add(new_order)
    await session.commit()
    await session.refresh(new_order)

    return new_order