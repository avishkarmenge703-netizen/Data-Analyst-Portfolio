import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Interactive Sales Dashboard")
st.markdown("Upload your CSV to see key metrics, regional sales, top products, and trends instantly.")

uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("File loaded successfully!")
else:
    try:
        df = pd.read_csv("sample_data.csv")
        st.sidebar.info("Using sample Superstore data. Upload your own CSV to override.")
    except FileNotFoundError:
        st.error("Please upload a CSV file or add sample_data.csv to the folder.")
        st.stop()

# Data cleaning (assumes Superstore-like columns)
if 'Order Date' in df.columns:
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month

# KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Sales", f"${df['Sales'].sum():,.0f}")
with col2:
    st.metric("Total Profit", f"${df['Profit'].sum():,.0f}")
with col3:
    st.metric("Number of Orders", f"{df['Row ID'].nunique():,}")
with col4:
    st.metric("Average Discount", f"{df['Discount'].mean():.1%}")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Sales by Region")
    region_sales = df.groupby('Region')['Sales'].sum().reset_index()
    fig = px.bar(region_sales, x='Region', y='Sales', color='Region',
                 title="Total Sales by Region")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏆 Top 10 Products by Sales")
    top_products = df.groupby('Product Name')['Sales'].sum().nlargest(10).reset_index()
    fig = px.bar(top_products, x='Sales', y='Product Name', orientation='h',
                 title="Top 10 Products")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("📈 Monthly Sales Trend")
if 'Order Date' in df.columns:
    monthly_sales = df.groupby(df['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
    monthly_sales['Order Date'] = monthly_sales['Order Date'].astype(str)
    fig = px.line(monthly_sales, x='Order Date', y='Sales', markers=True,
                  title="Sales Over Time")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 Profit by Category")
cat_profit = df.groupby('Category')['Profit'].sum().reset_index()
fig = px.pie(cat_profit, names='Category', values='Profit', title="Profit Distribution")
st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 Raw Data Preview"):
    st.dataframe(df.head(100))
