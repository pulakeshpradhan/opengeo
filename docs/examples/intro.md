# Examples

This section contains a collection of Jupyter notebooks demonstrating the capabilities of OpenGeo for various remote sensing tasks.

## 📓 Available Examples

### Vegetation Analysis

**[NDVI Analysis](landsat8_ndvi_analysis.ipynb)**  
Learn how to calculate the Normalized Difference Vegetation Index using Landsat 8 data.

<div class="notebook-buttons">
  <a href="https://raw.githubusercontent.com/pulakeshpradhan/opengeo/main/docs/examples/landsat8_ndvi_analysis.ipynb" download class="md-button md-button--primary">
    :material-download: Download
  </a>
  <a href="https://colab.research.google.com/github/pulakeshpradhan/opengeo/blob/main/docs/examples/landsat8_ndvi_analysis.ipynb" target="_blank" class="md-button">
    :simple-googlecolab: Open in Colab
  </a>
</div>

---

### Optical Imagery

**[Sentinel-2 Exploration](sentinel2_analysis_element84.ipynb)**  
Accessing and visualizing Sentinel-2 imagery from Element84.

<div class="notebook-buttons">
  <a href="https://raw.githubusercontent.com/pulakeshpradhan/opengeo/main/docs/examples/sentinel2_analysis_element84.ipynb" download class="md-button md-button--primary">
    :material-download: Download
  </a>
  <a href="https://colab.research.google.com/github/pulakeshpradhan/opengeo/blob/main/docs/examples/sentinel2_analysis_element84.ipynb" target="_blank" class="md-button">
    :simple-googlecolab: Open in Colab
  </a>
</div>

---

**[Landsat 8 USGS](landsat_analysis_usgs.ipynb)**  
Working with Landsat 8 collections from the USGS STAC API.

<div class="notebook-buttons">
  <a href="https://raw.githubusercontent.com/pulakeshpradhan/opengeo/main/docs/examples/landsat_analysis_usgs.ipynb" download class="md-button md-button--primary">
    :material-download: Download
  </a>
  <a href="https://colab.research.google.com/github/pulakeshpradhan/opengeo/blob/main/docs/examples/landsat_analysis_usgs.ipynb" target="_blank" class="md-button">
    :simple-googlecolab: Open in Colab
  </a>
</div>

---

### Earth Observation Products

**[MODIS NASA](modis_analysis_nasa.ipynb)**  
Accessing land surface temperature or other MODIS products.

<div class="notebook-buttons">
  <a href="https://raw.githubusercontent.com/pulakeshpradhan/opengeo/main/docs/examples/modis_analysis_nasa.ipynb" download class="md-button md-button--primary">
    :material-download: Download
  </a>
  <a href="https://colab.research.google.com/github/pulakeshpradhan/opengeo/blob/main/docs/examples/modis_analysis_nasa.ipynb" target="_blank" class="md-button">
    :simple-googlecolab: Open in Colab
  </a>
</div>

---

### Radar Imagery

**[SAR Analysis](sar_analysis_umbra_capella.ipynb)**  
Working with Synthetic Aperture Radar data from Umbra and Capella.

<div class="notebook-buttons">
  <a href="https://raw.githubusercontent.com/pulakeshpradhan/opengeo/main/docs/examples/sar_analysis_umbra_capella.ipynb" download class="md-button md-button--primary">
    :material-download: Download
  </a>
  <a href="https://colab.research.google.com/github/pulakeshpradhan/opengeo/blob/main/docs/examples/sar_analysis_umbra_capella.ipynb" target="_blank" class="md-button">
    :simple-googlecolab: Open in Colab
  </a>
</div>

---

## 🚀 Getting Started

!!! tip "Running Notebooks"

    **Option 1: Download and Run Locally**
    
    1. Click the **Download** button above
    2. Open in your preferred environment:
        - **Jupyter Lab**: `jupyter lab notebook_name.ipynb`
        - **VS Code**: Open with Jupyter extension
        - **JupyterHub**: Upload to your server
    
    **Option 2: Run in Google Colab (Cloud)**
    
    1. Click **Open in Colab** button
    2. The notebook opens in Google Colab (free cloud environment)
    3. No local installation needed!
    4. Note: You may need to install OpenGeo in Colab:
       ```python
       !pip install git+https://github.com/pulakeshpradhan/opengeo.git
       ```

!!! info "Requirements"

    **For Local Execution:**
    
    Make sure you have OpenGeo and its dependencies installed:
    ```bash
    pip install -e .
    ```
    
    **For Google Colab:**
    
    Add this cell at the beginning of the notebook:
    ```python
    # Install OpenGeo in Colab
    !pip install git+https://github.com/pulakeshpradhan/opengeo.git
    ```

!!! success "Pro Tips"

    - 🌐 **Colab** is great for quick testing without local setup
    - 💻 **Local** is better for large datasets and production workflows
    - 📊 All notebooks include visualization examples
    - 🔄 Notebooks are regularly updated with new features
