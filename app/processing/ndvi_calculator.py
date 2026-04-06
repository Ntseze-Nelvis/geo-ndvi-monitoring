import rasterio
import numpy as np
import os

def calculate_ndvi(red_path, nir_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Check if files exist
    if not os.path.exists(red_path):
        print(f"❌ Red band not found: {red_path}")
        return None
    if not os.path.exists(nir_path):
        print(f"❌ NIR band not found: {nir_path}")
        return None
    
    print("📊 Loading red band...")
    with rasterio.open(red_path) as red_src:
        red = red_src.read(1).astype(float)
        profile = red_src.profile
    
    print("📊 Loading NIR band...")
    with rasterio.open(nir_path) as nir_src:
        nir = nir_src.read(1).astype(float)
    
    print("🧮 Calculating NDVI...")
    epsilon = 1e-10
    ndvi = (nir - red) / (nir + red + epsilon)
    
    profile.update(dtype=rasterio.float32, count=1)
    
    print("💾 Saving NDVI result...")
    with rasterio.open(output_path, 'w', **profile) as dst:
        dst.write(ndvi.astype(rasterio.float32), 1)
    
    print(f"\n✅ NDVI saved to {output_path}")
    print(f"📈 NDVI range: {ndvi.min():.2f} to {ndvi.max():.2f}")
    
    # Statistics
    healthy = np.sum(ndvi > 0.5)
    stressed = np.sum((ndvi > 0) & (ndvi <= 0.5))
    bare = np.sum(ndvi <= 0)
    total = healthy + stressed + bare
    
    print(f"\n📊 Vegetation Statistics:")
    print(f"  🌱 Healthy (NDVI > 0.5): {healthy/total*100:.1f}%")
    print(f"  🟡 Stressed (0-0.5): {stressed/total*100:.1f}%")
    print(f"  🟤 Bare/Water (≤0): {bare/total*100:.1f}%")
    
    return ndvi

if __name__ == "__main__":
    red_path = "data/raw/b04_band.tif"
    nir_path = "data/raw/b08_band.tif"
    output_path = "data/processed/ndvi_output.tif"
    
    calculate_ndvi(red_path, nir_path, output_path)
