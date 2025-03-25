import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib import rcParams

def plot_exchange_rate(csv_path):
    try:
        # 設定字型以支援中文
        rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 使用微軟正黑體
        rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

        # 讀取 CSV 檔案
        df = pd.read_csv(csv_path, encoding='utf-8')

        # 將日期格式從 20250325 轉換為 2025-3-25，並排序
        df['資料日期'] = pd.to_datetime(df['資料日期'], format='%Y%m%d')
        df = df.sort_values(by='資料日期', ascending=False)  # 按日期降序排列

        # 將日期格式化為 2025-3-25
        df['資料日期'] = df['資料日期'].dt.strftime('%Y-%m-%d')

        # 提取資料日期、現金買與現金賣欄位
        dates = df['資料日期']
        cash_buy = df['現金買']  # 現金買價格
        cash_sell = df['現金賣']  # 現金賣價格

        # 繪製圖表
        plt.figure(figsize=(10, 6))
        plt.plot(dates, cash_buy, label='現金買', marker='o')
        plt.plot(dates, cash_sell, label='現金賣', marker='x')
        plt.xlabel('資料日期')
        plt.ylabel('匯率')
        plt.title('現金買與現金賣匯率（從 12 月到 3 月）')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Error processing the file: {e}")

if __name__ == "__main__":
    # 動態生成 CSV 檔案路徑
    base_dir = os.path.dirname(__file__)
    csv_file_path = os.path.join(base_dir, "ExchangeRate@202503251851.csv")
    plot_exchange_rate(csv_file_path)