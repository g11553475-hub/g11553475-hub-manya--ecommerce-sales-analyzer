from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
from src.analytics import prepare_sales_data, calculate_kpis, monthly_sales, product_performance, category_performance, regional_performance
from src.forecast import forecast_monthly_sales

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Manya | E-Commerce Sales Analyzer", page_icon="🛍️", layout="wide")
st.markdown("""<style>
.main {background:#f6f8fc}.block-container{padding-top:1.5rem}
.hero{padding:24px 28px;border-radius:18px;color:white;background:linear-gradient(120deg,#111827,#2563eb);margin-bottom:18px}
.hero h1{margin:0}.hero p{margin:8px 0 0;opacity:.9}
div[data-testid="stMetric"]{background:white;border:1px solid #e5e7eb;padding:14px;border-radius:12px}
</style><div class="hero"><h1>🛍️ E-Commerce Sales Analyzer</h1><p>Sales performance, customer transactions and three-month revenue forecast.</p></div>""", unsafe_allow_html=True)

@st.cache_data
def load_sample():
    return pd.read_csv(ROOT / "data" / "sample_sales.csv")

with st.sidebar:
    st.header("Data & filters")
    upload = st.file_uploader("Upload sales CSV", type=["csv"])
    try:
        raw = pd.read_csv(upload) if upload is not None else load_sample()
        data = prepare_sales_data(raw)
    except Exception as exc:
        st.error(f"Unable to load sales data: {exc}")
        st.stop()
    low, high = data["order_date"].min().date(), data["order_date"].max().date()
    selected_dates = st.date_input("Order date range", value=(low, high), min_value=low, max_value=high)
    categories = sorted(data["category"].astype(str).unique())
    selected_categories = st.multiselect("Categories", categories, default=categories)
    regions = sorted(data["region"].astype(str).unique())
    selected_regions = st.multiselect("Regions", regions, default=regions)
    statuses = sorted(data["order_status"].astype(str).unique())
    selected_statuses = st.multiselect("Order status", statuses, default=statuses)

filtered = data.copy()
if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    filtered = filtered[filtered["order_date"].dt.date.between(selected_dates[0], selected_dates[1])]
filtered = filtered[filtered["category"].astype(str).isin(selected_categories)]
filtered = filtered[filtered["region"].astype(str).isin(selected_regions)]
filtered = filtered[filtered["order_status"].astype(str).isin(selected_statuses)]
if filtered.empty:
    st.warning("No transactions match these filters. Adjust the filters in the sidebar.")
    st.stop()

k = calculate_kpis(filtered)
cols = st.columns(5)
for col, label, value in zip(cols, ["Revenue", "Gross profit", "Orders", "Units sold", "Profit margin"],
    [f"₹{k['revenue']:,.0f}", f"₹{k['profit']:,.0f}", f"{k['orders']:,}", f"{k['units']:,.0f}", f"{k['margin']:.1f}%"]):
    col.metric(label, value)

monthly = monthly_sales(filtered)
left, right = st.columns([1.6, 1])
with left:
    st.subheader("Monthly revenue")
    st.plotly_chart(px.line(monthly, x="month", y="revenue", markers=True, title="Revenue by month"), use_container_width=True)
with right:
    st.subheader("Category contribution")
    category = category_performance(filtered)
    st.plotly_chart(px.pie(category, names="category", values="revenue", hole=.48), use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Top products")
    products = product_performance(filtered).head(10)
    st.plotly_chart(px.bar(products.sort_values("revenue"), x="revenue", y="product", orientation="h", title="Top 10 products by revenue"), use_container_width=True)
with right:
    st.subheader("Regional performance")
    regional = regional_performance(filtered)
    st.plotly_chart(px.bar(regional, x="region", y="revenue", color="region", title="Revenue by region"), use_container_width=True)

st.subheader("Revenue forecast — next 3 months")
try:
    forecast, note = forecast_monthly_sales(monthly, 3)
    hist = monthly[["month", "revenue"]].rename(columns={"revenue": "amount"})
    fut = forecast.rename(columns={"forecast_revenue": "amount"})
    hist["series"] = "Historical"
    fut["series"] = "Forecast"
    chart = pd.concat([hist[["month", "amount", "series"]], fut[["month", "amount", "series"]]], ignore_index=True)
    st.plotly_chart(px.line(chart, x="month", y="amount", color="series", markers=True, title="Historical and forecast revenue"), use_container_width=True)
    st.dataframe(forecast, use_container_width=True, hide_index=True)
    st.caption(note)
    st.download_button("Download forecast CSV", forecast.to_csv(index=False).encode("utf-8"), "sales_forecast.csv", "text/csv")
except ValueError as exc:
    st.info(str(exc))

st.subheader("Transaction explorer")
st.dataframe(filtered.sort_values("order_date", ascending=False), use_container_width=True, hide_index=True)
st.download_button("Download filtered transactions CSV", filtered.to_csv(index=False).encode("utf-8"), "filtered_sales.csv", "text/csv")
st.caption("Forecasts are based on historical sales patterns and should be treated as estimates.")
