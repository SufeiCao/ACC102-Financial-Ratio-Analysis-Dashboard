import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import wrds

# ---------- Page config ----------
st.set_page_config(page_title="Financial Ratio Dashboard", layout="wide")
st.title("Financial Ratio Analysis Dashboard")
st.markdown("**ACC102 Mini Assignment – Track 4: Interactive Data Analysis Tool**")
st.markdown("**Data Source**: WRDS Compustat North America – Fundamentals Annual")

# ---------- Load data from WRDS ----------
@st.cache_data(ttl=3600)
def load_data():
    db = wrds.Connection(wrds_username='YOUR_WRDS_USERNAME',
                         wrds_password='YOUR_WRDS_PASSWORD')
    query = """
    SELECT TIC, FYEAR, REVT, COGS, NI, AT, LT, ACT, LCT, CEQ
    FROM COMP.FUNDA
    WHERE TIC IN ('AAPL', 'MSFT', 'AMZN', 'JPM', 'JNJ')
      AND FYEAR >= 2022
      AND FYEAR <= 2024
      AND DATAFMT = 'STD'
      AND INDFMT = 'INDL'
      AND CONSOL = 'C'
      AND POPSRC = 'D'
    ORDER BY TIC, FYEAR
    """
    df_raw = db.raw_sql(query)
    db.close()

    # Rename columns
    df = df_raw.rename(columns={
        'tic': 'Company', 'fyear': 'Year', 'revt': 'Total_Revenue',
        'cogs': 'COGS', 'ni': 'Net_Income', 'at': 'Total_Assets',
        'lt': 'Total_Liabilities', 'act': 'Current_Assets',
        'lct': 'Current_Liabilities', 'ceq': 'Stockholders_Equity'
    })

    # Compute ratios
    df['Gross_Profit'] = df['Total_Revenue'] - df['COGS']
    df['Gross_Margin'] = df['Gross_Profit'] / df['Total_Revenue']
    df['Net_Profit_Margin'] = df['Net_Income'] / df['Total_Revenue']
    df['Current_Ratio'] = df['Current_Assets'] / df['Current_Liabilities']
    df['Debt_to_Asset'] = df['Total_Liabilities'] / df['Total_Assets']
    df['ROE'] = df['Net_Income'] / df['Stockholders_Equity']

    return df.round(4)

# Load the data
with st.spinner("Loading data from WRDS Compustat..."):
    df = load_data()
st.success("Data loaded successfully!")

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")

company_options = df['Company'].unique().tolist()
selected_companies = st.sidebar.multiselect(
    "Select Companies",
    options=company_options,
    default=company_options
)

metric_options = ['Gross_Margin', 'Net_Profit_Margin', 'Current_Ratio', 'Debt_to_Asset', 'ROE']
selected_metric = st.sidebar.selectbox(
    "Select Financial Ratio",
    options=metric_options
)

# Filter data
filtered_df = df[df['Company'].isin(selected_companies)]

# ---------- Main content ----------
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader(f"Trend: {selected_metric} (2022–2024)")
    if not filtered_df.empty:
        fig_line = px.line(
            filtered_df,
            x='Year',
            y=selected_metric,
            color='Company',
            markers=True,
            title=f"{selected_metric} Over Time"
        )
        fig_line.update_layout(legend_title_text='Company')
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.warning("No data for the selected filters.")

with col2:
    st.subheader(f"Comparison: {selected_metric} (Latest Year)")
    if not filtered_df.empty:
        latest_year = filtered_df['Year'].max()
        latest_data = filtered_df[filtered_df['Year'] == latest_year]
        fig_bar = px.bar(
            latest_data,
            x='Company',
            y=selected_metric,
            color='Company',
            title=f"{selected_metric} ({latest_year})",
            text=selected_metric
        )
        fig_bar.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("No data for the selected filters.")

# ---------- Raw data table ----------
st.subheader("Raw Data")
st.dataframe(filtered_df, use_container_width=True)

# ---------- Quick insights ----------
st.markdown("---")
st.markdown("### Quick Industry Insights")
if selected_metric == 'Debt_to_Asset':
    st.info("Banks (e.g., JPMorgan) typically have debt-to-asset ratios above 0.90 due to their deposit-funded business model. This is normal and not a sign of financial distress.")
elif selected_metric == 'ROE':
    st.info("Technology companies (Apple, Microsoft) often show ROE above 1.0, indicating highly efficient use of shareholder equity. Retail and banking sectors tend to have lower ROE.")
elif selected_metric == 'Net_Profit_Margin':
    st.info("Software and technology firms generally enjoy higher net profit margins (above 20%) compared to retail (often below 5%). This reflects differences in cost structure and pricing power.")
elif selected_metric == 'Current_Ratio':
    st.info("A current ratio between 1.0 and 2.0 is generally considered healthy. Values below 1.0 may indicate liquidity concerns, while values well above 2.0 may suggest inefficient asset use.")
elif selected_metric == 'Gross_Margin':
    st.info("Gross margin reflects production efficiency and pricing strategy. High gross margins (above 60%) are common in software, while retail margins are typically much lower (20-30%).")