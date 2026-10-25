# Manya E-Commerce Sales Analyzer

A responsive, browser-based e-commerce analytics website with sales KPIs, revenue trends, category mix, product rankings, regional insights, a simple trend forecast, CSV import, filters, and CSV export.

## Website

**Expected GitHub Pages URL:** https://g11553475-hub.github.io/g11553475-hub-manya--ecommerce-sales-analyzer/

The repository now includes `index.html` and a GitHub Actions workflow that deploys the site on every push to `main`. First deployment can take a few minutes. Check the **Actions** tab for the workflow named **Deploy E-Commerce Sales Analyzer website**. If GitHub Pages is not enabled yet, open **Settings → Pages** and choose **GitHub Actions** as the source.

## Use the dashboard

- The dashboard loads sample sales data automatically.
- Filter by date range, category, region, and order status.
- Upload a CSV file to analyze your own transactions.
- Export the filtered report as CSV.

Recommended CSV headers: `order_date`, `product`, `category`, `quantity`, `unit_price`. Optional: `unit_cost`, `region`, `channel`, `order_status`, `order_id`. Date values should be parseable by your browser. `revenue` or `sales` can be used instead of `unit_price`. If you omit `unit_cost`, profit uses zero cost and is not a meaningful real-world profit estimate.

Uploaded CSV data is processed in your browser and is not sent to a server. The forecast is a simple trend-based estimate for educational analysis, not a guaranteed prediction.

## Files

- `index.html` — responsive website and client-side analysis
- `.github/workflows/pages.yml` — automatic GitHub Pages deployment
- `app.py`, `src/`, `requirements.txt` — Python/Streamlit version, if used
- `PRESENTATION_GUIDE.md` — project explanation for presentation, if present

## Local website use

You can open `index.html` directly in a modern browser. No Python server, build command, paid API key, or backend is required for the website version.
