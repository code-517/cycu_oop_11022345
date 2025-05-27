import json
from geopy.distance import geodesic
from playwright.sync_api import sync_playwright
from urllib.parse import quote

def get_coordinates(address):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 設為 False 以便調試
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = context.new_page()

        try:
            # 編碼地址
            encoded_address = quote(address)
            search_url = f"https://nominatim.openstreetmap.org/ui/search.html?q={encoded_address}"
            print(f"正在打開網址: {search_url}")
            page.goto(search_url, timeout=20000)
            page.wait_for_load_state('networkidle')  # 等待網頁完全加載

            # 等待並點擊 "details" 按鈕
            page.wait_for_selector('a.btn.btn-outline-secondary.btn-sm[href^="details.html"]', timeout=10000)
            details_link = page.locator('a.btn.btn-outline-secondary.btn-sm[href^="details.html"]').first
            details_link.click()

            # 等待跳轉到 details 頁面
            page.wait_for_selector('tr > td.svelte-1184nr4', timeout=10000)

            # 提取經緯度
            rows = page.locator('tr').all()  # 獲取所有表格行
            for row in rows:
                header = row.locator('td.svelte-1184nr4').first.inner_text()
                if "Centre Point (lat,lon)" in header:
                    lat_lon_text = row.locator('td.svelte-1184nr4:nth-child(2)').inner_text()
                    lat, lon = map(float, lat_lon_text.split(","))
                    print(f"地址: {address}")
                    print(f"經緯度: {lat}, {lon}")
                    return lat, lon

            print("未找到經緯度資訊")
            return None, None

        except Exception as e:
            print(f"發生錯誤: {e}")
            print(page.content())  # 打印頁面內容以便調試
            return None, None

        finally:
            browser.close()

def find_nearest_bus_stop(lat, lon, geojson_path):
    # 讀取 GeoJSON 檔案
    with open(geojson_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    nearest_stop = None
    nearest_distance = float('inf')

    # 遍歷所有站點
    for feature in data['features']:
        stop_coordinates = feature['geometry']['coordinates']
        stop_name = feature['properties']['BSM_CHINES']

        # 計算距離
        distance = geodesic((lat, lon), (stop_coordinates[1], stop_coordinates[0])).meters

        # 更新最近的站點
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_stop = {
                'name': stop_name,
                'distance': distance,
                'coordinates': stop_coordinates
            }

    return nearest_stop

# 主程式
if __name__ == "__main__":
    # 輸入起點和目的地地址
    start_address = input("請輸入起點地址：")
    destination_address = input("請輸入目的地地址：")

    # 從網站查詢起點經緯度
    start_lat, start_lon = get_coordinates(start_address)

    # 從網站查詢目的地經緯度
    dest_lat, dest_lon = get_coordinates(destination_address)

    if start_lat is not None and start_lon is not None and dest_lat is not None and dest_lon is not None:
        # GeoJSON 檔案路徑
        geojson_file = r"C:\Users\User\Desktop\1\cycu_oop_11022345\20250527\bus_stop2.geojson"

        # 找到起點最近的站點
        start_nearest_stop = find_nearest_bus_stop(start_lat, start_lon, geojson_file)

        # 找到目的地最近的站點
        dest_nearest_stop = find_nearest_bus_stop(dest_lat, dest_lon, geojson_file)

        if start_nearest_stop and dest_nearest_stop:
            print(f"起點最近的站點是：{start_nearest_stop['name']}")
            print(f"距離起點：{start_nearest_stop['distance']:.2f} 公尺")
            print(f"起點站點座標：{start_nearest_stop['coordinates']}")

            print(f"目的地最近的站點是：{dest_nearest_stop['name']}")
            print(f"距離目的地：{dest_nearest_stop['distance']:.2f} 公尺")
            print(f"目的地站點座標：{dest_nearest_stop['coordinates']}")

            # 計算兩個站點之間的距離
            stop_to_stop_distance = geodesic(
                (start_nearest_stop['coordinates'][1], start_nearest_stop['coordinates'][0]),
                (dest_nearest_stop['coordinates'][1], dest_nearest_stop['coordinates'][0])
            ).meters
            print(f"兩個站點之間的距離：{stop_to_stop_distance:.2f} 公尺")
        else:
            print("未找到起點或目的地的最近站點")
    else:
        print("無法取得起點或目的地的經緯度")