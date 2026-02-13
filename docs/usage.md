# Usage Guide

OpenGeo is designed to feel natural to those familiar with Google Earth Engine (`ee`). This guide covers the core concepts and common workflows.

---

## 🚀 Initialization

By default, OpenGeo uses the Earth Search STAC API. You can initialize it with a custom STAC API URL if needed.

```python
import opengeo as og

# Default initialization (Earth Search)
og.Initialize()

# Custom STAC API initialization
# og.Initialize(url="https://planetarycomputer.microsoft.com/api/stac/v1")
```

!!! tip "Available STAC APIs"
    OpenGeo supports multiple STAC catalogs:

    - **Earth Search** (Element84) - Default
    - **Microsoft Planetary Computer**
    - **USGS STAC**
    - **NASA CMR STAC**
    - Any custom STAC API endpoint

---

## 🗺️ Creating Geometries

Define regions of interest using the `Geometry` class:

```python
# Rectangle (bounding box)
roi = og.Geometry.Rectangle(xmin=77.58, ymin=12.96, xmax=77.60, ymax=12.98)

# Point
point = og.Geometry.Point(longitude=77.59, latitude=12.97)

# Polygon from coordinates
polygon = og.Geometry.Polygon([
    [77.58, 12.96],
    [77.60, 12.96],
    [77.60, 12.98],
    [77.58, 12.98],
    [77.58, 12.96]
])
```

---

## 📡 Working with ImageCollections

`og.ImageCollection` is the primary container for satellite imagery.

### Loading a Collection

```python
# Create a collection from STAC ID
col = og.ImageCollection("sentinel-2-l2a")
```

### Filtering

```python
# Filter by date range
col = col.filterDate("2023-01-01", "2023-06-01")

# Filter by spatial bounds
col = col.filterBounds(roi)

# Filter by metadata (cloud cover)
col = col.filter("eo:cloud_cover < 20")

# Chain filters
col = (og.ImageCollection("sentinel-2-l2a")
       .filterDate("2023-01-01", "2023-06-01")
       .filterBounds(roi)
       .filter("eo:cloud_cover < 20"))
```

### Selecting Bands

```python
# Select specific bands
col = col.select(["red", "green", "blue", "nir"])

# Select and rename
col = col.select(["B04", "B08"], ["red", "nir"])
```

---

## 🖼️ Working with Images

### Compositing

```python
# Create composites from collections
mean_image = col.mean()
median_image = col.median()
max_image = col.max()
min_image = col.min()
```

### Band Math

Perform arithmetic operations directly on `og.Image` objects:

```python
# Calculate NDVI
image = col.median()
ndvi = (image.select("nir") - image.select("red")) / \
       (image.select("nir") + image.select("red"))

# Calculate EVI (Enhanced Vegetation Index)
evi = 2.5 * ((image.select("nir") - image.select("red")) / 
             (image.select("nir") + 6 * image.select("red") - 
              7.5 * image.select("blue") + 1))
```

### Masking

```python
# Create a mask
mask = ndvi.gt(0.3)  # NDVI > 0.3

# Apply mask
masked_image = image.updateMask(mask)
```

---

## 🗺️ Visualization

OpenGeo integrates with `leafmap` for interactive mapping.

```python
# Create a map
m = og.Map(center=[12.97, 77.59], zoom=12)

# Add an RGB layer
m.addLayer(
    image, 
    {"bands": ["red", "green", "blue"], "min": 0, "max": 3000}, 
    "RGB Composite"
)

# Add NDVI layer with custom colormap
m.addLayer(
    ndvi,
    {"min": -1, "max": 1, "palette": ["red", "yellow", "green"]},
    "NDVI"
)

# Center on geometry
m.centerObject(roi, zoom=12)

# Display map (in Jupyter)
m
```

---

## 📊 Reducers

Compute statistics over regions using reducers.

```python
# Reduce over a region
stats = ndvi.reduceRegion(
    reducer="mean",
    geometry=roi,
    scale=10  # meters per pixel
)
print(f"Mean NDVI: {stats}")

# Multiple reducers
stats = ndvi.reduceRegion(
    reducer=["mean", "median", "stdDev", "min", "max"],
    geometry=roi,
    scale=10
)
```

---

## 🔄 Common Workflows

### Workflow 1: Time Series Analysis

```python
# Load collection
col = (og.ImageCollection("sentinel-2-l2a")
       .filterDate("2023-01-01", "2023-12-31")
       .filterBounds(roi)
       .select(["red", "nir"]))

# Calculate NDVI for each image
def calculate_ndvi(image):
    ndvi = (image.select("nir") - image.select("red")) / \
           (image.select("nir") + image.select("red"))
    return ndvi.rename("ndvi")

ndvi_collection = col.map(calculate_ndvi)

# Extract time series
time_series = ndvi_collection.getTimeSeries(geometry=roi, reducer="mean")
```

### Workflow 2: Multi-Sensor Fusion

```python
# Load Sentinel-2
s2 = (og.ImageCollection("sentinel-2-l2a")
      .filterDate("2023-06-01", "2023-06-30")
      .filterBounds(roi)
      .median())

# Load Landsat 8
l8 = (og.ImageCollection("landsat-c2-l2")
      .filterDate("2023-06-01", "2023-06-30")
      .filterBounds(roi)
      .median())

# Combine datasets
combined = s2.addBands(l8)
```

---

## 💡 Best Practices

!!! success "Performance Tips"

    1. **Filter early**: Apply spatial and temporal filters before processing
    2. **Select only needed bands**: Reduce data transfer and memory usage
    3. **Use lazy evaluation**: Dask only computes when you call `.compute()`
    4. **Chunk appropriately**: Balance chunk size for your workflow
    
    ```python
    # Good: Filter then select
    col = (og.ImageCollection("sentinel-2-l2a")
           .filterDate("2023-01-01", "2023-01-31")
           .filterBounds(roi)
           .select(["red", "nir"]))
    
    # Bad: Load everything first
    col = og.ImageCollection("sentinel-2-l2a").select(["red", "nir"])
    ```

!!! info "GEE vs OpenGeo"

    | Operation | Google Earth Engine | OpenGeo |
    |-----------|-------------------|---------|
    | Initialize | `ee.Initialize()` | `og.Initialize()` |
    | Image Collection | `ee.ImageCollection()` | `og.ImageCollection()` |
    | Filter Date | `.filterDate()` | `.filterDate()` |
    | Filter Bounds | `.filterBounds()` | `.filterBounds()` |
    | Reduce | `.reduce()` | `.mean()`, `.median()`, etc. |
    | Map Function | `.map()` | `.map()` |
