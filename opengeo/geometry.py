from shapely.geometry import Point as SPoint, Polygon as SPolygon, LineString as SLineString, MultiPolygon as SMultiPolygon, box
import geopandas as gpd
import json

class Geometry:
    """Wrapper for shapely geometries to mimic ee.Geometry."""
    
    def __init__(self, geo_obj, crs="EPSG:4326"):
        self._geo = geo_obj
        self.crs = crs

    @property
    def shapely(self):
        return self._geo
        
    @classmethod
    def Point(cls, x, y):
        return cls(SPoint(x, y))

    @classmethod
    def Polygon(cls, coords):
        # Flatten if necessary or handle ee style nested lists
        if len(coords) == 1 and isinstance(coords[0], list) and isinstance(coords[0][0], list):
             # ee style: [[[x,y], [x,y]]] 
             # shapely: [[x,y], [x,y]] (exterior ring)
             return cls(SPolygon(coords[0]))
        return cls(SPolygon(coords))

    @classmethod
    def Rectangle(cls, xMin, yMin, xMax, yMax):
        return cls(box(xMin, yMin, xMax, yMax))
        
    @classmethod
    def LineString(cls, coords):
        return cls(SLineString(coords))

    def buffer(self, distance):
        # Distance unit depends on CRS, for simplicity assuming degrees if 4326 
        # but GEE uses meters. This is a complex point.
        # For now, just wrap shapely buffer
        return Geometry(self._geo.buffer(distance), self.crs)

    def bounds(self):
        return Geometry(box(*self._geo.bounds), self.crs)
        
    def intersection(self, other):
        if isinstance(other, Geometry):
             other = other.shapely
        return Geometry(self._geo.intersection(other), self.crs)

    def union(self, other):
        if isinstance(other, Geometry):
             other = other.shapely
        return Geometry(self._geo.union(other), self.crs)
        
    def getInfo(self):
        # Return GeoJSON dict
        return json.loads(gpd.GeoSeries([self._geo]).to_json())['features'][0]['geometry']
        
    def __repr__(self):
        return f"og.Geometry({self._geo.wkt})"
