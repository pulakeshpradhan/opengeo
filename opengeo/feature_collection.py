import geopandas as gpd
import pandas as pd
from .feature import Feature
from .geometry import Geometry
import json

class FeatureCollection:
    """Wrapper for geopandas.GeoDataFrame to mimic ee.FeatureCollection."""

    def __init__(self, arg):
        if isinstance(arg, str):
            # assume path
            self._gdf = gpd.read_file(arg)
        elif isinstance(arg, gpd.GeoDataFrame):
            self._gdf = arg
        elif isinstance(arg, list):
             if len(arg) == 0:
                 self._gdf = gpd.GeoDataFrame(columns=['geometry'], geometry='geometry')
             elif isinstance(arg[0], Feature):
                 # List of Features
                 geoms = [f.geometry().shapely if f.geometry() else None for f in arg]
                 props = [f.toDictionary() for f in arg]
                 self._gdf = gpd.GeoDataFrame(props, geometry=geoms)
             else:
                 # List of dict/geojson?
                 # Try to parse
                 pass
        elif isinstance(arg, Feature):
             self._gdf = gpd.GeoDataFrame([arg.toDictionary()], geometry=[arg.geometry().shapely])
        else:
            # Maybe it's empty or None?
            if arg is None:
                 self._gdf = gpd.GeoDataFrame(columns=['geometry'], geometry='geometry')
            else:
                 raise ValueError(f"Cannot interpret FeatureCollection source: {arg}")
            
    def filterBounds(self, geometry):
        if hasattr(geometry, 'shapely'):
             geometry = geometry.shapely
        filtered = self._gdf[self._gdf.intersects(geometry)]
        return FeatureCollection(filtered)

    def filter(self, expr_or_filter):
        if isinstance(expr_or_filter, str):
            filtered = self._gdf.query(expr_or_filter)
            return FeatureCollection(filtered)
        elif callable(expr_or_filter):
            mask = self._gdf.apply(expr_or_filter, axis=1)
            return FeatureCollection(self._gdf[mask])
        else:
             raise NotImplementedError("Only string queries (pandas) or callables supported for filter()")

    def select(self, properties):
        if isinstance(properties, str): properties = [properties]
        cols = properties + ['geometry']
        cols = [c for c in cols if c in self._gdf.columns]
        return FeatureCollection(self._gdf[cols])
        
    def map(self, func):
        new_features = []
        for i, row in self._gdf.iterrows():
            geom = Geometry(row.geometry)
            props = row.drop('geometry').to_dict()
            feat = Feature(geom, props, id=i)
            res = func(feat)
            if isinstance(res, Feature):
                 new_features.append(res)
        
        return FeatureCollection(new_features)

    def size(self):
        return len(self._gdf)
        
    def first(self):
        if len(self._gdf) == 0: return None
        row = self._gdf.iloc[0]
        return Feature(Geometry(row.geometry), row.drop('geometry').to_dict())

    def getInfo(self):
        return json.loads(self._gdf.to_json())
        
    def aggregate_array(self, property):
        if property in self._gdf.columns:
            return self._gdf[property].tolist()
        return []

    def __repr__(self):
        return f"og.FeatureCollection({len(self._gdf)} elements)"
