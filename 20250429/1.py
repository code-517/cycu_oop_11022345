import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from fuzzywuzzy import process
from matplotlib import rcParams

# 設定中文字體
rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 使用微軟正黑體
rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

def match_stations(route_id, direction, geojson_file, output_image, icon_path, bus_icon_path):
    # 根據公車代碼讀取對應的 CSV 檔案
    csv_file = f"bus_stops_{route_id}.csv"
    csv_data = pd.read_csv(csv_file, encoding='utf-8')
    geojson_data = gpd.read_file(geojson_file)

    # 過濾方向（去程或返程）
    filtered_data = csv_data[csv_data['方向'] == direction]

    # 模糊匹配站點名稱
    filtered_data['Matched Station'] = None
    filtered_data['Matched Coordinates'] = None

    for index, row in filtered_data.iterrows():
        station_name = row['車站名稱']
        geojson_names = geojson_data['BSM_CHINES'].tolist()

        # 使用 fuzzywuzzy 進行模糊匹配
        best_match, score = process.extractOne(station_name, geojson_names)
        if score >= 80:  # 設定匹配分數閾值
            matched_row = geojson_data[geojson_data['BSM_CHINES'] == best_match].iloc[0]
            filtered_data.at[index, 'Matched Station'] = best_match
            filtered_data.at[index, 'Matched Coordinates'] = matched_row.geometry

    # 將匹配結果轉換為 GeoDataFrame
    matched_data = filtered_data.dropna(subset=['Matched Coordinates'])
    matched_data['geometry'] = matched_data['Matched Coordinates']
    matched_gdf = gpd.GeoDataFrame(matched_data, geometry='geometry')

    # 列出所有站名
    print(f"可用的站名如下（{direction}）：")
    print(matched_gdf['Matched Station'].tolist())

    # 讓使用者輸入一個站名
    target_station = input("請輸入要標記的小人站名：")
    target_match, target_score = process.extractOne(target_station, matched_gdf['Matched Station'].tolist())
    target_geometry = None

    if target_score >= 80:
        target_geometry = matched_gdf[matched_gdf['Matched Station'] == target_match].iloc[0].geometry
        print(f"已找到匹配站名：{target_match}，分數：{target_score}")
    else:
        print("未找到匹配的站名，將不繪製小人。")

    # 繪製地圖
    fig, ax = plt.subplots(figsize=(15, 15))
    geojson_data.plot(ax=ax, color='lightgrey', alpha=0.5)
    matched_gdf.plot(ax=ax, marker='o', color='red', markersize=50, label='Matched Stops')

    # 調整經緯度範圍，放大地圖間距
    x_min, x_max = matched_gdf.geometry.x.min(), matched_gdf.geometry.x.max()
    y_min, y_max = matched_gdf.geometry.y.min(), matched_gdf.geometry.y.max()
    padding = 0.01  # 增加的間距
    ax.set_xlim(x_min - padding, x_max + padding)
    ax.set_ylim(y_min - padding, y_max + padding)

    # 繪製小人和公車圖案，並標註時間
    for idx, row in matched_gdf.iterrows():
        x, y = row.geometry.x, row.geometry.y

        # 如果是目標站，繪製小人
        if row['Matched Station'] == target_match:
            img = plt.imread(icon_path)  # 小人圖案
            imagebox = OffsetImage(img, zoom=0.025)  # 縮小 2 倍
            ab = AnnotationBbox(imagebox, (x, y + 0.002), frameon=False)  # 向上偏移
            ax.add_artist(ab)

        # 如果是進站中，繪製公車圖案
        elif row['狀態'] == "進站中":
            bus_img = plt.imread(bus_icon_path)  # 公車圖案
            bus_imagebox = OffsetImage(bus_img, zoom=0.01)  # 公車圖案大小
            bus_ab = AnnotationBbox(bus_imagebox, (x - 0.003, y), frameon=False)  # 向右偏移
            ax.add_artist(bus_ab)

        # 標註其他站點的時間
        else:
            ax.text(x + 0.003, y , row['公車到達時間'], fontsize=8, color='blue')  # 向右上偏移

    plt.title(f"Matched Bus Stops ({direction})")
    plt.legend()
    plt.grid(True)

    # 儲存圖片
    plt.savefig(output_image, dpi=300)
    print(f"地圖已儲存為 {output_image}")
    plt.show()


# 主程式
if __name__ == "__main__":
    route_id = input("請輸入公車代碼: ")
    direction = input("請輸入方向（去程或返程）: ")
    geojson_file = r"C:\Users\User\Desktop\新增資料夾\cycu_oop_11022345\20250422\bus_stop2.geojson"
    output_image = f"matched_bus_stops_map_{route_id}_{direction}.png"
    icon_path = r"C:\Users\User\Desktop\新增資料夾\cycu_oop_11022345\20250429\peo.png"
    bus_icon_path = r"C:\Users\User\Desktop\新增資料夾\cycu_oop_11022345\20250429\download.png"

    match_stations(route_id, direction, geojson_file, output_image, icon_path, bus_icon_path)