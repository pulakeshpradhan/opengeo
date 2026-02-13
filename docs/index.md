# Welcome to OpenGeo

<p align="center">
  <img src="assets/logo.png" alt="OpenGeo Logo" width="200">
</p>

<p align="center">
  <strong>A Google Earth Engine-like Python package using open-source geospatial tools</strong>
</p>

<p align="center">
  <a href="https://github.com/pulakeshpradhan/opengeo"><img src="https://img.shields.io/github/stars/pulakeshpradhan/opengeo?style=social" alt="GitHub stars"></a>
  <a href="https://github.com/pulakeshpradhan/opengeo/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License"></a>
  <a href="https://github.com/pulakeshpradhan/opengeo"><img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python Version"></a>
</p>

---

**OpenGeo** (`og`) is a Python package designed to provide a **Google Earth Engine (GEE)**-like experience using open-source geospatial tools such as **Xarray**, **Dask**, **STAC**, and **GeoPandas**.

The goal is to smooth the transition for GEE users to the open Python ecosystem by mimicking the familiar Earth Engine API while leveraging the power of local or distributed cloud computing.

---

## 🚀 Key Features

* **🔄 API Familiarity**: Mimics `ee.Image`, `ee.ImageCollection`, `ee.FeatureCollection`, and `ee.Geometry` APIs
* **⚡ Lazy Loading**: Uses `stackstac` and `dask` to lazily load and process imagery from STAC catalogs
* **💻 Local Processing**: Run your analysis locally or on a standard Dask cluster without GEE quotas
* **🔗 Interoperability**: Seamlessly integrate with `xarray`, `geopandas`, and `shapely`
* **🌍 Open Access**: Focuses on community-maintained STAC APIs like Earth Search (Element84), Microsoft Planetary Computer, and more
* **📊 Interactive Visualization**: Built-in integration with Leafmap for beautiful, interactive maps

---

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
ndvi = (image.select("nir") - image.select("red")) / \
       (image.select("nir") + image.select("red"))

# Reduce over the region
stats = ndvi.reduceRegion(reducer="mean", geometry=roi, scale=10)
print(f"Mean NDVI: {stats}")
```

---

## 📊 API Comparison

| GEE | OpenGeo | Underlying Tech |
|-----|---------|-----------------|
| `ee.ImageCollection` | `og.ImageCollection` | `pystac_client` + `stackstac` |
| `ee.Image` | `og.Image` | `xarray.DataArray` |
| `ee.FeatureCollection` | `og.FeatureCollection` | `geopandas.GeoDataFrame` |
| `ee.Geometry` | `og.Geometry` | `shapely.geometry` |
| `geemap.Map` | `og.Map` | `leafmap.Map` |

---

## 🎯 Why OpenGeo?

!!! success "For GEE Users"
    - **Familiar API**: Minimal code changes needed to port GEE scripts
    - **No Quotas**: Process as much data as your hardware allows
    - **Full Control**: Run locally or on your own cloud infrastructure
    - **Open Source**: No vendor lock-in, fully transparent

!!! info "For Python Users"
    - **Modern Stack**: Built on Xarray, Dask, and STAC standards
    - **Pythonic**: Integrates seamlessly with pandas, numpy, matplotlib
    - **Extensible**: Easy to add custom functions and workflows
    - **Well Documented**: Comprehensive guides and examples

---

## 📚 Getting Started

<div class="grid cards" markdown>

* :material-clock-fast:{ .lg .middle } **Quick Installation**

    ---

    Get up and running in minutes

    [:octicons-arrow-right-24: Installation Guide](installation.md)

* :material-book-open-variant:{ .lg .middle } **Usage Guide**

    ---

    Learn the core concepts and workflows

    [:octicons-arrow-right-24: Usage Guide](usage.md)

* :material-code-braces:{ .lg .middle } **API Reference**

    ---

    Detailed documentation for all classes and methods

    [:octicons-arrow-right-24: API Reference](api/index.md)

* :material-notebook:{ .lg .middle } **Examples**

    ---

    Jupyter notebooks with real-world use cases

    [:octicons-arrow-right-24: View Examples](examples/intro.md)

</div>

---

## 🌟 Example Use Cases

* **🌾 Agriculture**: Monitor crop health with NDVI time series
* **🌳 Forestry**: Track deforestation and forest degradation
* **🌊 Water Resources**: Map water bodies and monitor changes
* **🏙️ Urban Planning**: Analyze urban growth and land use change
* **🔥 Disaster Response**: Assess wildfire damage and flood extent
* **🌡️ Climate Studies**: Analyze land surface temperature trends

---

## 🤝 Contributing

We welcome contributions! Whether it's:

* 🐛 Bug reports
* 💡 Feature requests
* 📝 Documentation improvements
* 🔧 Code contributions

Check out our [GitHub repository](https://github.com/pulakeshpradhan/opengeo) to get involved.

---

## 📄 License

OpenGeo is released under the **MIT License**. See [LICENSE](https://github.com/pulakeshpradhan/opengeo/blob/main/LICENSE) for details.

---

## 🙏 Acknowledgments

OpenGeo builds upon the excellent work of:

* [Xarray](https://xarray.dev/) - N-dimensional labeled arrays
* [Dask](https://dask.org/) - Parallel computing
* [STAC](https://stacspec.org/) - SpatioTemporal Asset Catalog
* [GeoPandas](https://geopandas.org/) - Geospatial data in Python
* [Leafmap](https://leafmap.org/) - Interactive mapping
* [Google Earth Engine](https://earthengine.google.com/) - Inspiration for the API design
