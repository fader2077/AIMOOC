# 🚀 AI 磨課師系統 - 生產環境部署指南

## ✅ 安全修復清單

本次更新解決了所有嚴重安全與架構問題：

- [x] **緊急修復**：移除硬編碼 API Keys，改用 `.env` 環境變量
- [x] **代碼清理**：統一 `base_agent.py`，刪除冗餘文件
- [x] **跨平台支持**：修復字體路徑，支持 Windows/Linux/macOS
- [x] **生產配置**：添加 WSGI 入口，支持 Gunicorn/Waitress
- [x] **依賴管理**：鎖定版本號，避免依賴衝突
- [x] **容器化**：提供 Dockerfile 和 docker-compose.yml

---

## 📋 部署前準備

### 1. 環境變量配置

```bash
# 複製環境變量模板
cp .env.example .env

# 編輯 .env 文件，填入實際值
nano .env
```

**`.env` 內容示例：**
```env
# Google Gemini API Key (可選，僅在使用 Gemini 時需要)
GEMINI_API_KEY=your_actual_api_key_here

# Ollama 配置
OLLAMA_BASE_URL=http://localhost:11434

# Flask 配置
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your_random_secret_key_32chars_min

# 端口配置
PORT=5001
```

### 2. 檢查 API Key 安全性

```bash
# 確保 .env 在 .gitignore 中
grep -q "^\.env$" .gitignore && echo "✅ .env 已被忽略" || echo "❌ 警告：.env 未在 .gitignore 中"

# 檢查是否有硬編碼的 Key
grep -r "AIzaSy" . --exclude-dir={.git,__pycache__,outputs} && echo "❌ 發現硬編碼 Key" || echo "✅ 無硬編碼 Key"
```

---

## 🐳 Docker 部署（推薦）

### 方式一：Docker Compose（最簡單）

```bash
# 啟動所有服務（包含 Ollama）
docker-compose up -d

# 查看日誌
docker-compose logs -f aimoddle

# 停止服務
docker-compose down
```

### 方式二：僅 Docker

```bash
# 構建鏡像
docker build -t aimoddle:latest .

# 運行容器
docker run -d \
  -p 5001:5001 \
  --env-file .env \
  -v $(pwd)/outputs:/app/outputs \
  --name aimoddle \
  aimoddle:latest

# 查看日誌
docker logs -f aimoddle
```

---

## 🖥️ 傳統部署（不使用 Docker）

### Linux / macOS

```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 啟動 Ollama (如果使用)
ollama serve &

# 3. 使用 Gunicorn 啟動 (生產環境)
gunicorn -w 4 \
  -b 0.0.0.0:5001 \
  --timeout 300 \
  --access-logfile - \
  --error-logfile - \
  wsgi:app
```

### Windows

```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 啟動 Ollama (在另一個終端)
ollama serve

# 3. 使用 Waitress 啟動 (生產環境)
waitress-serve --host=0.0.0.0 --port=5001 wsgi:app
```

---

## ⚙️ 系統需求

### 最低配置
- **CPU**: 4 核心
- **RAM**: 8GB (如果運行 Ollama 需要 16GB)
- **存儲**: 20GB 可用空間
- **網絡**: 音頻生成需要聯網（Edge TTS）

### 推薦配置
- **CPU**: 8 核心或以上
- **RAM**: 32GB
- **GPU**: NVIDIA GPU with CUDA (可選，加速 Ollama)
- **存儲**: 50GB SSD

---

## 🔧 進階配置

### 1. 使用 Nginx 作為反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # 長時任務超時設置
        proxy_read_timeout 600s;
        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
    }
}
```

### 2. 使用 Systemd 管理服務 (Linux)

創建 `/etc/systemd/system/aimoddle.service`：

```ini
[Unit]
Description=AI MOOC Generator
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/aimoddle
Environment="PATH=/opt/aimoddle/venv/bin"
ExecStart=/opt/aimoddle/venv/bin/gunicorn -w 4 -b 0.0.0.0:5001 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

啟動服務：
```bash
sudo systemctl enable aimoddle
sudo systemctl start aimoddle
sudo systemctl status aimoddle
```

---

## 🔒 安全檢查清單

### 部署前必須完成：

- [ ] **API Keys**：所有敏感資訊移至 `.env`
- [ ] **Debug Mode**：確保 `FLASK_DEBUG=False`
- [ ] **Secret Key**：生成強隨機密鑰 (`python -c "import secrets; print(secrets.token_hex(32))"`)
- [ ] **防火牆**：僅開放必要端口（80, 443, 5001）
- [ ] **HTTPS**：使用 Let's Encrypt 配置 SSL
- [ ] **日誌**：設置日誌輪轉（logrotate）
- [ ] **備份**：定期備份 `outputs/` 目錄

### 運行時監控：

```bash
# 檢查服務狀態
curl http://localhost:5001/health

# 監控資源使用
docker stats aimoddle  # Docker 方式
top -p $(pgrep -f gunicorn)  # 傳統方式

# 查看錯誤日誌
tail -f /var/log/aimoddle/error.log
```

---

## 📊 性能優化建議

### 1. 增加 Worker 數量

```bash
# CPU 密集型任務
gunicorn -w $((2 * $(nproc) + 1)) -b 0.0.0.0:5001 wsgi:app
```

### 2. 使用 Redis 緩存（未來）

```python
# 在 config.py 中添加
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CACHE_TTL = 3600  # 1 小時
```

### 3. 異步任務隊列（Celery）

```bash
# 安裝依賴
pip install celery redis

# 啟動 Worker
celery -A app.celery worker --loglevel=info
```

---

## 🆘 故障排除

### 問題：字體顯示為方框
**解決**：安裝中文字體
```bash
# Ubuntu/Debian
sudo apt-get install fonts-noto-cjk

# CentOS/RHEL
sudo yum install google-noto-cjk-fonts
```

### 問題：moviepy 視頻生成失敗
**解決**：確保 FFmpeg 已安裝
```bash
ffmpeg -version
# 如果未安裝：
sudo apt-get install ffmpeg  # Ubuntu
brew install ffmpeg          # macOS
```

### 問題：Ollama 連接失敗
**檢查**：
```bash
# 測試 Ollama 服務
curl http://localhost:11434/api/tags

# 查看 Ollama 日誌
journalctl -u ollama -f
```

---

## 📈 監控與日誌

### 推薦工具：
- **Prometheus + Grafana**：監控系統資源
- **ELK Stack**：日誌分析
- **Sentry**：錯誤追蹤

### 基礎監控腳本：

```bash
#!/bin/bash
# health_monitor.sh

while true; do
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/health)
    
    if [ $response -ne 200 ]; then
        echo "$(date): Service unhealthy - Response code: $response"
        # 發送告警（例如：發送郵件或 Slack 通知）
    fi
    
    sleep 60
done
```

---

## 🎓 最佳實踐

1. **定期更新依賴**：`pip list --outdated`
2. **監控磁盤空間**：`outputs/` 目錄會快速增長
3. **日誌輪轉**：避免日誌文件過大
4. **備份策略**：每日備份生成的課程文件
5. **負載測試**：使用 Locust 或 JMeter 測試系統負載

---

## 📞 技術支持

如遇到部署問題，請檢查：
1. 系統日誌：`/var/log/aimoddle/`
2. Docker 日誌：`docker logs aimoddle`
3. Health Check：`curl http://localhost:5001/health`

---

**部署完成後，訪問 `http://your-server:5001` 開始使用！** 🎉
