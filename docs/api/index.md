# API Reference

The OpenGeo API is structured to mirror the Earth Engine Python API, making it familiar for GEE users transitioning to open-source tools.

## 🧩 Core Modules

OpenGeo provides the following core classes that correspond to Earth Engine's API:

| OpenGeo Class | Earth Engine Equivalent | Description |
|---------------|------------------------|-------------|
| [`og.Image`](image.md) | `ee.Image` | Operations on single multi-band raster images |
| [`og.ImageCollection`](image_collection.md) | `ee.ImageCollection` | Operations on groups of raster images |
| [`og.FeatureCollection`](feature_collection.md) | `ee.FeatureCollection` | Operations on vector datasets |
| [`og.Geometry`](geometry.md) | `ee.Geometry` | Defining spatial regions and geometries |
| [`og.Map`](map.md) | `geemap.Map` | Interactive visualization and mapping |

---

## 🚀 Quick Navigation

* **[Image](image.md)** - Work with single raster images, perform band math, and apply masks
* **[ImageCollection](image_collection.md)** - Filter, map, and reduce collections of satellite imagery
* **[FeatureCollection](feature_collection.md)** - Handle vector data with GeoPandas integration
* **[Geometry](geometry.md)** - Create points, polygons, and other geometric shapes
* **[Map](map.md)** - Visualize your data interactively with Leafmap

---

!!! info "Implementation Details"
    OpenGeo uses the following underlying technologies:

    - **Xarray** for n-dimensional array operations
    - **Dask** for lazy evaluation and parallel computing
    - **STAC** (SpatioTemporal Asset Catalog) for data discovery
    - **GeoPandas** for vector data handling
    - **Leafmap** for interactive visualization
