# AI 磨課師：Multi-Agent 自動化教學影片生成系統

## 專案概述

本專案實現了一個基於 Multi-Agent 系統的自動化教學影片生成平台，能夠從主題輸入到最終 MP4 影片輸出的全流程自動化。

## 系統架構

### Multi-Agent 系統
1. **Curriculum Designer Agent** - 教學設計代理人
2. **Scriptwriter Agent** - 腳本代理人
3. **Visual Artist Agent** - 視覺代理人
4. **Producer Agent** - 製片代理人
5. **Orchestrator** - 協調者

### 技術棧
- **後端**: Python, Google Gemini API
- **前端**: HTML5, JavaScript, FFmpeg.wasm
- **API**: Flask RESTful API
- **影片合成**: 瀏覽器端 FFmpeg.wasm

## 安裝與執行

### 1. 安裝依賴
```bash
pip install -r requirements.txt
```

### 2. 設定 API Key
在 `config.py` 中設定您的 Gemini API Key

### 3. 啟動服務
```bash
python app.py
```

### 4. 開啟瀏覽器
訪問 http://localhost:5000

## 功能特色

- ✅ 多代理人協作決策
- ✅ 自動課程大綱生成
- ✅ 口語化教學腳本
- ✅ AI 圖像生成
- ✅ 自動語音合成
- ✅ 瀏覽器端影片合成
- ✅ MP4 一鍵導出

## 專案結構

```
aimoddle/
├── agents/           # Agent 實現
├── static/          # 前端靜態資源
├── templates/       # HTML 模板
├── outputs/         # 生成的輸出文件
├── app.py          # Flask 應用入口
├── config.py       # 配置文件
└── requirements.txt # Python 依賴
```

## 更多文檔

- [快速開始指南](QUICKSTART.md)
- [使用說明](USAGE.md)
- [專案總結](PROJECT_SUMMARY.md)
- [完成報告](COMPLETION_REPORT.md)
- [Ollama 配置指南](OLLAMA_GUIDE.md)

## License

MIT License