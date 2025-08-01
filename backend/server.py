from fastapi import FastAPI, HTTPException
from datetime import date
from typing import List
from pydantic import BaseModel

import db_helper


app = FastAPI()

class Expense(BaseModel):
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date
    
# class ExpenseMonth(BaseModel):
#     month: str
#     total_amount: float

@app.get("/")
def read_root():
    return {"message": "Welcome to the Expense Tracker API"}

@app.get("/expenses/{expense_date}")
def get_expenses(expense_date: date , response_model=List[Expense]):
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expenses from Database")
    return expenses


@app.post("/expenses/{expense_date}")
def add_expense(expense_date: date, expense: List[Expense]):
    db_helper.delete_expenses_for_date(expense_date)
    
    for expense_item in expense:
        db_helper.insert_expense(
            expense_date=expense_date,
            amount=expense_item.amount,
            category=expense_item.category,
            notes=expense_item.notes
        )
        
    return {"message": "Expenses added successfully", "expense_date": expense_date}


@app.post("/analytics/category")
def get_analytics(date_range: DateRange):
    summary = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
    if summary is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expenses from Database")
    
    total_amount = sum([row["total_amount"] for row in summary])
    breakdown = {}
    for row in summary:
        percentage = round(row["total_amount"] / total_amount * 100 if total_amount > 0 else 0,2)

        breakdown[row["category"]] = {
            "total_amount": row["total_amount"],
            "percentage": percentage
            }
    
    return breakdown

@app.get("/analytics/month")
def get_expense_summary_by_month():
    summary = db_helper.fetch_expense_summary_by_month()
    if summary is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expenses from Database")
    return summary