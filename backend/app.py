#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
后端 API 服务器

提供 REST API 接口，支持演示文稿生成、预览、用户认证与历史记录。
"""

import os
import sys
import json
import uuid
from pathlib import Path
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    pass

from flask import Flask, request, jsonify, send_file

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / ".claude" / "skills" / "ui-ux-pro-max" / "scripts"))

from presentation_generator import PresentationGenerator
from template_engine import TemplateEngine

app = Flask(__name__)
_db_url = os.environ.get('DATABASE_URL', 'sqlite:///pptgen.db')
if _db_url.startswith('sqlite:///') and not _db_url.startswith('sqlite:////'):
    _db_path = PROJECT_ROOT / 'pptgen.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(_db_path)
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = _db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret')

# CORS 支持（含 Authorization 用于 JWT）
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.after_request
def after_request(response):
    return add_cors_headers(response)

@app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def options_handler(path):
    response = app.make_response('')
    return add_cors_headers(response)

# 初始化数据库与认证（backend 目录即脚本所在目录）
sys.path.insert(0, str(PROJECT_ROOT))
try:
    from backend.models import db, User, Presentation, init_db
    from backend.auth import (
        hash_password, check_password, create_access_token,
        login_required, optional_login
    )
except ImportError:
    from models import db, User, Presentation, init_db
    from auth import (
        hash_password, check_password, create_access_token,
        login_required, optional_login
    )
init_db(app)

# 初始化引擎
DATA_DIR = PROJECT_ROOT / ".claude" / "skills" / "ui-ux-pro-max" / "data"
TEMPLATES_DIR = PROJECT_ROOT / ".claude" / "skills" / "ui-ux-pro-max" / "templates" / "revealjs"

presentation_generator = PresentationGenerator(data_dir=DATA_DIR)
template_engine = TemplateEngine(templates_dir=TEMPLATES_DIR)

# 输出目录
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


# ---------- 认证接口 ----------
@app.route('/api/auth/register', methods=['POST'])
def register():
    """用户注册。请求体: { "email": "", "password": "", "name": "" }"""
    try:
        data = request.json or {}
        email = (data.get('email') or '').strip().lower()
        password = data.get('password') or ''
        name = (data.get('name') or '').strip()
        if not email or not password:
            return jsonify({'error': 'email 和 password 必填'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'error': '该邮箱已注册'}), 400
        user = User(email=email, password_hash=hash_password(password), name=name)
        db.session.add(user)
        db.session.commit()
        token = create_access_token(user.id, user.email)
        return jsonify({
            'success': True,
            'user': user.to_dict(),
            'access_token': token
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """用户登录。请求体: { "email": "", "password": "" }"""
    try:
        data = request.json or {}
        email = (data.get('email') or '').strip().lower()
        password = data.get('password') or ''
        if not email or not password:
            return jsonify({'error': 'email 和 password 必填'}), 400
        user = User.query.filter_by(email=email).first()
        if not user or not check_password(password, user.password_hash):
            return jsonify({'error': '邮箱或密码错误'}), 401
        token = create_access_token(user.id, user.email)
        return jsonify({
            'success': True,
            'user': user.to_dict(),
            'access_token': token
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/presentations', methods=['GET'])
@login_required
def list_presentations():
    """当前用户的演示文稿历史（需配置 JWT_SECRET_KEY 后登录使用）"""
    try:
        user_id = getattr(request, 'current_user_id', None)
        if not user_id:
            return jsonify({'error': '未授权', 'presentations': []}), 401
        items = Presentation.query.filter_by(user_id=user_id).order_by(Presentation.created_at.desc()).limit(100).all()
        return jsonify({'success': True, 'presentations': [p.to_dict() for p in items]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        "status": "ok",
        "message": "PPT Generator API is running"
    })


# ---------- API 文档 (OpenAPI / Swagger) ----------
import yaml
_OPENAPI_PATH = Path(__file__).parent / "openapi.yaml"

@app.route('/api/openapi.json', methods=['GET'])
def openapi_spec():
    """OpenAPI 3.0 规范（JSON）"""
    if _OPENAPI_PATH.exists():
        with open(_OPENAPI_PATH, encoding='utf-8') as f:
            spec = yaml.safe_load(f)
        return jsonify(spec)
    return jsonify({"openapi": "3.0.3", "info": {"title": "AI PPT Generator API", "version": "1.0.0"}})


@app.route('/api/docs', methods=['GET'])
def api_docs():
    """Swagger UI 文档页"""
    html = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8"/>
  <title>AI PPT Generator - API 文档</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css"/>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = function() {
      window.ui = SwaggerUIBundle({
        url: "/api/openapi.json",
        dom_id: "#swagger-ui",
        presets: [SwaggerUIBundle.presets.apis, SwaggerUIBundle.SwaggerUIStandalonePreset]
      });
    };
  </script>
</body>
</html>'''
    from flask import Response
    return Response(html, mimetype='text/html')


@app.route('/api/templates', methods=['GET'])
def get_templates():
    """获取可用模板列表"""
    templates = template_engine.get_template_list()
    return jsonify({
        "templates": templates
    })


@app.route('/api/generate', methods=['POST'])
@optional_login
def generate_presentation():
    """
    生成演示文稿
    
    请求体:
    {
        "topic": "演示主题",
        "template": "modern-elegant",
        "type": "business_presentation",
        "audience": "general_employees",
        "duration": 15,
        "tone": "professional",
        "industry": "",
        "author": ""
    }
    """
    try:
        data = request.json
        
        # 验证必填字段
        if not data.get('topic'):
            return jsonify({"error": "topic is required"}), 400
        
        # 使用 PresentationGenerator 生成幻灯片数据
        result = presentation_generator.generate(
            title=data['topic'],
            presentation_type=data.get('type', 'business_presentation'),
            audience=data.get('audience', 'general_employees'),
            duration_minutes=data.get('duration', 15),
            tone=data.get('tone', 'professional'),
            industry=data.get('industry', ''),
            key_points=[],
            objectives=[]
        )
        
        # 获取模板
        template_id = data.get('template', 'modern-elegant')
        
        # 使用模板引擎渲染
        from template_engine import PresentationData, SlideContent
        
        # 构建演示数据
        presentation_data = PresentationData(
            title=result['metadata']['title'],
            subtitle=result['metadata'].get('subtitle', ''),
            author=data.get('author', result['metadata'].get('author', '')),
            date=result['metadata'].get('date', ''),
            template_id=template_id,
            industry=data.get('industry', ''),
            logo_icon="📊"
        )
        
        # 转换幻灯片
        for slide_dict in result.get('slides', []):
            slide = SlideContent(
                slide_id=slide_dict.get('id', ''),
                slide_type=slide_dict.get('type', 'content'),
                title=slide_dict.get('title', ''),
                subtitle=slide_dict.get('subtitle'),
                content_items=slide_dict.get('contents', []),
                notes=slide_dict.get('notes', '')
            )
            presentation_data.slides.append(slide)
        
        # 生成唯一文件名
        file_id = str(uuid.uuid4())[:8]
        output_filename = f"presentation_{file_id}.html"
        output_path = OUTPUT_DIR / output_filename
        
        # 渲染并保存
        template_engine.export(presentation_data, output_path)
        slide_count = len(result.get('slides', []))

        # 若已登录则写入历史
        user_id = getattr(request, 'current_user_id', None)
        if user_id:
            try:
                rec = Presentation(
                    user_id=user_id,
                    title=result['metadata']['title'],
                    template_id=template_id,
                    presentation_type=data.get('type', 'business_presentation'),
                    audience=data.get('audience', 'general_employees'),
                    duration=data.get('duration', 15),
                    tone=data.get('tone', 'professional'),
                    industry=data.get('industry', ''),
                    output_filename=output_filename,
                    slide_count=slide_count
                )
                db.session.add(rec)
                db.session.commit()
            except Exception:
                db.session.rollback()

        return jsonify({
            "success": True,
            "message": "演示文稿生成成功",
            "data": {
                "url": f"/output/{output_filename}",
                "filename": output_filename,
                "title": result['metadata']['title'],
                "slide_count": slide_count,
                "template": template_id
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/output/<filename>', methods=['GET'])
def serve_output(filename):
    """提供生成的演示文稿"""
    output_path = OUTPUT_DIR / filename
    if output_path.exists():
        return send_file(
            output_path,
            mimetype='text/html',
            as_attachment=False
        )
    return jsonify({"error": "File not found"}), 404


@app.route('/api/templates/render', methods=['POST'])
def render_template():
    """
    使用模板直接渲染
    
    请求体:
    {
        "title": "演示标题",
        "slides": [
            {"type": "title", "title": "第一页", "contents": [...]},
            {"type": "content", "title": "第二页", "contents": [...]}
        ],
        "template": "modern-elegant"
    }
    """
    try:
        data = request.json
        
        if not data.get('title') or not data.get('slides'):
            return jsonify({"error": "title and slides are required"}), 400
        
        from template_engine import PresentationData, SlideContent
        
        # 构建演示数据
        presentation_data = PresentationData(
            title=data['title'],
            subtitle=data.get('subtitle', ''),
            author=data.get('author', ''),
            date=data.get('date', ''),
            template_id=data.get('template', 'modern-elegant'),
            industry=data.get('industry', ''),
            logo_icon=data.get('logo_icon', '📊')
        )
        
        # 转换幻灯片
        for slide_data in data.get('slides', []):
            slide = SlideContent(
                slide_id=slide_data.get('id', ''),
                slide_type=slide_data.get('type', 'content'),
                title=slide_data.get('title', ''),
                subtitle=slide_data.get('subtitle'),
                content_items=slide_data.get('contents', []),
                notes=slide_data.get('notes', '')
            )
            presentation_data.slides.append(slide)
        
        # 渲染
        html = template_engine.render(data.get('template', 'modern-elegant'), presentation_data)
        
        # 生成唯一文件名
        file_id = str(uuid.uuid4())[:8]
        output_filename = f"presentation_{file_id}.html"
        output_path = OUTPUT_DIR / output_filename
        output_path.write_text(html, encoding='utf-8')
        
        return jsonify({
            "success": True,
            "url": f"/output/{output_filename}",
            "filename": output_filename
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/export/pptx', methods=['POST'])
def export_pptx():
    """
    导出为 PPTX 格式。请求体与 /api/generate 相同（topic 必填）。
    返回 .pptx 文件下载。
    """
    try:
        data = request.json or {}
        if not data.get('topic'):
            return jsonify({"error": "topic is required"}), 400

        # 直接调用生成器获取完整 slides + metadata（与 /api/generate 逻辑一致）
        result = presentation_generator.generate(
            title=data['topic'],
            presentation_type=data.get('type', 'business_presentation'),
            audience=data.get('audience', 'general_employees'),
            duration_minutes=data.get('duration', 15),
            tone=data.get('tone', 'professional'),
            industry=data.get('industry', ''),
            key_points=[],
            objectives=[]
        )
        slides = result.get('slides', [])
        meta = result.get('metadata', {})
        metadata = {
            'title': meta.get('title', data['topic']),
            'author': data.get('author', '') or meta.get('author', ''),
            'subtitle': meta.get('subtitle', ''),
        }
        if not slides:
            return jsonify({"error": "生成幻灯片为空"}), 500

        # 导出为 PPTX
        from pptx_exporter import PPTXExporter
        width = float(os.environ.get('PPTX_WIDTH', 13.333))
        height = float(os.environ.get('PPTX_HEIGHT', 7.5))
        exporter = PPTXExporter(width_inches=width, height_inches=height)
        pptx_bytes = exporter.export(slides, metadata)

        file_id = str(uuid.uuid4())[:8]
        output_filename = f"presentation_{file_id}.pptx"
        output_path = OUTPUT_DIR / output_filename
        output_path.write_bytes(pptx_bytes)

        return send_file(
            output_path,
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
            as_attachment=True,
            download_name=output_filename
        )
    except ImportError as e:
        return jsonify({
            "success": False,
            "error": "PPTX 导出需要安装 python-pptx: pip install python-pptx",
            "detail": str(e)
        }), 503
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
