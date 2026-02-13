# Installation

Installing OpenGeo is straightforward. We recommend using a virtual environment to manage dependencies.

## Standard Installation

You can install OpenGeo and its dependencies via `pip`.

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

## Dependencies

OpenGeo relies on the following key libraries:

* **pystac-client**: For searching STAC catalogs.
* **stackstac**: For loading STAC items into Xarray.
* **xarray**: For N-dimensional array processing.
* **dask**: For lazy evaluation and parallel computing.
* **geopandas**: For vector data handling.
* **leafmap**: For interactive visualization.

## Verification

To verify the installation, try importing `opengeo` in a Python shell:

```python
import opengeo as og
print(og.__version__)
```
