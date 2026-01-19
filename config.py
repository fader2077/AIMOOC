"""
配置文件 - Ollama 本地化多代理人架構
"""
import os

# ========== LLM 提供商選擇 ==========
AI_PROVIDER = "ollama"  # 可選："ollama" (本地) 或 "gemini" (雲端)

# ========== Ollama 配置（本地化）==========
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_TIMEOUT = 120  # 本地推理需要更長時間

# Ollama 模型配置 - 針對不同 Agent 使用不同模型優化
OLLAMA_MODELS = {
    "curriculum": "llama3.1:8b",      # 教學設計 (邏輯推理)
    "scriptwriter": "gemma2:9b",      # 腳本撰寫 (創意寫作)
    "visual": "llama3.1:8b",          # 視覺設計 (結構化)
    "producer": "qwen2.5:7b",         # 製片協調 (數據處理)
    "default": "llama3.1:8b"          # 預設模型
}

# 生成參數
OLLAMA_TEMPERATURE = 0.7
OLLAMA_NUM_CTX = 8192      # 支持長文本處理
OLLAMA_NUM_PREDICT = 4096  # 最大生成長度

# ========== Gemini API 配置（備用）==========
GEMINI_API_KEY = "AIzaSyAePl01WRZyDMMlxG3h0zeJrimD9wDlW6I"
GEMINI_MODEL = "gemini-1.5-flash"

# ========== 混合模式配置 ==========
HYBRID_MODE = False  # 邏輯本地，圖像/語音雲端
IMAGE_PROVIDER = "local"  # "local" 或 "gemini"
TTS_PROVIDER = "local"    # "local" 或 "gemini"

# 輸出目錄
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
SLIDES_DIR = os.path.join(OUTPUT_DIR, "slides")
AUDIO_DIR = os.path.join(OUTPUT_DIR, "audio")
VIDEO_DIR = os.path.join(OUTPUT_DIR, "videos")
CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache")

# 創建必要的目錄
for directory in [OUTPUT_DIR, SLIDES_DIR, AUDIO_DIR, VIDEO_DIR, CACHE_DIR]:
    os.makedirs(directory, exist_ok=True)

# Flask 配置
# Flask 配置
DEBUG = True
HOST = "0.0.0.0"
PORT = 5001  # 改用5001端口，避免与其他服务冲突

# Agent 配置
MAX_RETRIES = 3        # API 調用重試次數
TIMEOUT = 120          # API 調用超時時間（秒）- Ollama 需要更長時間

# 性能優化
ENABLE_STREAM = True   # 啟用流式輸出
ENABLE_CACHE = False   # 啟用緩存
VERBOSE = True         # 顯示詳細日誌
