import subprocess
import os

def run_ingestion():
    print("=" * 50)
    print("Step 1: Downloading satellite imagery...")
    print("=" * 50)
    subprocess.run(["python", "app/ingestion/fetch_sentinel.py"])
    print("\n")

def run_processing():
    print("=" * 50)
    print("Step 2: Calculating NDVI...")
    print("=" * 50)
    subprocess.run(["python", "app/processing/ndvi_calculator.py"])
    print("\n")

def run_visualization():
    print("=" * 50)
    print("Step 3: Generating vegetation map...")
    print("=" * 50)
    subprocess.run(["python", "app/processing/visualize.py"])
    print("\n")

if __name__ == "__main__":
    print("\n🚀 Starting NDVI Vegetation Monitoring Pipeline\n")
    
    run_ingestion()
    run_processing()
    run_visualization()
    
    print("✅ Pipeline complete!")
    print("📊 Check outputs/ndvi_map.png for vegetation health map")
