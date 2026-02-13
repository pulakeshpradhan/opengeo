# OpenGeo (`og`)

OpenGeo is a Python package designed to provide a Google Earth Engine-like experience using open-source geospatial tools such as Xarray, Dask, STAC, and GeoPandas. The goal is to smooth the transition for GEE users to the open Python ecosystem.

## Features

- **API Familiarity**: Mimics `ee.Image`, `ee.ImageCollection`, `ee.FeatureCollection` and `ee.Geometry` APIs.
- **Lazy Loading**: Uses `stackstac` and `dask` to lazily load and process imagery from STAC catalogs.
- **Local Processing**: Run your analysis locally or on a standard Dask cluster without GEE quotas.
- **Interoperability**: Seamlessly integrate with `xarray`, `geopandas`, and `shapely`.

## Installation

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install the package in editable mode:
   ```bash
   pip install -e .
   ```

## Usage

```python
import opengeo as og

# Initialize (optional, sets default STAC API)
og.Initialize()

# Create a region of interest
roi = og.Geometry.Rectangle(77.58, 12.96, 77.60, 12.98)

# Load an ImageCollection from a STAC ID (e.g., Sentinel-2 L2A)
col = og.ImageCollection("sentinel-2-l2a") \
    .filterDate("2023-01-01", "2023-01-31") \
    .filterBounds(roi) \
    .select(["red", "nir"])

# Compute a composite (mean)
image = col.mean()

# Calculate NDVI
ndvi = (image.select("nir") - image.select("red")) / (image.select("nir") + image.select("red"))

# Reduce over the region
stats = ndvi.reduceRegion(reducer="mean", geometry=roi, scale=10)
print(stats)
```

## Comparisons

| GEE | OpenGeo | Underlying Tech |
|---|---|---|
| `ee.ImageCollection` | `og.ImageCollection` | `pystac_client` + `stackstac` |
| `ee.Image` | `og.Image` | `xarray.DataArray` |
| `ee.FeatureCollection` | `og.FeatureCollection` | `geopandas.GeoDataFrame` |
| `ee.Geometry` | `og.Geometry` | `shapely.geometry` |

## Backend

OpenGeo defaults to using the [Earth Search](https://earth-search.aws.element84.com/v1) STAC API. You can change this via `og.Initialize(url="...")`.

## License

MIT
