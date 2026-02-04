#!/usr/bin/env node
/**
 * PPT Generator - 综合服务器
 * 
 * 功能:
 * 1. 提供前端页面
 * 2. 提供 API 接口生成演示文稿
 * 3. 预览生成的 HTML 文件
 * 
 * 运行: node server.js
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

// 配置
const PORT = process.env.PORT || 8080;
const FRONTEND_DIR = path.join(__dirname, 'frontend', 'public');
const OUTPUT_DIR = path.join(__dirname, 'output');
const TEMPLATES_DIR = path.join(__dirname, '.claude', 'skills', 'ui-ux-pro-max', 'templates', 'revealjs');
const SCRIPTS_DIR = path.join(__dirname, '.claude', 'skills', 'ui-ux-pro-max', 'scripts');

// 确保输出目录存在
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// MIME 类型映射
const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2'
};

// 生成唯一 ID
function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
}

// 生成演示文稿
async function generatePresentation(options) {
  return new Promise((resolve, reject) => {
    const python = spawn('python3', [
      path.join(SCRIPTS_DIR, 'search.py'),
      options.topic,
      '--presentation',
      '--type', options.type || 'business_presentation',
      '--audience', options.audience || 'general_employees',
      '--duration', String(options.duration || 15),
      '--tone', options.tone || 'professional',
      '--industry', options.industry || '',
      '--output', path.join(OUTPUT_DIR, `presentation_${generateId()}.html`),
      '--presentation-format', 'reveal_js'
    ], {
      cwd: SCRIPTS_DIR
    });

    let stdout = '';
    let stderr = '';

    python.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    python.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    python.on('close', (code) => {
      if (code === 0) {
        // 查找生成的 HTML 文件
        const files = fs.readdirSync(OUTPUT_DIR)
          .filter(f => f.startsWith('presentation_') && f.endsWith('.html'))
          .sort()
          .reverse();
        
        if (files.length > 0) {
          resolve({
            success: true,
            url: `/output/${files[0]}`,
            filename: files[0]
          });
        } else {
          resolve({
            success: false,
            error: '生成失败，未找到输出文件'
          });
        }
      } else {
        resolve({
          success: false,
          error: stderr || '生成失败'
        });
      }
    });
  });
}

// 处理请求
async function handleRequest(req, res) {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  const pathname = url.pathname;

  console.log(`${new Date().toISOString()} ${req.method} ${pathname}`);

  // CORS 头
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // API 路由
  if (pathname === '/api/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok', message: 'PPT Generator Server' }));
    return;
  }

  if (pathname === '/api/templates') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      templates: [
        { id: 'modern-elegant', name: '现代优雅', description: '渐变背景，现代排版，适合产品发布', preview: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
        { id: 'corporate-blue', name: '企业蓝调', description: '专业商务风格，适合企业汇报', preview: 'linear-gradient(180deg, #1a365d 0%, #2b6cb0 100%)' },
        { id: 'minimal-clean', name: '极简纯净', description: '极简主义设计，适合技术分享', preview: '#ffffff' },
        { id: 'creative-bold', name: '创意大胆', description: '赛博朋克风格，适合创意提案', preview: 'linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%)' }
      ]
    }));
    return;
  }

  if (pathname === '/api/presentation-types') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      types: [
        { id: 'business_presentation', name: '商业汇报', icon: '📊', desc: '季度总结、进度汇报' },
        { id: 'investor_pitch', name: '投资路演', icon: '🎯', desc: '创业融资、VC 演示' },
        { id: 'product_launch', name: '产品发布', icon: '🚀', desc: '新品发布、功能介绍' },
        { id: 'training_workshop', name: '培训研讨', icon: '📚', desc: '企业培训、工作坊' },
        { id: 'webinar', name: '在线讲座', icon: '🎥', desc: '网络研讨会、直播' },
        { id: 'keynote', name: '主题演讲', icon: '🎤', desc: '会议演讲、论坛' },
        { id: 'sales_pitch', name: '销售演示', icon: '💰', desc: '客户提案、商务洽谈' }
      ]
    }));
    return;
  }

  if (pathname === '/api/audiences') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      audiences: [
        { id: 'general_employees', name: '普通员工', icon: '👥' },
        { id: 'senior_executives', name: '高管领导', icon: '👔' },
        { id: 'investors', name: '投资人士', icon: '💼' },
        { id: 'clients', name: '客户伙伴', icon: '🤝' },
        { id: 'technical_team', name: '技术团队', icon: '💻' },
        { id: 'students', name: '学生群体', icon: '🎓' }
      ]
    }));
    return;
  }

  if (pathname === '/api/generate' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', async () => {
      try {
        const options = JSON.parse(body);
        
        if (!options.topic) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ success: false, error: '请输入演示主题' }));
          return;
        }

        const result = await generatePresentation(options);
        
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(result));
      } catch (e) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, error: e.message }));
      }
    });
    return;
  }

  if (pathname.startsWith('/output/')) {
    const filename = path.basename(pathname);
    const filePath = path.join(OUTPUT_DIR, filename);
    
    if (fs.existsSync(filePath)) {
      const ext = path.extname(filename).toLowerCase();
      res.writeHead(200, { 'Content-Type': MIME_TYPES[ext] || 'text/html' });
      res.end(fs.readFileSync(filePath));
    } else {
      res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end('<h1>404 - 文件未找到</h1>');
    }
    return;
  }

  // 前端静态文件
  let filePath;
  if (pathname === '/' || pathname === '/index.html') {
    filePath = path.join(FRONTEND_DIR, 'index.html');
  } else {
    filePath = path.join(FRONTEND_DIR, pathname);
  }

  const ext = path.extname(filePath).toLowerCase();
  
  if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    res.writeHead(200, { 'Content-Type': MIME_TYPES[ext] || 'application/octet-stream' });
    res.end(fs.readFileSync(filePath));
  } else {
    res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(`
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>PPT Generator</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      max-width: 800px;
      margin: 50px auto;
      padding: 20px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      color: white;
    }
    h1 { font-size: 2.5em; margin-bottom: 20px; }
    p { font-size: 1.2em; opacity: 0.9; }
    .links { margin-top: 30px; }
    a {
      display: inline-block;
      padding: 15px 30px;
      margin: 10px;
      background: rgba(255,255,255,0.2);
      color: white;
      text-decoration: none;
      border-radius: 10px;
      backdrop-filter: blur(10px);
      transition: all 0.3s;
    }
    a:hover { background: rgba(255,255,255,0.3); transform: translateY(-2px); }
    .info {
      background: rgba(0,0,0,0.2);
      padding: 20px;
      border-radius: 10px;
      margin-top: 30px;
    }
  </style>
</head>
<body>
  <h1>🎯 PPT Generator</h1>
  <p>AI 智能演示文稿生成平台</p>
  
  <div class="links">
    <a href="/">📱 打开前端界面</a>
  </div>
  
  <div class="info">
    <h2>使用说明</h2>
    <p>1. 在前端界面输入演示主题</p>
    <p>2. 选择模板、类型、受众等</p>
    <p>3. 点击生成，等待 AI 创建演示文稿</p>
    <p>4. 预览并下载生成的 HTML 文件</p>
  </div>
</body>
</html>
    `);
  }
}

// 启动服务器
const server = http.createServer(handleRequest);

server.listen(PORT, () => {
  console.log(`
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   🎉 PPT Generator 服务器已启动!                                        ║
║                                                                          ║
║   📱 访问地址: http://localhost:${PORT}                                   ║
║                                                                          ║
║   ┌──────────────────────────────────────────────────────────────────┐   ║
║   │                                                                  │   ║
║   │   💡 提示:                                                       │   ║
║   │                                                                  │   ║
║   │   1. 在浏览器打开 http://localhost:${PORT}                         │   ║
║   │                                                                  │   ║
║   │   2. 输入演示主题，选择模板和选项                                  │   ║
║   │                                                                  │   ║
║   │   3. 点击生成，等待 AI 创建演示文稿                                │   ║
║   │                                                                  │   ║
║   │   4. 预览并分享生成的 HTML 文件                                   │   ║
║   │                                                                  │   ║
║   └──────────────────────────────────────────────────────────────────┘   ║
║                                                                          ║
║   🎨 可用模板: modern-elegant | corporate-blue | minimal-clean | creative-bold   ║
║                                                                          ║
║   按 Ctrl+C 停止服务器                                                  ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
`);
});

// 优雅退出
process.on('SIGINT', () => {
  console.log('\n\n👋 正在停止服务器...');
  server.close(() => {
    console.log('✅ 服务器已停止');
    process.exit(0);
  });
});
