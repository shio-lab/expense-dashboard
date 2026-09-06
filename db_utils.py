import pandas as pd
import sqlite3
from datetime import date

DB_PATH = "expense.db"


# DB取得
def get_expense_df() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql("select * from expense", conn, parse_dates=["transaction_date"])


def get_payroll_monthly_df() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql(
            "select * from payroll_monthly", conn, parse_dates=["payment_date"]
        )


def get_payroll_bonus_df() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql(
            "select * from payroll_bonus", conn, parse_dates=["payment_date"]
        )


def get_expense_by_month(year: int, month: int) -> pd.DataFrame:
    """指定した年月のexpenseデータを取得"""
    query = """
        select * 
        from expense 
        where strftime('%Y', transaction_date) = ?
            and strftime('%m', transaction_date) = ?
        order by transaction_date
    """
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql(
            query, conn, params=[str(year), f"{month:02d}"], parse_dates=["transaction_date"]
        )
    return df

def insert_expense(transaction_date: date, category: str, amount: int, memo: str ="") -> None:
    """expenseテーブルに1件追加"""
    query = """
        insert into expense (transaction_date, category, amount, memo)
        values (?, ?, ?, ?)
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(query, (transaction_date.isoformat(), category, amount, memo))
        conn.commit()