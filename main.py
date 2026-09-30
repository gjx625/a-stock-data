import os
import requests
import smtplib
from email.mime.text import MIMEText
import warnings
warnings.filterwarnings('ignore')

# 读取环境变量
api_key = os.getenv("ANSPIRE_API_KEY")
mail_sender = os.getenv("MAIL_SENDER")    # 发件邮箱
mail_pass = os.getenv("MAIL_PASS")        # 邮箱授权码
mail_receiver = os.getenv("MAIL_RECEIVER")# 收件邮箱

if not api_key:
    print("❌没有读到安思派密钥")
else:
    print("✅安思派密钥已加载")

# 安思派接口
url = "https://api.anspire.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 股票分析prompt，可自行更换股票
prompt = """
请分析这只股票：华能蒙电，结合SKDJ、KDJ指标，给出支撑位、压力位、短线操作思路，提示风险。
"""

payload = {
    "model": "anspire-search",
    "messages": [{"role": "user", "content": prompt}]
}

# 请求AI，关闭SSL校验
resp = requests.post(url, headers=headers, json=payload, timeout=120, verify=False)
res_data = resp.json()
ai_result = res_data["choices"][0]["message"]["content"]
print("\n====AI分析结果====\n")
print(ai_result)

# ==========发送邮件部分==========
if mail_sender and mail_pass and mail_receiver:
    msg = MIMEText(ai_result, "plain", "utf-8")
    msg["Subject"] = "【股票AI分析】华能蒙电分析报告"
    msg["From"] = mail_sender
    msg["To"] = mail_receiver

    # QQ邮箱smtp服务器
    smtp_server = "smtp.qq.com"
    smtp_port = 465
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(mail_sender, mail_pass)
    server.send_message(msg)
    server.quit()
    print("\n✅邮件发送成功！")
else:
    print("\n⚠️邮箱密钥未配置，跳过邮件推送")
