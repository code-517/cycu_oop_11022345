import asyncio
from op import fetch_bus_stops  # 匯入 2.py 中的函式

if __name__ == "__main__":
    route_id = input("請輸入公車代碼: ")
    asyncio.run(fetch_bus_stops(route_id))  # 呼叫 2.py 中的函式