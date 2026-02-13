# Examples

This section contains a collection of Jupyter notebooks demonstrating the capabilities of OpenGeo for various remote sensing tasks.

## 📓 Available Examples

### Vegetation Analysis

* **[NDVI Analysis](landsat8_ndvi_analysis.ipynb)** [:material-download:](https://raw.githubusercontent.com/pulakeshpradhan/opengeo/main/docs/examples/landsat8_ndvi_analysis.ipynb){:download}  
    Learn how to calculate the Normalized Difference Vegetation Index using Landsat 8 data.

### Optical Imagery

* **[Sentinel-2 Exploration](sentinel2_analysis_element84.ipynb)** [:material-download:](https://raw.githubusercontent.com/pulakeshpradhan/opengeo/main/docs/examples/sentinel2_analysis_element84.ipynb){:download}  
    Accessing and visualizing Sentinel-2 imagery from Element84.

* **[Landsat 8 USGS](landsat_analysis_usgs.ipynb)** [:material-download:](https://raw.githubusercontent.com/pulakeshpradhan/opengeo/main/docs/examples/landsat_analysis_usgs.ipynb){:download}  
    Working with Landsat 8 collections from the USGS STAC API.

### Earth Observation Products

* **[MODIS NASA](modis_analysis_nasa.ipynb)** [:material-download:](https://raw.githubusercontent.com/pulakeshpradhan/opengeo/main/docs/examples/modis_analysis_nasa.ipynb){:download}  
    Accessing land surface temperature or other MODIS products.

### Radar Imagery

* **[SAR Analysis](sar_analysis_umbra_capella.ipynb)** [:material-download:](https://raw.githubusercontent.com/pulakeshpradhan/opengeo/main/docs/examples/sar_analysis_umbra_capella.ipynb){:download}  
    Working with Synthetic Aperture Radar data from Umbra and Capella.

---

!!! tip "Running Notebooks Locally"
    Click the :material-download: icon next to each notebook to download it. You can then run them locally using:

    === "Jupyter Lab"
        ```bash
        jupyter lab notebook_name.ipynb
        ```
    
    === "VS Code"
        Open the `.ipynb` file in VS Code with the Jupyter extension installed.
    
    === "Google Colab"
        Upload the notebook to [Google Colab](https://colab.research.google.com/) and run it in the cloud.

!!! info "Requirements"
    Make sure you have OpenGeo and its dependencies installed before running the notebooks:
    ```bash
    pip install -e .
    ```
