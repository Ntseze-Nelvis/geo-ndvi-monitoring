import rasterio
import requests
from rasterio.io import MemoryFile
import os
import time

def download_band(url, output_path, max_retries=3):
    """Download a file with retries and proper error handling"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    for attempt in range(max_retries):
        try:
            print(f"  Attempt {attempt + 1}/{max_retries}...")
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()
            
            # Download in chunks
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Verify the file is valid
            with rasterio.open(output_path) as src:
                print(f"  ✅ Downloaded successfully! Size: {src.width}x{src.height}")
            return True
            
        except Exception as e:
            print(f"  ❌ Attempt {attempt + 1} failed: {str(e)[:100]}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                print(f"  ❌ Failed after {max_retries} attempts")
                return False
    return False

def get_sentinel_data():
    """Get Sentinel-2 data from Planetary Computer (public, free)"""
    
    # Use a test region with known good data (Nairobi, Kenya region)
    # These are direct URLs to COGs (Cloud Optimized GeoTIFFs)
    
    # Example: Small tile from Kenya (reliable, small file size)
    base_url = "https://planetarycomputer.microsoft.com/api/data/v1/item/sentinel-2-l2a/"
    
    # Using a known good tile from Kenya (March 2024, clear sky)
    item_id = "S2B_MSIL2A_20240301T080909_R050_R006_T37MBR_20240301T115325"
    
    bands = {
        "B04": "https://planetarycomputer.microsoft.com/api/stac/v1/collections/sentinel-2-l2a/items/S2B_MSIL2A_20240301T080909_R050_R006_T37MBR_20240301T115325/assets/B04",
        "B08": "https://planetarycomputer.microsoft.com/api/stac/v1/collections/sentinel-2-l2a/items/S2B_MSIL2A_20240301T080909_R050_R006_T37MBR_20240301T115325/assets/B08"
    }
    
    print("\n📡 Downloading Sentinel-2 data from Planetary Computer")
    print("📍 Location: Kenya region (test area with good data)")
    print("📅 Date: March 1, 2024 (clear sky conditions)\n")
    
    success = True
    for band_name, url in bands.items():
        print(f"Downloading {band_name} band...")
        output_path = f"data/raw/{band_name.lower()}_band.tif"
        if not download_band(url, output_path):
            success = False
            break
    
    return success

if __name__ == "__main__":
    if get_sentinel_data():
        print("\n✅ All bands downloaded successfully!")
        print("📂 Files saved in data/raw/")
        print("🚀 Ready for NDVI calculation")
    else:
        print("\n❌ Download failed")
        print("💡 Alternative: Let's try a different data source")
