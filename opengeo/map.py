import leafmap
from .image import Image
from .image_collection import ImageCollection
from .feature import Feature
from .feature_collection import FeatureCollection

class Map(leafmap.Map):
    """
    Class to mimic GEE Map for visualization.
    Uses leafmap as the engine, supporting backends: 
    'ipyleaflet' (default), 'folium', 'heremap', 'keplergl', etc.
    """
    
    def __init__(self, **kwargs):
        # Allow backend selection: og.Map(backend='folium')
        if 'center' not in kwargs:
            kwargs['center'] = [20, 0]
        if 'zoom' not in kwargs:
            kwargs['zoom'] = 2
        super().__init__(**kwargs)

    def addLayer(self, ee_object, vis_params=None, name=None, shown=True, opacity=1):
        """
        Adds a layer to the map in GEE style.
        
        Args:
            ee_object: The object to add (Image, ImageCollection, etc.)
            vis_params: Dictionary of visualization parameters (min, max, palette, bands)
            name: Layer name
            shown: Whether the layer is visible
            opacity: Layer opacity
        """
        if vis_params is None:
            vis_params = {}
            
        if name is None:
            name = "Layer " + str(len(self.layers))

        if isinstance(ee_object, Image):
            da = ee_object._data
            
            # Handle band selection in vis_params
            sel_bands = vis_params.get('bands', None)
            if sel_bands:
                if isinstance(sel_bands, str): sel_bands = [sel_bands]
                if 'band' in da.dims:
                    da = da.sel(band=sel_bands)
                elif 'bands' in da.dims:
                    da = da.sel(bands=sel_bands)

            # Handle palette/cmap
            cmap = vis_params.get('palette', 'viridis')
            if isinstance(cmap, str) and ',' in cmap:
                cmap = [c.strip() for c in cmap.split(',')]
            
            vmin = vis_params.get('min', None)
            vmax = vis_params.get('max', None)
            
            # Prepare data for leafmap.add_raster
            plot_da = da
            # Squeeze single bands if not RGB
            is_rgb = False
            if 'band' in plot_da.dims and plot_da.sizes['band'] == 3: is_rgb = True
            elif 'bands' in plot_da.dims and plot_da.sizes['bands'] == 3: is_rgb = True
            
            if not is_rgb:
                if 'band' in plot_da.dims and plot_da.sizes['band'] == 1:
                    plot_da = plot_da.squeeze('band')
                elif 'bands' in plot_da.dims and plot_da.sizes['bands'] == 1:
                    plot_da = plot_da.squeeze('bands')
                
            self.add_raster(
                plot_da, 
                layer_name=name, 
                cmap=cmap, 
                vmin=vmin, 
                vmax=vmax, 
                opacity=opacity,
                visible=shown
            )
        
        elif isinstance(ee_object, ImageCollection):
            # For ImageCollection, visualize the mosaic
            return self.addLayer(ee_object.mosaic(), vis_params, name, shown, opacity)
            
        elif isinstance(ee_object, (Feature, FeatureCollection)):
            # TODO: add_gdf support
            pass
            
        return self

    def centerObject(self, obj, zoom=None):
        """Centers the map on an object."""
        from .geometry import Geometry
        
        b = None
        if isinstance(obj, Geometry):
            b = obj.shapely.bounds # (minx, miny, maxx, maxy)
        elif hasattr(obj, 'bounds'):
            b = obj.bounds
            if callable(b): b = b()
        
        if b and isinstance(b, (tuple, list)) and len(b) == 4:
            # leafmap zoom_to_bounds expects [minx, miny, maxx, maxy] per help
            # but ipyleaflet uses lat/lon [[miny, minx], [maxy, maxx]]
            # Let's try the leafmap standard list format
            try:
                self.zoom_to_bounds(bounds=[b[0], b[1], b[2], b[3]])
            except:
                self.fit_bounds([[b[1], b[0]], [b[3], b[2]]])
            
        if zoom is not None:
             self.zoom = zoom

    def add_layer(self, *args, **kwargs):
        # Maintain leafmap's native add_layer support
        return super().add_layer(*args, **kwargs)
