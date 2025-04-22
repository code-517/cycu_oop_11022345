#C:\Users\User\Desktop\1\bus_stops_0161000900.csv
#C:\Users\User\Desktop\1\cycu_oop_11022345\20250422\bus_stop2.geojson
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from fuzzywuzzy import process

def match_stations(csv_file, geojson_file, output_image):
    # 讀取 CSV 和 GeoJSON
    csv_data = pd.read_csv(csv_file)
    geojson_data = gpd.read_file(geojson_file)

    # 建立一個新的欄位來儲存匹配結果
    csv_data['Matched Station'] = None
    csv_data['Matched Coordinates'] = None

    # 遍歷 CSV 中的車站名稱，與 GeoJSON 中的車站名稱進行模糊匹配
    for index, row in csv_data.iterrows():
        station_name = row['車站名稱']
        geojson_names = geojson_data['BSM_CHINES'].tolist()

        # 使用 fuzzywuzzy 進行模糊匹配
        best_match, score = process.extractOne(station_name, geojson_names)
        if score >= 80:  # 設定匹配分數閾值
            matched_row = geojson_data[geojson_data['BSM_CHINES'] == best_match].iloc[0]
            csv_data.at[index, 'Matched Station'] = best_match
            csv_data.at[index, 'Matched Coordinates'] = matched_row.geometry

    # 將匹配結果轉換為 GeoDataFrame
    matched_data = csv_data.dropna(subset=['Matched Coordinates'])
    matched_data['geometry'] = matched_data['Matched Coordinates']
    matched_gdf = gpd.GeoDataFrame(matched_data, geometry='geometry')

    # 繪製地圖
    plt.figure(figsize=(10, 10))
    base = geojson_data.plot(color='lightgrey', alpha=0.5, figsize=(10, 10))
    matched_gdf.plot(ax=base, marker='o', color='red', markersize=50, label='Matched Stops')
    plt.title("Matched Bus Stops")
    plt.legend()
    plt.grid(True)

    # 儲存圖片
    plt.savefig(output_image, dpi=300)
    print(f"地圖已儲存為 {output_image}")
    plt.show()

# 主程式
if __name__ == "__main__":
    csv_file = r"C:\Users\User\Desktop\1\bus_stops_0161000900.csv"
    geojson_file = r"C:\Users\User\Desktop\1\cycu_oop_11022345\20250422\bus_stop2.geojson"
    output_image = "matched_bus_stops_map.png"

    match_stations(csv_file, geojson_file, output_image)