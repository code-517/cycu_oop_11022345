import cycu11022345 
from cycu11022345.hello import hello

# 測試封裝的函式
if __name__ == "__main__":
    route_id = "0161000900"  # 測試用公車代碼
    direction = "去程"  # 測試用方向
    geojson_file = r"C:\Users\User\Desktop\1\cycu_oop_11022345\20250422\bus_stop2.geojson"
    output_image = f"matched_bus_stops_map_{route_id}_{direction}.png"
    icon_path = r"C:\Users\User\Desktop\1\cycu_oop_11022345\20250429\peo.png"
    bus_icon_path = r"C:\Users\User\Desktop\1\cycu_oop_11022345\20250429\download.png"

    # 呼叫封裝的函式
    cycu11022345.match_stations(route_id, direction, geojson_file, output_image, icon_path, bus_icon_path)