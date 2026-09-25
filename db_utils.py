"""db_utils.py"""
import pandas as pd
import sqlite3
from datetime import date

DB_PATH = "expense.db"


# DB取得
def get_expense_df() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql("SELECT * FROM expense", conn, parse_dates=["transaction_date"])


def get_payroll_monthly_df() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql(
            "SELECT * FROM payroll_monthly", conn, parse_dates=["payment_date"]
        )


def get_payroll_bonus_df() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql(
            "SELECT * FROM payroll_bonus", conn, parse_dates=["payment_date"]
        )


def get_expense_by_month(year: int, month: int) -> pd.DataFrame:
    """指定した年月のexpenseデータを取得"""
    query = """
        SELECT * 
        FROM expense 
        where strftime('%Y', transaction_date) = ?
            and strftime('%m', transaction_date) = ?
        order by transaction_date
    """
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql(
            query, conn, params=[str(year), f"{month:02d}"], parse_dates=["transaction_date"]
        )
    return df

# def get_payroll_monthly_by_month(year: int, month: int) -> pd.DataFrame:
#     """指定した年月の給与明細を取得"""
#     query = """
#         SELECT * 
#         FROM payroll_monthly
#         where strftime('%Y', payment_date) = ?
#             and strftime('%m', payment_date) = ?
#         order by payment_date
#     """
#     with sqlite3.connect(DB_PATH) as conn:
#         df = pd.read_sql(
#             query, conn, params=[str(year), f"{month:02d}"], parse_dates=["payment_date"]
#         )
#     return df

# def get_payroll_bonus_by_month(year: int, month: int) -> pd.DataFrame:
#     """指定した年月の賞与明細を取得"""
#     query = """
#         SELECT *
#         FROM payroll_bonus
#         where strftime('%Y', payment_date) = ?
#             and strftime('%m', payment_date) = ?
#         order by payment_date
#     """
#     with sqlite3.connect(DB_PATH) as conn:
#         df = pd.read_sql(
#             query, conn, params=[str(year), f"{month:02d}"], parse_dates=["payment_date"]
#         )
#     return df

def insert_expense(transaction_date: date, category: str, amount: int, memo: str ="") -> None:
    """expenseテーブルに1件追加"""
    query = """
        INSERT INTO expense (transaction_date, category, amount, memo)
        values (?, ?, ?, ?)
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(query, (transaction_date.isoformat(), category, amount, memo))
        conn.commit()

def delete_expense(record_id: int) -> None:
    """expenseテーブルから1件削除"""
    query = "DELETE FROM expense WHRER id = ?"
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(query, (record_id,))
        conn.commit()


def insert_payroll_monthly(
        payment_date: date,
        base_salary: int,
        overtime_allowance: int = 0,
        other_allowance: int = 0,
        rent_deduction: int = 0,
        employment_insurance: int = 0,
        employee_pension: int = 0,
        health_insurance_basic: int = 0,
        health_insurance_special: int = 0,
        child_support_contribution: int = 0,
        income_tax: int = 0,
        resident_tax: int = 0,
        labor_union_fee: int = 0,
        other_deduction: int = 0,
        memo: str = "",
) -> None:
    """payroll_monthlyテーブルに1件追加"""
    query = """
        INSERT INTO payroll_monthly (
            payment_date, base_salary, overtime_allowance, other_allowance,
            rent_deduction, employment_insurance, employee_pension,
            health_insurance_basic, health_insurance_special,
            child_support_contribution, income_tax, resident_tax,
            labor_union_fee, other_deduction, memo
        )
       values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(query,(
            payment_date.isoformat(),
            base_salary,
            overtime_allowance,
            other_allowance,
            rent_deduction,
            employment_insurance,
            employee_pension,
            health_insurance_basic,
            health_insurance_special,
            child_support_contribution,
            income_tax,
            resident_tax,
            labor_union_fee,
            other_deduction,
            memo,
        ))
        conn.commit()
        

def insert_payroll_bonus(
    payment_date: date,
    base_bonus: int,
    employment_insurance: int = 0,
    employee_pension: int = 0,
    health_insurance_basic: int = 0,
    health_insurance_special: int = 0,
    child_support_contribution: int = 0,
    income_tax: int = 0,
    memo: str = "",
) -> None:
    """payroll_bonusテーブルに1件追加"""
    query = """
        INSERT INTO payroll_bonus (
            payment_date, base_bonus, employment_insurance, employee_pension,
            health_insurance_basic, health_insurance_special,
            child_support_contribution, income_tax, memo
        )
        values (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(query, (
            payment_date.isoformat(),
            base_bonus,
            employment_insurance,
            employee_pension,
            health_insurance_basic,
            health_insurance_special,
            child_support_contribution,
            income_tax,
            memo,
        ))
        conn.commit()


def get_payroll_monthly_by_year(year: int) -> pd.DataFrame:
    """指定した年の給与明細（毎月、支給合計・控除合計・差引支給額込み）を取得"""
    query = """
        SELECT *
        FROM payroll_monthly_view
        WHERE strftime('%Y', payment_date) = ?
        ORDER BY payment_date
    """
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql(
            query, conn, params=[str(year)], parse_dates=["payment_date"]
        )
    return df

def get_payroll_monthly_by_month(year: int, month: int) -> pd.DataFrame:
    """指定した年月の給与明細（毎月、支給合計・控除合計・差引支給額込み）を取得"""
    query = """
        select *
        from payroll_monthly_view
        where strftime('%Y', payment_date) = ?
            and strftime('%m', payment_date) = ?
        order by payment_date
    """
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql(
            query, conn, params=[str(year), f"{month:02d}"], parse_dates=["payment_date"]
        )
    return df

def get_payroll_bonus_by_year(year: int) -> pd.DataFrame:
    """指定した年のボーナス明細（支給合計・控除合計・差引支給額込み）を取得"""
    query = """
        select *
        from payroll_bonus_view
        where strftime('%Y', payment_date) = ?
        order by payment_date
    """
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql(
            query, conn, params=[str(year)], parse_dates=["payment_date"]
        )
    return df


def get_payroll_bonus_by_month(year: int, month: int) -> pd.DataFrame:
    """指定した年月のボーナス明細（支給合計・控除合計・差引支給額込み）を取得"""
    query = """
        select *
        from payroll_bonus_view
        where strftime('%Y', payment_date) = ?
            and strftime('%m', payment_date) = ?
        order by payment_date
    """
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql(
            query, conn, params=[str(year), f"{month:02d}"], parse_dates=["payment_date"]
        )
    return df


def get_expense_by_year_ground_by_category(year: int) -> pd.DataFrame:
    """指定した年度のカテゴリ別支出合計を取得"""
    query = """
        SELECT category, sum(amount) as total_amount
        FROM expense
        WHERE strftime('%Y', transaction_date) = ?
        GROUP BY category
        ORDER BY total_amount DESC
    """
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql(query, conn, params=[str(year)])
    return df