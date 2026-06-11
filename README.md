# Pocket Finance Tracker

Pocket Finance Tracker is a beginner-friendly Streamlit app for tracking income, expenses, category budgets, savings, and monthly cash flow. It is intentionally simple, easy to understand, and ready to deploy on Streamlit Community Cloud.

## Features

- Add income or expense transactions from the sidebar
- View income, expense, savings, and savings-rate metrics
- Filter transactions by month and category
- See monthly cash-flow and category spending charts
- Compare spending against simple category budgets
- Download filtered transactions as a CSV file

## Tech Stack

- Python 3
- Streamlit for the app interface
- Pandas for transaction data handling
- CSV starter data for a lightweight beginner setup

## Project Structure

```text
finance-tracker-streamlit/
├── app.py
├── data/
│   └── sample_transactions.csv
├── .streamlit/
│   └── config.toml
├── requirements.txt
├── Dockerfile
├── README.md
├── USER_MANUAL.md
├── CONTRIBUTING.md
├── COMPLIANCE_NOTES.md
├── SECURITY.md
├── CHANGELOG.md
└── CODE_OF_CONDUCT.md
```

## Run Locally

1. Clone or open the project folder:

```bash
cd finance-tracker-streamlit
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run app.py
```

If the `streamlit` command is not found, use:

```bash
python3 -m streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Deploy On Streamlit Community Cloud

1. Push this folder to a GitHub or GitLab repository.
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud).
3. Sign in and choose **New app**.
4. Select the repository, branch, and `app.py` as the main file path.
5. Click **Deploy**.

No secrets or environment variables are required for the default app.

## Docker

Build the image:

```bash
docker build -t pocket-finance-tracker .
```

Run the container:

```bash
docker run -p 8501:8501 pocket-finance-tracker
```

Then open `http://localhost:8501`.

## Roadmap

- Save user-entered transactions to a database
- Add custom budget editing
- Add recurring transactions
- Add income and expense goals
- Add charts for longer date ranges

## Author

- Archisha Singh

## Acknowledgements

- Built as a simple Streamlit hackathon-style project
- Inspired by the reference repository structure provided for the task
