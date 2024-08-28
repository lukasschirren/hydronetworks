import rasterio
from rasterio.windows import from_bounds
import geopandas as gpd
import numpy as np

def extract_area_of_interest(dem_path, flow_path, flow_acc_path, lat, lon, buffer=0.01):
    with rasterio.open(dem_path) as dem_dataset:
        bounds = rasterio.features.bounds(lat, lon, buffer)
        window = from_bounds(*bounds, dem_dataset.transform)
        dem = dem_dataset.read(1, window=window)

    with rasterio.open(flow_path) as flow_dataset:
        flow = flow_dataset.read(1, window=window)

    with rasterio.open(flow_acc_path) as flow_acc_dataset:
        flow_acc = flow_acc_dataset.read(1, window=window)
    
    return dem, flow, flow_acc, window