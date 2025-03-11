import pandas as pd

# 使用雙反斜杠
df = pd.read_excel('C:\\Users\\User\\Desktop\\cycu_oop_11022345\\20250311\\311.xlsx')

df["sum"] = df['x'] + df['y']

print(df['sum'])