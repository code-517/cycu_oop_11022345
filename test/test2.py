import asyncio
from cycu110.ebus_map2 import BusInfo  # 匯入 BusInfo 類別

async def main():
    bus_id = input("請輸入公車代碼: ")  # 提示使用者輸入公車代碼
    bus_info = BusInfo(bus_id)

    # 抓取所有車站資訊
    print("\n正在抓取所有車站資訊...")
    await bus_info.fetch_bus_stops()

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

if __name__ == "__main__":
    asyncio.run(main())