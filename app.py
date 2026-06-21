import streamlit as st
import pandas as pd
import numpy as np
import folium
import altair as alt
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gridlock · Bangalore Traffic Intelligence",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Premium Custom CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Dark background ── */
.stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 40%, #16213e 100%);
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
    border-right: 1px solid rgba(99, 102, 241, 0.15);
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stRadio label,
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
    color: #e2e8f0 !important;
}

/* ── Header styling ── */
h1 {
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
    font-size: 2.2rem !important;
    margin-bottom: 0 !important;
}
h2, h3 {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
}
p, span, label, .stMarkdown {
    color: #cbd5e1 !important;
}

/* ── KPI Metric Cards ── */
.kpi-container {
    display: flex;
    gap: 16px;
    margin: 12px 0 24px 0;
}
.kpi-card {
    flex: 1;
    background: linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(168,85,247,0.08) 100%);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(12px);
}
.kpi-card:hover {
    border-color: rgba(99,102,241,0.5);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(99,102,241,0.15);
}
.kpi-value {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}
.kpi-label {
    font-size: 0.78rem;
    color: #94a3b8 !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 6px;
    font-weight: 600;
}

/* ── Section Cards ── */
.section-card {
    background: rgba(30, 30, 50, 0.6);
    border: 1px solid rgba(99,102,241,0.12);
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(12px);
    margin-bottom: 16px;
}

/* ── Dataframe styling ── */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
}
[data-testid="stDataFrame"] {
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 12px;
}

/* ── Streamlit element overrides ── */
.stSelectbox > div > div {
    background: rgba(30, 30, 50, 0.8) !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* ── Divider ── */
.gradient-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, #6366f1, #a855f7, #ec4899, transparent);
    border: none;
    margin: 8px 0 24px 0;
    border-radius: 2px;
}

/* ── Badge pills ── */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.badge-purple {
    background: rgba(139, 92, 246, 0.2);
    color: #c4b5fd;
    border: 1px solid rgba(139, 92, 246, 0.3);
}
.badge-pink {
    background: rgba(236, 72, 153, 0.2);
    color: #f9a8d4;
    border: 1px solid rgba(236, 72, 153, 0.3);
}

/* ── Sidebar brand ── */
.sidebar-brand {
    text-align: center;
    padding: 16px 0 24px 0;
    border-bottom: 1px solid rgba(99,102,241,0.15);
    margin-bottom: 24px;
}
.sidebar-brand-title {
    font-size: 1.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sidebar-brand-sub {
    font-size: 0.7rem;
    color: #64748b !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 4px;
}

/* ── Shift selector radio buttons ── */
.shift-active {
    background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(168,85,247,0.1));
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 10px;
    padding: 10px 16px;
    margin: 4px 0;
}

