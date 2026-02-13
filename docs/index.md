# Welcome to OpenGeo

<p align="center">
  <img src="assets/logo.png" alt="OpenGeo Logo" width="200">
</p>

**OpenGeo** (`og`) is a Python package designed to provide a **Google Earth Engine (GEE)**-like experience using open-source geospatial tools such as **Xarray**, **Dask**, **STAC**, and **GeoPandas**. 

The goal is to smooth the transition for GEE users to the open Python ecosystem by mimicking the familiar Earth Engine API while leveraging the power of local or distributed cloud computing.

---

## 🚀 Key Features

*   **API Familiarity**: Mimics `ee.Image`, `ee.ImageCollection`, `ee.FeatureCollection`, and `ee.Geometry` APIs.
*   **Lazy Loading**: Uses `stackstac` and `dask` to lazily load and process imagery from STAC catalogs.
*   **Local Processing**: Run your analysis locally or on a standard Dask cluster without GEE quotas.
*   **Interoperability**: Seamlessly integrate with `xarray`, `geopandas`, and `shapely`.
*   **Open Access**: Focuses on community-maintained STAC APIs like Earth Search (Element84), Microsoft Planetary Computer, and more.

## 🛠️ Quick Start

```python
import opengeo as og

# Initialize (optional, sets default STAC API)
og.Initialize()

# Create a region of interest
roi = og.Geometry.Rectangle(77.58, 12.96, 77.60, 12.98)

# Load an ImageCollection from a STAC ID (e.g., Sentinel-2 L2A)
col = (og.ImageCollection("sentinel-2-l2a") 
       .filterDate("2023-01-01", "2023-01-31") 
       .filterBounds(roi) 
       .select(["red", "nir"]))

# Compute a composite (mean)
image = col.mean()

# Calculate NDVI
ndvi = (image.select("nir") - image.select("red")) / (image.select("nir") + image.select("red"))

# Reduce over the region
stats = ndvi.reduceRegion(reducer="mean", geometry=roi, scale=10)
print(stats)
```

## 📊 Comparisons

| GEE | OpenGeo | Underlying Tech |
|---|---|---|
| `ee.ImageCollection` | `og.ImageCollection` | `pystac_client` + `stackstac` |
| `ee.Image` | `og.Image` | `xarray.DataArray` |
| `ee.FeatureCollection` | `og.FeatureCollection` | `geopandas.GeoDataFrame` |
| `ee.Geometry` | `og.Geometry` | `shapely.geometry` |

---

## 📄 License

OpenGeo is released under the MIT License.
