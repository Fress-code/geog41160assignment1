from pathlib import Path
import geopandas as gpd
ROOT = Path(".")
DATA = ROOT / "Data"/"CSOElectoralDivisions"
ED_SHP = DATA/"CSOED.shp"
OUTPUT =  ROOT / "Outputs"
gdf = gpd.read_file(ED_SHP)
print(gdf.head())
def add_area_km2(gdf):
    """Add polygon area in square kilometres."""
    if gdf.crs.is_geographic:
        raise ValueError("Area calculation requires a projected CRS in metres.")
    result=gdf.copy()
    result["area_km2"]=result.geometry.area/1_000_000 
    return result
gdf=add_area_km2(gdf)
print(gdf[["ED_ENGLISH", "area_km2"]].head() )
output_file =  OUTPUT / "CSOED_clean.gpkg"
gdf.to_file(output_file, driver="GPKG")
