import os
import rasterio
import glob
import numpy as np
from datetime import datetime
from collections import defaultdict

data_dir = r"Data\2025Data"
ndvi_files = glob.glob(
os.path.join(data_dir, "*NDVI*.tif")
)
print("Number of NDVI files found:", len(ndvi_files))
for file in ndvi_files:
    print(os.path.basename(file))

    filename = os.path.basename(file)
    date_text = filename.split("doy")[1][:7]
        
    year = int(date_text[:4])
    day_of_year = int(date_text[4:])
        
    date = datetime.strptime(
f"{year} {day_of_year}", "%Y %j"
        ) 
        
    print(filename,"->",date.strftime("%Y-%m-%d"))  
        
    
    
    for file in ndvi_files:
           filename = os.path.basename(file)
    date_text = filename.split("doy")[1][:7]

    year = int(date_text[:4])
    day_of_year = int(date_text[4:])
    date = datetime.strptime(
            f"{year} {day_of_year}", "%Y %j"
            )
    month_key=date.strftime("%Y-%m")




def month_from_doy(year, doy):
     date = datetime.strptime(f"{year} {doy}", "%Y %j")
     return date.month

def group_files_by_month(file_list):
    monthly_files = {}

    for file in file_list:
        filename = os.path.basename(file)
        date_text = filename.split("doy")[1][:7]

        year = int(date_text[:4])
        day_of_year = int(date_text[4:])

        if year !=2025:
            continue

        month = month_from_doy(year, day_of_year)

        if month not in monthly_files:
            monthly_files[month] = []

        monthly_files[month].append(file)

    return monthly_files


print(month_from_doy(2025, 32))
monthly_files = group_files_by_month(ndvi_files)

def monthly_mean(filepaths):
    arrays =[]

    for filepath in filepaths:
        with rasterio.open(filepath) as src:
            data = src.read(1).astype(float)
            nodata = src.nodata
            profile = src.profile.copy()

            if nodata is not None:
                data[data == nodata] = np.nan

            data = data * 0.0001
            arrays.append(data)
    mean_array = np.nanmean(arrays,axis=0)
    profile.update(dtype=rasterio.float32, nodata=np.nan)
    return mean_array, profile          

for month,files in sorted(monthly_files.items()):
    print(f"Month {month}:{len(files)}files")
    mean_array, profile = monthly_mean(files)

    output_path = os.path.join("Outputs",f"NDVI_{month:02d}_2025.tif")
    with rasterio.open(output_path, "w", **profile) as dst:
        dst.write(mean_array.astype(rasterio.float32),1)
    
                
print("Checking January NoData Value:")

january_mean, january_profile = monthly_mean(monthly_files[1])
output_path = "january_mean_ndvi_2025.tif"
with rasterio.open(output_path, "w" , **january_profile) as dst:
    dst.write(january_mean.astype(rasterio.float32), 1) 
print("January mean shape:", january_mean.shape)
print("January mean minimum:", np.nanmin(january_mean))
print("January mean maximum:", np.nanmax(january_mean))
print("Checking saved raster:")
with rasterio.open(output_path) as check:
    print("Saved raster shape:", check.shape)
    print("Saved raster CRS:",check.crs)
    print("Saved raster NoData:", check.nodata)
    