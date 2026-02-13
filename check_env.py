try:
    import geoviews
    print("geoviews imported successfully")
except ImportError as e:
    print(f"geoviews import failed: {e}")

try:
    import cartopy
    print("cartopy imported successfully")
except ImportError as e:
    print(f"cartopy import failed: {e}")

import opengeo as og
try:
    print(f"opengeo.Map exists: {og.Map}")
except AttributeError:
    print("opengeo.Map NOT found")
