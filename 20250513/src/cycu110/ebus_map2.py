import asyncio
from playwright.async_api import async_playwright


class BusInfo:
    def __init__(self, bus_id):
        self.bus_id = bus_id
        self.stops = []  # 用於儲存所有車站的資訊

    async def fetch_bus_stops(self):
        """
        抓取此巴士的所有車站資訊（去程與返程）。
        """
        url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={self.bus_id}"

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)  # 啟動瀏覽器（非無頭模式，方便除錯）
            page = await browser.new_page()
            await page.goto(url)

            # 等待網頁載入完成
            try:
                await page.wait_for_selector("p.stationlist-come-go-c", timeout=15000)  # 等待切換按鈕出現
            except Exception as e:
                print("無法找到切換按鈕，請檢查網頁結構。")
                await browser.close()
                return []

            all_results = []

            # 點擊去程按鈕並抓取去程站點資訊
            go_button = await page.query_selector("a.stationlist-go")
            if go_button:
                await go_button.click()
                await page.wait_for_timeout(5000)  # 等待 5 秒，確保資料完全載入
                go_stops = await self.fetch_with_retry(page, "#GoDirectionRoute li .auto-list-stationlist")
                go_results = await self.extract_stops(go_stops, "去程")
                all_results.extend(go_results)
            else:
                print("無法找到去程按鈕。")

            # 點擊返程按鈕並抓取返程站點資訊
            return_button = await page.query_selector("a.stationlist-come")
            if return_button:
                await return_button.click()
                await page.wait_for_timeout(5000)  # 等待 5 秒，確保資料完全載入
                return_stops = await self.fetch_with_retry(page, "#BackDirectionRoute li .auto-list-stationlist")
                return_results = await self.extract_stops(return_stops, "返程")
                all_results.extend(return_results)
            else:
                print("無法找到返程按鈕。")

            await browser.close()

            self.stops = all_results  # 儲存所有車站資訊
            return all_results

    async def fetch_with_retry(self, page, selector, retries=3):
        for i in range(retries):
            try:
                await page.wait_for_selector(selector, timeout=15000)
                return await page.query_selector_all(selector)
            except Exception as e:
                print(f"嘗試第 {i+1} 次失敗，重試中...")
                await page.wait_for_timeout(2000)  # 等待 2 秒後重試
        print("多次嘗試後仍無法獲取資料。")
        return []

    async def extract_stops(self, stops, direction):
        results = []
        for stop in stops:
            # 抓取站點名稱
            name = await stop.query_selector(".auto-list-stationlist-place")
            name_text = await name.inner_text() if name else "未知站名"

            # 抓取到站狀態（進站時間或進站中）
            status = await stop.query_selector(".auto-list-stationlist-position")
            status_text = await status.inner_text() if status else "無資料"

            # 抓取站點編號
            stop_id = await stop.query_selector("input#item_UniStopId")
            stop_id_value = await stop_id.get_attribute("value") if stop_id else "未知編號"

            # 抓取緯度
            latitude = await stop.query_selector("input#item_Latitude")
            latitude_value = await latitude.get_attribute("value") if latitude else "未知緯度"

            # 抓取經度
            longitude = await stop.query_selector("input#item_Longitude")
            longitude_value = await longitude.get_attribute("value") if longitude else "未知經度"

            # 抓取站點序號
            number = await stop.query_selector(".auto-list-stationlist-number")
            number_text = await number.inner_text() if number else "未知序號"

            results.append({
                "方向": direction,
                "公車到達時間": status_text.strip() if status_text.strip() else "無資料",
                "車站序號": number_text.strip(),
                "車站名稱": name_text.strip(),
                "車站編號": stop_id_value.strip(),
                "經緯度座標": f"{latitude_value.strip()},{longitude_value.strip()}"
            })
        return results

    def get_all_stops(self):
        """
        回傳此巴士的所有車站資訊。
        """
        return self.stops

    def get_stop_name(self, stop_id):
        """
        根據站點 ID 回傳站點名稱與位置資訊。
        """
        for stop in self.stops:
            if stop["車站編號"] == stop_id:
                return {
                    "車站名稱": stop["車站名稱"],
                    "經緯度座標": stop["經緯度座標"]
                }
        return {"車站名稱": "未知站名", "經緯度座標": "未知座標"}

    def get_arrival_time_info(self, stop_id):
        """
        模擬回傳巴士到達時間（分鐘）。
        """
        # 模擬資料，實際應從 API 或其他來源獲取
        return {"車站編號": stop_id, "到達時間": "5 分鐘"}


# 測試區塊
if __name__ == "__main__":
    bus_id = input("請輸入公車代碼: ")  # 提示使用者輸入公車代碼
    bus_info = BusInfo(bus_id)

    # 抓取所有車站資訊
    asyncio.run(bus_info.fetch_bus_stops())

    # 列出所有車站
    print("\n所有車站資訊：")
    for stop in bus_info.get_all_stops():
        print(stop)

    # 測試取得特定站點名稱與位置
    test_stop_id = input("\n請輸入要查詢的站點 ID: ")
    stop_info = bus_info.get_stop_name(test_stop_id)
    print(f"站點資訊：{stop_info}")

    # 測試取得到達時間
    arrival_info = bus_info.get_arrival_time_info(test_stop_id)
    print(f"到達時間資訊：{arrival_info}")