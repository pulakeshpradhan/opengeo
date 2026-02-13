import sys
import os

# Ensure we can import the local package if running from source
sys.path.append(os.getcwd())

import opengeo as og

def main():
    print("Initializing OpenGeo...")
    og.Initialize()

    # ROI: A small area in Bangalore
    roi = og.Geometry.Rectangle(77.58, 12.96, 77.60, 12.98)
    print(f"ROI: {roi}")

    print("\n--- Sentinel-2 Example ---")
    try:
        # Sentinel-2 L2A from Element84
        s2_col = og.ImageCollection("sentinel-2-c1-l2a") \
            .filterDate("2023-01-01", "2023-01-31") \
            .filterBounds(roi) \
            .select(["red", "nir"]) # Common names usually work with Earth Search aliases
        
        print(f"Sentinel-2 images found: {s2_col.size()}")
        
        if s2_col.size() > 0:
            image = s2_col.median()
            # NDVI = (NIR - Red) / (NIR + Red)
            ndvi = (image.select("nir") - image.select("red")) / (image.select("nir") + image.select("red"))
            
            stats = ndvi.reduceRegion(reducer="mean", geometry=roi, scale=10)
            print(f"Sentinel-2 Mean NDVI: {stats}")
            
    except Exception as e:
        print(f"Sentinel-2 Example Failed: {e}")

    print("\n--- Landsat 8 Example ---")
    try:
        # Landsat 8 Collection 2 Level 2
        # Note: Earth Search usually hosts 'landsat-c2-l2'
        # Bands: Red is 'red', NIR is 'nir08' (or sometimes just 'nir' depending on STAC extensions)
        # Let's try 'red' and 'nir08' which are standard for L8 on Earth Search
        
        l8_col = og.ImageCollection("landsat-c2-l2") \
            .filterDate("2023-01-01", "2023-03-30") \
            .filterBounds(roi) \
            .select(["red", "nir08"]) 
            
        print(f"Landsat 8 images found: {l8_col.size()}")
        
        if l8_col.size() > 0:
            # Create a median composite
            l8_image = l8_col.median()
            
            # Rename bands for easier access transparency (optional but good for consistency)
            # The select returned 'red' and 'nir08'
            
            red = l8_image.select("red")
            nir = l8_image.select("nir08")
            
            # Calculate NDVI
            # (NIR - Red) / (NIR + Red)
            l8_ndvi = (nir - red) / (nir + red)
            
            # Reduce region
            # Landsat resolution is 30m
            l8_stats = l8_ndvi.reduceRegion(reducer="mean", geometry=roi, scale=30)
            print(f"Landsat 8 Mean NDVI: {l8_stats}")
            
    except Exception as e:
        print(f"Landsat 8 Example Failed: {e}")

if __name__ == "__main__":
    main()
