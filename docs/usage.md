# Usage Guide

OpenGeo is designed to feel natural to those familiar with Google Earth Engine (`ee`).

## Initialization

By default, OpenGeo uses the Earth Search STAC API. You can initialize it with a custom STAC API URL if needed.

```python
import opengeo as og

# Default initialization
og.Initialize()

# Custom STAC API initialization
# og.Initialize(url="https://planetarycomputer.microsoft.com/api/stac/v1")
```

## Working with ImageCollections

`og.ImageCollection` is the primary container for satellite imagery.

```python
# Create a collection
col = og.ImageCollection("sentinel-2-l2a")

# Filter by date and bounds
col = col.filterDate("2023-01-01", "2023-06-01").filterBounds(roi)

# Select specific bands
col = col.select(["red", "green", "blue", "nir"])
```

## Image Math

You can perform arithmetic operations directly on `og.Image` objects.

```python
image = col.median()
ndvi = (image.select("nir") - image.select("red")) / (image.select("nir") + image.select("red"))
```

## Visualization

OpenGeo integrates with `leafmap` for interactive mapping.

```python
m = og.Map()
m.addLayer(image, {"bands": ["red", "green", "blue"], "min": 0, "max": 3000}, "RGB")
m.centerObject(roi, zoom=12)
m
```

## Reducers

Compute statistics over regions using reducers.

```python
stats = ndvi.reduceRegion(
    reducer="mean",
    geometry=roi,
    scale=10
)
```
