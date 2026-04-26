# Financial Ratio Analysis Dashboard

**ACC102 Mini Assignment – Track 4: Interactive Data Analysis Tool**

---

## 1. Problem Definition and Target Audience

- **Analytical Problem**: Individual investors and non-finance professionals often lack accessible tools to quickly compare the financial health of companies across different sectors. Raw financial statements contain numerous line items, and meaningful cross-company comparison requires standardised financial ratios rather than absolute numbers.
- **Target Audience**: Retail investors with limited accounting knowledge, first-year finance students, and managers in non-financial roles who need to understand a company's profitability, liquidity, and solvency at a glance.
- **Product Purpose**: This project delivers an interactive Streamlit dashboard that allows users to select one or more companies and a financial ratio, instantly generating trend line charts and cross-company bar charts. The underlying analysis is performed in Python and documented in a Jupyter Notebook.

---

## 2. Data Source

- **Platform**: Wharton Research Data Services (WRDS)
- **Database**: Compustat North America – Fundamentals Annual (COMP.FUNDA)
- **Access Date**: 24 April 2026
- **Companies Analysed**: Apple Inc. (AAPL), Microsoft Corp. (MSFT), Amazon.com Inc. (AMZN), JPMorgan Chase & Co. (JPM), Johnson & Johnson (JNJ)
- **Fiscal Years**: 2022, 2023, 2024
- **Variables Extracted**: TIC (Ticker), FYEAR (Fiscal Year), REVT (Total Revenue), COGS (Cost of Goods Sold), NI (Net Income), AT (Total Assets), LT (Total Liabilities), ACT (Current Assets), LCT (Current Liabilities), CEQ (Stockholders' Equity)
- **Justification**: WRDS Compustat provides standardised, audited financial data widely used in academic accounting and finance research. It is listed as an approved data source in the ACC102 assignment guidance. Programmatic SQL queries via the `wrds` Python package ensure a fully reproducible data acquisition pipeline.

---

## 3. Python Methods and Workflow

The analysis pipeline consists of six main stages:

i. **Data Acquisition** – Connect to WRDS via the `wrds` library and execute a SQL query to extract financial statement variables for five US-listed companies.

ii. **Data Inspection** – Examine the structure, dimensions, and variable types of the raw data. Check for missing values.

iii. **Data Cleaning and Renaming** – Rename Compustat variable codes (e.g., REVT → Total_Revenue) to descriptive English column names. Compute Gross Profit.

iv. **Ratio Computation** – Calculate five key financial ratios:
   - Gross Margin = Gross Profit / Total Revenue
   - Net Profit Margin = Net Income / Total Revenue
   - Current Ratio = Current Assets / Current Liabilities
   - Debt-to-Asset Ratio = Total Liabilities / Total Assets
   - Return on Equity (ROE) = Net Income / Stockholders' Equity

v. **Exploratory Analysis and Visualisation** – Generate static charts (bar, line, scatter) using `matplotlib` in the Jupyter Notebook.

vi. **Interactive Dashboard** – Build a Streamlit web application (`app.py`) with `plotly` interactive charts, sidebar filters for company selection and financial ratio selection.

---

## 4. Key Findings and Insights

- **Profitability**: Apple and Microsoft consistently achieve the highest net profit margins and ROE among the five companies, reflecting strong competitive advantages in the technology sector.
- **Leverage and Industry Norms**: JPMorgan Chase operates with a debt-to-asset ratio above 0.90, which is structurally typical for banks due to their deposit-funded business model. This highlights the importance of industry context when interpreting financial ratios.
- **Margin Structures**: Amazon shows lower profit margins compared to technology peers, consistent with its high-volume, low-margin retail and logistics model. However, its margins have improved from 2022 to 2024.
- **Liquidity**: All five companies maintain current ratios close to or above 1.0, indicating adequate short-term liquidity.
- **Cross-Industry Variation**: Ratio benchmarks differ significantly by industry. Comparing a bank's leverage ratio directly to a technology company's is misleading without sector-specific context.
- **Temporal Trends**: Most companies in the sample showed stable or improving profitability from 2022 to 2024, suggesting a post-pandemic normalisation of business operations.

---

## 5. How to Run

**Prerequisites**: Python 3.9 or above, an active WRDS account.

**Step 1 — Clone the repository**

git clone https://github.com/SufeiCao/acc102-financial-ratio-dashboard.git
cd acc102-financial-ratio-dashboard

**Step 2 — Install dependencies**

pip install -r requirements.txt

**Step 3 — Set WRDS credentials**
Open the file `app.py` in any text editor.
- Go to **line 16** and replace `YOUR_WRDS_USERNAME` with your WRDS username.
- Go to **line 17** and replace `YOUR_WRDS_PASSWORD` with your WRDS password.

The lines should look like this before editing:
```python
db = wrds.Connection(wrds_username='YOUR_WRDS_USERNAME',
                     wrds_password='YOUR_WRDS_PASSWORD')

After editing, save the file.

Step 4 — Run the Streamlit application

streamlit run app.py

Open your browser and go to http://localhost:8501.

---

6. Repository Structure

acc102-financial-ratio-dashboard/
│
├── financial_analysis.ipynb    # Full analytical workflow
├── app.py                       # Streamlit interactive dashboard
├── README.md                    # This documentation
└── requirements.txt             # Python package dependencies

---

7. Demo Video

[Insert Mediasite link here after uploading your video]

---

8. Limitations and Future Work

· Sample Size: The analysis is limited to five companies across four sectors. Future versions could incorporate a larger peer group and industry-level benchmarks.
· Ratio Coverage: Only five fundamental ratios are calculated. Additional metrics such as Inventory Turnover, Interest Coverage Ratio, or P/E ratio could be added.
· Data Frequency: Only fiscal year-end data is used. Quarterly data could reveal intra-year trends and seasonal effects.
· Predictive Scope: The analysis is descriptive. Future work could incorporate simple forecasting models (e.g., linear regression) to project future ratio trends.

---

9. Acknowledgements

· Financial data sourced from Compustat via Wharton Research Data Services (WRDS).
· Developed for the ACC102 Mini Assignment at Xi'an Jiaotong-Liverpool University, Semester 2, 2024–25.
· Python libraries used: pandas, numpy, matplotlib, plotly, streamlit, wrds.
