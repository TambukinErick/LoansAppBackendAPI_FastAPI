from fastapi import Depends, FastAPI
import logging
from .models import models
from .database import engine
from .routers import loan_items, clients, transactions, block_out

models.Base.metadata.create_all(bind=engine)

description = """

This application is a recreated prototype of a preexisitng application made for a student organization.


## Context
One of the responsibilities of the student organization was to manage and facilitate transactions for students who wanted to borrow
items for their school work such as adapters, chargers, speakers, etc.



## Clients
Clients are students who are registered within the system.

## Loan Items
The actual items that the organization manages, tracks and loans out to students.
Items are categorized into two categories, A and B. These 2 categories have their own borrowing policies and penalties if the students
return the borrowed items late.

## Transactions
A record of the loan made by a client when borrowing an item from the organization.

## Block Out Dates
A record of which days are blocked out which render the organization's office is closed

## Block Out Times
A record of timespans within days wherein the organization's office cannot render services.
"""
app = FastAPI(
    title="Loans System App",
    description=description,
    summary="A Backend API for an internal web application used to facilitate item transactions within a university",
    version="0.0.1"
)

app.include_router(loan_items.router)
app.include_router(clients.router)
app.include_router(transactions.router)
app.include_router(block_out.router)


@app.get("/Home/")
async def root():
    return {"message": "Hello World"}
