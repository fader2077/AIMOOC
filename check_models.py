"""
检查可用的 Gemini 模型
"""
from google import genai
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

try:
    # 列出所有可用模型
    print("可用的模型：")
    for model in client.models.list():
        print(f"  - {model.name}")
        print(f"    支持的方法：{model.supported_generation_methods}")
        print()
except Exception as e:
    print(f"错误：{e}")
