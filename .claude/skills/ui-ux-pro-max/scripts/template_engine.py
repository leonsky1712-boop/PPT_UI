#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模板引擎 - 专业演示文稿模板系统

提供模板加载、内容注入、渲染功能。
支持多种专业设计的 Reveal.js 模板。
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class Template:
    """模板定义"""
    name: str
    template_id: str
    description: str
    style_category: str
    color_palette: str
    typography: str
    animation_style: str
    transition_style: str
    file_path: Path
    
    # 可自定义元素
    customizable_elements: List[str] = field(default_factory=list)
    
    # 行业适配
    industry_suitability: str = ""
    
    # 复杂度评分 (1-5)
    complexity_score: int = 1


@dataclass
class SlideContent:
    """单张幻灯片内容"""
    slide_id: str
    slide_type: str  # title, content, section_divider, agenda, thank_you, etc.
    title: str
    subtitle: Optional[str] = None
    content_items: List[Dict[str, Any]] = field(default_factory=list)
    notes: str = ""
    animation: Optional[Dict[str, Any]] = None


@dataclass
class PresentationData:
    """演示文稿完整数据"""
    title: str
    subtitle: str = ""
    author: str = ""
    author_title: str = ""
    date: str = ""
    
    # 幻灯片列表
    slides: List[SlideContent] = field(default_factory=list)
    
    # 元数据
    template_id: str = "modern-elegant"
    theme_style: str = ""
    industry: str = ""
    tone: str = "professional"
    
    # 额外数据
    tags: List[str] = field(default_factory=list)
    logo_icon: str = ""
    contact_info: Dict[str, str] = field(default_factory=dict)


