from pystac_client import Client
import stackstac
import xarray as xr
import numpy as np
import copy
from .image import Image
from .geometry import Geometry
from .config import get_stac_api

class ImageCollection:
    """Wrapper for STAC search + stackstac to mimic ee.ImageCollection."""

    def __init__(self, collection_id, api_url=None, filters=None, bands=None):
        self._id = collection_id
        if isinstance(collection_id, ImageCollection):
             # Copy constructor logic if passed an instance
             self._id = collection_id._id
             self._api = collection_id._api
             self._filters = copy.deepcopy(collection_id._filters)
             self._bands = copy.deepcopy(collection_id._bands)
             return

        self._api = api_url or get_stac_api()
        self._filters = filters or {
            "collections": [self._id] if self._id else [],
            "datetime": None,
            "intersects": None,
            "bbox": None
        }
        self._bands = bands # Assets

    def _clone(self):
        # Helper to create a copy
        return ImageCollection(
            self._id, 
            api_url=self._api, 
            filters=copy.deepcopy(self._filters),
            bands=copy.deepcopy(self._bands)
        )

    def filterDate(self, start, end):
        new_col = self._clone()
        # start, end are strings 'YYYY-MM-DD'
        new_col._filters["datetime"] = f"{start}/{end}"
        return new_col

    def filterBounds(self, geometry):
        new_col = self._clone()
        if isinstance(geometry, Geometry):
             new_col._filters["intersects"] = geometry.shapely
        else:
             # Assume shapely or GeoJSON dict
             new_col._filters["intersects"] = geometry
        return new_col

    def filter(self, **kwargs):
        """Add arbitrary STAC filters."""
        new_col = self._clone()
        new_col._filters.update(kwargs)
        return new_col

    def select(self, bands):
        new_col = self._clone()
        if isinstance(bands, str): bands = [bands]
        new_col._bands = bands
        return new_col

    def _search(self):
        # Check for MS Planetary Computer
        modifier = None
        if "planetarycomputer" in self._api:
            try:
                import planetary_computer
                modifier = planetary_computer.sign_inplace
            except ImportError:
                 print("Warning: accessing Microsoft Planetary Computer but 'planetary-computer' package is not installed.")
        
        client = Client.open(self._api, modifier=modifier)
        # remove None values
        params = {k: v for k, v in self._filters.items() if v is not None}
        
        search = client.search(**params)
        return search.item_collection()

    def _to_xarray(self, **kwargs):
        items = self._search()
        if len(items) == 0:
            raise ValueError(f"No images found in collection '{self._id}' with current filters.")
        
        # Determine bounds from filters if possible
        bounds_latlon = None
        if self._filters["intersects"]:
             try:
                 bounds_latlon = self._filters["intersects"].bounds
             except: pass
        
        # Load stack. 
        da = stackstac.stack(
             items, 
             assets=self._bands, 
             bounds_latlon=bounds_latlon,
             **kwargs
        )
        return da

    def mean(self, **kwargs):
        da = self._to_xarray(**kwargs)
        # Reduce time dimension
        return Image(da.mean(dim="time", keep_attrs=True))

    def median(self, **kwargs):
        da = self._to_xarray(**kwargs)
        return Image(da.median(dim="time", keep_attrs=True))
        
    def min(self, **kwargs):
        da = self._to_xarray(**kwargs)
        return Image(da.min(dim="time", keep_attrs=True))

    def max(self, **kwargs):
        da = self._to_xarray(**kwargs)
        return Image(da.max(dim="time", keep_attrs=True))
        
    def mosaic(self, **kwargs):
        # Mosaic by taking max (common simple mosaic) or last.
        # stackstac.mosaic is more sophisticated if available.
        # Fallback to mean/median/max
        return self.max(**kwargs) 

    def first(self, **kwargs):
        # Return first image
        try:
             client = Client.open(self._api)
             params = {k: v for k, v in self._filters.items() if v is not None}
             params['max_items'] = 1
             search = client.search(**params)
             items = list(search.items())
             if not items: return None
             da = stackstac.stack(items[0], assets=self._bands, **kwargs)
             return Image(da.squeeze("time"))
        except Exception as e:
             print(f"Error fetching first image: {e}")
             return None
        
    def size(self):
        return len(self._search())
    
    def getInfo(self):
        return [i.to_dict() for i in self._search()]

    def __repr__(self):
        return f"og.ImageCollection({self._id}, filters={self._filters})"
