import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="JalMap Kolkata", layout="wide")
st.title("🌊 JalMap Kolkata - Live")

# --- 1. Jayga gulo ---
areas = {
    "Park Street": [22.5552, 88.3509],
    "Behala": [22.5025, 88.3142],
    "AJC Bose Road": [22.5435, 88.3650],
    "Ultadanga": [22.5925, 88.3860],
    "Howrah Bridge": [22.5851, 88.3468],
    "Salt Lake Sector V": [22.5726, 88.3639],
}

# --- 2. Memory: Report gulo mone rakhar jonno ---
if 'reports' not in st.session_state:
    # Surute sob clear, karon ekhon sotti te jol nei
    st.session_state.reports = {name: "Clear ✅" for name in areas}
    st.session_state.custom_clear = []

# --- 3. Bam dike: Report Korun ---
st.sidebar.header("📢 Has it become waterlogged? Report it")
area = st.sidebar.selectbox("Select Area", list(areas.keys()))
status = st.sidebar.radio("Current situation?", ["Waterlogged 🔴", "Clear Road 🟢", "Knee-deep water 🟠"])
rain = st.sidebar.slider("Current Rain Update? (mm/hr)", 0, 100, 0)
custom_road = st.sidebar.text_input("If you know of any other clear path, write it down (e.g. EM Bypass)")

if st.sidebar.button("Submit report"):
    st.session_state.reports[area] = status
    if custom_road:
        st.session_state.custom_clear.append(custom_road)
    st.sidebar.success(f"Thanks! Report of {area} has been saved.")

# --- 4. Map ---
m = folium.Map(location=[22.57, 88.36], zoom_start=12)
for name, latlon in areas.items():
    rep = st.session_state.reports[name]
    if "Clear" in rep:
        color = "green"
    elif "Knee" in rep:
        color = "orange"
    else:
        color = "red"
    folium.Marker(latlon, popup=f"{name}: {rep}", icon=folium.Icon(color=color)).add_to(m)

col1, col2 = st.columns([2, 1])
with col1:
    st_folium(m, width=700, height=450)
    st.caption("Green Dot = Road Clear, Red Dot = Waterlogged")

# --- 5. Smart Safe Route - Ekhon ar AJC Bose fixed na ---
with col2:
    st.subheader("🗺️ Safe Route Suggestion")
    
    # Konta clear, konta block - seta ber kora
    clear_roads = [k for k, v in st.session_state.reports.items() if "Clear" in v]
    blocked_roads = [k for k, v in st.session_state.reports.items() if "Clear" not in v]
    # User er deoa custom clear rasta jog kora
    clear_roads = clear_roads + st.session_state.custom_clear

    if "Clear" in st.session_state.reports[area]:
        st.success(f"✅ {area}: The road is clear now. You can follow this road!")
    else:
        st.error(f"❌ {area}: Don't follow this road - Here {st.session_state.reports[area]}")
        if clear_roads:
            st.info(f"✅ Now you can follow this road: **{', '.join(clear_roads)}** - Users are saying that the road is clear.")
        else:
            st.warning("⚠️ No clear road has been reported yet. Wait a moment.")

    st.write("---")
    st.write("**Live Update:**")
    for k, v in st.session_state.reports.items():
        st.write(f"{k}: {v}")
