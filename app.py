import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import os

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

# Load shipment data
@st.cache_data
def load_data():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'shipments.csv')
    df = pd.read_csv(data_path)
    return df

# Load the data
shipments_df = load_data()

# Sidebar
st.sidebar.title("🌍 Global Hotspots")
st.sidebar.markdown("---")

# Risk Filter - Checkboxes
st.sidebar.markdown("**🎯 Risk Filter**")
show_high = st.sidebar.checkbox("🔴 High Risk", value=True)
show_medium = st.sidebar.checkbox("🟡 Medium Risk", value=True)
show_low = st.sidebar.checkbox("🔵 Low Risk", value=True)

# Filter data based on risk selection
filtered_data = shipments_df.copy()
risk_filters = []
if show_high:
    risk_filters.append("High")
if show_medium:
    risk_filters.append("Medium")
if show_low:
    risk_filters.append("Low")

filtered_data = filtered_data[filtered_data['risk_level'].isin(risk_filters)]

# Sidebar stats
st.sidebar.markdown("---")
st.sidebar.markdown("**📊 Active Routes**")
st.sidebar.markdown(f"• Total: {len(filtered_data)}")
st.sidebar.markdown(f"• High Risk: {len(filtered_data[filtered_data['risk_level'] == 'High'])}")
st.sidebar.markdown(f"• Medium Risk: {len(filtered_data[filtered_data['risk_level'] == 'Medium'])}")
st.sidebar.markdown(f"• Low Risk: {len(filtered_data[filtered_data['risk_level'] == 'Low'])}")
st.sidebar.markdown("---")

# Determine overall intelligence level
high_count = len(filtered_data[filtered_data['risk_level'] == 'High'])
if high_count >= 3:
    intel_level = "🔴 CRITICAL"
elif high_count > 0:
    intel_level = "🟡 ELEVATED"
else:
    intel_level = "🟢 NORMAL"
st.sidebar.markdown(f"**Intelligence Level**: {intel_level}")

# Main title
st.title("🛰️ Geoeconomic Intelligence Dashboard")
st.markdown("Real-time defense & aerospace trade flow monitoring")

# Function to get color based on risk level
def get_risk_color(risk_level):
    """Return RGB color based on risk level"""
    color_map = {
        "High": [255, 0, 0, 255],      # Red
        "Medium": [255, 255, 0, 255],  # Yellow
        "Low": [0, 100, 255, 255]      # Blue
    }
    return color_map.get(risk_level, [255, 255, 255, 255])

# Function to calculate arc width based on value_usd
def calculate_width(value_usd):
    """Scale arc width based on shipment value"""
    # Normalize to 1-10 scale
    min_width = 2
    max_width = 12
    min_value = shipments_df['value_usd'].min()
    max_value = shipments_df['value_usd'].max()

    if max_value == min_value:
        return min_width

    normalized = (value_usd - min_value) / (max_value - min_value)
    width = min_width + (normalized * (max_width - min_width))
    return width

# Function to format currency values
def format_currency(value):
    """Format USD values to human-readable format (e.g., $450M, $1.2B)"""
    if value >= 1e9:
        return f"${value/1e9:.1f}B"
    elif value >= 1e6:
        return f"${value/1e6:.0f}M"
    elif value >= 1e3:
        return f"${value/1e3:.0f}K"
    else:
        return f"${value:.0f}"

# Prepare arc data with colors and widths
arc_data = filtered_data.copy()
arc_data['color'] = arc_data['risk_level'].apply(get_risk_color)
arc_data['width'] = arc_data['value_usd'].apply(calculate_width)
arc_data['formatted_value'] = arc_data['value_usd'].apply(format_currency)

# Create point data for unique cities (origins and destinations)
origin_points = filtered_data[['origin_city', 'origin_lat', 'origin_lon']].copy()
origin_points.columns = ['city', 'lat', 'lon']

dest_points = filtered_data[['dest_city', 'dest_lat', 'dest_lon']].copy()
dest_points.columns = ['city', 'lat', 'lon']

# Combine and remove duplicates
point_data = pd.concat([origin_points, dest_points]).drop_duplicates(subset=['city'])
point_data['size'] = 200

# Define arc layer with dynamic colors and widths
arc_layer = pdk.Layer(
    "ArcLayer",
    data=arc_data,
    get_source_position=["origin_lon", "origin_lat"],
    get_target_position=["dest_lon", "dest_lat"],
    get_source_color="color",
    get_target_color="color",
    get_width="width",
    get_height=0.4,
    pickable=True,
    auto_highlight=True
)