class TemplateEngine:
    """模板引擎"""
    
    # 可用模板列表
    AVAILABLE_TEMPLATES = {
        "modern-elegant": {
            "name": "现代优雅",
            "description": "渐变背景，现代排版，适合产品发布和创意展示",
            "style_category": "Modern Gradient",
            "color_palette": "Purple/Pink Gradient",
            "typography": "Modern Sans",
            "animation_style": "Smooth Fade",
            "transition_style": "Slide",
            "customizable_elements": ["Logo Icon", "Accent Colors", "Background Gradient"],
            "industry_suitability": "Technology, Startup, Creative",
            "complexity_score": 3
        },
        "corporate-blue": {
            "name": "企业蓝调",
            "description": "专业商务风格，适合企业汇报和培训",
            "style_category": "Corporate Professional",
            "color_palette": "Navy/Blue/Gold",
            "typography": "Business Sans",
            "animation_style": "Minimal",
            "transition_style": "Slide",
            "customizable_elements": ["Company Logo", "Brand Colors", "Footer"],
            "industry_suitability": "Finance, Corporate, Consulting",
            "complexity_score": 2
        },
        "minimal-clean": {
            "name": "极简纯净",
            "description": "极简主义设计，适合技术分享和学术报告",
            "style_category": "Minimalist",
            "color_palette": "Black/White/Gray",
            "typography": "Clean Sans",
            "animation_style": "None",
            "transition_style": "Fade",
            "customizable_elements": ["Typography Scale", "Spacing"],
            "industry_suitability": "Technology, Academic, Research",
            "complexity_score": 1
        },
        "creative-bold": {
            "name": "创意大胆",
            "description": "赛博朋克风格，适合创意提案和年轻团队",
            "style_category": "Cyberpunk/Neon",
            "color_palette": "Neon Pink/Cyan/Purple",
            "typography": "Space Grotesk",
            "animation_style": "Glitch/Pulse",
            "transition_style": "Convex",
            "customizable_elements": ["Neon Colors", "Glitch Effects", "Tags"],
            "industry_suitability": "Creative, Gaming, Marketing",
            "complexity_score": 4
        }
    }
    
    def __init__(self, templates_dir: Optional[Path] = None):
        """
        初始化模板引擎
        
        Args:
            templates_dir: 模板目录路径
        """
        if templates_dir is None:
            templates_dir = Path(__file__).parent.parent / "templates" / "revealjs"
        self.templates_dir = Path(templates_dir)
        
        # 加载所有模板
        self.templates: Dict[str, Template] = {}
        self._load_templates()
    
    def _load_templates(self):
        """加载所有可用模板"""
        if not self.templates_dir.exists():
            return
        
        for template_file in self.templates_dir.glob("*.html"):
            template_id = template_file.stem
            
            if template_id in self.AVAILABLE_TEMPLATES:
                config = self.AVAILABLE_TEMPLATES[template_id]
                self.templates[template_id] = Template(
                    name=config["name"],
                    template_id=template_id,
                    description=config["description"],
                    style_category=config["style_category"],
                    color_palette=config["color_palette"],
                    typography=config["typography"],
                    animation_style=config["animation_style"],
                    transition_style=config["transition_style"],
                    file_path=template_file,
                    customizable_elements=config.get("customizable_elements", []),
                    industry_suitability=config.get("industry_suitability", ""),
                    complexity_score=config.get("complexity_score", 1)
                )
    
    def get_template_list(self) -> List[Dict[str, Any]]:
        """获取可用模板列表"""
        return [
            {
                "id": tid,
                "name": t.name,
                "description": t.description,
                "style": t.style_category,
                "colors": t.color_palette,
                "industries": t.industry_suitability,
                "complexity": t.complexity_score
            }
            for tid, t in self.templates.items()
        ]
    
    def get_template(self, template_id: str) -> Optional[Template]:
        """获取指定模板"""
        return self.templates.get(template_id)
    
    def load_template(self, template_id: str) -> Optional[str]:
        """
        加载模板文件内容
        
        Args:
            template_id: 模板 ID
            
        Returns:
            str: 模板 HTML 内容
        """
        template = self.get_template(template_id)
        if template is None:
            return None
        
        if template.file_path.exists():
            return template.file_path.read_text(encoding='utf-8')
        return None
    
    def render(self, template_id: str, data: PresentationData) -> str:
        """
        渲染演示文稿
        
        Args:
            template_id: 模板 ID
            data: 演示文稿数据
            
        Returns:
            str: 渲染后的 HTML
        """
        template_content = self.load_template(template_id)
        if template_content is None:
            raise ValueError(f"Template not found: {template_id}")
        
        # 基础替换
        result = template_content
        
        # 替换基础元数据
        replacements = {
            "{{TITLE}}": data.title or "演示文稿",
            "{{SUBTITLE}}": data.subtitle or "",
            "{{AUTHOR}}": data.author or "",
            "{{AUTHOR_TITLE}}": data.author_title or "",
            "{{DATE}}": data.date or "",
            "{{LOGO_ICON}}": data.logo_icon or "📊",
            "{{SECTION_TAG}}": data.industry or "Presentation",
            "{{THANK_YOU_TITLE}}": "感谢聆听",
            "{{THANK_YOU_SUBTITLE}}": data.subtitle or "",
            "{{AGENDA_TITLE}}": "议程",
        }
        
        for placeholder, value in replacements.items():
            result = result.replace(placeholder, str(value))
        
        # 生成幻灯片
        slides_html = self._generate_slides_html(data)
        result = result.replace("{{CONTENT_SLIDES}}", slides_html)
        
        # 生成议程
        agenda_html = self._generate_agenda(data)
        result = result.replace("{{AGENDA_ITEMS}}", agenda_html)
        
        # 生成标签
        tags_html = self._generate_tags(data.tags)
        result = result.replace("{{TAGS}}", tags_html)
        
        # 生成联系信息
        contact_html = self._generate_contact_info(data.contact_info)
        result = result.replace("{{CONTACT_INFO}}", contact_html)
        
        # 生成 CTA 按钮
        cta_html = self._generate_cta_button(data)
        result = result.replace("{{CTA_BUTTON}}", cta_html)
        
        # 生成 meta 信息
        meta_html = self._generate_meta_info(data)
        result = result.replace("{{META_INFO}}", meta_html)
        
        return result
    
    def _generate_slides_html(self, data: PresentationData) -> str:
        """生成幻灯片 HTML"""
        slides_html = []
        
        for i, slide in enumerate(data.slides):
            slide_html = self._render_single_slide(slide, data)
            slides_html.append(slide_html)
        
        return '\n'.join(slides_html)
    
    def _render_single_slide(self, slide: SlideContent, data: PresentationData) -> str:
        """渲染单张幻灯片"""
        
        if slide.slide_type == "section_divider":
            return self._render_section_slide(slide)
        elif slide.slide_type == "agenda":
            return self._render_agenda_slide(slide)
        elif slide.slide_type == "thank_you":
            return self._render_thankyou_slide(slide)
        else:
            return self._render_content_slide(slide)
    
    def _render_section_slide(self, slide: SlideContent) -> str:
        """渲染章节分隔幻灯片"""
        return f'''
        <section data-background-gradient="linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
          <h2>{slide.title}</h2>
          {f'<p class=\"subtitle\">{slide.subtitle}</p>' if slide.subtitle else ''}
        </section>
        '''
    
    def _render_agenda_slide(self, slide: SlideContent) -> str:
        """渲染议程幻灯片"""
        items_html = []
        for item in slide.content_items:
            items_html.append(f'<li>{item.get("text", "")}</li>')
        
        return f'''
        <section>
          <h2>{slide.title}</h2>
          <ul>
            {"".join(items_html)}
          </ul>
        </section>
        '''
    
    def _render_thankyou_slide(self, slide: SlideContent) -> str:
        """渲染结束页"""
        return f'''
        <section data-background-gradient="linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)">
          <h1>{slide.title}</h1>
          {f'<p class=\"subtitle\">{slide.subtitle}</p>' if slide.subtitle else ''}
        </section>
        '''
    
    def _render_content_slide(self, slide: SlideContent) -> str:
        """渲染内容幻灯片"""
        contents_html = []
        
        for item in slide.content_items:
            item_type = item.get("type", "paragraph")
            text = item.get("text", "")
            
            if item_type == "title":
                contents_html.append(f'<h3>{text}</h3>')
            elif item_type == "bullet":
                level = item.get("level", 0)
                indent = "  " * level
                contents_html.append(f'{indent}<li>{text}</li>')
            elif item_type == "paragraph":
                contents_html.append(f'<p>{text}</p>')
            elif item_type == "quote":
                contents_html.append(f'<blockquote>{text}</blockquote>')
            elif item_type == "metric":
                value = item.get("value", "")
                label = item.get("label", "")
                contents_html.append(f'''
                <div class="metric-card">
                  <div class="metric-value">{value}</div>
                  <div class="metric-label">{label}</div>
                </div>
                ''')
            elif item_type == "feature":
                icon = item.get("icon", "★")
                feature_title = item.get("feature_title", "")
                feature_desc = item.get("description", "")
                contents_html.append(f'''
                <div class="feature-item">
                  <div class="feature-icon">{icon}</div>
                  <div class="feature-title">{feature_title}</div>
                  <div class="feature-desc">{feature_desc}</div>
                </div>
                ''')
        
        return f'''
        <section>
          <h2>{slide.title}</h2>
          {"".join(contents_html)}
        </section>
        '''
    
    def _generate_agenda(self, data: PresentationData) -> str:
        """生成议程 HTML"""
        items = []
        for i, slide in enumerate(data.slides):
            if slide.slide_type not in ["title", "thank_you"]:
                items.append(f'<div class=\"agenda-item\"><span class=\"agenda-number\">{len(items) + 1}</span><span class=\"agenda-text\">{slide.title}</span></div>')
        return "".join(items)
    
    def _generate_tags(self, tags: List[str]) -> str:
        """生成标签 HTML"""
        if not tags:
            return '<span class="tag">Presentation</span>'
        return "".join([f'<span class="tag">{tag}</span>' for tag in tags])
    
    def _generate_contact_info(self, contact: Dict[str, str]) -> str:
        """生成联系信息 HTML"""
        if not contact:
            return '<span class="contact-link">📧 contact@example.com</span>'
        
        items = []
        for platform, value in contact.items():
            icon = self._get_contact_icon(platform)
            items.append(f'<span class="contact-link\">{icon} {value}</span>')
        return "".join(items)
    
    def _get_contact_icon(self, platform: str) -> str:
        """获取联系图标"""
        icons = {
            "email": "📧",
            "phone": "📱",
            "website": "🌐",
            "linkedin": "💼",
            "twitter": "🐦",
            "github": "🐙"
        }
        return icons.get(platform.lower(), "📧")
    
    def _generate_cta_button(self, data: PresentationData) -> str:
        """生成 CTA 按钮"""
        return '''
        <a href="#" class="cta-button">立即体验</a>
        '''
    
    def _generate_meta_info(self, data: PresentationData) -> str:
        """生成 meta 信息"""
        items = []
        if data.author:
            items.append(f'<span class=\"meta-item\">👤 {data.author}</span>')
        if data.date:
            items.append(f'<span class=\"meta-item\">📅 {data.date}</span>')
        return "".join(items)
    
    def export(self, data: PresentationData, output_path: Path) -> Path:
        """
        导出渲染后的 HTML 文件
        
        Args:
            data: 演示文稿数据
            output_path: 输出路径
            
        Returns:
            Path: 输出文件路径
        """
        template_id = data.template_id
        html_content = self.render(template_id, data)
        
        # 确保扩展名为 .html
        if output_path.suffix.lower() != '.html':
            output_path = output_path.with_suffix('.html')
        
        # 写入文件
        output_path.write_text(html_content, encoding='utf-8')
        
        return output_path