/* ── Bar chart styling ── */
.bar-row {
    display: flex;
    align-items: center;
    margin: 6px 0;
    gap: 10px;
}
.bar-label {
    width: 110px;
    font-size: 0.78rem;
    color: #94a3b8 !important;
    text-align: right;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex-shrink: 0;
}
.bar-track {
    flex: 1;
    height: 24px;
    background: rgba(30,30,50,0.5);
    border-radius: 6px;
    overflow: hidden;
    position: relative;
}
.bar-fill {
    height: 100%;
    border-radius: 6px;
    display: flex;
    align-items: center;
    padding-left: 10px;
    font-size: 0.72rem;
    font-weight: 600;
    color: #fff;
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── Map container ── */
.map-container iframe {
    border-radius: 12px !important;
    border: 1px solid rgba(99,102,241,0.15) !important;
}

/* ── Hide default streamlit elements ── */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* ── Table rank badge ── */
.rank-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    font-size: 0.75rem;
    font-weight: 700;
    background: linear-gradient(135deg, #6366f1, #a855f7);
    color: #fff;
}
</style>
""", unsafe_allow_html=True)


# ── Data Loading with Cache ─────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def load_data():
    """Load and preprocess the hotspot data with caching."""
    df = pd.read_csv("hotspot_Data.csv")
    df['created_datetime'] = pd.to_datetime(df['created_datetime'], format='mixed')
    df['hour'] = df['created_datetime'].dt.hour
    df['month'] = df['created_datetime'].dt.month_name()
    # Filter out DBSCAN noise
    df = df[df['hotspot_cluster'] != -1]
    return df


df = load_data()

# ── Shift Definitions ───────────────────────────────────────────────────────
SHIFTS = {
    "🌅  All Shifts": None,
    "☀️  Morning (08:00–14:00)": (8, 14, "standard"),
    "🌤️  Afternoon (14:00–20:00)": (14, 20, "standard"),
    "🌙  Evening (20:00–02:00)": (20, 2, "overnight"),
    "🌃  Nighttime (02:00–08:00)": (2, 8, "standard"),
}

SHIFT_COLORS = {
    "🌅  All Shifts": "#6366f1",
    "☀️  Morning (08:00–14:00)": "#f59e0b",
    "🌤️  Afternoon (14:00–20:00)": "#f97316",
    "🌙  Evening (20:00–02:00)": "#8b5cf6",
    "🌃  Nighttime (02:00–08:00)": "#3b82f6",
}

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-title">🚦 GRIDLOCK</div>
        <div class="sidebar-brand-sub">Traffic Intelligence System</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎯 Enforcement Controls")

    selected_shift = st.selectbox(
        "Shift Window",
        list(SHIFTS.keys()),
        index=0,
        help="Filter violations by police shift timing"
    )

    st.markdown("---")
    st.markdown("### 📊 Display Options")

    num_hotspots = st.slider(
        "Top Hotspots to Display",
        min_value=5,
        max_value=25,
        value=10,
        step=5,
        help="Number of highest-violation clusters to show"
    )

    st.markdown("---")

    # Sidebar stats
    st.markdown("### 📋 Dataset Info")
    st.markdown(f"""
    <div style="font-size: 0.82rem; color: #94a3b8; line-height: 2;">
        📌 <b style="color:#c4b5fd;">{len(df):,}</b> validated violations<br/>
        📌 <b style="color:#c4b5fd;">{df['hotspot_cluster'].nunique()}</b> hotspot clusters<br/>
        📌 <b style="color:#c4b5fd;">{df['police_station'].nunique()}</b> police stations<br/>
        📌 <b style="color:#c4b5fd;">{df['junction_name'].nunique()}</b> junction names
    </div>
    """, unsafe_allow_html=True)


# ── Filter Data by Shift ────────────────────────────────────────────────────
def filter_by_shift(data, shift_key):
    """Apply shift-window time filter."""
    shift_def = SHIFTS[shift_key]
    if shift_def is None:
        return data
    start, end, mode = shift_def
    if mode == "overnight":
        return data[(data['hour'] >= start) | (data['hour'] < end)]
    else:
        return data[(data['hour'] >= start) & (data['hour'] < end)]


df_filtered = filter_by_shift(df, selected_shift)


# ── Aggregate Hotspot Profiles ──────────────────────────────────────────────
def compute_profiles(data, n):
    """Compute top N cluster profiles from filtered data.
    
    Performance: identifies top N clusters FIRST by simple count,
    then computes expensive mode aggregations on only those N groups.
    """
    # Step 1: Find top N cluster IDs by violation count (instant)
    top_cluster_ids = data['hotspot_cluster'].value_counts().head(n).index
    subset = data[data['hotspot_cluster'].isin(top_cluster_ids)]
    
    # Step 2: Fast numeric aggregations on the small subset
    profiles = subset.groupby('hotspot_cluster').agg(
        total_violations=('hotspot_cluster', 'size'),
        lat=('latitude', 'mean'),
        lon=('longitude', 'mean')
    )
    
    # Step 3: Compute modes only for the top N clusters (fast: only N groups)
    for src_col, dst_col in [('junction_name', 'primary_junction'),
                              ('police_station', 'police_station'),
                              ('vehicle_type', 'top_vehicle'),
                              ('violation_type', 'top_violation')]:
        profiles[dst_col] = (
            subset.groupby('hotspot_cluster')[src_col]
            .agg(lambda x: x.value_counts().index[0] if len(x) > 0 else "Unknown")
        )
    
    profiles = profiles.sort_values('total_violations', ascending=False)
    profiles['rank'] = range(1, len(profiles) + 1)
    return profiles


with st.spinner("🔄 Crunching hotspot data..."):
    top_profiles = compute_profiles(df_filtered, num_hotspots)


# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("# 🚦 Bangalore Traffic Intelligence Dashboard")
st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)


# ── KPI Metrics ─────────────────────────────────────────────────────────────
total_violations = df_filtered['hotspot_cluster'].count()
active_clusters = df_filtered['hotspot_cluster'].nunique()
top_zone_name = top_profiles.iloc[0]['primary_junction'] if len(top_profiles) > 0 else "N/A"
top_zone_count = int(top_profiles.iloc[0]['total_violations']) if len(top_profiles) > 0 else 0
avg_per_cluster = int(total_violations / active_clusters) if active_clusters > 0 else 0

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-value">{total_violations:,}</div>
        <div class="kpi-label">Total Violations</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{active_clusters}</div>
        <div class="kpi-label">Active Clusters</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{avg_per_cluster:,}</div>
        <div class="kpi-label">Avg. per Cluster</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{top_zone_count:,}</div>
        <div class="kpi-label">🔥 Worst Hotspot</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Main Layout ─────────────────────────────────────────────────────────────
col_map, col_data = st.columns([3, 2], gap="large")


# ── Map ─────────────────────────────────────────────────────────────────────
with col_map:
    shift_color = SHIFT_COLORS[selected_shift]
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
        <h3 style="margin:0;">📍 Hotspot Deployment Map</h3>
        <span class="badge badge-purple">{selected_shift.split('  ')[1] if '  ' in selected_shift else 'All Shifts'}</span>
    </div>
    """, unsafe_allow_html=True)

    # Build the Folium map — plotting CLUSTER CENTROIDS, not individual rows
    m = folium.Map(
        location=[12.9716, 77.5946],
        zoom_start=12,
        tiles="OpenStreetMap"
    )

    # Color scale for markers based on violation severity
    max_violations = top_profiles['total_violations'].max() if len(top_profiles) > 0 else 1

    for _, row in top_profiles.iterrows():
        # Scale radius by violation count (min 8, max 22)
        ratio = row['total_violations'] / max_violations
        radius = 8 + ratio * 14

        # Color gradient: low=blue → medium=purple → high=red
        if ratio > 0.7:
            color = "#ef4444"
            fill_color = "#fca5a5"
        elif ratio > 0.4:
            color = "#a855f7"
            fill_color = "#d8b4fe"
        else:
            color = "#6366f1"
            fill_color = "#a5b4fc"

        # Rich popup HTML
        popup_html = f"""
        <div style="font-family:Inter,sans-serif; min-width:220px; padding:4px;">
            <div style="font-size:14px; font-weight:700; color:#1e1b4b; margin-bottom:8px;
                        border-bottom:2px solid #6366f1; padding-bottom:6px;">
                🔴 Zone #{int(row['rank'])} — Cluster {row.name}
            </div>
            <table style="width:100%; font-size:12px; border-collapse:collapse;">
                <tr><td style="padding:3px 0; color:#64748b;">📍 Junction</td>
                    <td style="padding:3px 0; font-weight:600;">{row['primary_junction']}</td></tr>
                <tr><td style="padding:3px 0; color:#64748b;">🏛️ Station</td>
                    <td style="padding:3px 0; font-weight:600;">{row['police_station']}</td></tr>
                <tr><td style="padding:3px 0; color:#64748b;">⚠️ Violations</td>
                    <td style="padding:3px 0; font-weight:700; color:#dc2626;">{int(row['total_violations']):,}</td></tr>
                <tr><td style="padding:3px 0; color:#64748b;">🚗 Vehicle</td>
                    <td style="padding:3px 0; font-weight:600;">{row['top_vehicle']}</td></tr>
                <tr><td style="padding:3px 0; color:#64748b;">📋 Offence</td>
                    <td style="padding:3px 0; font-weight:600;">{row['top_violation'][:40]}</td></tr>
            </table>
        </div>
        """

        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=radius,
            color=color,
            fill=True,
            fill_color=fill_color,
            fill_opacity=0.5,
            weight=2,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"#{int(row['rank'])} · {row['primary_junction']} ({int(row['total_violations']):,} violations)"
        ).add_to(m)

    st_folium(m, width=None, height=520, key=f"map_{selected_shift}_{num_hotspots}")


