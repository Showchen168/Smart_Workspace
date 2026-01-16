#!/bin/bash

echo "===================================="
echo "   智能工作台 (Smart Workspace)"
echo "===================================="
echo ""

# 檢查 Python 是否安裝
if ! command -v python3 &> /dev/null; then
    echo "[錯誤] 找不到 Python，請先安裝 Python 3.8+"
    exit 1
fi

# 檢查 .env 檔案
if [ ! -f .env ]; then
    echo "[警告] 找不到 .env 檔案"
    echo "正在從 .env.example 建立..."
    cp .env.example .env
    echo ""
    echo "[重要] 請編輯 .env 檔案，填入你的 GEMINI_API_KEY"
    echo ""
    read -p "按 Enter 繼續..."
fi

# 檢查依賴是否安裝
echo "檢查依賴套件..."
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[提示] 正在安裝依賴套件..."
    pip3 install -r requirements.txt
fi

# 啟動應用
echo ""
echo "正在啟動智能工作台..."
echo ""
python3 app.py
