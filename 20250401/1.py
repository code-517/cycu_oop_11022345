import re
import os
from playwright.sync_api import sync_playwright

# 指定 URL
url = "https://pda5284.gov.taipei/MQS/route.jsp?rid=10417"
base_url = "https://pda5284.gov.taipei/MQS/"  # 基本網址，用於拼接完整超連結

# 使用 Playwright 渲染並抓取內容
def fetch_and_save_station_with_playwright(station, browser, output_dir):
    station_id = station["id"]
    station_url = station["link"]

    # 使用 Playwright 打開頁面
    page = browser.new_page()
    page.goto(station_url)
    page.wait_for_load_state("networkidle")  # 等待網頁完全載入
    station_html = page.content()  # 獲取渲染後的 HTML
    page.close()

    # 將內容存為 HTML 檔案
    file_path = os.path.join(output_dir, f"bus_stop_{station_id}.html")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(station_html)
    print(f"已儲存: {file_path}")

# 主程式
def main():
    # 發送 GET 請求取得 HTML 內容
    import requests
    response = requests.get(url)
    response.encoding = 'utf-8'  # 設定編碼為 UTF-8
    html_content = response.text

    # 使用正則表達式抓取去程與回程的車站名稱和超連結
    go_pattern = re.compile(r'<tr class="ttego1"><td><a href="([^"]+)">([^<]+)</a>')
    back_pattern = re.compile(r'<tr class="tteback1"><td><a href="([^"]+)">([^<]+)</a>')

    # 去程車站
    go_matches = go_pattern.findall(html_content)
    go_stations = [{"id": match[0].split('sid=')[1], "link": base_url + match[0]} for match in go_matches]

    # 回程車站
    back_matches = back_pattern.findall(html_content)
    back_stations = [{"id": match[0].split('sid=')[1], "link": base_url + match[0]} for match in back_matches]

    # 創建資料夾存放 HTML 檔案
    output_dir = "bus_stops"
    os.makedirs(output_dir, exist_ok=True)

    # 使用 Playwright 渲染並抓取內容
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # 啟動無頭瀏覽器
        for station in go_stations:
            fetch_and_save_station_with_playwright(station, browser, output_dir)
        for station in back_stations:
            fetch_and_save_station_with_playwright(station, browser, output_dir)
        browser.close()

    print(f"所有站點的 HTML 檔案已生成並存放於資料夾: {output_dir}")

if __name__ == "__main__":
    main()