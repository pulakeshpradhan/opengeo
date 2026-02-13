import opengeo as og

def test_aliases():
    print("Testing STAC API Aliases...")
    
    # Test Microsoft
    og.Initialize("MICROSOFT")
    print(f"MICROSOFT: {og.STAC_API()}")
    
    # Test NASA
    og.Initialize("NASA")
    print(f"NASA: {og.STAC_API()}")
    
    # Test USGS
    og.Initialize("USGS")
    print(f"USGS: {og.STAC_API()}")
    
    # Test GEE
    og.Initialize("GEE")
    print(f"GEE: {og.STAC_API()}")
    
    # Test Direct URL
    og.Initialize("https://api.umbra.space/stac/v1")
    print(f"UMBRA Direct: {og.STAC_API()}")

if __name__ == "__main__":
    test_aliases()
