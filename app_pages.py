def create_map(view_type, risk_type):
    state_url = 'https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_state_20m.zip'
    county_url = 'https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_county_20m.zip'

    us_states = gpd.read_file(state_url)
    us_counties = gpd.read_file(county_url)

    np.random.seed(42)
    states = us_states['NAME']
    state_risk_scores = np.random.randint(1, 11, size=len(states))  # Fix here
    state_flood_risk_scores = np.random.randint(1, 11, size=len(states))  # Fix here

    random_state_risk_data = pd.DataFrame({
        'NAME': states,
        'Earthquake_Risk_Score': state_risk_scores,
        'Flood_Risk_Score': state_flood_risk_scores
    })

    us_states_risk = us_states.merge(random_state_risk_data, left_on='NAME', right_on='NAME', how='left')

    counties = us_counties['NAME']
    county_risk_scores = np.random.randint(1, 11, size=len(counties))  # Fix here
    county_flood_risk_scores = np.random.randint(1, 11, size=len(counties))  # Fix here

    random_county_risk_data = pd.DataFrame({
        'NAME': counties,
        'Earthquake_Risk_Score': county_risk_scores,
        'Flood_Risk_Score': county_flood_risk_scores
    })

    us_counties_risk = us_counties.merge(random_county_risk_data, left_on='NAME', right_on='NAME', how='left')

    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4, tiles="cartodbpositron")

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
            fill_color="RdYlGn_r",
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
            fill_color="RdYlGn_r",
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
