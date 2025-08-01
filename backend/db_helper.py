from contextlib import contextmanager
import mysql.connector

from logging_setup import setup_logging

logger = setup_logging("db_helper")

@contextmanager
def get_db_connection(commit = False):
    """Create a new database connection."""
    connector = mysql.connector.connect(
        host='localhost',
        user='root',
        password= '',
        database='personal_expense'
    )
    cursor = connector.cursor(dictionary=True)
    yield cursor
    if commit:
        connector.commit()
    print("Closing cursor")
    cursor.close()
    connector.close()
    
def fetch_all_records():
    logger.info("Fetching all records from the database")
    querry = "SELECT * FROM expenses"
    
    with get_db_connection() as cursor:
        cursor.execute(querry)
        expenses = cursor.fetchall()
        for expense in expenses:
            print(expense)
    
def fetch_expenses_for_date(expense_date):
    logger.info(f"Fetching expenses for date: {expense_date}")
    with get_db_connection() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses



def insert_expense(expense_date, amount, category, notes):
    logger.info(f"Inserting expense: {expense_date}, {amount}, {category}, {notes}")
    with get_db_connection(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )
        
        
def delete_expenses_for_date(expense_date):
    logger.info(f"Deleting expenses for date: {expense_date}")
    with get_db_connection(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))
        
def fetch_expense_summary(start_date, end_date):
    logger.info(f"Fetching expense summary from {start_date} to {end_date}")
    with get_db_connection() as cursor:
        cursor.execute(
            "SELECT  category, SUM(amount) AS total_amount FROM expenses WHERE expense_date BETWEEN %s AND %s GROUP BY category",
            (start_date, end_date)
        )
        summary = cursor.fetchall()
        return summary
    
def fetch_expense_summary_by_month():
    logger.info("Fetching expense summary by month")
    with get_db_connection() as cursor:
        cursor.execute(
            "SELECT DATE_FORMAT(expense_date, '%Y-%m') AS month, SUM(amount) AS total_amount FROM expenses GROUP BY month ORDER BY DATE_FORMAT(expense_date, '%Y-%m')"
        )
        summary = cursor.fetchall()
        
        return summary
        
if __name__ == "__main__":
    # fetch_all_records()
    # Example usage:
    # fetch_expenses_for_date("2025-07-29")
    # # insert_expense("2025-07-29", 300, "Food", "Panipuri")
    # delete_expenses_for_date("2025-07-29")
    # summary = fetch_expense_summary("2024-08-01", "2024-08-05")
    # for item in summary:
    #     print(item)
    summary = fetch_expense_summary_by_month()
    print(summary)
    # pass