# ── Data Panel ──────────────────────────────────────────────────────────────
with col_data:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
        <h3 style="margin:0;">📊 Resource Allocation Brief</h3>
    </div>
    """, unsafe_allow_html=True)

    # Prepare display table
    display_df = top_profiles[['rank', 'total_violations', 'primary_junction', 'police_station', 'top_violation', 'top_vehicle']].copy()
    display_df.columns = ['Rank', 'Violations', 'Junction', 'Police Station', 'Top Offence', 'Top Vehicle']
    display_df = display_df.reset_index(drop=True)

    st.dataframe(
        display_df,
        use_container_width=True,
        height=400,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("🏅", width="small"),
            "Violations": st.column_config.NumberColumn("⚠️ Count", format="%d"),
            "Junction": st.column_config.TextColumn("📍 Junction", width="medium"),
            "Police Station": st.column_config.TextColumn("🏛️ Station", width="medium"),
            "Top Offence": st.column_config.TextColumn("📋 Offence", width="medium"),
            "Top Vehicle": st.column_config.TextColumn("🚗 Vehicle", width="small"),
        }
    )

    # ── Top Vehicles mini-chart ──────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🚗 Top Vehicle Types in Current View")

    vehicle_data = df_filtered['vehicle_type'].value_counts().head(6).reset_index()
    vehicle_data.columns = ['Vehicle', 'Count']

    vehicle_chart = alt.Chart(vehicle_data).mark_bar(
        cornerRadiusTopRight=6,
        cornerRadiusBottomRight=6,
    ).encode(
        x=alt.X('Count:Q', axis=alt.Axis(grid=False, labelColor='#94a3b8', tickColor='#334155')),
        y=alt.Y('Vehicle:N', sort='-x', axis=alt.Axis(labelColor='#e2e8f0', tickColor='#334155')),
        color=alt.Color('Vehicle:N', scale=alt.Scale(
            range=['#6366f1', '#7c3aed', '#a855f7', '#c084fc', '#d8b4fe', '#e9d5ff']
        ), legend=None),
        tooltip=['Vehicle', 'Count']
    ).properties(
        height=220,
    ).configure_view(
        strokeWidth=0,
    ).configure_axis(
        domainColor='#334155',
    )

    st.altair_chart(vehicle_chart, use_container_width=True)


# ── Bottom Insights Row ─────────────────────────────────────────────────────
st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

ins_col1, ins_col2 = st.columns(2, gap="large")

with ins_col1:
    st.markdown("#### 🏛️ Top Police Stations by Violation Load")

    station_data = df_filtered['police_station'].value_counts().head(8).reset_index()
    station_data.columns = ['Station', 'Count']

    station_chart = alt.Chart(station_data).mark_bar(
        cornerRadiusTopRight=6,
        cornerRadiusBottomRight=6,
    ).encode(
        x=alt.X('Count:Q', axis=alt.Axis(grid=False, labelColor='#94a3b8', tickColor='#334155')),
        y=alt.Y('Station:N', sort='-x', axis=alt.Axis(labelColor='#e2e8f0', tickColor='#334155')),
        color=alt.Color('Station:N', scale=alt.Scale(
            range=['#ec4899', '#f43f5e', '#f97316', '#f59e0b', '#eab308', '#84cc16', '#22c55e', '#14b8a6']
        ), legend=None),
        tooltip=['Station', 'Count']
    ).properties(
        height=280,
    ).configure_view(
        strokeWidth=0,
    ).configure_axis(
        domainColor='#334155',
    )

    st.altair_chart(station_chart, use_container_width=True)


with ins_col2:
    st.markdown("#### ⏰ Violations by Hour of Day")

    hour_counts = df_filtered.groupby('hour').size().reindex(range(24), fill_value=0).reset_index()
    hour_counts.columns = ['Hour', 'Violations']

    # Assign shift labels for color coding
    def get_shift(h):
        if 8 <= h < 14:
            return 'Morning'
        elif 14 <= h < 20:
            return 'Afternoon'
        elif h >= 20 or h < 2:
            return 'Evening'
        else:
            return 'Night'

    hour_counts['Shift'] = hour_counts['Hour'].apply(get_shift)

    hourly_chart = alt.Chart(hour_counts).mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3,
    ).encode(
        x=alt.X('Hour:O', axis=alt.Axis(labelColor='#94a3b8', tickColor='#334155', labelAngle=0)),
        y=alt.Y('Violations:Q', axis=alt.Axis(grid=False, labelColor='#94a3b8', tickColor='#334155')),
        color=alt.Color('Shift:N', scale=alt.Scale(
            domain=['Morning', 'Afternoon', 'Evening', 'Night'],
            range=['#f59e0b', '#f97316', '#8b5cf6', '#3b82f6']
        ), legend=alt.Legend(orient='bottom', titleColor='#94a3b8', labelColor='#cbd5e1')),
        tooltip=['Hour', 'Violations', 'Shift']
    ).properties(
        height=280,
    ).configure_view(
        strokeWidth=0,
    ).configure_axis(
        domainColor='#334155',
    )

    st.altair_chart(hourly_chart, use_container_width=True)


# ── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:32px 0 16px 0; color:#475569; font-size:0.72rem; letter-spacing:0.5px;">
    GRIDLOCK · Bangalore Traffic Intelligence System · Built with Streamlit & Folium · Data: Jan–May Anonymised Police Records
</div>
""", unsafe_allow_html=True)