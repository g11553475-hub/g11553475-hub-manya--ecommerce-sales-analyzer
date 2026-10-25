import pandas as pd
from src.analytics import prepare_sales_data, calculate_kpis, monthly_sales
from src.forecast import forecast_monthly_sales

def test_revenue_profit_and_orders():
    raw = pd.DataFrame({"order_date":["2026-01-01","2026-01-02"],"product":["A","B"],"category":["X","Y"],"quantity":[2,1],"unit_price":[10,20],"unit_cost":[4,5],"order_id":["1","2"]})
    data = prepare_sales_data(raw)
    kpis = calculate_kpis(data)
    assert kpis["revenue"] == 40
    assert kpis["profit"] == 27
    assert kpis["orders"] == 2

def test_monthly_aggregation():
    raw = pd.DataFrame({"order_date":["2026-01-01","2026-01-15","2026-02-01","2026-03-01"],"product":["A"]*4,"category":["X"]*4,"quantity":[1]*4,"unit_price":[10,20,30,40]})
    result = monthly_sales(prepare_sales_data(raw))
    assert len(result) == 3
    assert result.iloc[0]["revenue"] == 30

def test_forecast_periods():
    history = pd.DataFrame({"month":pd.date_range("2025-01-01", periods=6, freq="MS"),"revenue":[100,120,125,140,155,170]})
    forecast, _ = forecast_monthly_sales(history, 3)
    assert len(forecast) == 3
    assert (forecast["forecast_revenue"] >= 0).all()
