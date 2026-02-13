import os

# Set PROJ_LIB for Windows conda environments if needed
# This must be done before pyproj is imported by any submodule
if 'PROJ_LIB' not in os.environ:
    # Common path in Windows conda envs
    potential_path = r"C:\Users\pulak\anaconda3\envs\maps\Library\share\proj"
    if os.path.exists(os.path.join(potential_path, "proj.db")):
        os.environ['PROJ_LIB'] = potential_path
        try:
            import pyproj
            pyproj.datadir.set_data_dir(potential_path)
        except ImportError:
            pass

from .image import Image
from .image_collection import ImageCollection
from .feature import Feature
from .feature_collection import FeatureCollection
from .geometry import Geometry
from .config import Initialize, STAC_API, DisplayCatalogs, Catalogs, Catalog, Urls, Aliases, Collections, Items, Assets, Item, AssetUrls, DisplayItem

__all__ = [
    "Image",
    "ImageCollection", 
    "Feature",
    "FeatureCollection",
    "Geometry",
    "Initialize",
    "Map",
    "STAC_API",
    "Catalogs",
    "Catalog",
    "DisplayCatalogs",
    "Urls",
    "Aliases",
    "Collections",
    "Items",
    "Assets",
    "Item",
    "AssetUrls",
    "DisplayItem"
]
