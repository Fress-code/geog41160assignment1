import numpy as np
import rasterio
def monthly_mean(filepaths,scale_factor=0.0001):
    arrays =[]

    for filepath in filepaths:
        with rasterio.open(filepath) as src:
            data = src.read(1).astype(float)
            nodata = src.nodata
            profile = src.profile.copy()

            if nodata is not None:
                data[data == nodata] = np.nan

            data = data * scale_factor
            arrays.append(data)
    mean_array = np.nanmean(arrays,axis=0)
    profile.update(dtype=rasterio.float32, nodata=np.nan)
    return mean_array, profile