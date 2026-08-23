import pandas as pd
import sqlite3
from datetime import date

DB_PATH = "expense.db"


# DB取得
def get_expense_df(DB_PATH: str) -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql("select * from expense", conn, parse_dates=["expense_date"])


def get_payroll_monthly_df(DB_PATH: str) -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql(
            "select * from payroll_monthly", conn, parse_dates=["payment_date"]
        )


def get_payroll_bonus_df(DB_PATH: str) -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql(
            "select * from payroll_bonus", conn, parse_dates=["payment_date"]
        )


def get_expense_by_month(year: int, month: int) -> pd.DataFrame:
    """指定した年月のexpenseデータを取得"""
    query = """
        select * 
        from expense 
        where strftime('%Y, expense_date) = ?
            and strftime('%m', expense_date) = ?
        order by expense_date
    """
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql(
            query, conn, parms=[str(year), f"{month:02d}"], parse_dates=["expense_date"]
        )
    return df

def insert_expense(expense_date: date, category: str, amount: int, memo: str ="") -> None:
    """expenseテーブルに1件追加"""
    query = """
        insert into expense (expense_date, category, amount, memo)
        values (?, ?, ?, ?)
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(query, (expense_date.isoformat(), category, amount, memo))
        conn.commit()