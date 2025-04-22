import geopandas as gpd

def read_geojson(file_path):
    """
    讀取 GeoJSON 檔案並返回 GeoDataFrame。
    :param file_path: GeoJSON 檔案的路徑
    :return: GeoDataFrame
    """
    gdf = gpd.read_file(file_path)
    return gdf