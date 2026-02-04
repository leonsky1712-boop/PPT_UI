#!/bin/bash
# 启动前端（需先执行: cd frontend && npm install）
cd "$(dirname "$0")/frontend"
echo "Starting frontend at http://localhost:3000"
echo "Ensure backend is running at http://localhost:5000 (or set REACT_APP_API_URL in .env)"
npm start
