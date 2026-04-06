import rasterio
import matplotlib.pyplot as plt
import os
import numpy as np

def create_ndvi_map(ndvi_path, output_png="outputs/ndvi_map.png"):
    os.makedirs("outputs", exist_ok=True)
    
    if not os.path.exists(ndvi_path):
        print(f"❌ NDVI file not found: {ndvi_path}")
        return
    
    with rasterio.open(ndvi_path) as src:
        ndvi = src.read(1)
    
    # Create a clean visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # NDVI heatmap
    im1 = ax1.imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
    ax1.set_title('Vegetation Health (NDVI)', fontsize=14)
    ax1.axis('off')
    plt.colorbar(im1, ax=ax1, label='NDVI Value', shrink=0.8)
    
    # Simplified binary mask (healthy vs unhealthy)
    healthy = ndvi > 0.5
    ax2.imshow(healthy, cmap='Greens', interpolation='none')
    ax2.set_title(f'Healthy Vegetation Mask\n{np.sum(healthy)} pixels healthy', fontsize=14)
    ax2.axis('off')
    
    plt.suptitle('NDVI Vegetation Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_png, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Map saved to {output_png}")

if __name__ == "__main__":
    create_ndvi_map("data/processed/ndvi_output.tif")
