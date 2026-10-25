# Project Presentation Guide

## Title
E-Commerce Sales Analyzer Using Data Analytics and Machine Learning

## Problem statement
Online stores produce many transaction records. Manual review makes it difficult to monitor revenue, identify successful products, compare regions and estimate future sales. This project turns transaction data into an interactive dashboard.

## Objectives
- Validate and clean transaction CSV files.
- Calculate revenue, gross profit, order count, units sold and margin.
- Compare performance by month, category, product and region.
- Forecast revenue for the next three months.
- Export filtered transactions and forecast output.

## Technologies
- Python: application logic.
- Pandas: cleaning, transformation and aggregation.
- NumPy: numeric arrays for forecasting.
- Streamlit: interactive dashboard.
- Plotly Express: interactive charts.
- Scikit-learn: polynomial features and linear regression.
- Pytest: automated tests.

## Workflow
1. Load the bundled sample CSV or upload another sales CSV.
2. Validate required columns and normalize dates/numeric values.
3. Calculate line revenue, cost and profit.
4. Filter by date, category, region and order status.
5. Calculate KPI cards and group data for charts.
6. Train a simple polynomial regression on monthly revenue.
7. Display and download the next three monthly estimates.

## Main formulas
- Revenue = quantity × unit price × (1 − discount percentage / 100)
- Cost = quantity × unit cost
- Gross profit = revenue − cost
- Profit margin = gross profit / revenue × 100

## Important note
The bundled dataset is synthetic for academic demonstration. The forecasting model is a baseline trend model, not a guarantee of future sales.
