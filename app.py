import streamlit as st
import pandas as pd
import sqlite3
from datetime import date
from db_utils import get_expense_by_month, insert_expense, get_expense_df, get_payroll_monthly_df, get_payroll_bonus_df



st.title('Moneybook')

#
col1, col2 = st.columns(2)
with col1:
    year = st.selectbox("年", options = range(2020, date.today().year + 1),
                        index = date.today().year - 2020)

with col2:
    month = st.selectbox("月", options = range(1, 13),
                         index = date.today().month - 1)

with st.sidebar:

    st.subheader("支出を追加")
    with st.form("expense_form", clear_on_submit=True):
        input_date = st.date_input("日付", value = date.today())
        input_category = st.selectbox("カテゴリ", ["食費", "交通費", "娯楽", "光熱費", "通信費", "医療費", "教育費", "その他"])
        input_amount = st.number_input("金額", min_value= 0, step=100)
        input_memo = st.text_input("メモ")

        submitted = st.form_submit_button("追加")

        if submitted:
            insert_expense(input_date, input_category, input_amount, input_memo)
            st.success("追加しました！")
            st.rerun()


st.subheader('給与明細')
payroll_monthly_df = get_payroll_monthly_df()
st.write(payroll_monthly_df)

st.subheader('賞与明細')
payroll_bonus_df = get_payroll_bonus_df()
st.write(payroll_bonus_df)

st.subheader('支出一覧')
expense_df = get_expense_df()
st.write(expense_df)