# 便捷函数
def create_presentation(
    title: str,
    slides: List[Dict[str, Any]],
    template_id: str = "modern-elegant",
    output_path: str = "presentation.html",
    **kwargs
) -> str:
    """
    创建演示文稿的便捷函数
    
    Args:
        title: 演示文稿标题
        slides: 幻灯片数据列表
        template_id: 模板 ID
        output_path: 输出路径
        **kwargs: 其他参数 (subtitle, author, date 等)
        
    Returns:
        str: 渲染后的 HTML
    """
    engine = TemplateEngine()
    
    # 构建演示数据
    data = PresentationData(
        title=title,
        subtitle=kwargs.get("subtitle", ""),
        author=kwargs.get("author", ""),
        author_title=kwargs.get("author_title", ""),
        date=kwargs.get("date", ""),
        template_id=template_id,
        industry=kwargs.get("industry", ""),
        tags=kwargs.get("tags", []),
        logo_icon=kwargs.get("logo_icon", "📊"),
        contact_info=kwargs.get("contact_info", {})
    )
    
    # 构建幻灯片
    for slide_data in slides:
        slide = SlideContent(
            slide_id=slide_data.get("id", ""),
            slide_type=slide_data.get("type", "content"),
            title=slide_data.get("title", ""),
            subtitle=slide_data.get("subtitle"),
            content_items=slide_data.get("contents", []),
            notes=slide_data.get("notes", "")
        )
        data.slides.append(slide)
    
    # 渲染
    html = engine.render(template_id, data)
    
    # 保存文件
    path = Path(output_path)
    engine.export(data, path)
    
    return str(path)


