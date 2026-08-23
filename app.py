import streamlit as st
import pandas as pd
import sqlite3


#DB取得
def get_expense_df(db_path: str = "expense.db") -> pd.DataFrame:
    with sqlite3.connect(db_path) as conn:
        return  pd.read_sql("select * from expense", conn, parse_dates = ["expense_date"])

def get_payroll_monthly_df(db_path: str = "expense.db") -> pd.DataFrame:
    with sqlite3.connect(db_path) as conn:
        return  pd.read_sql("select * from payroll_monthly", conn, parse_dates = ["payment_date"])

def get_payroll_bonus_df(db_path: str = "expense.db") -> pd.DataFrame:
    with sqlite3.connect(db_path) as conn:
        return  pd.read_sql("select * from payroll_bonus", conn, parse_dates = ["payment_date"])


st.title('家計簿管理')
st.subheader('給与明細（毎月）')
payroll_monthly_df = get_payroll_monthly_df()
st.write(payroll_monthly_df)

st.subheader('給与明細（ボーナス）')
payroll_bonus_df = get_payroll_bonus_df()
st.write(payroll_bonus_df)

st.subheader('支出一覧')
expense_df = get_expense_df()
st.write(expense_df)



if st.button('登録'):
    st.write('登録完了！')
