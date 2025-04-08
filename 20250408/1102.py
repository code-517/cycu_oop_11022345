from datetime import datetime
from math import floor

def calculate_julian_date(input_time):
    """
    計算輸入時間的星期幾以及至今經過的太陽日數 (Julian date)。
    
    :param input_time: str, 格式為 "YYYY-MM-DD HH:MM" (例如 "2020-04-15 20:30")
    :return: tuple, (星期幾, 經過的太陽日數)
    """
    # 解析輸入時間
    input_datetime = datetime.strptime(input_time, "%Y-%m-%d %H:%M")
    
    # 計算該天是星期幾
    weekday = input_datetime.strftime("%A")  # 星期幾 (英文)
    
    # 計算 Julian date
    julian_start = datetime(4713, 1, 1, 12)  # Julian date 起始點 (公元前 4713 年 1 月 1 日 12:00)
    delta_days = (input_datetime - julian_start).total_seconds() / 86400  # 轉換為天數
    julian_date = 2400000.5 + delta_days  # Julian date 的計算公式
    
    # 計算至今的太陽日數
    now = datetime.now()
    delta_days_now = (now - input_datetime).total_seconds() / 86400  # 轉換為天數
    
    return weekday, delta_days_now

# 讓使用者輸入時間
input_time = input("請輸入時間 (格式為 YYYY-MM-DD HH:MM，例如 2020-04-15 20:30)： ")
weekday, elapsed_days = calculate_julian_date(input_time)
print(f"輸入時間為：{input_time}")
print(f"該天是：{weekday}")
print(f"至今經過的太陽日數為：{elapsed_days:.6f}")