
# -*- coding: utf-8 -*-
import streamlit as st
import folium
from streamlit_folium import st_folium
import os
import pandas as pd
import matplotlib.pyplot as plt

# Title and Description
st.title("Xingu National Park Land Cover Analysis")
st.write("""
This app visualizes land cover classification, deforestation trends, 
and class change dynamics in Xingu National Park over the years.
""")

# Sidebar Navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio(
    "Choose a section:",
    ["Overview", "Classified Maps", "Class Change Maps", "Trends and Conclusions"]
)

# Define folders for GeoTIFF files and CSV data
tiff_folder = "data/"
csv_folder = os.path.join(tiff_folder, "csv/")

# Helper function to list GeoTIFF files in a folder
def list_files(folder, extension=".tif"):
    return [f for f in os.listdir(folder) if f.endswith(extension)]

# Helper function to create a Folium map with raster overlay
def create_map(raster_path, bounds, layer_name):
    m = folium.Map(location=[-11.8, -53.5], zoom_start=7)
    folium.raster_layers.ImageOverlay(
        name=layer_name,
        image=raster_path,
        bounds=bounds,
        opacity=0.6,
    ).add_to(m)
    folium.LayerControl().add_to(m)
    return m

# Section: Overview
if options == "Overview":
    st.subheader("Overview")
    st.write("""
    This app allows you to:
    - Explore **classified maps** of land cover over multiple years.
    - Understand **class change dynamics**, such as deforestation and reforestation.
    - Visualize and download **CSV data** with trends and percentages.
    """)

# Section: Classified Maps
if options == "Classified Maps":
    st.subheader("Classified Maps")
    st.write("Explore classified maps of land cover.")

    classified_folder = os.path.join(tiff_folder, "classified/")
    classified_files = list_files(classified_folder)

    selected_file = st.selectbox("Select Classified Map:", classified_files)

    if selected_file:
        file_path = os.path.join(classified_folder, selected_file)
        bounds = [[-13.0, -54.2], [-10.6, -52.5]]  # Adjust bounds to Xingu region
        folium_map = create_map(file_path, bounds, f"Classified Map: {selected_file}")
        st_folium(folium_map, width=700, height=500)

# Section: Class Change Maps
if options == "Class Change Maps":
    st.subheader("Class Change Maps")
    st.write("Analyze changes between classes (e.g., forest to agriculture, reforestation).")

    class_change_folder = os.path.join(tiff_folder, "class_change/")
    class_change_files = list_files(class_change_folder)

    selected_file = st.selectbox("Select Class Change Map:", class_change_files)

    if selected_file:
        file_path = os.path.join(class_change_folder, selected_file)
        bounds = [[-13.0, -54.2], [-10.6, -52.5]]  # Adjust bounds to Xingu region
        folium_map = create_map(file_path, bounds, f"Class Change Map: {selected_file}")
        st_folium(folium_map, width=700, height=500)

# Section: Trends and Conclusions
if options == "Trends and Conclusions":
    st.subheader("Trends and Conclusions")
    st.write("""
    This section provides statistical trends and key conclusions from the analysis.
    """)

    # Load CSV data
    class_evolution_file = os.path.join(csv_folder, "class_evolution_with_percentage.csv")
    deforestation_trends_file = os.path.join(csv_folder, "deforestation_trends.csv")

    if os.path.exists(class_evolution_file):
        class_evolution = pd.read_csv(class_evolution_file)

        st.write("### Class Evolution Data")
        st.dataframe(class_evolution)

        # Plot class areas
        st.write("### Land Cover Class Areas Over Time")
        fig, ax = plt.subplots(figsize=(10, 6))
        for cls in class_evolution["Class"].unique():
            data = class_evolution[class_evolution["Class"] == cls]
            ax.plot(data["Year"], data["Area (km²)"], marker='o', label=cls)
        ax.set_title("Land Cover Class Areas Over Time")
        ax.set_xlabel("Year")
        ax.set_ylabel("Area (km²)")
        ax.legend(title="Classes")
        st.pyplot(fig)

        # Plot percentages
        st.write("### Percentage Change Over Time")
        fig, ax = plt.subplots(figsize=(10, 6))
        for cls in class_evolution["Class"].unique():
            data = class_evolution[class_evolution["Class"] == cls]
            ax.plot(data["Year"], data["Percentage (%)"], marker='o', label=cls)
        ax.set_title("Land Cover Class Percentages Over Time")
        ax.set_xlabel("Year")
        ax.set_ylabel("Percentage (%)")
        ax.legend(title="Classes")
        st.pyplot(fig)

    if os.path.exists(deforestation_trends_file):
        deforestation_trends = pd.read_csv(deforestation_trends_file)

        st.write("### Deforestation Trends")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(deforestation_trends["Period"], deforestation_trends["Deforested Area (km²)"], color="red")
        ax.set_title("Deforested Area Per Period")
        ax.set_xlabel("Period")
        ax.set_ylabel("Deforested Area (km²)")
        ax.set_xticklabels(deforestation_trends["Period"], rotation=45)
        st.pyplot(fig)

        st.download_button(
            label="Download Deforestation Trends Data",
            data=deforestation_trends.to_csv(index=False),
            file_name="deforestation_trends.csv",
            mime="text/csv"
        )
