import xarray as xr
import rioxarray
import numpy as np
import stackstac
from .geometry import Geometry

class Image:
    """Wrapper for xarray.DataArray to mimic ee.Image."""

    def __init__(self, data):
        if isinstance(data, xr.DataArray):
            self._da = data
        elif isinstance(data, (int, float)):
             # Constant image
             self._da = xr.DataArray(data)
             # Add dummy coords?
        elif isinstance(data, str) and (data.startswith("http") or data.endswith(".tif")):
             # Load from URL/Path?
             # For simplicity, use rioxarray open_rasterio
             self._da = rioxarray.open_rasterio(data, chunks="auto") 
        else:
             print(f"Warning: Image constructor received unknown type: {type(data)}")
             self._da = xr.DataArray(data)

    @property  
    def _data(self):
        return self._da

    def select(self, bands):
        if isinstance(bands, str): bands = [bands]
        # Assuming band dimension exists
        if 'band' in self._da.dims:
            return Image(self._da.sel(band=bands))
        if 'bands' in self._da.dims:
             return Image(self._da.sel(bands=bands))
             
        # If no band dim but variables in Dataset? We handle DataArray primarily.
        return self
        
    def addBands(self, other):
        # Merge bands. complicated if coordinates differ.
        # Xarray align
        if isinstance(other, Image):
            other = other._data
        # If both have band dim, concatenate?
        # If different bands, merge?
        # For simplicity, if same coords, just add as new band?
        # TODO: Implement full merge logic
        return self 

    def clip(self, geometry):
        if isinstance(geometry, Geometry):
             geometry = geometry.shapely
        # User rioxarray clip
        # Ensure CRS is set
        if self._da.rio.crs is None:
             # If constant image, clip doesn't make sense unless we conform to geometry grid
             # Just return self? Or mask?
             print("Warning: Image has no CRS, skipping clip.")
             return self
             
        try:
             clipped = self._da.rio.clip([geometry], all_touched=True, drop=True)
             return Image(clipped)
        except Exception as e:
             print(f"Clip failed: {e}")
             return self

    def mask(self):
        # In GEE returns the mask
        return Image(self._da.notnull())

    def updateMask(self, mask):
        if isinstance(mask, Image): mask = mask._data
        return Image(self._da.where(mask))

    def add(self, other):
        return self + other
    def subtract(self, other):
        return self - other
    def multiply(self, other):
        return self * other
    def divide(self, other):
        return self / other

    def _prepare_for_math(self, other):
        val = other._data if isinstance(other, Image) else other
        self_da = self._da
        
        if isinstance(val, xr.DataArray):
            # If both have single band but different names, squeeze to allow math
            if 'band' in self_da.dims and self_da.sizes['band'] == 1:
                if 'band' in val.dims and val.sizes['band'] == 1:
                    return self_da.squeeze('band'), val.squeeze('band')
            elif 'bands' in self_da.dims and self_da.sizes['bands'] == 1:
                if 'bands' in val.dims and val.sizes['bands'] == 1:
                    return self_da.squeeze('bands'), val.squeeze('bands')
        return self_da, val

    def __add__(self, other):
        s, o = self._prepare_for_math(other)
        return Image(s + o)
    def __sub__(self, other):
        s, o = self._prepare_for_math(other)
        return Image(s - o)
    def __mul__(self, other):
        s, o = self._prepare_for_math(other)
        return Image(s * o)
    def __truediv__(self, other):
        s, o = self._prepare_for_math(other)
        return Image(s / o)

    def rename(self, names):
        # Rename bands
        if isinstance(names, str): names = [names]
        da = self._da.copy()
        if 'band' in da.dims:
             da['band'] = names
        elif 'bands' in da.dims:
             da['bands'] = names
        return Image(da)
        
    def reduceRegion(self, reducer='mean', geometry=None, scale=None, bestEffort=False, maxPixels=1e9, tileScale=1):
        """
        Execute reduction over region using Dask for efficiency.
        """
        target = self
        if geometry:
            target = target.clip(geometry)
        
        da = target._da
        
        # Spatial dimensions are usually 'x' and 'y'
        spatial_dims = []
        if 'x' in da.dims: spatial_dims.append('x')
        if 'y' in da.dims: spatial_dims.append('y')
        
        if not spatial_dims:
            # Nothing to reduce spatially?
            return {"constant": float(da.compute()) if hasattr(da, 'compute') else float(da)}

        # Define reduction mapping
        reducers = {
            'mean': xr.DataArray.mean,
            'max': xr.DataArray.max,
            'min': xr.DataArray.min,
            'sum': xr.DataArray.sum,
            'count': xr.DataArray.count,
            'median': xr.DataArray.median
        }
        
        if reducer not in reducers:
            raise ValueError(f"Unsupported reducer: {reducer}")
            
        # Apply lazy reduction
        reduced = reducers[reducer](da, dim=spatial_dims, keep_attrs=True)
        
        # Trigger single computation for all bands
        results = reduced.compute()
        
        dict_res = {}
        
        # Handle band dimension if it exists
        band_dim = None
        if 'band' in results.dims: band_dim = 'band'
        elif 'bands' in results.dims: band_dim = 'bands'
        
        if band_dim:
            for b in results[band_dim].values:
                val = results.sel({band_dim: b}).item()
                dict_res[str(b)] = val
        else:
            dict_res['constant'] = results.item()
             
        return dict_res

    def normalizedDifference(self, bands):
        if len(bands) != 2:
            raise ValueError("normalizedDifference requires exactly 2 bands.")
        b1 = self.select(bands[0])
        b2 = self.select(bands[1])
        # Force float to avoid integer division issues
        return (b1 - b2) / (b1 + b2)

    def to_file(self, path, vmin=None, vmax=None, palette=None, **kwargs):
        """
        Saves the image to a file. 
        If path ends in .tif, saves as GeoTIFF.
        If path ends in .jpg or .png, saves as a rendered image.
        """
        da = self._da
        if 'band' in da.dims:
            if da.sizes['band'] == 1:
                da = da.squeeze('band')
            elif da.sizes['band'] == 3:
                # RGB
                pass
        elif 'bands' in da.dims:
            if da.sizes['bands'] == 1:
                da = da.squeeze('bands')
            elif da.sizes['bands'] == 3:
                # RGB
                pass

        if path.lower().endswith(('.tif', '.tiff')):
            da.rio.to_raster(path, **kwargs)
        else:
            import matplotlib.pyplot as plt
            # Normalize for visualization if not RGB
            is_rgb = (len(da.shape) == 3 and (da.shape[0] == 3 or da.shape[-1] == 3))
            
            plt.figure(figsize=(10, 10))
            if is_rgb:
                # Handle (C, H, W) to (H, W, C) for matplotlib if needed
                if da.shape[0] == 3:
                    da = da.transpose('y', 'x', 'band') if 'band' in da.dims else da.transpose('y', 'x', 'bands')
                da.plot.imshow(vmin=vmin, vmax=vmax)
            else:
                da.plot.imshow(cmap=palette or 'viridis', vmin=vmin, vmax=vmax)
            
            plt.axis('off')
            plt.savefig(path, bbox_inches='tight', pad_inches=0)
            plt.close()
            print(f"Image saved to {path}")

    def getInfo(self):
        # Metadata
        bands = []
        if 'band' in self._da.dims: bands = self._da.band.values.tolist()
        elif 'bands' in self._da.dims: bands = self._da.bands.values.tolist()
            
        return {
            'type': 'Image',
            'bands': bands,
            'dtype': str(self._da.dtype),
            'shape': self._da.shape,
            'crs': str(self._da.rio.crs) if hasattr(self._da, 'rio') else None
        }

    def __repr__(self):
        import json
        return f"og.Image({json.dumps(self.getInfo(), indent=2)})"
