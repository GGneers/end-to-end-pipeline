from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, Customer
from schemas import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse
)


# Create tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Customer API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "FastAPI Database API is running"
    }


# =========================
# POST
# =========================

@app.post(
    "/customers",
    response_model=CustomerResponse
)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):

    # Check if email already exists
    existing_customer = (
        db.query(Customer)
        .filter(Customer.email == customer.email)
        .first()
    )

    if existing_customer:
        raise HTTPException(
            status_code=409,
            detail="Customer already exists"
        )

    new_customer = Customer(
        name=customer.name,
        email=customer.email,
        balance=customer.balance
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


# =========================
# GET
# =========================

@app.get(
    "/customers/{customer_id}",
    response_model=CustomerResponse
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):

    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


# =========================
# PUT
# =========================

@app.put(
    "/customers/{customer_id}",
    response_model=CustomerResponse
)
def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db)
):

    existing_customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not existing_customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if customer.name is not None:
        existing_customer.name = customer.name

    if customer.email is not None:
        existing_customer.email = customer.email

    if customer.balance is not None:
        existing_customer.balance = customer.balance

    db.commit()
    db.refresh(existing_customer)

    return existing_customer


# =========================
# DELETE
# =========================

@app.delete("/customers/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):

    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    db.delete(customer)
    db.commit()

    return {
        "message": "Customer deleted"
    }