# 🚀 快速開始指南

## 專案已完成！✅

所有檢查通過，專案已準備就緒。

---

## 立即體驗

### 方式 1：演示模式（推薦）⭐

最快速的體驗方式，無需 API 配額：

```bash
python demo.py
```

**這會做什麼？**
- 自動生成 3 個示例課程
- 展示完整的 Multi-Agent 工作流程
- 輸出結構化的課程數據（JSON）
- 顯示每個 Agent 的執行過程

**預期輸出：**
```
🚀 AI 磨課師系統啟動（演示模式）
📚 主題：Python 程式設計入門
...
✅ 所有 Agent 執行完成！耗時：4.00 秒
```

---

### 方式 2：Web 介面

啟動完整的 Web 應用：

```bash
python app.py
```

然後訪問：**http://localhost:5000**

**功能：**
- 🎨 現代化的用戶介面
- 📝 課程參數設置
- 🤖 Agent 執行狀態可視化
- 📊 實時日誌查看
- 💾 課程數據下載

---

### 方式 3：使用啟動腳本

#### Windows:
```bash
start.bat
```

#### Linux/Mac:
```bash
chmod +x start.sh
./start.sh
```

提供互動式選單，選擇運行模式。

---

## 查看生成的結果

演示完成後，查看生成的課程數據：

```bash
cd outputs
dir  # Windows
ls   # Linux/Mac
```

你會看到：
- `demo_course_1_*.json` - Python 程式設計入門
- `demo_course_2_*.json` - 機器學習基礎
- `demo_course_3_*.json` - 深度學習與神經網路

用任何文本編輯器打開這些 JSON 文件，查看完整的課程結構。

---

## 驗證專案

確認所有功能正常：

```bash
python verify.py
```

應該看到所有檢查都通過 ✅

---

## 專案結構一覽

```
aimoddle/
├── agents/              # 4個專業 Agent
├── templates/           # Web 介面
├── static/             # 前端資源
├── outputs/            # 生成的課程
│   ├── demo_course_1_*.json
│   ├── demo_course_2_*.json
│   └── demo_course_3_*.json
├── app.py              # Flask 服務器
├── demo.py             # 演示腳本 ⭐
├── orchestrator.py     # 協調者
└── config.py           # 配置
```

---

## API 配額問題？

如果遇到 `429 RESOURCE_EXHAUSTED` 錯誤：

1. **使用演示模式**（推薦）
   ```bash
   python demo.py
   ```
   
2. **等待配額重置**（24小時）

3. **修改模型**
   編輯 `config.py`：
   ```python
   GEMINI_MODEL = "gemini-1.5-flash"  # 嘗試不同模型
   ```

---

## 詳細文檔

- [README.md](README.md) - 專案概述
- [USAGE.md](USAGE.md) - 完整使用指南
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 專案總結報告

---

## 示例輸出

### 課程大綱
```json
{
  "course_title": "Python 程式設計入門 - 完整教學",
  "target_audience": "初學者",
  "chapters": [
    {
      "chapter_number": 1,
      "title": "導論與基礎概念",
      "key_points": ["定義", "歷史發展", "應用領域"]
    }
  ]
}
```

### Agent 執行日誌
```
【階段 1/4】教學設計
🎓 Curriculum Designer 正在設計課程大綱...
✅ 課程大綱生成完成

【階段 2/4】腳本撰寫
📝 Scriptwriter 正在撰寫教學腳本...
✅ 教學腳本生成完成

【階段 3/4】視覺設計
🎨 Visual Artist 正在設計投影片...
✅ 投影片設計完成

【階段 4/4】製片協調
🎬 Producer 正在規劃製片方案...
✅ 製片方案完成
```

---

## 系統要求

- ✅ Python 3.x
- ✅ google-genai 套件
- ✅ Flask 和相關依賴
- ✅ 約 50MB 磁碟空間

---

## 常見問題

### Q: 需要 Gemini API Key 嗎？
**A:** 演示模式不需要！實際使用需要（已在 config.py 中配置）

### Q: 生成一個課程需要多久？
**A:** 演示模式約 4 秒，實際 API 調用約 30-60 秒

### Q: 可以修改課程主題嗎？
**A:** 可以！編輯 `demo.py` 中的 `topics` 列表，或使用 Web 介面

### Q: 生成的課程可以用於教學嗎？
**A:** 可以作為參考，但建議人工審核和調整

---

## 下一步

1. ✅ **運行演示** - `python demo.py`
2. 📖 **閱讀文檔** - 查看 USAGE.md
3. 🌐 **啟動 Web** - `python app.py`
4. 🎨 **自定義主題** - 修改 demo.py
5. 🚀 **擴展功能** - 添加新的 Agent

---

## 獲得幫助

- 查看錯誤日誌
- 運行 `python verify.py`
- 閱讀 USAGE.md 的故障排除章節

---

## 🎉 開始探索吧！

現在就運行：
```bash
python demo.py
```

享受 AI 驅動的自動化教學內容生成！

---

**最後更新**：2026-01-14  
**版本**：1.0.0  
**狀態**：✅ 生產就緒
