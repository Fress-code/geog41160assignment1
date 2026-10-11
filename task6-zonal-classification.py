import rasterio
import rasterio.mask
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

raster_path = "Outputs/AnnualMeanNDVI_2025.tif"
vector_path = "Outputs/DublinCityED.gpkg"
dublin = gpd.read_file(vector_path)
dublin = dublin.to_crs("EPSG:4326")
print("Raster CRS:", rasterio.open(raster_path).crs)
print("Dublin CRS:", dublin.crs)
with rasterio.open(raster_path) as src:
    clipped_array, clipped_transform = rasterio.mask.mask(
        src, dublin.geometry, crop=True
    )
    clipped_profile = src.profile.copy()
    clipped_profile.update({
        "height":clipped_array.shape[1],
        "width":clipped_array.shape[2],
        "transform": clipped_transform
    })
    print("Clipped raster shape:", clipped_array.shape)
    clipped_output = "Outputs/DublinCity_AnnualMeanNDVI_2025.tif"
    with rasterio.open(clipped_output, "w", **clipped_profile) as dst:
        dst.write(clipped_array)

        print("Clipped raster saved to:", clipped_output)
        print("Number of electoral divisions:", len(dublin))
with rasterio.open(clipped_output) as src:
    print("Clipped raster Nodata value:",src.nodata)
eds_path ="Outputs/DublinCityED.gpkg"
eds = gpd.read_file(eds_path)
eds = eds.to_crs("EPSG:4326")

with rasterio.open(clipped_output)as src:
    ndvi = src.read(1).astype(float)
    print("Valid NDVI pixels:", np.count_nonzero(np.isfinite(ndvi)))
    print("NDVI range:", np.nanmin(ndvi), np.nanmax(ndvi))
    transform = src.transform
mean_ndvi = []
for _, row in eds.iterrows():
    print("First ED bounds:", row.geometry.bounds)
    print("Raster bounds:", rasterio.open(clipped_output).bounds)
    geom = [row.geometry]


    mask = rasterio.features.geometry_mask(
        geom,
        transform=transform,
        invert=True,
        out_shape=ndvi.shape,
        all_touched=True
    )
    values = ndvi[mask]
    print("Selected pixels:", len(values))
    print("Valid selected pixels:", np.count_nonzero(np.isfinite(values)))
    mean_value = np.nanmean(values)
    mean_ndvi.append(mean_value)
eds["mean_ndvi"] = mean_ndvi
print("Number of EDs:", len(eds))
print("First 10 mean NDVI values:", eds["mean_ndvi"].head(10).tolist())
print("EDs with missing mean NDVI:", eds["mean_ndvi"].isna().sum())
print("EDs with valid mean NDVI:", eds["mean_ndvi"].notna().sum())
print(eds.loc[eds["mean_ndvi"].isna(), "ED_ENGLISH"].tolist())


threshold = eds["mean_ndvi"].mean()

def classify_greenness(mean_ndvi, threshold):
    if np.isnan(mean_ndvi):
        return "No Data"
    elif mean_ndvi >= threshold:
        return "High"
    else:
        return "Low"

eds["greenness"] = eds["mean_ndvi"].apply(
    lambda value: classify_greenness(value, threshold)
)

print("Classification threshold:", threshold)
print(eds["greenness"].value_counts())

fig, ax = plt.subplots(figsize=(10, 10))

eds.plot(
    column="greenness",
    categorical=True,
    legend=True,
    ax=ax,
    missing_kwds={
        "color": "lightgrey",
        "label": "No Data"
    }
)

ax.set_title("Dublin City Electoral Divisions: 2025 Mean NDVI")
ax.set_axis_off()

ax.text(
    0.5, -0.04,
    "Electoral divisions are classified as High or Low greenness using the mean of valid ED mean NDVI values.",
    transform=ax.transAxes,
    ha="center",
    wrap=True
)

plt.tight_layout()

map_path = "Outputs/DublinED_NDVI_Classification.png"
plt.savefig(map_path, dpi=300, bbox_inches="tight")
plt.close()

print("Choropleth map saved to:", map_path)