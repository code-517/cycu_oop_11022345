def hello(name: str) -> str:
    """
    傳回一個問候語的字串。

    Args:
        name (str): 要問候的名字。

    Returns:
        str: 問候語。
    """
    return f"Hello, {name}!"

# 測試函式
if __name__ == "__main__":
    user_name = input("請輸入您的名字: ")
    print(hello(user_name))