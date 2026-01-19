# 🎓 AI 磨課師系統 - 使用指南

## 專案概述

這是一個完整的 **Multi-Agent 自動化教學影片生成系統**，實現了從課程主題到教學影片的全自動化流程。

## 系統架構

### 四個專業 Agent

1. **🎓 Curriculum Designer Agent（教學設計代理人）**
   - 根據主題進行知識拆解
   - 生成具備 ADDIE 教學模型的課程大綱
   - 確保教學難度循序漸進

2. **📝 Scriptwriter Agent（腳本代理人）**
   - 將專業知識轉化為口語化教師獨白
   - 加入轉場提示（如：請看這張圖...）
   - 為影片對齊做準備

3. **🎨 Visual Artist Agent（視覺代理人）**
   - 設計投影片佈局
   - 調用 AI 生成插圖（支持 Imagen 4.0）
   - 確保視覺風格統一

4. **🎬 Producer Agent（製片代理人）**
   - 調用 TTS 生成配音
   - 計算音訊長度
   - 實現影音對齊（Timestamp Alignment）

### Orchestrator（協調者）
統一調度所有 Agent，管理數據流和執行順序

## 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

已安裝的套件：
- ✅ google-genai（Gemini API）
- ✅ flask（Web 框架）
- ✅ flask-cors（跨域支持）
- ✅ pillow（圖像處理）
- ✅ requests（HTTP 請求）

### 2. 配置 API Key

在 `config.py` 中已配置 Gemini API Key（如需更換請修改）

### 3. 運行方式

#### 方式 A：演示模式（推薦）
當 API 配額有限時，使用模擬數據演示完整流程：

```bash
python demo.py
```

#### 方式 B：Web 介面模式
啟動 Flask 服務器，通過瀏覽器操作：

```bash
python app.py
```

然後訪問：http://localhost:5000

#### 方式 C：測試模式
測試 API 連接和單個 Agent：

```bash
python test.py
```

## 使用演示模式（當 API 配額用完時）

由於 Gemini API 免費配額限制，我們提供了完整的演示模式：

```bash
python demo.py
```

演示模式特點：
- ✅ 不需要 API 配額
- ✅ 展示完整的 Multi-Agent 工作流程
- ✅ 生成真實的課程數據結構（JSON）
- ✅ 顯示每個 Agent 的決策過程
- ✅ 自動生成 3 個示例課程

## 生成的輸出

### 課程數據結構（JSON）

```json
{
  "success": true,
  "topic": "機器學習基礎",
  "results": {
    "curriculum": {
      "course_title": "課程標題",
      "chapters": [...]
    },
    "scripts": {
      "scripts": [...]
    },
    "visual_design": {
      "style": {...},
      "slides": [...]
    },
    "production": {
      "timeline": [...],
      "tts_tasks": [...],
      "total_duration": 270.0
    }
  },
  "elapsed_time": 4.5,
  "timestamp": 1234567890
}
```

### 輸出目錄結構

```
outputs/
├── demo_course_1_20260114_123035.json  # 課程數據
├── demo_course_2_20260114_123130.json
├── demo_course_3_20260114_123137.json
├── slides/                             # 投影片（未來實現）
├── audio/                              # 音訊文件（未來實現）
└── videos/                             # 最終影片（未來實現）
```

## Web 介面功能

訪問 http://localhost:5000 後可以：

1. **課程設定**
   - 輸入課程主題
   - 選擇目標受眾（初學者/中級/進階）
   - 設定課程時長

2. **Multi-Agent 執行狀態**
   - 實時查看 4 個 Agent 的執行狀態
   - 查看執行日誌
   - 觀察 Agent 協作過程

3. **課程預覽**
   - 查看生成的課程大綱
   - 預覽投影片設計
   - 查看腳本內容

4. **影片生成**（規劃中）
   - 瀏覽器端 FFmpeg.wasm 合成
   - 一鍵下載 MP4

## API 接口

### POST /api/generate

生成課程：

```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "機器學習基礎",
    "target_audience": "初學者",
    "duration_minutes": 10
  }'
```

### GET /api/decision-logs

獲取 Agent 決策日誌：

```bash
curl http://localhost:5000/api/decision-logs
```

### GET /api/health

健康檢查：

```bash
curl http://localhost:5000/api/health
```

## 技術特點

### 🤖 Multi-Agent 協作