# CLI 支持
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Template Engine for Presentations")
    parser.add_argument("--list-templates", action="store_true", help="List available templates")
    parser.add_argument("--template", "-t", default="modern-elegant", help="Template ID")
    parser.add_argument("--title", "-T", default="我的演示文稿", help="Presentation title")
    parser.add_argument("--output", "-o", default="output.html", help="Output file")
    
    args = parser.parse_args()
    
    engine = TemplateEngine()
    
    if args.list_templates:
        print("可用模板:")
        for t in engine.get_template_list():
            print(f"  - {t['id']}: {t['name']} ({t['description']})")
    else:
        # 创建示例演示文稿
        data = PresentationData(
            title=args.title,
            subtitle="这是一个使用 AI 生成的演示文稿",
            author="作者",
            date="2024年1月",
            template_id=args.template,
            industry="Technology"
        )
        
        # 添加幻灯片
        data.slides.append(SlideContent(
            slide_id="agenda",
            slide_type="agenda",
            title="议程",
            content_items=[
                {"type": "bullet", "text": "第一部分：介绍"},
                {"type": "bullet", "text": "第二部分：主要内容"},
                {"type": "bullet", "text": "第三部分：总结"},
            ]
        ))
        
        data.slides.append(SlideContent(
            slide_id="content1",
            slide_type="content",
            title="主要内容",
            content_items=[
                {"type": "title", "text": "核心要点"},
                {"type": "bullet", "text": "要点一：详细的说明内容"},
                {"type": "bullet", "text": "要点二：详细的说明内容"},
                {"type": "bullet", "text": "要点三：详细的说明内容"},
            ]
        ))
        
        # 渲染并保存
        output_path = engine.export(data, Path(args.output))
        print(f"演示文稿已保存: {output_path}")
