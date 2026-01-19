# 🤖 Ollama 本地化快速指南

## 什麼是 Ollama？

Ollama 是一個在本地運行大型語言模型的工具，讓您可以：
- ✅ **完全本地化** - 無需網絡，數據不上傳
- ✅ **零 API 成本** - 不受配額限制
- ✅ **長文本處理** - 支持 8K+ token 上下文
- ✅ **多模型支持** - llama3.1, gemma2, qwen2.5 等

---

## 快速開始（3 步驟）

### 1. 安裝 Ollama

#### Windows
```bash
# 下載並安裝
https://ollama.com/download/windows
```

#### macOS
```bash
# 下載並安裝
https://ollama.com/download/mac
```

#### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. 下載模型

打開終端，運行以下命令下載推薦模型：

```bash
# 推薦組合（約 15GB 總大小）
ollama pull llama3.1:8b    # ~4.7GB - 通用模型
ollama pull gemma2:9b      # ~5.5GB - 創意寫作
ollama pull qwen2.5:7b     # ~4.4GB - 中文優化

# 或只下載一個基礎模型
ollama pull llama3.1:8b
```

**下載時間**：取決於網速，通常 5-20 分鐘

### 3. 啟動服務

```bash
# 啟動 Ollama 服務
ollama serve
```

**注意**：在 Windows 上，Ollama 安裝後通常會自動啟動

---

## 運行 AI 磨課師

### 方式 1：自動設置（推薦）

```bash
python setup_ollama.py
```

這會自動：
- ✅ 檢查 Ollama 是否安裝
- ✅ 檢查服務是否運行
- ✅ 檢查模型是否下載
- ✅ 自動下載缺失的模型

### 方式 2：測試連接

```bash
python test_ollama.py
```

這會測試：
- ✅ Ollama 基本連接
- ✅ Agent 創建
- ✅ 簡單課程生成

### 方式 3：運行演示

```bash
python demo.py
```

生成 3 個完整的示例課程！

---

## 模型選擇指南

### llama3.1 (推薦)
- **大小**: 8B (~4.7GB)
- **優勢**: 邏輯推理強，通用性好
- **適用**: Curriculum Designer, Visual Artist
- **速度**: ⭐⭐⭐⭐

### gemma2
- **大小**: 9B (~5.5GB)
- **優勢**: 創意寫作好，Google 開發
- **適用**: Scriptwriter
- **速度**: ⭐⭐⭐⭐

### qwen2.5
- **大小**: 7B (~4.4GB)
- **優勢**: 中文理解強，數據處理快
- **適用**: Producer, 中文內容生成
- **速度**: ⭐⭐⭐⭐⭐

### qwen2.5-coder
- **大小**: 7B (~4.4GB)
- **優勢**: 程式碼生成優化
- **適用**: 程式設計教學課程
- **速度**: ⭐⭐⭐⭐

---

## 配置說明

編輯 `config.py`:

```python
# 使用 Ollama 本地模式
AI_PROVIDER = "ollama"

# 針對不同 Agent 使用不同模型
OLLAMA_MODELS = {
    "curriculum": "llama3.1:8b",   # 教學設計
    "scriptwriter": "gemma2:9b",   # 腳本撰寫
    "visual": "llama3.1:8b",       # 視覺設計
    "producer": "qwen2.5:7b",      # 製片協調
    "default": "llama3.1:8b"
}
```

### 切換回 Gemini

```python
# 切換為雲端模式
AI_PROVIDER = "gemini"
```

---

## 性能優化

### 硬件需求

| 配置 | RAM | 速度 | 推薦 |
|------|-----|------|------|
| 最低 | 8GB | 慢 | 僅測試 |
| 推薦 | 16GB | 中 | ⭐⭐⭐ |
| 最佳 | 32GB+ | 快 | ⭐⭐⭐⭐⭐ |

### GPU 加速

如果您有 NVIDIA GPU：

```bash
# Ollama 會自動檢測並使用 GPU
# 速度提升 5-10 倍！
```

### 調整參數

在 `config.py` 中：

```python
OLLAMA_NUM_CTX = 8192      # 上下文長度
OLLAMA_NUM_PREDICT = 4096  # 生成長度
OLLAMA_TEMPERATURE = 0.7   # 創意程度 (0-1)
```

---

## 故障排除

### 問題 1: "連接被拒絕"

**解決方案**：
```bash
# 確認 Ollama 正在運行
ollama serve

# 或在 Windows 上檢查系統托盤
```

### 問題 2: "模型未找到"

**解決方案**：
```bash
# 檢查已安裝的模型
ollama list

# 下載缺失的模型
ollama pull llama3.1:8b
```

### 問題 3: 生成速度慢

**解決方案**：
1. 使用更小的模型（如 7B 而非 13B）
2. 減少 `OLLAMA_NUM_CTX`
3. 檢查是否有 GPU 可用
4. 關閉其他占用資源的程序

### 問題 4: CORS 錯誤（瀏覽器前端）

**解決方案**：

**Windows**:
```bash
# 設置環境變量
setx OLLAMA_ORIGINS "*"
# 重啟 Ollama
```

**macOS/Linux**:
```bash
# 啟動時設置
OLLAMA_ORIGINS="*" ollama serve
```

---

## 命令參考

### 基本命令

```bash
ollama serve              # 啟動服務
ollama list               # 列出已安裝模型
ollama pull MODEL         # 下載模型
ollama rm MODEL           # 刪除模型
ollama run MODEL          # 交互式運行模型
```

### 測試命令

```bash
# 快速測試
ollama run llama3.1:8b "你好"

# 查看模型信息
ollama show llama3.1:8b
```

---

## 與 Gemini 對比

| 特性 | Ollama 本地 | Gemini 雲端 |
|------|-------------|-------------|
| 隱私性 | ⭐⭐⭐⭐⭐ 完全本地 | ⭐⭐⭐ 上傳數據 |
| 成本 | ⭐⭐⭐⭐⭐ 免費 | ⭐⭐⭐ 有配額 |
| 速度 | ⭐⭐⭐⭐ 取決硬件 | ⭐⭐⭐⭐ 取決網絡 |
| 離線 | ⭐⭐⭐⭐⭐ 完全支持 | ❌ 需要網絡 |
| 質量 | ⭐⭐⭐⭐ 開源模型 | ⭐⭐⭐⭐⭐ Google |

---

## 進階功能

### 混合模式

在 `config.py` 中啟用：

```python
HYBRID_MODE = True
AI_PROVIDER = "ollama"       # 邏輯使用 Ollama
IMAGE_PROVIDER = "gemini"    # 圖像使用 Gemini
TTS_PROVIDER = "local"       # 語音使用本地
```

### 自定義模型

```bash
# 創建自定義模型（基於現有模型）
ollama create my-teacher -f Modelfile
```

---

## 資源鏈接

- 📖 Ollama 官方文檔: https://github.com/ollama/ollama
- 🤗 模型庫: https://ollama.com/library
- 💬 社區: https://github.com/ollama/ollama/discussions

---

## 下一步

✅ Ollama 已設置完成？運行：

```bash
python demo.py        # 生成示例課程
python test_ollama.py # 運行測試
python app.py         # 啟動 Web 介面（端口5001）
```

**Web 訪問地址**: http://127.0.0.1:5001

🎉 享受完全本地化的 AI 磨課師體驗！