# Define point layer for cities with cyan color
point_layer = pdk.Layer(
    "ScatterplotLayer",
    data=point_data,
    get_position=["lon", "lat"],
    get_color=[0, 255, 255, 255],  # Cyan
    get_radius="size",
    radius_scale=600,
    radius_min_pixels=8,
    radius_max_pixels=15,
    pickable=True
)

# Define GeoJSON layer for country borders
geojson_layer = pdk.Layer(
    "GeoJsonLayer",
    data="https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json",
    stroked=True,
    filled=True,
    get_fill_color=[10, 20, 50, 80],  # Very dark and transparent
    get_line_color=[100, 200, 200, 100],  # Dim cyan for borders
    line_width_min_pixels=1,
    pickable=False
)

# Define the initial view state
view_state = pdk.ViewState(
    latitude=30,
    longitude=0,
    zoom=1.3,
    pitch=50,
    bearing=0
)

# Create the deck with dark map style - layer order: countries, arcs, points
r = pdk.Deck(
    layers=[geojson_layer, arc_layer, point_layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/dark-v10",
    tooltip={
        "html": "<b>{origin_city} → {dest_city}</b><br/>"
                "Risk: {risk_level}<br/>"
                "Value: {formatted_value}<br/>"
                "Vessel: {vessel_type}<br/>"
                "Flag: {flag_state}",
        "style": {
            "backgroundColor": "#0a0e27",
            "color": "#00ffff",
            "border": "1px solid #ff0000"
        }
    }
)

# Display the map
st.pydeck_chart(r, use_container_width=True)

# Calculate metrics from filtered data
total_value = filtered_data['value_usd'].sum()
avg_value = filtered_data['value_usd'].mean()
high_risk_count = len(filtered_data[filtered_data['risk_level'] == 'High'])

# Add metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Active Routes", len(filtered_data), delta=f"{len(filtered_data) - len(shipments_df) + len(filtered_data)}")
with col2:
    st.metric("Total Trade Volume", f"${total_value/1e9:.1f}B", delta="+2.3%")
with col3:
    if high_risk_count == 0:
        risk_status = "LOW"
        risk_delta = "IMPROVED"
    elif high_risk_count <= 2:
        risk_status = "MODERATE"
        risk_delta = "STABLE"
    else:
        risk_status = "ELEVATED"
        risk_delta = "RISING"
    st.metric("Risk Level", risk_status, delta=risk_delta)

# Compliance Intelligence - Alert Console
st.markdown("---")
st.markdown("### ⚠️ LIVE COMPLIANCE ALERTS")

# Function to check for compliance violations
def check_compliance_violations(data):
    """Check for High Risk shipments with flags of convenience"""
    flags_of_convenience = ['Panama', 'Liberia', 'Marshall Islands']

    violations = data[
        (data['risk_level'] == 'High') &
        (data['flag_state'].isin(flags_of_convenience))
    ]

    return violations

# Get compliance violations from filtered data
compliance_violations = check_compliance_violations(filtered_data)

if len(compliance_violations) > 0:
    for idx, row in compliance_violations.iterrows():
        alert_html = f"""
        <div class="alert-box">
            <div class="alert-title">🚨 ALERT: High-Risk Shipment on Flag of Convenience</div>
            <div class="alert-detail">
                <strong>Route:</strong> {row['origin_city']} → {row['dest_city']}<br/>
                <strong>Vessel Type:</strong> {row['vessel_type']}<br/>
                <strong>Flag State:</strong> {row['flag_state']}<br/>
                <strong>Shipment Value:</strong> ${row['value_usd']:,.0f}<br/>
                <strong>Risk Level:</strong> {row['risk_level']}<br/>
                <strong>Action Required:</strong> Enhanced screening and documentation review recommended
            </div>
        </div>
        """
        st.markdown(alert_html, unsafe_allow_html=True)

    st.markdown(f"**Total Alerts:** {len(compliance_violations)}")
else:
    st.success("✅ No compliance violations detected in current filtered view")

# Data table section
st.markdown("---")
st.markdown("### 📋 Shipment Details")

# Format the display dataframe with new columns
display_df = filtered_data[['origin_city', 'dest_city', 'risk_level', 'value_usd', 'vessel_type', 'flag_state']].copy()
display_df['value_usd'] = display_df['value_usd'].apply(lambda x: f"${x/1e6:.0f}M")
display_df.columns = ['Origin', 'Destination', 'Risk Level', 'Value (USD)', 'Vessel Type', 'Flag State']

st.dataframe(display_df, use_container_width=True, hide_index=True)
