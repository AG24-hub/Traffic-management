import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.set_page_config(layout="wide")
st.title("🚨 Bangalore Traffic Hotspot Deployment Dashboard")

df = pd.read_csv("hotspot_Data.csv")

st.sidebar.header("Enforcement Controls")
view_mode = st.sidebar.selectbox(
    "Select Shift Window", 
    ["Overall View", "Morning (08:00 - 14:00)", "Afternoon (14:00 - 20:00)", "Evening (20:00 - 02:00)", "Nighttime (02:00 - 08:00)"]
)

df['created_datetime'] = pd.to_datetime(df['created_datetime'], format='mixed')
df['hour'] = df['created_datetime'].dt.hour

# Filter out noise records
df_filtered = df[df['hotspot_cluster'] != -1]

if view_mode == "Morning (08:00 - 14:00)":
    df_filtered = df_filtered[(df_filtered['hour'] >= 8) & (df_filtered['hour'] < 14)]
elif view_mode == "Afternoon (14:00 - 20:00)":
    df_filtered = df_filtered[(df_filtered['hour'] >= 14) & (df_filtered['hour'] < 20)]
elif view_mode == "Evening (20:00 - 02:00)":
    df_filtered = df_filtered[(df_filtered['hour'] >= 20) | (df_filtered['hour'] < 2)]
elif view_mode == "Nighttime (02:00 - 08:00)":
    df_filtered = df_filtered[(df_filtered['hour'] >= 2) & (df_filtered['hour'] < 8)]

# 3. Dynamic Aggregations based on your operational shift profiles
top_profiles = df_filtered.groupby('hotspot_cluster').agg(
    total_violations=('hotspot_cluster', 'count'),
    primary_junction=('junction_name', lambda x: x.mode()[0] if not x.mode().empty else "Unknown"),
    top_vehicle=('vehicle_type', lambda x: x.mode()[0] if not x.mode().empty else "Unknown"),
    top_violation=('violation_type', lambda x: x.mode()[0] if not x.mode().empty else "Unknown"),
    lat=('latitude', 'mean'),
    lon=('longitude', 'mean')
).sort_values(by='total_violations', ascending=False).head(10)

# 4. App UI Layout split
col1, col2 = st.columns([2, 1])

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"📍 Active Hotspot Deployment Map ({view_mode})")
    m = folium.Map(location=[12.9716, 77.5946], zoom_start=12)
    
    # Initialize the marker cluster on the map
    marker_cluster = MarkerCluster().add_to(m)
    
    # Plot all matching filtered individual rows within the clustered view
    for idx, row in df_filtered.iterrows():
        popup_text = f"Junction: {row['junction_name']}<br>Cluster: {row['hotspot_cluster']}"
        folium.Marker(
            location=[row['latitude'], row['longitude']], 
            popup=folium.Popup(popup_text, max_width=300), 
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(marker_cluster)
        
    # Unique key prevents component re-render loops in streamlit-folium
    st_folium(m, width=800, height=550, key=f"map_{view_mode}")

with col2:
    st.subheader("📊 Deployment Resource Allocation")
    st.dataframe(
        top_profiles[['total_violations', 'primary_junction', 'top_violation', 'top_vehicle']],
        use_container_width=True
    )