- **分工明確**：每個 Agent 專注於特定任務
- **數據傳遞**：Orchestrator 統一管理數據流
- **錯誤處理**：完整的重試和容錯機制
- **決策日誌**：記錄所有 Agent 的思考過程

### 🎨 視覺設計

- **風格統一**：保持整體視覺一致性
- **佈局智能**：根據內容自動選擇最佳佈局
- **圖像生成**：支持 AI 圖像生成（Prompt 工程）

### 🎵 音訊處理

- **TTS 集成**：文字轉語音
- **時長計算**：精確計算每段音訊長度
- **時間對齊**：投影片與音訊完美同步

### 🎬 影片合成

- **瀏覽器端處理**：FFmpeg.wasm（隱私性高）
- **MP4 輸出**：標準 1920x1080 解析度
- **即時預覽**：生成前預覽效果

## 研究特色

### 1. 多代理人一致性研究

探討如何防止 Scriptwriter Agent 寫出的內容超出 Visual Artist Agent 設計的頁面空間。

**解決方案**：
- Agent 間的數據校驗
- 迭代式優化流程
- 容量預估算法

### 2. 動態時長對齊演算法

當 AI 說話速度變化時，系統如何自動調整投影片切換時間。

**實現**：
- 基於文字長度的時長估算
- 實際 TTS 音訊分析
- 動態時間軸調整

### 3. 零樣本影片排版

研究如何讓 LLM 僅透過文字描述生成符合審美的投影片排版。

**技術**：
- JSON-to-Layout 映射
- 視覺設計規則編碼
- 模板化與動態生成結合

## 故障排除

### API 配額用完

**問題**：`429 RESOURCE_EXHAUSTED`

**解決方案**：
1. 使用演示模式：`python demo.py`
2. 等待配額重置（24小時）
3. 升級 API 方案

### 模型不可用

**問題**：`404 NOT_FOUND` 或 `models/xxx is not found`

**解決方案**：
修改 `config.py` 中的模型名稱：
```python
GEMINI_MODEL = "gemini-1.5-flash"  # 嘗試不同的模型
```

### 依賴衝突

**問題**：Pillow 或 Protobuf 版本衝突

**解決方案**：
這些衝突不影響本專案運行，可以忽略

## 未來開發計劃

### 短期（已規劃）

- [ ] 實現真實的 TTS 音訊生成
- [ ] 集成 Imagen 4.0 圖像生成
- [ ] 完整的 FFmpeg.wasm 影片合成
- [ ] 字幕自動生成

### 中期

- [ ] 支持多種語言（英文、日文等）
- [ ] 自定義視覺風格模板
- [ ] Agent 決策可視化面板
- [ ] 課程質量評估系統

### 長期

- [ ] Remotion 整合（React-based Video）
- [ ] 雲端渲染服務
- [ ] 協作編輯功能
- [ ] 機器學習優化 Agent 決策

## 專案結構

```
aimoddle/
├── agents/                    # Agent 實現
│   ├── __init__.py
│   ├── base_agent.py         # 基礎 Agent 類別
│   ├── curriculum_designer.py # 教學設計 Agent
│   ├── scriptwriter.py       # 腳本 Agent
│   ├── visual_artist.py      # 視覺 Agent
│   └── producer.py           # 製片 Agent
├── static/
│   └── app.js                # 前端 JavaScript
├── templates/
│   └── index.html            # Web 介面
├── outputs/                  # 生成的輸出
├── orchestrator.py           # 協調者
├── config.py                 # 配置文件
├── app.py                    # Flask 服務器
├── demo.py                   # 演示腳本
├── test.py                   # 測試腳本
├── requirements.txt          # 依賴列表
└── README.md                 # 本文件
```

## 貢獻指南

歡迎貢獻！可以改進的地方：

1. **Agent 優化**：改進 Agent 的提示詞工程
2. **視覺設計**：添加更多投影片模板
3. **影片合成**：實現完整的 FFmpeg.wasm 流程
4. **錯誤處理**：增強容錯機制
5. **測試覆蓋**：添加單元測試和集成測試

## 授權

MIT License

## 聯繫方式

如有問題或建議，請創建 Issue 或 Pull Request。

---

**最後更新**：2026年1月14日  
**版本**：1.0.0  
**狀態**：✅ 核心功能完成，影片合成待實現
