import streamlit as st
import geopandas as gpd
import pandas as pd
import numpy as np
import folium
from folium.features import GeoJsonTooltip
from streamlit_folium import st_folium

# Adjusted CSS to position the image top-right, above the title
st.markdown(
    """
    <style>
    .logo {
        position: absolute;
        top: 0px;
        right: 20px;
        width: 120px;
        z-index: 100;
    }
    .header {
        margin-top: 100px;  /* Add margin to push the title below the logo */
    }
    </style>
    <img src="http://ormiro.com/cdn/shop/articles/backup-article-607842304304.jpg?v=1721254571" class="logo">
    """,
    unsafe_allow_html=True
)

# Title in the center with some margin to ensure it's placed below the image
st.markdown(
    "<h1 class='header' style='text-align: center; color:#7EC8E3;'>US Earthquake and Flood Risk Map</h1>", 
    unsafe_allow_html=True
)

# Function to generate and return a Folium map
def create_map(view_type, risk_type):
    # Load state and county shapefiles
    state_url = 'https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_state_20m.zip'
    county_url = 'https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_county_20m.zip'

    us_states = gpd.read_file(state_url)
    us_counties = gpd.read_file(county_url)

    # Generate random risk data for each state
    np.random.seed(42)
    states = us_states['NAME']
    state_risk_scores = np.random.randint(1, 11, size=len(states))  # Random risk scores between 1 and 10
    state_flood_risk_scores = np.random.randint(1, 11, size=len(states))  # Random flood risk scores

    random_state_risk_data = pd.DataFrame({
        'NAME': states,
        'Earthquake_Risk_Score': state_risk_scores,
        'Flood_Risk_Score': state_flood_risk_scores
    })

    us_states_risk = us_states.merge(random_state_risk_data, left_on='NAME', right_on='NAME', how='left')

    counties = us_counties['NAME']
    county_risk_scores = np.random.randint(1, 11, size=len(counties))  # Random risk scores between 1 and 10
    county_flood_risk_scores = np.random.randint(1, 11, size=len(counties))  # Random flood risk scores

    random_county_risk_data = pd.DataFrame({
        'NAME': counties,
        'Earthquake_Risk_Score': county_risk_scores,
        'Flood_Risk_Score': county_flood_risk_scores
    })

    us_counties_risk = us_counties.merge(random_county_risk_data, left_on='NAME', right_on='NAME', how='left')

    # Fill missing risk scores with 0 (shouldn't be needed here but good practice)
    us_states_risk['Earthquake_Risk_Score'] = us_states_risk['Earthquake_Risk_Score'].fillna(0)
    us_counties_risk['Earthquake_Risk_Score'] = us_counties_risk['Earthquake_Risk_Score'].fillna(0)
    us_states_risk['Flood_Risk_Score'] = us_states_risk['Flood_Risk_Score'].fillna(0)
    us_counties_risk['Flood_Risk_Score'] = us_counties_risk['Flood_Risk_Score'].fillna(0)

    # Create a Folium map centered over the US
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4, tiles="cartodbpositron")

    # Define color scale based on risk type
    if risk_type == "Earthquake":
        risk_column = "Earthquake_Risk_Score"
        legend_name = "Earthquake Risk Score"
    else:
        risk_column = "Flood_Risk_Score"
        legend_name = "Flood Risk Score"

    # Add choropleth layer based on the view type (State or County)
    if view_type == "State":
        folium.Choropleth(
            geo_data=us_states_risk.__geo_interface__,
            name=f"State {risk_type} Risk",
            data=us_states_risk,
            columns=["NAME", risk_column],
            key_on="feature.properties.NAME",
            fill_color="RdYlGn",  # Inverted: Red for high risk, Green for low risk
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=legend_name,
            nan_fill_color="white",
            threshold_scale=[0, 1, 3, 5, 7, 10]  # Define threshold for color breaks
        ).add_to(m)

        # Add tooltips for State-Level Risk
        folium.GeoJson(
            us_states_risk.__geo_interface__,
            name="State Tooltips",
            style_function=lambda feature: {
                'fillColor': 'orange' if feature['properties'][risk_column] > 0 else 'white',
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
            fill_color="RdYlGn",  # Inverted: Red for high risk, Green for low risk
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=legend_name,
            nan_fill_color="white",
            threshold_scale=[0, 1, 3, 5, 7, 10]  # Define threshold for color breaks
        ).add_to(m)

        # Add tooltips for County-Level Risk
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

    # Add layer control to toggle between State and County views
    folium.LayerControl().add_to(m)

    return m

# Sidebar for selecting view type and risk type
st.sidebar.markdown("<h3>View and Risk Selection</h3>", unsafe_allow_html=True)
view_type = st.sidebar.selectbox('Select View Type', ['State', 'County'])
risk_type = st.sidebar.selectbox('Select Risk Type', ['Earthquake', 'Flood'])

# Generate and display the map based on the selected view type and risk type
m = create_map(view_type, risk_type)
st_folium(m, width=700, height=500)

# Footer style to hide Streamlit's default footer
st.markdown(
    """
    <style>
    .reportview-container .main footer {
        visibility: hidden;
    }
    .reportview-container .main {
        padding-top: 10px;
        padding-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
