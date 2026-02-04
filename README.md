# AI PPT 智能生成器

<p align="center">
  <img src="https://img.shields.io/badge/UI样式-57种-purple?style=for-the-badge" alt="UI样式">
  <img src="配色方案-95套-blue?style=for-the-badge" alt="配色方案">
  <img src="字体搭配-56组-green?style=for-the-badge" alt="字体搭配">
  <img src="Python-3.x-yellow?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.x">
</p>

<p align="center">
  <b>基于 AI 的专业 UI/UX 设计指南 + 智能演示文稿生成平台</b>
</p>

<p align="center">
  <img src="screenshots/website.png" alt="UI UX Pro Max" width="800">
</p>

---

## 项目简介

本项目是一个 AI 驱动的设计智能工具集，包含两大核心功能：

1. **UI/UX 设计指南** - 提供专业的界面设计建议、样式推荐、配色方案、字体搭配等
2. **智能 PPT 生成器** - 输入主题即可自动生成专业演示文稿，支持多种模板和输出格式

---

## 核心功能

### 设计指南功能

| 功能 | 数量 | 说明 |
|------|------|------|
| UI 样式 | 57 种 | 玻璃拟态、极简主义、赛博朋克等 |
| 配色方案 | 95 套 | 按行业分类的专业配色 |
| 字体搭配 | 56 组 | Google Fonts 字体组合 |
| 图表类型 | 24 种 | 数据可视化推荐 |
| 技术栈指南 | 11 个 | React、Vue、SwiftUI 等 |
| UX 规范 | 98 条 | 最佳实践与反模式 |
| 推理规则 | 100 条 | 行业特定设计规则 |

### PPT 生成功能

| 功能 | 说明 |
|------|------|
| 演示类型 | 商业汇报、投资路演、产品发布、培训研讨等 |
| 幻灯片版式 | 25 种专业版式 |
| 动画效果 | 35 种动画效果 |
| 输出格式 | Reveal.js HTML、PPTX、Markdown |
| 专业模板 | 4 套精心设计的主题模板 |

---

## 快速开始

### 方式一：命令行生成

```bash
# 进入脚本目录
cd .claude/skills/ui-ux-pro-max/scripts

# 生成 HTML 演示文稿
python3 search.py "2024年Q4销售回顾" \
  --presentation \
  --type business_presentation \
  --output review.html

# 生成 PPTX 文件（需要安装 python-pptx）
pip install python-pptx
python3 search.py "产品发布会" \
  --presentation \
  --type product_launch \
  --output demo.pptx
```

### 方式二：Web 界面预览

直接双击打开 `preview.html` 文件，或在浏览器中访问：

```
file:///Users/lance/Downloads/ui-ux-pro-max-skill-main/preview.html
```

### 方式三：完整前后端（推荐）

```bash
# 1. 安装后端依赖
pip install -r requirements.txt

# 2. 启动后端 API（默认 http://localhost:5000）
python backend/app.py

# 3. 另开终端，启动前端
cd frontend && npm install && npm start

# 4. 浏览器打开 http://localhost:3000，前端会请求同机 5000 端口 API
# 若前后端不同机，在 frontend/.env 中设置 REACT_APP_API_URL=http://你的后端地址:5000
```

### 方式四：Docker 部署

```bash
# 复制环境变量并修改
cp .env.example .env

# 仅启动应用与 Redis
docker-compose up -d app redis

# 访问 http://localhost:5000/api/health 检查健康
# API 文档 http://localhost:5000/api/docs
```

---

## API 与认证

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/health` | GET | 健康检查 |
| `/api/templates` | GET | 获取模板列表 |
| `/api/generate` | POST | 生成演示文稿（topic 必填） |
| `/api/auth/register` | POST | 用户注册（email, password） |
| `/api/auth/login` | POST | 用户登录 |
| `/api/presentations` | GET | 当前用户历史（需 JWT） |
| `/output/<filename>` | GET | 下载生成的 HTML |
| `/api/export/pptx` | POST | 导出为 PPTX 文件（请求体同 `/api/generate`，返回 .pptx 下载） |
| `/api/docs` | GET | Swagger API 文档 |

配置 `JWT_SECRET_KEY` 后，登录接口返回 `access_token`，请求需登录的接口时在 Header 中加：`Authorization: Bearer <access_token>`。不配置则生成接口仍可用，仅历史记录不可用。

---

## 使用示例

### 生成商业汇报

```bash
python3 search.py "季度销售总结" \
  --presentation \
  --type business_presentation \
  --audience senior_executives \
  --duration 20 \
  --output quarterly_review.html
```

### 生成投资路演

```bash
python3 search.py "AI创业项目路演" \
  --presentation \
  --type investor_pitch \
  --industry technology \
  --template modern-elegant \
  --output investor_pitch.html
```

### 生成培训课件

```bash
python3 search.py "安全意识培训" \
  --presentation \
  --type training_workshop \
  --duration 45 \
  --output training.html
