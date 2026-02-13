
import opengeo as og
import os

def test_discovery():
    print("=== Testing Discovery Features ===")
    
    # 1. Catalogs
    catalogs = og.Catalogs()
    print(f"Total STAC catalogs registered: {len(catalogs)}")
    # Print first 3 aliases
    print(f"Top Aliases: {og.Aliases()[:3]}")
    
    # 2. Initialization
    print("\nInitializing with Microsoft Planetary Computer...")
    og.Initialize('MICROSOFT')
    
    # 3. Collections
    collections = og.Collections()
    print(f"Found {len(collections)} collections at Microsoft.")
    # Check if a specific collection exists
    if 'sentinel-2-l2a' in collections:
        print("Sentinel-2 L2A collection found.")
        
        # 4. Assets & Items
        print("\nExploring collection 'sentinel-2-l2a'...")
        assets = og.Assets('sentinel-2-l2a')
        print(f"Available assets (count: {len(assets)}): {assets[:5]}...")
        
        items = og.Items('sentinel-2-l2a', limit=1)
        if items:
            print("\nItem Detail Sample:")
            og.DisplayItem(items[0])
            
            urls = og.AssetUrls(items[0])
            print(f"Sample asset URL (visual): {urls.get('visual') or 'N/A'}")

def test_core_functionality():
    print("\n=== Testing Core ImageCollection Functionality ===")
    try:
        # Using Element84 for a simple search test
        og.Initialize('ELEMENT84')
        
        # Filter a small area (London approx)
        roi = og.Geometry.Rectangle(-0.2, 51.4, 0.1, 51.6)
        
        collection = og.ImageCollection('sentinel-2-l2a') \
            .filterBounds(roi) \
            .filterDate('2024-01-01', '2024-01-31') \
            .select(['red', 'green', 'blue', 'nir'])
        
        size = collection.size()
        print(f"Number of images in London for Jan 2024: {size}")
        
        # 1. Calculate NDVI for the first available image or mosaic
        print("\nCalculating NDVI for the collection...")
        # Get the first image with a coarse resolution for speed
        image = collection.first(epsg=4326, resolution=500)
        if image:
            # Sentinel-2 bands for NDVI are B8 (NIR) and B4 (RED)
            # Element84 names them 'nir' and 'red'
            # Force float to avoid issues with uint16 data
            ndvi = image.normalizedDifference(['nir', 'red']).rename('ndvi')
            print("NDVI calculation complete.")
            
            # 2. Save as JPG
            output_path = "london_ndvi_jan2024.jpg"
            print(f"Saving NDVI map to {output_path}...")
            # NDVI ranges from -1 to 1. Using RdYlGn palette.
            ndvi.to_file(output_path, vmin=-0.1, vmax=0.8, palette='RdYlGn')
            
            # 3. Verify file exists
            if os.path.exists(output_path):
                print(f"Success! {output_path} created. Size: {os.path.getsize(output_path)} bytes")
            else:
                print(f"Failed to create {output_path}")

    except Exception as e:
        print(f"Core test failed or skipped (might need network): {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_discovery()
    test_core_functionality()
    print("\n=== Comprehensive Test Complete ===")
