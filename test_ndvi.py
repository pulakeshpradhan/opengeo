import opengeo as og
import os

def test():
    try:
        og.Initialize()
        roi = og.Geometry.Rectangle(77.55, 12.90, 77.65, 13.00)
        print("ROI Defined.")
        
        # Filter for Landsat 8 specifically 
        l8_col = og.ImageCollection("landsat-c2-l2") \
            .filterDate("2023-01-01", "2023-06-30") \
            .filterBounds(roi) \
            .filter(query={"platform": {"eq": "landsat-8"}}) \
            .select(["red", "nir08"])
            
        count = l8_col.size()
        print(f"Number of images found: {count}")
        
        if count > 0:
            # Use a common EPSG 
            l8_image = l8_col.median(epsg=32643)
            print("Median composite created.")
            
            # Calculate NDVI using normalizedDifference
            ndvi = l8_image.normalizedDifference(["nir08", "red"]).rename("NDVI")
            print("NDVI calculation complete.")
            
            # Print image metadata (calls getInfo via __repr__)
            print("\nNDVI Image info:")
            print(ndvi)
            
            # Try to add to map (won't show in terminal but verifies logic)
            og.Map.addLayer(ndvi, {"palette": ['red', 'yellow', 'green'], "min": 0, "max": 1}, "NDVI")
            print("Successfully added to Map.")
            
            return True
        else:
            print("No images found.")
            return False
    except Exception as e:
        print(f"Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test()
