"""
Ollama 環境檢查和初始化腳本
"""
import subprocess
import sys
import time
import requests


def check_ollama_installed():
    """檢查 Ollama 是否已安裝"""
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ Ollama 已安裝: {result.stdout.strip()}")
            return True
        return False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("❌ Ollama 未安裝")
        print("請訪問 https://ollama.com 下載並安裝 Ollama")
        return False


def check_ollama_running():
    """檢查 Ollama 服務是否運行"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            print("✅ Ollama 服務正在運行")
            return True
        return False
    except requests.exceptions.RequestException:
        print("❌ Ollama 服務未運行")
        return False


def start_ollama_service():
    """啟動 Ollama 服務"""
    print("\n嘗試啟動 Ollama 服務...")
    print("請在另一個終端窗口運行: ollama serve")
    print("或在 Windows 上，Ollama 應該會自動啟動")
    
    # 等待用戶啟動服務
    print("\n等待 Ollama 服務啟動...")
    for i in range(30):
        time.sleep(1)
        if check_ollama_running():
            return True
        if i % 5 == 0:
            print(f"  等待中... ({i+1}/30 秒)")
    
    print("❌ Ollama 服務啟動超時")
    return False


def check_model_installed(model_name):
    """檢查指定模型是否已下載"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]
            
            # 檢查精確匹配或包含匹配
            for installed_model in model_names:
                if model_name in installed_model or installed_model in model_name:
                    print(f"✅ 模型 {model_name} 已安裝")
                    return True
            
            print(f"❌ 模型 {model_name} 未安裝")
            return False
    except Exception as e:
        print(f"⚠️ 無法檢查模型: {str(e)}")
        return False


def pull_model(model_name):
    """下載模型"""
    print(f"\n📥 開始下載模型: {model_name}")
    print(f"請運行: ollama pull {model_name}")
    print("這可能需要幾分鐘到幾十分鐘，取決於模型大小和網速...")
    
    try:
        process = subprocess.Popen(
            ["ollama", "pull", model_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 顯示下載進度
        for line in process.stdout:
            print(f"  {line.strip()}")
        
        process.wait()
        
        if process.returncode == 0:
            print(f"✅ 模型 {model_name} 下載完成")
            return True
        else:
            print(f"❌ 模型 {model_name} 下載失敗")
            return False
            
    except Exception as e:
        print(f"❌ 下載過程出錯: {str(e)}")
        return False


def setup_ollama():
    """完整的 Ollama 設置流程"""
    print("=" * 60)
    print("🚀 Ollama 環境檢查和設置")
    print("=" * 60)
    print()
    
    # 1. 檢查安裝
    if not check_ollama_installed():
        print("\n請先安裝 Ollama:")
        print("  Windows: https://ollama.com/download/windows")
        print("  macOS: https://ollama.com/download/mac")
        print("  Linux: curl -fsSL https://ollama.com/install.sh | sh")
        sys.exit(1)
    
    print()
    
    # 2. 檢查服務
    if not check_ollama_running():
        if not start_ollama_service():
            print("\n請手動啟動 Ollama:")
            print("  運行: ollama serve")
            sys.exit(1)
    
    print()
    
    # 3. 檢查必需模型
    import config
    
    required_models = set(config.OLLAMA_MODELS.values())
    print(f"📋 需要的模型: {', '.join(required_models)}")
    print()
    
    missing_models = []
    for model in required_models:
        if not check_model_installed(model):
            missing_models.append(model)
    
    # 4. 下載缺失的模型
    if missing_models:
        print(f"\n需要下載 {len(missing_models)} 個模型")
        print("推薦模型大小和用途:")
        print("  - llama3.1:8b  (~4.7GB) - 通用模型，邏輯推理強")
        print("  - gemma2:9b    (~5.5GB) - Google 開發，創意寫作好")
        print("  - qwen2.5:7b   (~4.4GB) - 中文優化，數據處理快")
        print()
        
        choice = input("是否自動下載所有缺失的模型? (y/n): ").lower()
        if choice == 'y':
            for model in missing_models:
                pull_model(model)
        else:
            print("\n請手動下載模型:")
            for model in missing_models:
                print(f"  ollama pull {model}")
            sys.exit(1)
    
    print()
    print("=" * 60)
    print("✅ Ollama 環境準備完成！")
    print("=" * 60)
    print()
    print("現在可以運行:")
    print("  python demo.py       # 演示模式")
    print("  python test_ollama.py # 測試 Ollama")
    print("  python app.py        # Web 介面")
    print()


if __name__ == "__main__":
    setup_ollama()
