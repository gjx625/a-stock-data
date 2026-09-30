import os
import requests
import smtplib
from email.mime.text import MIMEText
import warnings
warnings.filterwarnings('ignore')

# 读取环境变量
api_key = os.getenv("ANSPIRE_API_KEY")
mail_sender = os.getenv("MAIL_SENDER")
mail_pass = os.getenv("MAIL_PASS")
mail_receiver = os.getenv("MAIL_RECEIVER")

if not api_key:
    print("❌没有读到安思派密钥")
else:
    print("✅安思派密钥已加载")

url = "https://api.anspire.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

prompt = """
请分析这只股票：华能蒙电，结合SKDJ、KDJ指标，给出支撑位、压力位、短线操作思路，提示风险。
"""

payload = {
    "model": "anspire-search",
    "messages": [{"role": "user", "content": prompt}]
}

resp = requests.post(url, headers=headers, json=payload, timeout=120, verify=False)
print(f"HTTP状态码: {resp.status_code}")
print(f"接口原始返回文本:\n---\n{resp.text}\n---")

ai_result = ""
try:
    res_data = resp.json()
    ai_result = res_data["choices"][0]["message"]["content"]
    print("\n====AI分析结果====\n")
    print(ai_result)
except Exception as e:
    ai_result = f"接口解析失败，异常信息：{str(e)}，原始返回：{resp.text}"
    print(ai_result)

# 邮件推送
if mail_sender and mail_pass and mail_receiver:
    msg = MIMEText(ai_result, "plain", "utf-8")
    msg["Subject"] = "【股票AI分析】华能蒙电分析报告"
    msg["From"] = mail_sender
    msg["To"] = mail_receiver

    smtp_server = "smtp.qq.com"
    smtp_port = 465
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(mail_sender, mail_pass)
    server.send_message(msg)
    server.quit()
    print("\n✅邮件发送成功！")
else:
    print("\n⚠️邮箱密钥未配置，跳过邮件推送")
