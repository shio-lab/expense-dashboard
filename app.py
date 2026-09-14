"""app.py"""
import streamlit as st
import pandas as pd
import sqlite3
from datetime import date
from db_utils import (
    get_expense_by_month,
    insert_expense,
     delete_expense,
    get_payroll_monthly_by_month,
    get_payroll_bonus_by_month
)



st.title('Moneybook')

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


col1, col2 = st.columns(2)
with col1:
    year = st.selectbox("年", options = range(2020, date.today().year + 1),
                        index = date.today().year - 2020)

with col2:
    month = st.selectbox("月", options = range(1, 13),
                         index = date.today().month - 1)



st.subheader('給与明細')
payroll_monthly_df = get_payroll_monthly_by_month(year, month)
st.dataframe(
    payroll_monthly_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "id":None,
        "payment_date":"支給日",
        "base_salary":"基本給",
        "overtime_allowance":"時間外手当",
        "other_allowance":"その他給与",
        "rent_deduction":"家賃",
        "employment_insurance":"雇用保険",
        "employee_pension":"厚生年金",
        "health_insurance_basic":"健康保険(基本)",
        "health_insurance_special":"健康保険(特定)",
        "child_support_contribution":"子ども・子育て支援金",
        "income_tax":"所得税",
        "resident_tax":"住民税",
        "labor_union_fee":"労働組合費",
        "memo":"備考"
    },
)


payroll_bonus_df = get_payroll_bonus_by_month(year, month)

if not payroll_bonus_df.empty:
    st.subheader('賞与明細')
    st.dataframe(
        payroll_bonus_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "id":None,
            "payment_date":"支給日",
            "base_bonus":"基本賞与",
            "employment_insurance":"雇用保険",
            "employee_pension":"厚生年金",
            "health_insurance_basic":"健康保険(基本)",
            "health_insurance_special":"健康保険(特定)",
            "child_support_contribution":"子ども・子育て支援金",
            "income_tax":"所得税",
            "memo":"備考"
        },
    )


st.subheader('支出一覧')

df = get_expense_by_month(year, month)

event = st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
    column_config={
        "id": None,
        "transaction_date": "日付",
        "category": "カテゴリ",
        "amount": "金額",
        "memo": "メモ",
    },
)



selected_rows = event.selection.rows

if selected_rows:
    selected_index = selected_rows[0]
    selected_record = df.iloc[selected_index]

    st.write(f"選択中: {selected_record['transaction_date'].date()} / {selected_record['category']} / {selected_record['amount']}円")

    if st.button("このレコードを削除", type="primary"):
        delete_expense(int(selected_record["id"]))
        st.success("削除しました")
        st.rerun()