
# -*- coding: utf-8 -*-
import streamlit as st
import folium
from streamlit_folium import st_folium
import os
import pandas as pd
import matplotlib.pyplot as plt

# Title and Description
st.set_page_config(
    page_title="Xingu National Park Analysis",
    page_icon="🌳",
    layout="wide"
)

st.title("Xingu National Park Land Cover Analysis 🌳")
st.write("""
This app visualizes land cover classification and class change dynamics in Xingu National Park over the years.
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

# Function to display a legend as a Streamlit component
def display_legend(legend_dict, title):
    st.markdown(f"### {title}")
    for label, color in legend_dict.items():
        r, g, b = color
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
                <div style="width: 20px; height: 20px; background-color: rgb({r}, {g}, {b}); margin-right: 10px; border: 1px solid black;"></div>
                <span>{label}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Section: Overview
if options == "Overview":
    st.subheader("Overview 🌍")
    st.markdown("""
    Welcome to the **Xingu National Park Land Cover Analysis** app!
    
    **Features of this application:**
    - 🌳 Explore **Classified Maps** of land cover over multiple years.
    - 🔄 Analyze **Class Change Maps**, such as deforestation and reforestation.
    - 📊 View **Trends and Conclusions** with data visualizations and downloadable CSVs.
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
        bounds = [[-13.0298, -54.0623], [-10.5564, -52.4912]]  # Exact bounds for Xingu

        classified_legend = {
            "Forest": (0, 255, 0),
            "Water": (0, 0, 255),
            "Agriculture": (255, 255, 0),
            "Exposed Soil": (255, 0, 0)
        }

        folium_map = create_map(file_path, bounds, f"Classified Map: {selected_file}")
        st_folium(folium_map, width=700, height=500)

        # Display legend below the map
        display_legend(classified_legend, "Land Cover Classes")

# Section: Class Change Maps
if options == "Class Change Maps":
    st.subheader("Class Change Maps")
    st.write("Analyze changes between classes (e.g., forest to agriculture, reforestation).")

    class_change_folder = os.path.join(tiff_folder, "class_change/")
    class_change_files = list_files(class_change_folder)

    selected_file = st.selectbox("Select Class Change Map:", class_change_files)

    if selected_file:
        file_path = os.path.join(class_change_folder, selected_file)
        bounds = [[-13.0298, -54.0623], [-10.5564, -52.4912]]  # Exact bounds for Xingu

        change_class_legend = {
            "Forest → Forest (Maintenance)": (0, 255, 0),  # Green
            "Forest → Agriculture (Deforestation)": (255, 165, 0),  # Orange
            "Forest → Exposed Soil (Deforestation)": (255, 0, 0),  # Red
            "Exposed Soil → Forest (Reforestation)": (0, 0, 255),  # Blue
            "Agriculture → Forest (Reforestation)": (255, 255, 0)  # Yellow
        }

        folium_map = create_map(file_path, bounds, f"Class Change Map: {selected_file}")
        st_folium(folium_map, width=700, height=500)

        # Display legend below the map
        display_legend(change_class_legend, "Class Change Dynamics")

# Section: Trends and Conclusions
if options == "Trends and Conclusions":
    st.subheader("Trends and Conclusions 📊")
    st.write("""
    This section provides statistical trends and key conclusions from the analysis.
    """)

    # Load CSV data
    class_evolution_file = os.path.join(csv_folder, "class_evolution_with_percentage.csv")
    transition_areas_file = os.path.join(csv_folder, "transition_areas.csv")

    if os.path.exists(class_evolution_file):
        class_evolution = pd.read_csv(class_evolution_file)

        st.write("### Class Evolution Data")
        st.dataframe(class_evolution)

        # Define consistent colors
        color_dict = {
            "Forest": "green",
            "Water": "blue",
            "Agriculture": "yellow",
            "Exposed Soil": "red"
        }

        # Plot class areas
        st.write("### Land Cover Class Areas Over Time")
        fig, ax = plt.subplots(figsize=(10, 6))
        for cls in class_evolution["Class"].unique():
            data = class_evolution[class_evolution["Class"] == cls]
            ax.plot(data["Year"], data["Area (km²)"], marker='o', label=cls, color=color_dict.get(cls, "black"))
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
            ax.plot(data["Year"], data["Percentage (%)"], marker='o', label=cls, color=color_dict.get(cls, "black"))
        ax.set_title("Land Cover Class Percentages Over Time")
        ax.set_xlabel("Year")
        ax.set_ylabel("Percentage (%)")
        ax.legend(title="Classes")
        st.pyplot(fig)

    if os.path.exists(transition_areas_file):
        transition_areas = pd.read_csv(transition_areas_file)

        # Remove rows with "Unknown Transition"
        transition_areas = transition_areas[~transition_areas["Transition"].str.contains("Unknown Transition", na=False)]

        # Exibir a tabela de áreas de transição
        st.write("### Transition Areas Data")
        st.dataframe(transition_areas)

        st.write("### Transition Areas by Period")
        periods = transition_areas["Period"].unique()

        # Definir as cores correspondentes às transições
        color_dict = {
            "Forest → Forest (Maintenance)": "green",
            "Forest → Agriculture (Deforestation)": "orange",
            "Forest → Exposed Soil (Deforestation)": "red",
            "Exposed Soil → Forest (Reforestation)": "blue",
            "Agriculture → Forest (Reforestation)": "yellow"
        }

        for period in periods:
            data = transition_areas[transition_areas["Period"] == period]

            # Calcular soma de Deforestation e Reforestation
            deforestation_transitions = ["Forest → Agriculture (Deforestation)", "Forest → Exposed Soil (Deforestation)"]
            reforestation_transitions = ["Exposed Soil → Forest (Reforestation)", "Agriculture → Forest (Reforestation)"]

            total_deforestation = data[data["Transition"].isin(deforestation_transitions)]["Area (km²)"].sum()
            total_reforestation = data[data["Transition"].isin(reforestation_transitions)]["Area (km²)"].sum()

            st.write(f"#### Summary for {period}")
            st.write(f"**Total Deforestation:** {total_deforestation:.2f} km²")
            st.write(f"**Total Reforestation:** {total_reforestation:.2f} km²")

            # Gráfico de barras para o período atual
            labels = data["Transition"]
            sizes = data["Area (km²)"]

            fig, ax = plt.subplots(figsize=(8, 5))
            bars = ax.bar(labels, sizes, color=[color_dict.get(label, "gray") for label in labels])
            ax.set_title(f"Transitions in {period}")
            ax.set_xlabel("Transitions")
            ax.set_ylabel("Area (km²)")
            ax.set_xticks(range(len(labels)))
            ax.set_xticklabels(labels, rotation=45, ha="right")

            # Adicionar os valores no topo das barras
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2.0, height, f"{height:.1f}", ha="center", va="bottom")

            st.pyplot(fig)
