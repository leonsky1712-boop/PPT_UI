#!/usr/bin/env node
/**
 * 简单的 HTTP 服务器
 * 用于预览生成的演示文稿
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;
const OUTPUT_DIR = path.join(__dirname, '..', 'output');
const TEMPLATES_DIR = path.join(__dirname, '..', '.claude', 'skills', 'ui-ux-pro-max', 'templates', 'revealjs');

const MIME_TYPES = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

const server = http.createServer((req, res) => {
  console.log(`${new Date().toISOString()} ${req.method} ${req.url}`);

  // 处理 API 请求
  if (req.url.startsWith('/api/')) {
    handleApiRequest(req, res);
    return;
  }

  // 处理静态文件
  let filePath = req.url === '/' 
    ? path.join(__dirname, 'build', 'index.html')
    : path.join(__dirname, 'build', req.url);

  // 如果 build 目录不存在，使用 public 目录
  if (!fs.existsSync(path.join(__dirname, 'build'))) {
    filePath = req.url === '/' 
      ? path.join(__dirname, 'public', 'index.html')
      : path.join(__dirname, 'public', req.url);
  }

  // 处理输出目录的文件
  if (req.url.startsWith('/output/')) {
    filePath = path.join(OUTPUT_DIR, path.basename(req.url));
  }

  const ext = path.extname(filePath).toLowerCase();
  const contentType = MIME_TYPES[ext] || 'application/octet-stream';

  fs.readFile(filePath, (err, data) => {
    if (err) {
      if (err.code === 'ENOENT') {
        res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end('<h1>404 - 文件未找到</h1>');
      } else {
        res.writeHead(500);
        res.end('服务器错误');
      }
      return;
    }

    res.writeHead(200, { 'Content-Type': contentType });
    res.end(data);
  });
});

function handleApiRequest(req, res) {
  // 模拟 API 响应
  if (req.url === '/api/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'ok',
      message: 'PPT Generator Server is running'
    }));
    return;
  }

  if (req.url === '/api/templates') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      templates: [
        { id: 'modern-elegant', name: '现代优雅', description: '渐变背景，现代排版' },
        { id: 'corporate-blue', name: '企业蓝调', description: '专业商务风格' },
        { id: 'minimal-clean', name: '极简纯净', description: '极简主义设计' },
        { id: 'creative-bold', name: '创意大胆', description: '赛博朋克风格' }
      ]
    }));
    return;
  }

  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'API not found' }));
}

server.listen(PORT, () => {
  console.log(`
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🎉 PPT 生成器服务器已启动!                                 ║
║                                                              ║
║   📱 访问地址: http://localhost:${PORT}                       ║
║                                                              ║
║   💡 提示:                                                   ║
║      - 前端页面: http://localhost:${PORT}                    ║
║      - 输出目录: /output/                                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
`);
});
