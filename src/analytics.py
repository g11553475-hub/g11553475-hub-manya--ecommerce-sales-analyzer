import pandas as pd

REQUIRED_COLUMNS = {"order_date", "product", "category", "quantity", "unit_price"}

def prepare_sales_data(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate, clean and calculate transaction-level sales metrics."""
    if frame is None or frame.empty:
        raise ValueError("The CSV contains no transaction rows.")
    data = frame.copy()
    data.columns = [str(c).strip().lower().replace(" ", "_") for c in data.columns]
    missing = REQUIRED_COLUMNS - set(data.columns)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
    data["order_date"] = pd.to_datetime(data["order_date"], errors="coerce")
    data["quantity"] = pd.to_numeric(data["quantity"], errors="coerce")
    data["unit_price"] = pd.to_numeric(data["unit_price"], errors="coerce")
    if "unit_cost" not in data:
        data["unit_cost"] = 0.0
    data["unit_cost"] = pd.to_numeric(data["unit_cost"], errors="coerce").fillna(0)
    defaults = {
        "order_id": None, "customer_id": "Unknown", "region": "Unknown",
        "channel": "Unknown", "order_status": "Completed", "discount_pct": 0
    }
    for col, default in defaults.items():
        if col not in data:
            data[col] = [f"ROW{i+1}" for i in range(len(data))] if default is None else default
    data["discount_pct"] = pd.to_numeric(data["discount_pct"], errors="coerce").fillna(0).clip(0, 100)
    data = data.dropna(subset=["order_date", "quantity", "unit_price", "product", "category"])
    data = data[(data["quantity"] > 0) & (data["unit_price"] >= 0) & (data["unit_cost"] >= 0)]
    if data.empty:
        raise ValueError("No valid rows remain. Check dates, quantities, prices and product names.")
    data["revenue"] = data["quantity"] * data["unit_price"] * (1 - data["discount_pct"] / 100)
    data["cost"] = data["quantity"] * data["unit_cost"]
    data["profit"] = data["revenue"] - data["cost"]
    data["month"] = data["order_date"].dt.to_period("M").dt.to_timestamp()
    return data.reset_index(drop=True)

def calculate_kpis(data: pd.DataFrame) -> dict:
    return {
        "revenue": float(data["revenue"].sum()),
        "profit": float(data["profit"].sum()),
        "orders": int(data["order_id"].nunique()),
        "units": int(data["quantity"].sum()),
        "customers": int(data["customer_id"].nunique()),
        "margin": float(data["profit"].sum() / data["revenue"].sum() * 100) if data["revenue"].sum() else 0.0,
    }

def monthly_sales(data: pd.DataFrame) -> pd.DataFrame:
    return data.groupby("month", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique")).sort_values("month")

def product_performance(data: pd.DataFrame) -> pd.DataFrame:
    return data.groupby("product", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"), units=("quantity", "sum")).sort_values("revenue", ascending=False)

def category_performance(data: pd.DataFrame) -> pd.DataFrame:
    return data.groupby("category", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum")).sort_values("revenue", ascending=False)

def regional_performance(data: pd.DataFrame) -> pd.DataFrame:
    return data.groupby("region", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique")).sort_values("revenue", ascending=False)
