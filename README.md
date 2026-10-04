# E-Commerce Revenue & Customer Intelligence Analytics

An end-to-end e-commerce analytics project using **SQL, Python, Pandas, NumPy, and BI-ready reporting** to analyze revenue, profitability, customer behavior, retention, and product performance.

## 🛠️ Tools & Technologies

* **SQL** — CTEs, Window Functions, Aggregations
* **Python** — Pandas, NumPy
* **Analytics** — RFM Segmentation, Cohort Analysis
* **BI** — Power BI / Tableau-ready datasets
* **Data** — 520K+ e-commerce transactions

## 📊 Key Analysis

* Analyzed **520K+ e-commerce transactions**
* Calculated revenue, profit, profit margin, AOV, repeat purchase rate, and return rate
* Performed customer-level aggregation using SQL
* Used **CTEs and Window Functions** for advanced analysis
* Performed **RFM customer segmentation**
* Conducted **cohort retention analysis**
* Identified high-value and at-risk customer segments
* Analyzed product and regional performance
* Identified **high-revenue / low-margin products**
* Generated monthly revenue and profit trends

## 📁 Project Structure

```text
ecommerce-revenue-customer-intelligence/
│
├── sql/
│   └── advanced_analysis.sql
│
├── src/
│   ├── 01_generate_data.py
│   └── 02_analysis.py
│
├── output/
│   ├── kpi_summary.csv
│   ├── monthly_sales.csv
│   ├── regional_performance.csv
│   ├── product_performance.csv
│   ├── rfm_segments.csv
│   └── cohort_retention.csv
│
└── README.md
```

## 🚀 How to Run

### 1. Install dependencies

```bash
pip3 install pandas numpy
```

### 2. Generate the dataset

```bash
python3 src/01_generate_data.py
```

This generates **520,000 e-commerce transactions**.

### 3. Run the analysis

```bash
python3 src/02_analysis.py
```

The processed analytics files will be generated inside the `output/` folder.

## 📈 Business Insights

The analysis focuses on:

* Revenue and profitability trends
* Customer retention and repeat purchasing behavior
* RFM-based customer segmentation
* Customer cohort retention
* Regional revenue and profitability
* Product-level revenue and margin performance
* Identification of high-revenue but low-margin products

## 🎯 Business Recommendations

Based on the analysis, businesses can:

* Target **Champions and Loyal customers** with personalized offers
* Create retention campaigns for **At-Risk customers**
* Review pricing and discount strategies for **high-revenue / low-margin products**
* Optimize regional marketing based on revenue and profitability
* Use cohort retention trends to improve customer lifetime value

## 📌 Project Outcome

This project demonstrates practical skills in:

**SQL Analytics → Python Data Analysis → Customer Segmentation → Cohort Analysis → Business Insights**
