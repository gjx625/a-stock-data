import os
key = os.getenv("ANSPIRE_API_KEY")
if key:
    print("✅密钥读取成功")
else:
    print("❌没有读到密钥")
