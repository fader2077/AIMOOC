#!/bin/bash

# AI 磨課師系統 - 快速啟動（Linux/Mac）

echo "================================================"
echo "  AI 磨課師系統 - 快速啟動"
echo "================================================"
echo ""

show_menu() {
    echo "請選擇運行模式："
    echo ""
    echo "1. 演示模式（推薦，不需要 API 配額）"
    echo "2. Web 介面模式"
    echo "3. 測試模式"
    echo "4. 檢查系統狀態"
    echo "5. 查看生成的文件"
    echo "6. 退出"
    echo ""
}

while true; do
    show_menu
    read -p "請輸入選項 (1-6): " choice
    
    case $choice in
        1)
            echo ""
            echo "================================================"
            echo "啟動演示模式..."
            echo "================================================"
            python demo.py
            read -p "按 Enter 繼續..."
            ;;
        2)
            echo ""
            echo "================================================"
            echo "啟動 Web 介面..."
            echo "訪問: http://localhost:5000"
            echo "按 Ctrl+C 停止服務器"
            echo "================================================"
            python app.py
            ;;
        3)
            echo ""
            echo "================================================"
            echo "啟動測試模式..."
            echo "================================================"
            python test.py
            read -p "按 Enter 繼續..."
            ;;
        4)
            echo ""
            echo "================================================"
            echo "系統狀態檢查"
            echo "================================================"
            echo ""
            echo "Python 版本:"
            python --version
            echo ""
            echo "已安裝的套件:"
            pip list | grep -E "google-genai|flask|pillow"
            echo ""
            echo "輸出目錄:"
            if [ -d "outputs" ]; then
                echo "  outputs/ [OK]"
            else
                echo "  outputs/ [不存在]"
            fi
            echo ""
            read -p "按 Enter 繼續..."
            ;;
        5)
            echo ""
            echo "================================================"
            echo "生成的文件"
            echo "================================================"
            if [ -d "outputs" ]; then
                ls -lh outputs/
            else
                echo "輸出目錄不存在"
            fi
            echo ""
            read -p "按 Enter 繼續..."
            ;;
        6)
            echo ""
            echo "感謝使用 AI 磨課師系統！"
            echo ""
            exit 0
            ;;
        *)
            echo "無效的選項，請重新選擇"
            echo ""
            ;;
    esac
done
