import os

# Set PROJ_LIB for Windows conda environments if needed
# This must be done before pyproj/geopandas are heavily used
if 'PROJ_LIB' not in os.environ:
    # Common path in Windows conda envs
    # We can try to detect the environment path dynamically or use the one we found
    potential_path = r"C:\Users\pulak\anaconda3\envs\maps\Library\share\proj"
    if os.path.exists(os.path.join(potential_path, "proj.db")):
        os.environ['PROJ_LIB'] = potential_path

from .catalogs import STAC_CATALOGS

_STAC_API = "https://earth-search.aws.element84.com/v1"

def Catalogs():
    """
    Returns the full list of available STAC catalogs.
    """
    return STAC_CATALOGS

def DisplayCatalogs():
    """
    Prints a formatted list of all available STAC catalogs and their aliases.
    """
    print(f"{'Alias':<25} | {'Name':<40} | {'Type'}")
    print("-" * 80)
    for alias, info in STAC_CATALOGS.items():
        print(f"{alias:<25} | {info['name']:<40} | {info['type']}")

def Urls():
    """
    Returns a list of all available STAC API URLs.
    """
    return [info['url'] for info in STAC_CATALOGS.values()]

def Aliases():
    """
    Returns a list of all available STAC API aliases.
    """
    return list(STAC_CATALOGS.keys())

def Collections():
    """
    Returns a list of collection IDs from the currently initialized STAC API.
    """
    from pystac_client import Client
    # Handle Microsoft signing if needed
    modifier = None
    if "planetarycomputer" in _STAC_API:
        try:
            import planetary_computer
            modifier = planetary_computer.sign_inplace
        except ImportError:
            pass
            
    client = Client.open(_STAC_API, modifier=modifier)
    return [c.id for c in client.get_all_collections()]

def Items(collection_id, limit=10):
    """
    Returns a list of items from a specific collection in the currently initialized STAC API.
    """
    from pystac_client import Client
    modifier = None
    if "planetarycomputer" in _STAC_API:
        try:
            import planetary_computer
            modifier = planetary_computer.sign_inplace
        except ImportError:
            pass
            
    client = Client.open(_STAC_API, modifier=modifier)
    search = client.search(collections=[collection_id], max_items=limit)
    return [item.to_dict() for item in search.items()]

def Assets(collection_id):
    """
    Returns a list of available assets (bands/keys) for a specific collection.
    """
    from pystac_client import Client
    modifier = None
    if "planetarycomputer" in _STAC_API:
        try:
            import planetary_computer
            modifier = planetary_computer.sign_inplace
        except ImportError:
            pass
            
    client = Client.open(_STAC_API, modifier=modifier)
    collection = client.get_collection(collection_id)
    
    # Try getting from item_assets extension first
    if collection.extra_fields and "item_assets" in collection.extra_fields:
        return list(collection.extra_fields["item_assets"].keys())
    
    # Fallback: get assets from the first item
    search = client.search(collections=[collection_id], max_items=1)
    items = list(search.items())
    if items:
        return list(items[0].assets.keys())
    
    return []

def Item(collection_id, item_id):
    """
    Returns a specific item from a collection.
    """
    from pystac_client import Client
    modifier = None
    if "planetarycomputer" in _STAC_API:
        try:
            import planetary_computer
            modifier = planetary_computer.sign_inplace
        except ImportError:
            pass
            
    client = Client.open(_STAC_API, modifier=modifier)
    collection = client.get_collection(collection_id)
    if collection:
        item = collection.get_item(item_id)
        return item.to_dict() if item else None
    return None

def AssetUrls(item):
    """
    Returns a dictionary mapping asset names to their download/access URLs.
    Pass either an item dictionary or a Pystac Item.
    """
    assets = item.get('assets', {}) if isinstance(item, dict) else item.assets
    return {k: v.get('href') if isinstance(v, dict) else v.href for k, v in assets.items()}

def DisplayItem(item):
    """
    Prints a formatted summary of a STAC item.
    """
    if not item:
        print("No item to display.")
        return
    
    print(f"Item ID: {item.get('id')}")
    print(f"Collection: {item.get('collection')}")
    
    props = item.get('properties', {})
    print(f"Datetime: {props.get('datetime', props.get('start_datetime'))}")
    
    if 'bbox' in item:
        print(f"BBox: {item['bbox']}")
    
    assets = item.get('assets', {})
    print(f"Assets ({len(assets)}): {', '.join(list(assets.keys())[:10])}...")

def Catalog(alias):
    """
    Returns information about a specific catalog alias.
    """
    return STAC_CATALOGS.get(alias.upper())

def Initialize(url=None):
    """
    Initialize the OpenGeo module, optionally setting the default STAC API URL.
    Supports aliases from STAC_CATALOGS.
    """
    global _STAC_API
    
    if url:
        alias_info = Catalog(url)
        if alias_info:
            _STAC_API = alias_info['url']
        else:
            # Fallback for some legacy or common aliases not in the list or custom URL
            legacy_aliases = {
                'PLANETARY_COMPUTER': "https://planetarycomputer.microsoft.com/api/stac/v1",
                'CMR': "https://cmr.earthdata.nasa.gov/stac",
                'LANDSATLOOK': "https://landsatlook.usgs.gov/stac-server",
                'GEE': "https://earthengine-stac.storage.googleapis.com/catalog/catalog.json",
                'GOOGLE': "https://earthengine-stac.storage.googleapis.com/catalog/catalog.json",
                'EARTH_SEARCH': "https://earth-search.aws.element84.com/v1",
            }
            if url.upper() in legacy_aliases:
                _STAC_API = legacy_aliases[url.upper()]
            else:
                _STAC_API = url
    
    os.environ['AWS_NO_SIGN_REQUEST'] = 'YES'
            
    print(f"OpenGeo initialized with STAC API: {_STAC_API}")

def STAC_API():
    return _STAC_API
