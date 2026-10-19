# Deforestation Analysis

Explore land-cover classification, transition maps, and trends for the study region around Xingu, 2014–2024.

## Run the dashboard

Use Python 3.11 or newer:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

On Windows, activate with `.venv\Scripts\activate`. Data paths are resolved relative to `app.py`, so launching from a different working directory is supported.

The dashboard uses the committed files in `data/`; it does not require Earth Engine authentication. GeoTIFFs are read with Rasterio, reprojected to Web Mercator, resized with nearest-neighbor sampling to preserve class colors, and embedded as PNG overlays. Geographic bounds come from each raster. Display resolution is capped at 1400 pixels per side; the original rasters and CSV statistics are unchanged.

## Regenerate categorical transition maps

The original `Change_Map_*.tif` exports use a continuous color scale over sparse transition codes. Their colors cannot reliably identify the categories in the old legend. The dashboard labels these as legacy maps and suppresses that legend.

To generate corrected maps:

1. Open `Deforestation_Analysis.ipynb` in a notebook environment with Earth Engine access.
2. Authenticate and replace the Earth Engine project ID with a project you can access.
3. Run the classification and change-map cells, followed by the updated categorical visualization and export cells. This starts exports to the `EarthEngineImages` folder in Google Drive; wait for the tasks to finish.
4. Download `Categorical_Change_Map_*.tif` into `data/class_change/` and restart the dashboard.

The updated notebook explicitly maps codes `0, 2, 3, 30, 20` to green, orange, red, blue, and yellow. Other transitions are masked. The app prefers corrected files when available and displays their categorical legend. If only some corrected periods have been downloaded, only those periods are offered; download all ten exports for full coverage.

Existing RGB exports cannot safely be repaired by relabeling colors: distinct transitions may already share a color. Regeneration therefore requires the original Earth Engine classification. The source region is a rectangular study area, not an official park-boundary polygon; this patch does not revise the scientific methodology or recompute statistics.

## Tests

```bash
pip install pytest
python -m pytest -q
```

Tests check PNG conversion of all committed rasters, transparency and class-color preservation, and all dashboard sections when launched from a different directory.
