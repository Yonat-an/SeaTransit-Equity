import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
equity_df = gpd.read_file("equity_index.geojson")
corridors_df = gpd.read_file("transit_corridors.geojson")
seattle_joined = gpd.sjoin(corridors_df, equity_df, how="inner", predicate="intersects")
seattle_joined["TES"] = seattle_joined["POP_ADULT_CIVILIAN_NONINST"] * seattle_joined["COMPOSITE_SCORE"]
seattle_joined["TES"] = (seattle_joined["TES"] / seattle_joined["TES"].max()) * 100
population = seattle_joined["POP_ADULT_CIVILIAN_NONINST"].max()
half = population/2
st.set_page_config(layout="wide")
def get_color(score):
    if score >= 75:
        return "#d73027"
    elif score >= 50:
        return "#f46d43"
    elif score >= 25:
        return "#fdae61"
    else:
        return "#1a9850"

with st.sidebar:
    st.header("Control Panel")
    score_cutOff = st.slider("Select the equity range",0,100,0)
    pop_cutOff = st.slider("Filter by population size",0,population, 2000, 10)
filtered_display_df = seattle_joined[(seattle_joined["TES"] >= score_cutOff) &
                                     (seattle_joined["POP_ADULT_CIVILIAN_NONINST"] >= pop_cutOff)]
seaMap = folium.Map(location=[47.606, -122.332], zoom_start=11)
folium.GeoJson(filtered_display_df,
               style_function=lambda feature:{
                   "color": get_color(feature["properties"]["TES"]),
                   "weight":4,
                   "opacity":0.8
               }).add_to(seaMap)
col1, col2 = st.columns([3, 5])

with col1:
    st.subheader("Description")
    st.write("My project uses Seattle's open data program,"
             " specifically the 'Racial and Social Equity Composite Index Current,"
             " and the 'Transit Capital Corridors', in order to make a transit equity score (TES).")
    st.write(" The TES is out of 100, the bus corridors with a high TES (red), are a critical priority zone where targeted infrastructure investment is required."
             " The green highlighted (low TES) bus corridors are areas of low socioeconomic vulnerability."
             " Such high income citizens dont face any consequences for late arrivals to work.")
    st.write(" However low income citizens can possibly face termination, missed promotions and reduced hours."
             " The population slider in the control panel can be used to filter in terms of how much the bus corridors are used."
             " By setting the slider to 0 the map shows every bus corridor.")
    st.write("**Note that the website may take time to load, after changing options on the control panel.*")


with col2:
    maps = st_folium(seaMap, use_container_width=True, height=800)