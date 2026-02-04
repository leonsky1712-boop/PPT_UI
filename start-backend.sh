#!/bin/bash
# 启动后端 API（需先执行: pip install -r requirements.txt）
cd "$(dirname "$0")"
export PORT=${PORT:-5000}
echo "Starting backend at http://127.0.0.1:$PORT"
python3 backend/app.py
