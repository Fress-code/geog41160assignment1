import os
import rasterio
import numpy as np
import glob
import sys
sys.path.append("Scripts1")
from ndvi_helpers import monthly_mean

input_dir = "Outputs"
output_dir = "Outputs"

monthly_files = sorted(glob.glob(os.path.join(input_dir, "NDVI_??_2025.tif")))
print("Number of monthly files found:", len(monthly_files))


arrays = []
for filepath in monthly_files:
     with rasterio.open(filepath) as src:
        data = src.read(1).astype(float)
        nodata = src.nodata
        profile = src.profile.copy()
        if nodata is not None:
           data[data == nodata] = np.nan
        arrays.append(data)
annual_mean,profile = monthly_mean(monthly_files, scale_factor=1.0)
print("Monthly files used:",monthly_files)

profile.update(dtype=rasterio.float32, nodata=np.nan)
output_path = os.path.join(output_dir, "AnnualMeanNDVI_2025.tif")
with rasterio.open(output_path, "w", **profile)as dst:
    dst.write(annual_mean.astype(rasterio.float32),1)
print("Annual mean NDVI saved to:",output_path)    