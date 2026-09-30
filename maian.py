code_20260930(2).py
QQ浏览器万能格式查看器
使用其他应用打开
import os
import sys
import requests
import pandas as pd
sys.path.append(os.path.dirname(__file__))
from a_stock_data import stock
# 读取安思派密钥
ANSPIRE_API_KEY = os.getenv("ANSPIRE_API_KEY")
if not ANSPIRE_API_KEY:
    print("错误：未读取到安思派API密钥，请检查仓库Secret配置")
    exit(1)
def get_stock_analysis():
    # 华能蒙电 600863，取20根日线
    df = stock.get_kline(symbol="600863", period="day", count=20)
    data_str = df.to_string()
    prompt = f"""
你是股票技术分析助手，根据下面近20个交易日K线数据，
输出：趋势判断、支撑位、压力位、SKDJ指标状态，结论简洁。
数据：
{data_str}
"""
    headers = {
        "Authorization": f"Bearer {ANSPIRE_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "anspire-search",
        "messages": [{"role": "user", "content": prompt}]
    }
    res = requests.post("https://api.anspire.com/v1/chat/completions", headers=headers, json=body)
    json_data = res.json()
    ai_result = json_data["choices"][0]["message"]["content"]
    print("====AI股票分析结果====\n")
    print(ai_result)
    return ai_result
if __name__ == "__main__":
    get_stock_analysis()
