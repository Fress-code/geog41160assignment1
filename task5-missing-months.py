import os
import rasterio
import numpy as np
import glob
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),"Scripts1"))
from ndvi_helpers import monthly_mean

input_dir = "Outputs"
output_dir = "Outputs"

monthly_files = sorted(glob.glob(os.path.join(input_dir, "NDVI_??_2025.TIF")))
print("Number of monthly files found:", len(monthly_files))
monthly_files = monthly_files[:10]
print("Monthly files used:", monthly_files)
for filepath in monthly_files:
    with rasterio.open(filepath) as src:
        print(os.path.basename(filepath),np.nanmean(src.read(1)))

annual_mean_10 , profile = monthly_mean(monthly_files,scale_factor=1.0)
profile.update(dtype=rasterio.float32,nodata=np.nan)
output_path = os.path.join(output_dir, "AnnualMean10MonthsNDVI_2025.tif")
with rasterio.open(output_path, "w", **profile) as dst:
    dst.write(annual_mean_10.astype(rasterio.float32),1)
print("10-month meanNDVI saved to:", output_path)                
with rasterio.open("Outputs/AnnualMeanNDVI_2025.tif") as src:
    annual_12 = src.read(1).astype(float)
    if src.nodata is not None:
        annual_12[annual_12 == src.nodata] = np.nan
        mean_12 = np.nanmean( annual_12)
with rasterio.open("Outputs/AnnualMean10MonthsNDVI_2025.tif") as src:
            annual_10 = src.read(1).astype(float)
            if src.nodata is not None:
                 annual_10[annual_10 == src.nodata] =np.nan
mean_10 = np.nanmean( annual_10)
print("10-month raster shape:", annual_10.shape)
print("10-month raster valid pixels:",np.count_nonzero(~np.isnan(annual_10)))
change = mean_10 - mean_12
print("12-month file:", os.path.getsize("Outputs/AnnualMeanNDVI_2025.tif"))
print("10-month file:", os.path.getsize("Outputs/AnnualMean10MonthsNDVI_2025.tif"))
difference_array = annual_10 - annual_12
print("Largest pixel difference:", np.nanmax(np.abs(difference_array)))
print("10-month raster minimum:", np.nanmin(annual_10))
print("10-month raster maximum:",np.nanmax(annual_10))
print("12-month mean NDVI:", mean_12)
print("10-month mean NDVI",mean_10)
print("Change (10-month minus 12-month):", change)

#My results show that the ten‑month mean NDVI is about 0.011 higher than the twelve‑month mean,
#  which tells us that removing two months increased the overall annual average in this dataset. 
# However, this difference alone does not prove that November and December 
# necessarily have lower NDVI than the other months—it only shows what happened when
#  those two specific months were excluded.
#  The potential bias comes from the fact that dropping any months,
#  especially if they differ systematically from the rest of the year,
#  can make the annual estimate less representative of the full seasonal cycle.
#  If the omitted months tend to have lower NDVI, the annual mean will be biased upward;
#  if they tend to have higher NDVI, it will be biased downward.
#  This result illustrates that the annual mean is sensitive to missing data, 
# but the exact direction and cause of the bias depend on the vegetation values 
# in the months that are left out.