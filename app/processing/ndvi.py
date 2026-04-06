import os
import numpy as np
import rasterio

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def compute_ndvi(red_path, nir_path):
    print("Computing NDVI...")

    with rasterio.open(red_path) as red_src:
        red = red_src.read(1).astype(float)

    with rasterio.open(nir_path) as nir_src:
        nir = nir_src.read(1).astype(float)
        profile = nir_src.profile

    ndvi = (nir - red) / (nir + red + 1e-10)

    output_file = os.path.join(PROCESSED_DIR, "ndvi.tif")

    profile.update(dtype=rasterio.float32)

    with rasterio.open(output_file, "w", **profile) as dst:
        dst.write(ndvi.astype(rasterio.float32), 1)

    print(f"NDVI saved: {output_file}")
    return output_file