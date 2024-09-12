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
    .logo {
        position: absolute;
        top: 0;
        right: 20px;
        width: 100px;
        z-index: 100;
    }
    .header {
        text-align: center;
        margin-top: 120px;
        margin-bottom: 20px;
    }
    .main-content {
        display: flex;
        flex-direction: row;
    }
    .metrics-container {
        flex: 0.3;
        padding: 10px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .map-container {
        flex: 0.7;
        padding-left: 10px;
    }
    .metrics-box {
        background-color: #f5f5f5;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 8px;
        text-align: center;
    }
    .metrics-box h2 {
        margin: 0;
        font-size: 14px;
        color: #333;
    }
    .metrics-box p {
        margin: 5px 0 0;
        font-size: 16px;
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

# Display KPI boxes on the left (smaller size)
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
        <p>{customers:,}</p>
    </div>
    <div class='metrics-box'>
        <h2>Revenue ($)</h2>
        <p>${revenue:,.2f}</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)  # Close metrics container

# Map on the right side
st.markdown("<div class='map-container'>", unsafe_allow_html=True)
view_type = st.sidebar.selectbox('Select View Type', ['State', 'County'])
risk_type = st.sidebar.selectbox('Select Risk Type', ['Earthquake', 'Flood'])

# Function to generate and return a Folium map
def create_map(view_type, risk_type):
    state_url = 'https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_state_20m.zip'
    county_url = 'https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_county_20m.zip'

    us_states = gpd.read_file(state_url)
    us_counties = gpd.read_file(county_url)

    np.random.seed(42)
    states = us_states['NAME']
    state_risk_scores = np.random.randint(1, 11, size=len(states))
    state_flood_risk_scores = np.random.randint(1, 11, size=len(states))

    random_state_risk_data = pd.DataFrame({
        'NAME': states,
        'Earthquake_Risk_Score': state_risk_scores,
        'Flood_Risk_Score': state_flood_risk_scores
    })

    us_states_risk = us_states.merge(random_state_risk_data, left_on='NAME', right_on='NAME', how='left')

    counties = us_counties['NAME']
    county_risk_scores = np.random.randint(1, 11, size=len(counties))
    county_flood_risk_scores = np.random.randint(1, 11, size=len(counties))

    random_county_risk_data = pd.DataFrame({
        'NAME': counties,
        'Earthquake_Risk_Score': county_risk_scores,
        'Flood_Risk_Score': county_flood_risk_scores
    })

    us_counties_risk = us_counties.merge(random_county_risk_data, left_on='NAME', right_on='NAME', how='left')

    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4, tiles="cartodbpositron")

    # Inverted color scale: Red for high risk (> 5), Green for low risk (≤ 5)
    if risk_type == "Earthquake":
        risk_column = "Earthquake_Risk_Score"
        legend_name = "Earthquake Risk Score"
    else:
        risk_column = "Flood_Risk_Score"
        legend_name = "Flood Risk Score"

    if view_type == "State":
        folium.Choropleth(
            geo_data=us_states_risk.__geo_interface__,
            name=f"State {risk_type} Risk",
            data=us_states_risk,
            columns=["NAME", risk_column],
            key_on="feature.properties.NAME",
            fill_color="RdYlGn_r",  # Reversed: Red for high risk, Green for low risk
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=legend_name,
            threshold_scale=[0, 1, 3, 5, 7, 10]
        ).add_to(m)

        folium.GeoJson(
            us_states_risk.__geo_interface__,
            name="State Tooltips",
            style_function=lambda feature: {
                'fillColor': 'red' if feature['properties'][risk_column] > 5 else 'green',
                'color': 'black',
                'weight': 0.5,
                'fillOpacity': 0.6,
            },
            tooltip=GeoJsonTooltip(
                fields=['NAME', risk_column],
                aliases=['State:', f'{risk_type} Risk Score:'],
                localize=True
            )
        ).add_to(m)

    elif view_type == "County":
        folium.Choropleth(
            geo_data=us_counties_risk.__geo_interface__,
            name=f"County {risk_type} Risk",
            data=us_counties_risk,
            columns=["NAME", risk_column],
            key_on="feature.properties.NAME",
            fill_color="RdYlGn_r",  # Reversed: Red for high risk, Green for low risk
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=legend_name,
            threshold_scale=[0, 1, 3, 5, 7, 10]
        ).add_to(m)

        folium.GeoJson(
            us_counties_risk.__geo_interface__,
            name="County Tooltips",
            style_function=lambda feature: {
                'fillColor': 'red' if feature['properties'][risk_column] > 5 else 'green',
                'color': 'black',
                'weight': 0.5,
                'fillOpacity': 0.6,
            },
            tooltip=GeoJsonTooltip(
                fields=['NAME', risk_column],
                aliases=['County:', f'{risk_type} Risk Score:'],
                localize=True
            )
        ).add_to(m)

    folium.LayerControl().add_to(m)

    return m

# Display the map
m = create_map(view_type, risk_type)
st_folium(m, width=700, height=500)

st.markdown("</div>", unsafe_allow_html=True)  # Close map container

st.markdown("</div>", unsafe_allow_html=True)  # Close main content

# Customer Sales Trend line chart at the bottom
years = [2020, 2021, 2022, 2023]
customers_per_year = np.random.randint(100000, 500000, size=len(years))

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(years, customers_per_year)
ax.set_xlabel('Year')
ax.set_ylabel('Number of Customers')
ax.set_title('Customer Sales Trend')

st.pyplot(fig)
