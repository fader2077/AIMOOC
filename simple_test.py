"""
简单测试 - 测试基本的 Gemini API 调用
"""
from google import genai

# 使用提供的 API Key
api_key = "AIzaSyAePl01WRZyDMMlxG3h0zeJrimD9wDlW6I"
client = genai.Client(api_key=api_key)

try:
    # 尝试简单的内容生成
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents="請用一句話說明 AI 是什麼",
    )
    print("✅ API 调用成功！")
    print(f"回应：{response.text}")
except Exception as e:
    print(f"❌ 错误：{e}")
    print("\n尝试使用不同的模型...")
    
    # 尝试其他模型
    models_to_try = [
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash",
        "gemini-pro",
        "gemini-flash-1.5"
    ]
    
    for model in models_to_try:
        try:
            print(f"\n尝试模型：{model}")
            response = client.models.generate_content(
                model=model,
                contents="Hello",
            )
            print(f"✅ 模型 {model} 可用！")
            print(f"回应：{response.text}")
            break
        except Exception as e2:
            print(f"❌ 模型 {model} 失败：{str(e2)[:100]}")
