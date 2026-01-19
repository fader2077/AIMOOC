@echo off
echo ================================================
echo   AI 磨課師系統 - 快速啟動
echo ================================================
echo.

:menu
echo 請選擇運行模式：
echo.
echo 1. 演示模式（推薦，不需要 API 配額）
echo 2. Web 介面模式
echo 3. 測試模式
echo 4. 檢查系統狀態
echo 5. 查看生成的文件
echo 6. 退出
echo.
set /p choice="請輸入選項 (1-6): "

if "%choice%"=="1" goto demo
if "%choice%"=="2" goto web
if "%choice%"=="3" goto test
if "%choice%"=="4" goto status
if "%choice%"=="5" goto files
if "%choice%"=="6" goto end

echo 無效的選項，請重新選擇
echo.
goto menu

:demo
echo.
echo ================================================
echo 啟動演示模式...
echo ================================================
python demo.py
echo.
pause
goto menu

:web
echo.
echo ================================================
echo 啟動 Web 介面...
echo 訪問: http://localhost:5000
echo 按 Ctrl+C 停止服務器
echo ================================================
python app.py
echo.
pause
goto menu

:test
echo.
echo ================================================
echo 啟動測試模式...
echo ================================================
python test.py
echo.
pause
goto menu

:status
echo.
echo ================================================
echo 系統狀態檢查
echo ================================================
echo.
echo Python 版本:
python --version
echo.
echo 已安裝的套件:
pip list | findstr "google-genai flask pillow"
echo.
echo 輸出目錄:
if exist outputs (
    echo   outputs/ [OK]
) else (
    echo   outputs/ [不存在]
)
echo.
pause
goto menu

:files
echo.
echo ================================================
echo 生成的文件
echo ================================================
if exist outputs (
    dir /b outputs
) else (
    echo 輸出目錄不存在
)
echo.
pause
goto menu

:end
echo.
echo 感謝使用 AI 磨課師系統！
echo.
pause
