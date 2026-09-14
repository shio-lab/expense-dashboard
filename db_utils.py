"""db_utils.py"""
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

def get_payroll_monthly_by_month(year: int, month: int) -> pd.DataFrame:
    """指定した年月の給与明細を取得"""
    query = """
        select * 
        from payroll_monthly
        where strftime('%Y', payment_date) = ?
            and strftime('%m', payment_date) = ?
        order by payment_date
    """
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql(
            query, conn, params=[str(year), f"{month:02d}"], parse_dates=["payment_date"]
        )
    return df

def get_payroll_bonus_by_month(year: int, month: int) -> pd.DataFrame:
    """指定した年月の賞与明細を取得"""
    query = """
        select *
        from payroll_bonus
        where strftime('%Y', payment_date) = ?
            and strftime('%m', payment_date) = ?
        order by payment_date
    """
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql(
            query, conn, params=[str(year), f"{month:02d}"], parse_dates=["payment_date"]
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

def delete_expense(record_id: int) -> None:
    """expenseテーブルから1件削除"""
    query = "delete from expense where id = ?"
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(query, (record_id,))
        conn.commit()
    