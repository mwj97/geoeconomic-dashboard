import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Geoeconomic Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark cyberpunk theme
st.markdown("""
    <style>
    .stApp {
        background-color: #0a0e27;
    }
    [data-testid="stSidebar"] {
        background-color: #0f1229;
    }
    h1, h2, h3, p {
        color: #00ffff !important;
    }
    .alert-box {
        background-color: #1a0000;
        border: 2px solid #ff0000;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        color: #ff3333;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
    }
    .alert-title {
        color: #ff0000;
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 8px;
    }
    .alert-detail {
        color: #ffaaaa;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Generate economic corridor data with quarterly values
@st.cache_data
def generate_corridor_data():
    """Generate synthetic quarterly trade data for major economic corridors"""

    # Define major economic corridors with their geographic coordinates
    # Base values verified from authoritative sources (see DATA_SOURCES.md)
    # Values in billions USD annually, updated January 2026
    corridors = {
        'South China Sea': {
            'region': [(5.0, 110.0), (5.0, 120.0), (20.0, 120.0), (20.0, 110.0)],
            'center': (12.5, 115.0),
            'base_value': 5300  # $5.3T - CSIS, ASEAN Maritime Outlook, U.S. EIA
        },
        'Malacca Strait': {
            'region': [(1.0, 102.5), (1.5, 104.0), (5.5, 100.0), (5.0, 99.5)],
            'center': (3.0, 101.5),
            'base_value': 3500  # $3.5T - Maritime & Port Authority of Singapore
        },
        'Strait of Hormuz': {
            'region': [(26.5, 56.0), (26.5, 57.0), (25.5, 57.0), (25.5, 56.0)],
            'center': (26.0, 56.5),
            'base_value': 1400  # $1.4T - U.S. EIA, IEA, UNCTAD
        },
        'English Channel': {
            'region': [(50.5, -1.5), (50.5, 2.0), (51.0, 2.0), (51.0, -1.5)],
            'center': (50.75, 0.25),
            'base_value': 1400  # $1.4T - UK Office for National Statistics
        },
        'Strait of Gibraltar': {
            'region': [(35.9, -5.5), (35.9, -5.2), (36.1, -5.2), (36.1, -5.5)],
            'center': (36.0, -5.35),
            'base_value': 1200  # $1.2T - UNCTAD (10% of global trade)
        },
        'Red Sea / Suez Canal': {
            'region': [(30.5, 32.3), (30.5, 32.5), (12.5, 43.5), (12.5, 43.0)],
            'center': (20.0, 38.0),
            'base_value': 700  # $700B - Suez Canal Authority (2024, impacted by disruptions)
        },
        'Bosphorus Strait': {
            'region': [(41.0, 28.9), (41.0, 29.1), (41.3, 29.1), (41.3, 28.9)],
            'center': (41.15, 29.0),
            'base_value': 400  # $400B - Turkish Ministry of Transport
        },
        'Panama Canal': {
            'region': [(9.0, -79.9), (9.0, -79.4), (9.5, -79.4), (9.5, -79.9)],
            'center': (9.25, -79.65),
            'base_value': 270  # $270B - Panama Canal Authority
        }
    }

    # Generate 20 quarters of data (Q1 2021 - Q4 2025)
    quarters = []
    start_date = datetime(2021, 1, 1)
    for i in range(20):
        quarter_num = (i % 4) + 1
        year = 2021 + (i // 4)
        quarters.append(f"Q{quarter_num} {year}")

    # Generate heat map points for each corridor and quarter
    all_data = []

    for corridor_name, corridor_info in corridors.items():
        for q_idx, quarter in enumerate(quarters):
            # Calculate quarterly value with some variance
            # Add growth trend and seasonal variation
            growth_factor = 1 + (q_idx * 0.015)  # 1.5% growth per quarter
            seasonal_factor = 1 + 0.1 * np.sin(2 * np.pi * (q_idx % 4) / 4)  # Seasonal variation
            random_factor = np.random.uniform(0.9, 1.1)

            quarterly_value = (corridor_info['base_value'] / 4) * growth_factor * seasonal_factor * random_factor

            # Generate multiple points within the corridor region for heat map effect
            num_points = int(quarterly_value / 10)  # More valuable corridors get more points

            region = corridor_info['region']
            lat_min = min(p[0] for p in region)
            lat_max = max(p[0] for p in region)
            lon_min = min(p[1] for p in region)
            lon_max = max(p[1] for p in region)

            for _ in range(num_points):
                lat = np.random.uniform(lat_min, lat_max)
                lon = np.random.uniform(lon_min, lon_max)
                all_data.append({
                    'corridor': corridor_name,
                    'quarter': quarter,
                    'quarter_index': q_idx,
                    'lat': lat,
                    'lon': lon,
                    'value': quarterly_value,
                    'weight': 1
                })

    return pd.DataFrame(all_data), quarters, corridors

# Load the corridor data
corridor_df, available_quarters, corridor_info = generate_corridor_data()

# Sidebar
st.sidebar.title("🌍 Economic Corridors")
st.sidebar.markdown("---")

# Corridor Filter - Checkboxes
st.sidebar.markdown("**🎯 Active Corridors**")
corridor_filters = {}
for corridor_name in corridor_info.keys():
    corridor_filters[corridor_name] = st.sidebar.checkbox(
        corridor_name.replace('/', '/\n'),
        value=True,
        key=corridor_name
    )

# Get selected corridors
selected_corridors = [name for name, selected in corridor_filters.items() if selected]

# Sidebar stats
st.sidebar.markdown("---")
st.sidebar.markdown("**📊 Corridor Statistics**")
st.sidebar.markdown(f"• Active Corridors: {len(selected_corridors)}/{len(corridor_info)}")

# Calculate total trade value for selected corridors
total_base_value = sum(corridor_info[c]['base_value'] for c in selected_corridors)
st.sidebar.markdown(f"• Annual Trade Volume: ${total_base_value:.0f}B")
st.sidebar.markdown("---")

# Main title
st.title("🛰️ Strategic Trade Chokepoints")
st.markdown("Quarterly trade flow heat map across key economic corridors | **Values in Billions USD ($B)**")

# Add time slider for selecting quarters
st.markdown("### 📅 Time Period Selection")
selected_quarter_index = st.slider(
    "Select Quarter",
    min_value=0,
    max_value=len(available_quarters) - 1,
    value=len(available_quarters) - 1,  # Default to most recent quarter
    format="",
    label_visibility="collapsed"
)

# Display selected quarter prominently
selected_quarter = available_quarters[selected_quarter_index]
st.markdown(f"**Current Period: {selected_quarter}**")
st.markdown("---")

# Filter data based on selected corridors and quarter
filtered_data = corridor_df[
    (corridor_df['corridor'].isin(selected_corridors)) &
    (corridor_df['quarter_index'] == selected_quarter_index)
].copy()

# Function to format currency values
def format_currency(value):
    """Format USD values to human-readable format with units (Billions or Millions)"""
    if value >= 1e9:
        return f"${value/1e9:.1f}B"  # Billions
    elif value >= 1e6:
        return f"${value/1e6:.0f}M"  # Millions
    elif value >= 1e3:
        return f"${value/1e3:.0f}K"  # Thousands
    else:
        return f"${value:.0f}"

# Load country boundaries GeoJSON
@st.cache_data
def load_countries_geojson():
    """Load world countries GeoJSON data from Natural Earth"""
    import requests
    url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
    response = requests.get(url)
    return response.json()

countries_geojson = load_countries_geojson()

# Define country boundaries layer
countries_layer = pdk.Layer(
    "GeoJsonLayer",
    data=countries_geojson,
    opacity=0.3,
    stroked=True,
    filled=True,
    extruded=False,
    wireframe=False,
    get_fill_color=[15, 18, 41, 80],  # Dark blue with low opacity (#0f1229)
    get_line_color=[0, 255, 255, 120],  # Cyan borders with medium opacity
    get_line_width=500,
    line_width_min_pixels=1,
    pickable=True
)

# Define heat map layer for economic corridors
heatmap_layer = pdk.Layer(
    "HeatmapLayer",
    data=filtered_data,
    get_position=["lon", "lat"],
    get_weight="weight",
    radiusPixels=60,
    intensity=1,
    threshold=0.05,
    colorRange=[
        [0, 0, 0, 0],           # Transparent for low activity
        [65, 182, 196, 100],    # Light teal
        [127, 205, 187, 150],   # Medium teal
        [199, 233, 180, 200],   # Light yellow-green
        [237, 248, 177, 230],   # Yellow
        [255, 237, 160, 255],   # Light orange
        [254, 178, 76, 255],    # Orange
        [240, 59, 32, 255]      # Red for highest activity
    ],
    pickable=False
)

# Create corridor center points for labels with quarterly data
# Calculate total global trade for percentage calculations
global_total = sum(corridor_info[c]['base_value'] for c in corridor_info.keys())

corridor_centers = []
for corridor_name in selected_corridors:
    center = corridor_info[corridor_name]['center']
    # Get quarterly value for this corridor
    corridor_quarter_data = filtered_data[filtered_data['corridor'] == corridor_name]
    quarterly_value = corridor_quarter_data['value'].iloc[0] if len(corridor_quarter_data) > 0 else 0

    # Calculate percentage of global total (using annual base values)
    annual_base = corridor_info[corridor_name]['base_value']
    global_share_pct = (annual_base / global_total) * 100

    corridor_centers.append({
        'name': corridor_name,
        'lat': center[0],
        'lon': center[1],
        'quarterly_value': quarterly_value,
        'formatted_value': format_currency(quarterly_value),
        'quarter': selected_quarter,
        'annual_estimate': format_currency(quarterly_value * 4),
        'global_share': f"{global_share_pct:.1f}%"
    })

corridor_centers_df = pd.DataFrame(corridor_centers)

# Define scatter plot layer for corridor labels - made more prominent
if len(corridor_centers_df) > 0:
    # Prominent corridor marker points
    corridor_points_layer = pdk.Layer(
        "ScatterplotLayer",
        data=corridor_centers_df,
        get_position=["lon", "lat"],
        get_color=[0, 255, 255, 255],  # Bright cyan with full opacity
        get_radius=300000,  # Large visible markers
        pickable=True,
        auto_highlight=True,
        stroked=True,
        get_line_color=[255, 255, 255, 255],  # White border
        line_width_min_pixels=4
    )

    # Black shadow/outline for corridor names (rendered first for outline effect)
    corridor_text_shadow = pdk.Layer(
        "TextLayer",
        data=corridor_centers_df,
        get_position=["lon", "lat"],
        get_text="name",
        get_size=22,  # Large, visible text
        get_color=[0, 0, 0, 255],  # Black outline
        get_angle=0,
        get_text_anchor="'middle'",
        get_alignment_baseline="'bottom'",
        offset=[0, -40],  # Position above marker
        font_family="'Arial', 'Helvetica', sans-serif",
        font_weight="bold",
        pickable=False,
        outline_width=4
    )

    # White text for corridor names (rendered on top)
    corridor_text_layer = pdk.Layer(
        "TextLayer",
        data=corridor_centers_df,
        get_position=["lon", "lat"],
        get_text="name",
        get_size=20,  # Large, visible text
        get_color=[255, 255, 255, 255],  # White text with full opacity
        get_angle=0,
        get_text_anchor="'middle'",
        get_alignment_baseline="'bottom'",
        offset=[0, -40],  # Position above marker
        font_family="'Arial', 'Helvetica', sans-serif",
        font_weight="bold",
        pickable=False
    )

    # Black shadow/outline for trade values
    corridor_value_shadow = pdk.Layer(
        "TextLayer",
        data=corridor_centers_df,
        get_position=["lon", "lat"],
        get_text="formatted_value",
        get_size=20,  # Large, visible values
        get_color=[0, 0, 0, 255],  # Black outline
        get_angle=0,
        get_text_anchor="'middle'",
        get_alignment_baseline="'top'",
        offset=[0, 40],  # Position below marker
        font_family="'Arial', 'Helvetica', sans-serif",
        font_weight="bold",
        pickable=False,
        outline_width=4
    )

    # Cyan text for trade values (rendered on top)
    corridor_value_layer = pdk.Layer(
        "TextLayer",
        data=corridor_centers_df,
        get_position=["lon", "lat"],
        get_text="formatted_value",
        get_size=18,  # Large, visible values
        get_color=[0, 255, 255, 255],  # Bright cyan text for values
        get_angle=0,
        get_text_anchor="'middle'",
        get_alignment_baseline="'top'",
        offset=[0, 40],  # Position below marker
        font_family="'Arial', 'Helvetica', sans-serif",
        font_weight="bold",
        pickable=False
    )
else:
    corridor_points_layer = None
    corridor_text_shadow = None
    corridor_text_layer = None
    corridor_value_shadow = None
    corridor_value_layer = None

# Define the initial view state
view_state = pdk.ViewState(
    latitude=20,
    longitude=30,
    zoom=1.5,
    pitch=45,
    bearing=0
)

# Create layers list with proper ordering (bottom to top)
# Order: countries → heatmap → corridor points → text shadows → text labels
layers_list = [countries_layer, heatmap_layer]
if corridor_points_layer is not None:
    layers_list.append(corridor_points_layer)
if corridor_text_shadow is not None:
    layers_list.append(corridor_text_shadow)
if corridor_text_layer is not None:
    layers_list.append(corridor_text_layer)
if corridor_value_shadow is not None:
    layers_list.append(corridor_value_shadow)
if corridor_value_layer is not None:
    layers_list.append(corridor_value_layer)

# Create the deck with dark map style - layer order: countries, heatmap, corridor points
r = pdk.Deck(
    layers=layers_list,
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/dark-v10",
    tooltip={
        "html": "<div style='font-family: monospace;'>"
                "<b style='font-size: 16px; color: #00ffff;'>{name}</b><br/>"
                "<div style='margin-top: 8px; padding-top: 8px; border-top: 1px solid #00ffff;'>"
                "<b>Period:</b> {quarter}<br/>"
                "<b>Quarterly Trade:</b> {formatted_value} (Billions USD)<br/>"
                "<b>Annual Estimate:</b> {annual_estimate} (Billions USD)<br/>"
                "<b>Share of Global Total:</b> {global_share}<br/>"
                "</div>"
                "</div>",
        "style": {
            "backgroundColor": "#0a0e27",
            "color": "#00ffff",
            "border": "2px solid #00ffff",
            "borderRadius": "8px",
            "padding": "12px",
            "boxShadow": "0 0 20px rgba(0, 255, 255, 0.3)"
        }
    }
)

# Display the map
st.pydeck_chart(r, use_container_width=True)

# Calculate quarterly metrics for selected corridors
quarterly_values = filtered_data.groupby('corridor')['value'].first().reset_index()
total_quarterly_value = quarterly_values['value'].sum() if len(quarterly_values) > 0 else 0

# Calculate quarter-over-quarter change if not first quarter
if selected_quarter_index > 0:
    prev_quarter_data = corridor_df[
        (corridor_df['corridor'].isin(selected_corridors)) &
        (corridor_df['quarter_index'] == selected_quarter_index - 1)
    ]
    prev_quarterly_value = prev_quarter_data.groupby('corridor')['value'].first().sum() if len(prev_quarter_data) > 0 else 0

    if prev_quarterly_value > 0:
        qoq_change = ((total_quarterly_value - prev_quarterly_value) / prev_quarterly_value) * 100
        qoq_delta = f"{qoq_change:+.1f}%"
    else:
        qoq_delta = "N/A"
else:
    qoq_delta = "N/A"

# Add metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Active Corridors", len(selected_corridors), delta=None)
with col2:
    st.metric("Quarterly Trade Volume", format_currency(total_quarterly_value), delta=qoq_delta)
with col3:
    # Calculate average trade intensity
    avg_corridor_value = total_quarterly_value / len(selected_corridors) if len(selected_corridors) > 0 else 0
    intensity_status = "HIGH" if avg_corridor_value > 200 else "MODERATE" if avg_corridor_value > 100 else "LOW"
    st.metric("Trade Intensity", intensity_status, delta=None)

# Corridor Rankings
st.markdown("---")
st.markdown("### 📊 Corridor Rankings by Trade Volume")

if len(quarterly_values) > 0:
    # Sort by value and display
    quarterly_values_sorted = quarterly_values.sort_values('value', ascending=False)

    ranking_data = []
    for idx, row in quarterly_values_sorted.iterrows():
        ranking_data.append({
            'Rank': len(ranking_data) + 1,
            'Corridor': row['corridor'],
            'Quarterly Value': format_currency(row['value']),
            'Share of Total': f"{(row['value']/total_quarterly_value*100):.1f}%" if total_quarterly_value > 0 else "0%"
        })

    ranking_df = pd.DataFrame(ranking_data)
    st.dataframe(ranking_df, use_container_width=True, hide_index=True)
else:
    st.info("Select corridors to view rankings")

# Quarterly trend chart
st.markdown("---")
st.markdown("### 📈 Historical Trade Trends")

if len(selected_corridors) > 0:
    # Prepare trend data for selected corridors
    trend_data = []
    for corridor_name in selected_corridors:
        corridor_trend = corridor_df[corridor_df['corridor'] == corridor_name].groupby('quarter_index')['value'].first().reset_index()
        corridor_trend['corridor'] = corridor_name
        trend_data.append(corridor_trend)

    if trend_data:
        combined_trend = pd.concat(trend_data, ignore_index=True)
        combined_trend['quarter'] = combined_trend['quarter_index'].apply(lambda x: available_quarters[x])

        # Pivot for display
        trend_pivot = combined_trend.pivot(index='quarter', columns='corridor', values='value')

        # Display as line chart
        st.line_chart(trend_pivot, use_container_width=True)
else:
    st.info("Select corridors to view trends")
