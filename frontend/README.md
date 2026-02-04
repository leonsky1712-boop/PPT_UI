# AI PPT Generator - Frontend

精美的 React 前端界面，用于 AI 演示文稿生成器。

## 功能特点

- 现代化 UI 设计
- 三步式操作流程
- 多种模板选择
- 实时预览功能
- 响应式布局

## 安装和运行

### 前置条件

- Node.js 16+
- npm 或 yarn

### 安装依赖

```bash
cd frontend
npm install
```

### 启动开发服务器

```bash
npm start
```

应用将在 http://localhost:3000 打开

### 构建生产版本

```bash
npm run build
```

## 项目结构

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── App.js           # 主应用组件
│   ├── index.js         # 入口文件
│   └── index.css        # 样式文件
├── package.json
└── README.md
```

## 集成后端

默认情况下，前端使用模拟数据。如需连接真实后端：

1. 启动后端服务：`python backend/app.py`
2. 修改 `App.js` 中的 API 调用地址

## 技术栈

- React 18
- Tailwind CSS 3
- Framer Motion（动画效果）
- Axios（HTTP 请求）
