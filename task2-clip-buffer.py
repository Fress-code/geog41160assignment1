import geopandas as gpd
def clip_to_boundary(gdf, boundary):
    """ Clip a GeoDataFrame to a boundary polygon using a spatial intersection.
    Takes an input layer(gdf) and a boundary layer, and returns only the features that fall inside the boundary.
    Returns a new GeoDataFrame containing the clipped geometries.
"""
    gdf_ed_in_dub = gpd.overlay(gdf,boundary, how="intersection")
    print("Clipped rows:", len(gdf_ed_in_dub))
    return (gdf_ed_in_dub)

def buffer_boundary(boundary, distance_m):
    """
    Create a 500 -metre buffer around all geometries in a GeoDataFrame. 
    It's useful for expanding ED boundaries for proximity analysis or spatial joins. 
    Returns a new GeoDataFrame with the buffered geometries.
    """
    buffered_boundary = boundary.geometry.buffer(distance_m)
    result=boundary.copy()
    result.geometry = buffered_boundary
    return (result)

gdf = gpd.read_file(r"D:\GEOG41160 ASSIGNMENT\Outputs\CSOED_clean.gpkg")
boundary = gpd.read_file(r"D:\GEOG41160 ASSIGNMENT\Data\DublinCityBoundary\DublinCityBoundary.shp") 
clipped = clip_to_boundary(gdf, boundary)
buffered = buffer_boundary(boundary, 500)
clipped.to_file(r"D:\GEOG41160 ASSIGNMENT\Outputs\DublinCityED.gpkg", driver="GPKG")
buffered.to_file(r"D:\GEOG41160 ASSIGNMENT\Outputs\Dublin500mBuffer.gpkg", driver="GPKG")