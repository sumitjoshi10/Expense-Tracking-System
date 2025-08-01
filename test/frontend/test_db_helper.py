import pytest
from backend import db_helper

def test_fetch_expenses_for_date_aug_04():
    expense  = db_helper.fetch_expenses_for_date("2024-08-04")
    print(expense)

    assert len(expense) == 3
    assert expense[0]['amount'] == 25.0
    assert expense[0]['category'] == "Food"
    assert expense[0]["notes"] == "Lunch"
    
    assert expense[1]['amount'] == 200.0
    assert expense[1]['category'] == "Shopping"
    assert expense[1]["notes"] == "Home supplies"
    

def test_fetch_expenses_for_invalid_date():
    expenses = db_helper.fetch_expenses_for_date("9999-08-15")

    assert len(expenses) == 0
    
def test_fetch_expense_summary_invalid_range():
    summary = db_helper.fetch_expense_summary("2099-01-01", "2099-12-31")
    assert len(summary) == 0