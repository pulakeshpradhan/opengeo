# Installation

Installing OpenGeo is straightforward. We recommend using a virtual environment to manage dependencies.

## 📦 Quick Install

=== "From Source (Recommended)"
    ```bash
    git clone https://github.com/pulakeshpradhan/opengeo.git
    cd opengeo
    pip install -e .
    ```

=== "From PyPI (Coming Soon)"
    ```bash
    pip install opengeo
    ```

---

## 🔧 Standard Installation

### 1. Create a Virtual Environment

=== "Windows"
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```

=== "macOS / Linux"
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

### 2. Install Dependencies

Install the core dependencies required for geospatial processing:

```bash
pip install -r requirements.txt
```

### 3. Install OpenGeo

Install the package in editable mode if you are developing or just want to use the latest local version:

```bash
pip install -e .
```

---

## 📚 Dependencies

OpenGeo relies on the following key libraries:

| Library | Purpose |
|---------|---------|
| **pystac-client** | Searching STAC catalogs |
| **stackstac** | Loading STAC items into Xarray |
| **xarray** | N-dimensional array processing |
| **dask** | Lazy evaluation and parallel computing |
| **geopandas** | Vector data handling |
| **shapely** | Geometric operations |
| **leafmap** | Interactive visualization |
| **rioxarray** | Raster I/O with Xarray |

---

## ✅ Verification

To verify the installation, try importing `opengeo` in a Python shell:

```python
import opengeo as og
print(f"OpenGeo version: {og.__version__}")

# Test basic functionality
og.Initialize()
print("OpenGeo initialized successfully!")
```

---

## 🐛 Troubleshooting

!!! warning "Common Issues"

    **GDAL Installation Issues**
    
    If you encounter GDAL-related errors, try installing it via conda:
    ```bash
    conda install -c conda-forge gdal
    ```
    
    **Memory Issues with Large Datasets**
    
    Configure Dask to limit memory usage:
    ```python
    import dask
    dask.config.set({'array.chunk-size': '128MB'})
    ```

!!! tip "Recommended Setup"
    For the best experience, we recommend using **Python 3.9-3.11** with a conda environment:
    ```bash
    conda create -n opengeo python=3.11
    conda activate opengeo
    pip install -e .
    ```
