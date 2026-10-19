"""Convert georeferenced RGB exports into browser-compatible overlays."""
import numpy as np
import rasterio
from rasterio.enums import Resampling, ColorInterp
from rasterio.vrt import WarpedVRT
from rasterio.warp import transform_bounds


def raster_overlay(path, max_size=1400):
    """Return bounded RGBA pixels in Web Mercator and Leaflet bounds."""
    if max_size < 1:
        raise ValueError("max_size must be positive")
    with rasterio.open(path) as source:
        if source.crs is None:
            raise ValueError("Raster has no coordinate reference system")
        if source.count < 3:
            raise ValueError("Expected an RGB GeoTIFF exported with visualize()")
        with WarpedVRT(source, crs="EPSG:3857", resampling=Resampling.nearest,
                       add_alpha=ColorInterp.alpha not in source.colorinterp) as raster:
            scale = min(1.0, max_size / max(raster.width, raster.height))
            width = max(1, round(raster.width * scale))
            height = max(1, round(raster.height * scale))
            rgb = raster.read([1, 2, 3], out_shape=(3, height, width),
                              resampling=Resampling.nearest)
            alpha = raster.dataset_mask(out_shape=(height, width),
                                        resampling=Resampling.nearest)
            west, south, east, north = transform_bounds(
                raster.crs, "EPSG:4326", *raster.bounds)
    rgba = np.dstack((np.moveaxis(rgb, 0, -1), alpha)).astype(np.uint8)
    return rgba, [[south, west], [north, east]]
