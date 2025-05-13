import asyncio
from cycu110.ebus_map import get_stop_info  # 匯入函式

if __name__ == "__main__":
    bus_id = input("請輸入公車代碼: ")  # 提示使用者輸入公車代碼
    asyncio.run(get_stop_info(bus_id))  # 執行異步函式