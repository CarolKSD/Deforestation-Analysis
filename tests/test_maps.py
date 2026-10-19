from pathlib import Path
import os
import folium
import numpy as np
import rasterio
from rasterio.transform import from_origin
from streamlit.testing.v1 import AppTest
from raster_maps import raster_overlay

ROOT = Path(__file__).resolve().parents[1]

def test_real_rasters_generate_png():
    paths = sorted((ROOT / 'data').glob('*/*.tif'))
    assert len(paths) >= 21
    for path in paths:
        rgba, bounds = raster_overlay(path, max_size=256)
        assert max(rgba.shape[:2]) <= 256
        assert rgba.shape[2] == 4
        assert bounds[0][0] < bounds[1][0]
        assert bounds[0][1] < bounds[1][1]
        assert folium.raster_layers.ImageOverlay(rgba, bounds).url.startswith('data:image/png;base64,')

def test_nodata_transparency_and_colors(tmp_path):
    path = tmp_path / 'rgb.tif'
    rgb = np.zeros((3, 10, 10), dtype='uint8')
    rgb[1, 2:8, 2:8] = 255
    with rasterio.open(path, 'w', driver='GTiff', height=10, width=10,
                       count=3, dtype='uint8', crs='EPSG:4326',
                       transform=from_origin(-54, -10, 0.01, 0.01)) as ds:
        ds.write(rgb)
        ds.write_mask(np.where(rgb[1] == 255, 255, 0).astype('uint8'))
    rgba, _ = raster_overlay(path)
    assert rgba[0, 0, 3] == 0
    assert (rgba[5, 5] == [0, 255, 0, 255]).all()

def test_app_all_sections_from_another_directory(tmp_path):
    previous = Path.cwd()
    os.chdir(tmp_path)
    try:
        app = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=60).run()
        assert not app.exception
        for section in ['Classified Maps', 'Class Change Maps', 'Trends and Conclusions']:
            app.sidebar.radio[0].set_value(section).run()
            assert not app.exception, app.exception
            if section == 'Class Change Maps':
                assert any('Legacy map' in w.value for w in app.warning)
    finally:
        os.chdir(previous)
