import datetime
from lunarcalendar import Converter, Solar, Lunar

# 定義星期和月份的列表
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# 生肖列表
zodiacs = ['Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake', 'Horse', 'Goat', 'Monkey', 'Rooster', 'Dog', 'Pig']

# 輸入日期
date_input = input("Please enter a date (format: YYYY-MM-DD): ")

# 將輸入的日期轉換為 datetime 對象
date_object = datetime.datetime.strptime(date_input, "%Y-%m-%d")

# 獲取星期幾
weekday = weekdays[date_object.weekday()]

# 獲取農曆日期
solar = Solar(date_object.year, date_object.month, date_object.day)
lunar = Converter.Solar2Lunar(solar)

# 獲取生肖
zodiac = zodiacs[(lunar.year - 4) % 12]

# 輸出結果
print(f"{date_input} is a {weekday}")
print(f"The lunar year for {date_input} is {lunar.year}, and the zodiac sign is {zodiac}")