from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = Path("data/sample_transactions.csv")
CATEGORY_BUDGETS = {
    "Food": 12000,
    "Transport": 4000,
    "Bills": 9000,
    "Shopping": 7000,
    "Health": 3500,
    "Education": 5000,
    "Entertainment": 4500,
}


@st.cache_data
def load_transactions() -> pd.DataFrame:
    """Load the starter finance data from CSV."""
    transactions = pd.read_csv(DATA_PATH, parse_dates=["date"])
    transactions["amount"] = transactions["amount"].astype(float)
    return transactions


def prepare_transactions(transactions: pd.DataFrame) -> pd.DataFrame:
    prepared = transactions.copy()
    prepared["month"] = prepared["date"].dt.strftime("%b %Y")
    prepared["signed_amount"] = prepared.apply(
        lambda row: row["amount"] if row["type"] == "Income" else -row["amount"],
        axis=1,
    )
    return prepared


def money(value: float) -> str:
    return f"Rs. {value:,.0f}"


st.set_page_config(
    page_title="Pocket Finance Tracker",
    page_icon="💸",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .finance-title {
        font-size: 2.2rem;
        font-weight: 750;
        margin-bottom: 0.2rem;
    }
    .finance-subtitle {
        color: #4f5b62;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .status-card {
        border: 1px solid #d8dee4;
        border-radius: 8px;
        padding: 1rem;
        background: #f8fafc;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='finance-title'>Pocket Finance Tracker</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='finance-subtitle'>Track income, spending, budgets, and savings from one simple Streamlit dashboard.</div>",
    unsafe_allow_html=True,
)

if "transactions" not in st.session_state:
    st.session_state.transactions = load_transactions()

with st.sidebar:
    st.header("Add Transaction")
    with st.form("transaction_form", clear_on_submit=True):
        entry_date = st.date_input("Date")
        entry_type = st.selectbox("Type", ["Expense", "Income"])
        entry_category = st.selectbox(
            "Category",
            [
                "Food",
                "Transport",
                "Bills",
                "Shopping",
                "Health",
                "Education",
                "Entertainment",
                "Salary",
                "Freelance",
                "Other",
            ],
        )
        entry_note = st.text_input("Note", placeholder="Example: Groceries")
        entry_amount = st.number_input("Amount", min_value=1.0, step=100.0)
        submitted = st.form_submit_button("Add")

    if submitted:
        new_row = pd.DataFrame(
            [
                {
                    "date": pd.to_datetime(entry_date),
                    "type": entry_type,
                    "category": entry_category,
                    "note": entry_note or "Manual entry",
                    "amount": float(entry_amount),
                }
            ]
        )
        st.session_state.transactions = pd.concat(
            [st.session_state.transactions, new_row],
            ignore_index=True,
        )
        st.success("Transaction added.")

    st.divider()
    st.caption("This demo stores added transactions only for your current browser session.")

transactions = prepare_transactions(st.session_state.transactions)

filter_col_1, filter_col_2 = st.columns([1, 2])
with filter_col_1:
    selected_months = st.multiselect(
        "Month",
        sorted(transactions["month"].unique()),
        default=sorted(transactions["month"].unique()),
    )
with filter_col_2:
    selected_categories = st.multiselect(
        "Category",
        sorted(transactions["category"].unique()),
        default=sorted(transactions["category"].unique()),
    )

filtered = transactions[
    transactions["month"].isin(selected_months)
    & transactions["category"].isin(selected_categories)
]

income_total = filtered.loc[filtered["type"] == "Income", "amount"].sum()
expense_total = filtered.loc[filtered["type"] == "Expense", "amount"].sum()
savings_total = income_total - expense_total
savings_rate = (savings_total / income_total * 100) if income_total else 0

metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric("Income", money(income_total))
metric_2.metric("Expenses", money(expense_total))
metric_3.metric("Savings", money(savings_total))
metric_4.metric("Savings Rate", f"{savings_rate:.1f}%")

st.divider()

chart_col, budget_col = st.columns([1.4, 1])

with chart_col:
    st.subheader("Monthly Cash Flow")
    monthly = (
        filtered.groupby(["month", "type"], as_index=False)["amount"]
        .sum()
        .pivot(index="month", columns="type", values="amount")
        .fillna(0)
    )
    if not monthly.empty:
        st.bar_chart(monthly)
    else:
        st.info("No transactions match the selected filters.")

with budget_col:
    st.subheader("Budget Check")
    expenses = filtered[filtered["type"] == "Expense"]
    category_spend = expenses.groupby("category")["amount"].sum().sort_values(ascending=False)

    if category_spend.empty:
        st.info("No expense data available for the selected filters.")
    else:
        for category, spent in category_spend.items():
            budget = CATEGORY_BUDGETS.get(category)
            if budget:
                progress = min(spent / budget, 1)
                st.write(f"{category}: {money(spent)} of {money(budget)}")
                st.progress(progress)
            else:
                st.write(f"{category}: {money(spent)}")

table_col, category_col = st.columns([1.4, 1])

with table_col:
    st.subheader("Transactions")
    display = filtered.sort_values("date", ascending=False)[
        ["date", "type", "category", "note", "amount"]
    ].copy()
    display["date"] = display["date"].dt.strftime("%Y-%m-%d")
    st.dataframe(display, width="stretch", hide_index=True)

with category_col:
    st.subheader("Expense Categories")
    expense_by_category = (
        filtered[filtered["type"] == "Expense"]
        .groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )
    if not expense_by_category.empty:
        st.bar_chart(expense_by_category)
    else:
        st.info("No expenses to chart yet.")

st.download_button(
    "Download Filtered Transactions",
    data=filtered[["date", "type", "category", "note", "amount"]].to_csv(index=False),
    file_name="finance_tracker_transactions.csv",
    mime="text/csv",
)
