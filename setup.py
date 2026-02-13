from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="opengeo",
    version="0.0.1",
    author="Pulakesh Pradhan",
    author_email="pulakesh.mid@gmail.com",
    description="A Google Earth Engine-like Python package using Xarray and Dask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pulakeshpradhan/opengeo",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "xarray",
        "dask[complete]",
        "pystac-client",
        "stackstac",
        "rioxarray",
        "geopandas",
        "shapely",
        "numpy",
        "pandas",
        "toolz",
        "odc-stac",
        "hvplot",
        "holoviews"
    ],
)
