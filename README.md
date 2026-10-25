# Manya E-Commerce Sales Analyzer

A complete Python + Streamlit student project for sales analytics and monthly revenue forecasting. It runs locally and requires no API key or paid service.

## Features
- KPI cards for revenue, gross profit, orders, units sold and margin
- CSV upload with validation and cleaning
- Filters for date, category, region and order status
- Monthly trend, category contribution, top products and regional charts
- Three-month revenue forecast using scikit-learn polynomial regression
- Download filtered transactions and forecast CSV
- Included sample dataset with 144 transactions over 18 months
- Automated tests and GitHub Actions checks

## Run on Windows
Install Python 3.10 or newer (Python 3.11 recommended), then open a terminal in the repository folder:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed in the terminal, normally http://localhost:8501.

## Run on macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Required CSV columns
`order_date`, `product`, `category`, `quantity`, `unit_price`.

Optional columns include `order_id`, `customer_id`, `unit_cost`, `region`, `channel`, `discount_pct`, and `order_status`. If unit_cost is omitted, profit is calculated with zero cost, so include cost data for meaningful profit estimates.

## Tests
```bash
pip install pytest
python -m compileall -q app.py src tests
python -m pytest -q
```

## Deployment note
This is a Streamlit Python app, not a static GitHub Pages site. GitHub stores the source and runs the automated checks; to make it publicly accessible, deploy it to a Python-capable host such as Streamlit Community Cloud and select `app.py` as the entry point.

The included sample data is synthetic and intended for project demonstration. Forecasts are estimates, not guaranteed outcomes.
