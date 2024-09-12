import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import folium
from folium.features import GeoJsonTooltip
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

def main():
    st.set_page_config(
        page_title='US Risk Dashboard',
        page_icon='✅',
        layout='wide'
    )

    st.sidebar.title("Navigation")
    pages = {
        "Dashboard": dashboard,
        "Maps": maps,
        "Customer Sales Trend": customer_sales_trend,
    }
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    pages[selection]()

def dashboard():
    st.markdown("## KPI First Row")

    # KPI 1
    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        st.markdown("**First KPI**")
        number1 = np.random.randint(100, 200)
        st.markdown(f"<h1 style='text-align: center; color: red;'>{number1}</h1>", unsafe_allow_html=True)

    with kpi2:
        st.markdown("**Second KPI**")
        number2 = np.random.randint(200, 300)
        st.markdown(f"<h1 style='text-align: center; color: red;'>{number2}</h1>", unsafe_allow_html=True)

    with kpi3:
        st.markdown("**Third KPI**")
        number3 = np.random.randint(300, 400)
        st.markdown(f"<h1 style='text-align: center; color: red;'>{number3}</h1>", unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)

    st.markdown("## KPI Second Row")

    # KPI 2
    kpi01, kpi02, kpi03, kpi04, kpi05 = st.columns(5)

    with kpi01:
        st.markdown("**Another 1st KPI**")
        number1 = np.random.randint(400, 500)
        st.markdown(f"<h1 style='text-align: center; color: yellow;'>{number1}</h1>", unsafe_allow_html=True)

    with kpi02:
        st.markdown("**Another 2nd KPI**")
        number2 = np.random.randint(500, 600)
        st.markdown(f"<h1 style='text-align: center; color: yellow;'>{number2}</h1>", unsafe_allow_html=True)

    with kpi03:
        st.markdown("**Another 3rd KPI**")
        number3 = np.random.randint(600, 700)
        st.markdown(f"<h1 style='text-align: center; color: yellow;'>{number3}</h1>", unsafe_allow_html=True)

    with kpi04:
        st.markdown("**Another 4th KPI**")
        number4 = np.random.randint(700, 800)
        st.markdown(f"<h1 style='text-align: center; color: yellow;'>{number4}</h1>", unsafe_allow_html=True)

    with kpi05:
        st.markdown("**Another 5th KPI**")
        number5 = np.random.randint(800, 900)
        st.markdown(f"<h1 style='text-align: center; color: yellow;'>{number5}</h1>", unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)

    st.markdown("## Chart Layout")

    # Chart layout
    chart1, chart2 = st.columns(2)

    with chart1:
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
        st.line_chart(chart_data)

    with chart2:
        chart_data = pd.DataFrame(np.random.randn(2000, 3), columns=['a', 'b', 'c'])
        st.line_chart(chart_data)

def maps():
    st.markdown("## Map Layout")

    # Sidebar for year filter
    st.sidebar.markdown("<h3>Filter by Year</h3>", unsafe_allow_html=True)
    year = st.sidebar.selectbox('Select Year', [2020, 2021, 2022, 2023])

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

        us_states_risk = us_states.merge(random_state_risk_data, on='NAME', how='left')

        counties = us_counties['NAME']
        county_risk_scores = np.random.randint(1, 11, size=len(counties))
        county_flood_risk_scores = np.random.randint(1, 11, size=len(counties))

        random_county_risk_data = pd.DataFrame({
            'NAME': counties,
            'Earthquake_Risk_Score': county_risk_scores,
            'Flood_Risk_Score': county_flood_risk_scores
        })

        us_counties_risk = us_counties.merge(random_county_risk_data, on='NAME', how='left')

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

# Customer Sales Trend
elif page == "Customer Sales Trend":
    st.title("Customer Sales Trend")
    # Generate random data for the customer sales trend
    years = [2020, 2021, 2022, 2023]
    customers_per_year = np.random.randint(100000, 500000, size=len(years))

    # Create a line chart for customer sales trend
    fig, ax = plt
