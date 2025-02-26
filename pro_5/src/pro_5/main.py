import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import yfinance as yf
import altair as alt

# Page configuration
st.set_page_config(
    page_title="Advanced Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Dashboard Settings")
analysis_type = st.sidebar.selectbox(
    "Choose Analysis Type",
    ["Financial Analysis", "Sales Analytics", "Performance Metrics"]
)

# Main page
st.title("Advanced Analytics Dashboard")

# Date range selector
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime.now().date().replace(month=1, day=1))
with col2:
    end_date = st.date_input("End Date", datetime.now().date())

# Function to load financial data
@st.cache_data
def load_financial_data(symbol):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

# Function to generate sample sales data
@st.cache_data
def generate_sales_data():
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    data = {
        'Date': dates,
        'Sales': np.random.normal(1000, 100, len(dates)),
        'Customers': np.random.randint(50, 200, len(dates)),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], len(dates))
    }
    return pd.DataFrame(data)

# Different dashboard views based on selection
if analysis_type == "Financial Analysis":
    st.subheader("Financial Market Analysis")
    
    # Stock selector
    symbol = st.selectbox("Select Stock Symbol", ["AAPL", "GOOGL", "MSFT", "AMZN"])
    data = load_financial_data(symbol)
    
    # Financial metrics
    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
    with metrics_col1:
        try:
            if not data.empty and 'Close' in data.columns:
                current_price = data['Close'].iloc[-1]
                previous_price = data['Close'].iloc[-2] if len(data) > 1 else current_price
                price_change = ((current_price - previous_price)/previous_price * 100) if previous_price != 0 else 0
                st.metric("Current Price", f"${current_price:.2f}", f"{price_change:.2f}%")
            else:
                st.warning("No price data available")
        except Exception as e:
            st.error(f"Error loading price data: {str(e)}")

    with metrics_col2:
        try:
            if not data.empty and 'Volume' in data.columns:
                st.metric("Volume", f"{data['Volume'].iloc[-1]:,.0f}")
            else:
                st.warning("No volume data available")
        except Exception as e:
            st.error(f"Error loading volume data: {str(e)}")

    with metrics_col3:
        try:
            if not data.empty and 'High' in data.columns:
                st.metric("52-Week High", f"${data['High'].max():.2f}")
            else:
                st.warning("No high price data available")
        except Exception as e:
            st.error(f"Error loading high price data: {str(e)}")
    
    # Stock price chart
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='OHLC'
    ))
    fig.update_layout(title=f"{symbol} Stock Price", xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig, use_container_width=True)

elif analysis_type == "Sales Analytics":
    st.subheader("Sales Performance Dashboard")
    
    sales_data = generate_sales_data()
    
    # Sales metrics
    total_sales = sales_data['Sales'].sum()
    avg_customers = sales_data['Customers'].mean()
    
    metrics_col1, metrics_col2 = st.columns(2)
    with metrics_col1:
        st.metric("Total Sales", f"${total_sales:,.2f}")
    with metrics_col2:
        st.metric("Average Daily Customers", f"{avg_customers:.0f}")
    
    # Sales trend
    sales_trend = px.line(sales_data, x='Date', y='Sales', title='Daily Sales Trend')
    st.plotly_chart(sales_trend, use_container_width=True)
    
    # Regional distribution
    regional_sales = sales_data.groupby('Region')['Sales'].sum().reset_index()
    fig_pie = px.pie(regional_sales, values='Sales', names='Region', title='Sales by Region')
    st.plotly_chart(fig_pie, use_container_width=True)

else:
    st.subheader("Performance Metrics")
    
    # Generate sample performance data
    performance_data = pd.DataFrame({
        'Metric': ['Revenue', 'Costs', 'Profit', 'ROI', 'Customer Satisfaction'],
        'Value': [1250000, 850000, 400000, 47, 4.2],
        'Target': [1300000, 800000, 500000, 50, 4.5]
    })
    
    # Create gauge charts for each metric
    for idx, row in performance_data.iterrows():
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=row['Value'],
            title={'text': row['Metric']},
            gauge={'axis': {'range': [None, row['Target']*1.2]},
                  'threshold': {
                      'line': {'color': "red", 'width': 4},
                      'thickness': 0.75,
                      'value': row['Target']}}))
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit by Your Name")
