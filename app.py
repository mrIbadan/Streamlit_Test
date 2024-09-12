import streamlit as st
import geopandas as gpd
import pandas as pd
import numpy as np
import folium
from folium.features import GeoJsonTooltip
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

# Set page layout
st.set_page_config(page_title="US Risk Dashboard", layout="wide")

# CSS for layout and styling adjustments
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f4;
    }
    .logo {
        position: absolute;
        top: 0;
        right: 20px;
        width: 100px;
        z-index: 100;
    }
    .header {
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .main-content {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }
    .metrics-container {
        flex: 0.3;  /* Width of the KPI container */
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .map-container {
        flex: 0.7;  /* Width of the map container */
        padding-left: 10px;
    }
    .metrics-box {
        background-color: #f5f5f5;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 1px 5px rgba(0,0,0,0.1);
    }
    .metrics-box h2 {
        margin: 0;
        font-size: 16px;
        color: #333;
    }
    .metrics-box p {
        margin: 5px 0 0;
        font-size: 20px;
        font-weight: bold;
        color: #007BFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Logo and Title
st.markdown(
    """
    <div class="header">
        <img src="http://ormiro.com/cdn/shop/articles/backup-article-607842304304.jpg?v=1721254571" class="logo">
        <h1 style="color:#007BFF;">US Earthquake and Flood Risk Dashboard</h1>
        <h4 style="color:#6c757d;">Interactive map of earthquake and flood risks by state and county</h4>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar for year filter
st.sidebar.markdown("<h3>Filter by Year</h3>", unsafe_allow_html=True)
year = st.sidebar.selectbox('Select Year', [2020, 2021, 2022, 2023])

# Generate random summary data for display
np.random.seed(42)

loss_ratio = np.random.uniform(0.1, 0.5) * 100  # Random Loss Ratio %
roi = np.random.uniform(5, 20)  # Random ROI %
customers = np.random.randint(100000, 500000)  # Random number of customers
revenue = np.random.uniform(1, 5) * 1e6  # Random Revenue in $

# Main content area with KPI boxes and map side by side
st.markdown("<div class='main-content'>", unsafe_allow_html=True)

# Display KPI boxes on the left
st.markdown("<div class='metrics-container'>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div class='metrics-box'>
        <h2>Loss Ratio (%)</h2>
        <p>{loss_ratio:.2f}%</p>
    </div>
    <div class='metrics-box'>
        <h2>Return on Investment (ROI) (%)</h2>
        <p>{roi:.2f}%</p>
    </div>
    <div class='metrics-box'>
        <h2>Number of Customers</h2>