```

---

## 命令行参数

### 演示文稿参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--presentation` | 启用演示文稿生成模式 | - |
| `--type` | 演示类型 | business_presentation |
| `--audience` | 目标受众 | general_employees |
| `--duration` | 预计时长（分钟） | 15 |
| `--tone` | 语调风格 | professional |
| `--industry` | 行业领域 | 空 |
| `--template` | 模板风格 | modern-elegant |
| `--output` | 输出文件路径 | stdout |
| `--presentation-format` | 输出格式 | json |

### 可用选项

**演示类型：**
- `business_presentation` - 商业汇报
- `investor_pitch` - 投资路演
- `product_launch` - 产品发布
- `training_workshop` - 培训研讨
- `webinar` - 在线讲座
- `keynote` - 主题演讲
- `sales_pitch` - 销售演示

**模板风格：**
- `modern-elegant` - 现代优雅（渐变背景）
- `corporate-blue` - 企业蓝调（商务风格）
- `minimal-clean` - 极简纯净（极简设计）
- `creative-bold` - 创意大胆（赛博朋克）

**输出格式：**
- `reveal_js` - Reveal.js HTML 幻灯片
- `pptx` - PowerPoint 文件
- `markdown` - Markdown 格式
- `json` - 原始 JSON 数据

---

## 项目结构

```
ui-ux-pro-max-skill-main/
├── .claude/                          # Claude Code 技能配置
│   └── skills/ui-ux-pro-max/
│       ├── data/                     # 数据文件
│       │   ├── *.csv               # 设计数据表
│       │   └── stacks/              # 技术栈指南
│       ├── scripts/                 # Python 脚本
│       │   ├── search.py            # 搜索入口
│       │   ├── core.py              # 核心搜索算法
│       │   ├── presentation_generator.py  # PPT 生成器
│       │   ├── slide_generator.py    # 幻灯片生成
│       │   ├── presentation_reasoning.py # 推理引擎
│       │   ├── revealjs_exporter.py # Reveal.js 导出
│       │   ├── pptx_exporter.py     # PPTX 导出
│       │   └── template_engine.py   # 模板引擎
│       └── templates/revealjs/       # PPT 模板
│           ├── modern-elegant.html
│           ├── corporate-blue.html
│           ├── minimal-clean.html
│           └── creative-bold.html
├── .shared/                         # 共享数据
├── backend/                         # Flask 后端 API
├── frontend/                        # React 前端界面
│   ├── src/
│   │   ├── App.js                 # 主应用组件
│   │   └── index.css              # 样式文件
│   └── server.js                   # 开发服务器
├── cli/                            # CLI 工具配置
├── server.js                        # 综合服务器
├── preview.html                     # 独立预览页面
├── CLAUDE.md                        # Claude Code 配置
└── README.md                        # 本文档
```

---

## 模板预览

### 1. 现代优雅 (modern-elegant)

渐变背景，现代排版，适合产品发布、创意展示。

### 2. 企业蓝调 (corporate-blue)

专业商务风格，适合企业汇报、培训研讨。

### 3. 极简纯净 (minimal-clean)

极简主义设计，适合技术分享、学术报告。

### 4. 创意大胆 (creative-bold)

赛博朋克霓虹风格，适合创意提案、年轻团队。

---

## 技术栈

### 后端
- **Python 3.x** - 核心逻辑
- **BM25 搜索算法** - 智能检索
- **Flask** - Web API（可选）

### 前端
- **React 18** - UI 框架
- **Tailwind CSS** - 样式框架
- **Framer Motion** - 动画效果

### 输出格式
- **Reveal.js** - HTML 幻灯片
- **python-pptx** - PowerPoint 文件
- **Markdown** - 文档格式

---

## 安装依赖

```bash
# 核心依赖（搜索功能需要）
pip install -r requirements.txt

# PPTX 导出需要（API 与 CLI）
pip install python-pptx
# PPTX 导出器支持：标题/副标题、正文、列表、引用、CTA、图片（本地路径或占位符）、图表（柱状/折线/饼图）

# Web 前端需要
cd frontend
npm install
```

---

## 常见问题

### Q: 生成 PPT 需要多长时间？
A: 通常 3-5 秒即可生成完成。

### Q: 生成的 HTML 文件如何分享？
A: 直接发送 HTML 文件，对方用浏览器打开即可。也可以部署到 Web 服务器分享链接。

### Q: 支持自定义模板吗？
A: 支持。可以在 `templates/revealjs/` 目录下添加自定义模板。

### Q: 能生成中文内容吗？
A: 完全支持。演示文稿生成引擎原生支持中文主题和内容。

---

## 许可证

本项目采用 MIT 许可证开源。

---

## 更新日志

### v2.1 (2024)
- 新增 AI PPT 智能生成器
- 新增 4 套专业设计模板
- 新增 Reveal.js HTML 导出
- 新增 PPTX 导出支持
- 新增 React 前端界面

### v2.0 (2024)
- 智能设计系统生成器
- 100 条行业特定推理规则
- 57 种 UI 样式
- 95 套配色方案

---

<p align="center">
  <b>Powered by AI | 快速生成专业设计</b>
</p>
# PPT_UI
# PPT_UI
