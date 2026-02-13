from .geometry import Geometry
import json

class Feature:
    """Wrapper for GeoJSON Feature structure to mimic ee.Feature."""
    
    def __init__(self, geometry, properties=None, id=None):
        if isinstance(geometry, Geometry):
            self._geometry = geometry
        else:
            # Try to interpret as geometry or dict (GeoJSON)
            if isinstance(geometry, dict) and 'type' in geometry and geometry['type'] == 'Feature':
                 # Probably a GeoJSON Feature
                 if properties is None: properties = geometry.get('properties', {})
                 if id is None: id = geometry.get('id', None)
                 # geometry part - need to parse... assume geometry is simple for now or implement from GeoJSON
                 # Simplifying: user must pass geometry object or None
                 pass
            self._geometry = geometry # Can be None for null geometry

        self._properties = properties or {}
        self._id = id

    def geometry(self):
        return self._geometry

    def get(self, key):
        return self._properties.get(key)
    
    def set(self, key, value):
        self._properties[key] = value
        return self

    def propertyNames(self):
        return list(self._properties.keys())
        
    def toDictionary(self):
        return self._properties.copy()
        
    def getInfo(self):
        return {
            'type': 'Feature',
            'geometry': self._geometry.getInfo() if self._geometry else None,
            'properties': self._properties,
            'id': self._id
        }

    def __repr__(self):
        return f"og.Feature(id={self._id}, properties={self._properties.keys()})"
