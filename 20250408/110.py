import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm

def plot_lognormal_cdf(mu, sigma, x_range=(0.01, 10), num_points=500, output_file='lognormal_cdf.jpg'):
    """
    繪製對數常態累積分布函數 (CDF) 並儲存為 JPG 檔案。

    參數:
    - mu: 對數常態分布的 μ
    - sigma: 對數常態分布的 σ
    - x_range: x 軸範圍 (tuple, 預設為 (0.01, 10))
    - num_points: x 軸取樣點數 (預設為 500)
    - output_file: 輸出的 JPG 檔案名稱 (預設為 'lognormal_cdf.jpg')
    """
    # 定義 x 範圍
    x = np.linspace(x_range[0], x_range[1], num_points)

    # 計算對數常態累積分布函數 (CDF)
    cdf = lognorm.cdf(x, s=sigma, scale=np.exp(mu))

    # 繪製圖形
    plt.figure(figsize=(8, 6))
    plt.plot(x, cdf, label='Log-normal CDF', color='blue')
    plt.title('Log-normal Cumulative Distribution Function')
    plt.xlabel('x')
    plt.ylabel('CDF')
    plt.grid(True)
    plt.legend()

    # 儲存為 JPG 檔案
    plt.savefig(output_file, format='jpg')
    plt.show()
    print(f"圖形已儲存為 {output_file}")

# 主程式執行
if __name__ == "__main__":
    # 使用者輸入參數
    mu = float(input("請輸入 μ (例如 1.5): "))
    sigma = float(input("請輸入 σ (例如 0.4): "))
    plot_lognormal_cdf(mu, sigma)