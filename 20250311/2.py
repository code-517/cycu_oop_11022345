import pandas as pd
import matplotlib.pyplot as plt

def read_and_plot_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        x = df['x']
        y = df['y']
        
        plt.plot(x, y, marker='o')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('X vs Y')
        plt.grid(True)
        plt.show()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

if __name__ == "__main__":
    excel_file_path = "C:\\Users\\User\\Desktop\\cycu_oop_11022345\\20250311\\311.xlsx"  # 替換為實際的 Excel 檔案路徑
    read_and_plot_excel(excel_file_path)