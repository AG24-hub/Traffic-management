# 🚨 Bangalore Traffic Hotspot Deployment Dashboard

A data-driven tool that helps traffic police **identify violation hotspots** across Bangalore and **optimise officer deployment** by shift window. It combines machine learning clustering on historical violation records with an interactive map dashboard built in Streamlit.

---

## 📌 Overview

Traffic violations are rarely random — they concentrate around specific junctions, at specific times, and involve specific vehicle types. This project mines that pattern from real anonymised police records (January–May) and surfaces the top 10 enforcement hotspots per shift so officers know exactly **where to go, when, and what to look for**.

**Pipeline at a glance:**

```
Raw police violation data
        ↓
DBSCAN spatial clustering  (traffic.ipynb)
        ↓
hotspot_Data.csv  (violations tagged with cluster IDs)
        ↓
Streamlit dashboard  (app.py)
        ↓
Interactive map + resource allocation table for police deployment
```

---

## 🗂️ Repository Structure

```
Traffic-management/
├── traffic.ipynb                          # Data analysis & clustering notebook
├── app.py                                 # Streamlit deployment dashboard
├── hotspot_Data.csv                       # Processed dataset with cluster labels (Git LFS)
├── jan to may police violation_anonymized791b166.csv   # Raw source data
└── requirements.txt                       # Python dependencies
```

---

## 🧠 How It Works

### 1. Clustering — `traffic.ipynb`

The notebook loads the raw anonymised violation records and applies **DBSCAN** (Density-Based Spatial Clustering of Applications with Noise) on the latitude/longitude coordinates of each incident.

- Violations that fall geographically close together get assigned a shared `hotspot_cluster` ID
- Isolated, low-density incidents are labelled `-1` (noise) and excluded from the dashboard
- The processed data, with cluster labels appended, is saved as `hotspot_Data.csv`

DBSCAN is a natural fit for this problem: it finds clusters of arbitrary shape, scales well to large datasets, and automatically discards sparse outliers — no need to specify the number of clusters upfront.

### 2. Dashboard — `app.py`

The Streamlit app gives police a real-time operational view:

**Shift filter (sidebar)**
Select one of four shift windows to focus on violations from that time of day:

| Shift | Hours |
|---|---|
| Morning | 08:00 – 14:00 |
| Afternoon | 14:00 – 20:00 |
| Evening | 20:00 – 02:00 |
| Nighttime | 02:00 – 08:00 |

**Interactive map (left panel)**
A Folium map centred on Bangalore shows red markers for the top 10 hotspot clusters in the selected shift. Clicking a marker reveals:
- Zone ID and primary junction name
- Total violation count
- Most common vehicle type targeted
- Most common offence type

**Resource allocation table (right panel)**
A sortable data table listing the same top 10 clusters, ranked by violation count — ready to use as a deployment brief.

---

## 📊 Data

| File | Description |
|---|---|
| `jan to may police violation_anonymized791b166.csv` | Raw police violation records, Jan–May. Anonymised. Columns include datetime, location (lat/lon), junction name, vehicle type, violation type. |
| `hotspot_Data.csv` | Same records after clustering. Adds `hotspot_cluster` (integer cluster ID, or `-1` for noise) and `hour` (extracted from datetime). 33.9 MB — stored via Git LFS. |

---

## ⚙️ Setup & Running

### Prerequisites

- Python 3.9+
- Git LFS (to pull the large CSV)

```bash
git lfs install
git clone https://github.com/AG24-hub/Traffic-management.git
cd Traffic-management
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the dashboard

```bash
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

### Re-run the analysis notebook (optional)

Open `traffic.ipynb` in Jupyter and run all cells to regenerate `hotspot_Data.csv` from the raw violation data.

```bash
jupyter notebook traffic.ipynb
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `streamlit` | 1.32.0 | Web dashboard framework |
| `pandas` | 2.2.1 | Data loading and aggregation |
| `numpy` | 1.26.4 | Numerical operations |
| `folium` | 0.16.0 | Interactive map rendering |
| `streamlit-folium` | 0.18.0 | Folium integration for Streamlit |
| `scikit-learn` | — | DBSCAN clustering (notebook) |

---

## 🗺️ Dashboard Preview

The map is centred on Bangalore (12.97°N, 77.59°E) and updates dynamically based on the shift window selected. Each hotspot marker popup provides a self-contained deployment brief — junction, offence type, and primary vehicle — so officers need no additional reference material.

---

## 📝 Notes

- All violation records are **anonymised** — no personally identifiable information is present in either CSV
- The `-1` cluster label (DBSCAN noise points) is filtered out before display; only confirmed spatial clusters appear on the map
- Cluster centroids are computed as the **mean latitude/longitude** of all violations in the cluster; the primary junction, vehicle type, and offence are determined by **mode** (most frequent value)
- The dashboard currently supports a single city (Bangalore). To adapt it for another city, update the `folium.Map` centre coordinates in `app.py`

---

## 🤝 Contributing

Pull requests are welcome. For significant changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project does not currently specify a license. Please contact the repository owner before reuse or redistribution.
