import matplotlib.pyplot as plt
from geojson_reader import read_geojson  # 匯入第一個檔案的函式

# 1. 讀取 GeoJSON 檔案為 GeoDataFrame
geojson_file = "bus_stop2.geojson"  # 替換為您的 GeoJSON 檔案名稱
gdf = read_geojson(r'C:\Users\User\Desktop\1\cycu_oop_11022345\20250422\bus_stop2.geojson')

# 檢查資料
print(gdf.head())

# 2. 使用 matplotlib 繪製所有站點
plt.figure(figsize=(10, 10))
gdf.plot(marker='o', color='blue', markersize=5, alpha=0.7)
plt.title("Bus Stops")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True)

# 儲存圖片
plt.savefig("bus_stops_map.png", dpi=300)
print("靜態地圖已儲存為 bus_stops_map.png")
plt.show()