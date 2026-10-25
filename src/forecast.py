import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

def forecast_monthly_sales(monthly: pd.DataFrame, periods: int = 3):
    """Forecast future monthly revenue from historical monthly totals."""
    if periods < 1:
        raise ValueError("periods must be at least 1")
    data = monthly[["month", "revenue"]].dropna().sort_values("month").copy()
    data["month"] = pd.to_datetime(data["month"])
    data = data.groupby("month", as_index=False)["revenue"].sum()
    if len(data) < 4:
        raise ValueError("At least four months of sales history are needed for forecasting.")
    x = np.arange(len(data)).reshape(-1, 1)
    y = data["revenue"].astype(float).to_numpy()
    model = make_pipeline(PolynomialFeatures(degree=2, include_bias=False), LinearRegression())
    model.fit(x, y)
    future_x = np.arange(len(data), len(data) + periods).reshape(-1, 1)
    predictions = np.maximum(model.predict(future_x), 0)
    last_month = data["month"].max()
    future_months = pd.date_range(last_month + pd.offsets.MonthBegin(1), periods=periods, freq="MS")
    result = pd.DataFrame({"month": future_months, "forecast_revenue": np.round(predictions, 2)})
    return result, f"Polynomial regression trained on {len(data)} monthly observations. Forecasts are estimates, not guarantees."
