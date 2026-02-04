#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reveal.js 幻灯片导出器

将生成的幻灯片序列导出为 Reveal.js HTML 格式。
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class RevealJSConfig:
    """Reveal.js 配置"""
    width: int = 1280
    height: int = 720
    margin: float = 0.05
    min_scale: float = 0.2
    max_scale: float = 2.0
    controls: bool = True
    progress: bool = True
    slide_number: bool = False
    hash: bool = True
    history: bool = True
    center: bool = True
    transition: str = "slide"
    transition_speed: str = "default"
    show_notes: bool = False
    auto_play_media: bool = True
    auto_animate: bool = False
    auto_animate_matcher: str = None
    auto_animate_unmatched: bool = True
    auto_slide: int = 0
    auto_slide_stoppable: bool = True
    auto_slide_method: str = "default"
    loop: bool = False
    rtl: bool = False
    shuffle: bool = False
    fragments: bool = True
    embedded: bool = False
    help: bool = True
    alert: bool = False
    slide_count: bool = False
    enable_chalkboard: bool = False
    enable_title_slide: bool = True
    enable_zoom: bool = False
    enable_wheel: bool = False
    enable_pdfexport: bool = False
    enable_Overview: bool = True
    enable_developermode: bool = False
    buttons_style: str = "auto"
    controls_layout: str = "bottom-right"
    controls_back_arrows: str = "faded"
    control_postscript: float = 0.5
    shift_key: bool = True
    view_distance: int = 3
    mobile_view_distance: int = 2
    parallax_background_image: str = ""
    parallax_background_size: str = ""
    parallax_background_horizontal: int = 0
    parallax_background_vertical: int = 0
    parallax_background_image_darken: int = 0
    background_transition: str = "fade"
    hideInactiveCursor: bool = True
    hideCursorTime: int = 5000
    width_fixed: int = 0
    height_fixed: int = 0
    keyboard: bool = True
    overview: bool = True
    keyboard_separated: bool = False
    touch: bool = True
    loop: bool = False


class RevealJSExporter:
    """Reveal.js 幻灯片导出器"""
    
    # 可用的主题
    THEMES = [
        'black', 'white', 'league', 'beige', 'sky', 'night', 
        'moon', 'solarized', 'blood', 'dracula', 'codeforces', 
        'copper', 'cobalt', 'monokai', 'synthwave84', 'zenburn'
    ]
    
    # 可用的过渡效果
    TRANSITIONS = [
        'none', 'fade', 'slide', 'convex', 'concave', 'zoom', 'crossfade'
    ]
    
    # 默认配置
    DEFAULT_CONFIG = RevealJSConfig()
    
    def __init__(self, theme: str = 'black', config: Optional[RevealJSConfig] = None):
        """
        初始化导出器
        
        Args:
            theme: Reveal.js 主题
            config: Reveal.js 配置
        """
        self.theme = theme if theme in self.THEMES else 'black'
        self.config = config or self.DEFAULT_CONFIG
    
    def export(self, slides: List[Dict[str, Any]], metadata: Dict[str, Any]) -> str:
        """
        导出幻灯片为 Reveal.js HTML
        
        Args:
            slides: 幻灯片数据列表
            metadata: 元数据
            
        Returns:
            str: HTML 字符串
        """
        # 生成幻灯片 HTML
        slides_html = self._generate_slides_html(slides)
        
        # 生成配置
        config_json = self._generate_config()
        
        # 生成自定义 CSS
        custom_css = self._generate_custom_css(metadata, slides)
        
        # 生成完整 HTML
        html = f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="description" content="{metadata.get('title', 'Presentation')}">
    <title>{metadata.get('title', 'Presentation')}</title>
    
    <!-- Reveal.js CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/theme/{self.theme}.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/highlight/monokai.css">
    
    <!-- 自定义样式 -->
    <style>
      {custom_css}
    </style>
  </head>
  <body>
    <div class="reveal">
      <div class="slides">
        {slides_html}
      </div>
    </div>
    
    <!-- Reveal.js -->
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/markdown/markdown.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/highlight/highlight.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/notes/notes.js"></script>
    
    <!-- 初始化 -->
    <script>
      {config_json}
    </script>
    
    <script>
      // 初始化 Reveal.js
      Reveal.initialize({{
        width: {self.config.width},
        height: {self.config.height},
        margin: {self.config.margin},
        minScale: {self.config.min_scale},
        maxScale: {self.config.max_scale},
        controls: {str(self.config.controls).lower()},
        progress: {str(self.config.progress).lower()},
        slideNumber: {str(self.config.slide_number).lower()},
        hash: {str(self.config.hash).lower()},
        history: {str(self.config.history).lower()},
        center: {str(self.config.center).lower()},
        transition: '{self.config.transition}',
        transitionSpeed: '{self.config.transition_speed}',
        showNotes: {str(self.config.show_notes).lower()},
        autoPlayMedia: {str(self.config.auto_play_media).lower()},
        autoAnimate: {str(self.config.auto_animate).lower()},
        autoAnimateUnmatched: {str(self.config.auto_animate_unmatched).lower()},
        loop: {str(self.config.loop).lower()},
        rtl: {str(self.config.rtl).lower()},
        shuffle: {str(self.config.shuffle).lower()},
        fragments: {str(self.config.fragments).lower()},
        embedded: {str(self.config.embedded).lower()},
        help: {str(self.config.help).lower()},
        keyboard: {str(self.config.keyboard).lower()},
        overview: {str(self.config.overview).lower()},
        touch: {str(self.config.touch).lower()},
        loop: {str(self.config.loop).lower()},
        width_fixed: {self.config.width_fixed},
        height_fixed: {self.config.height_fixed},
        viewDistance: {self.config.view_distance},
        mobileViewDistance: {self.config.mobile_view_distance},
        backgroundTransition: '{self.config.background_transition}',
        hideInactiveCursor: {str(self.config.hideInactiveCursor).lower()},
        hideCursorTime: {self.config.hideCursorTime},
        shiftKey: {str(self.config.shift_key).lower()},
        
        // 插件
        plugins: [ RevealMarkdown, RevealHighlight, RevealNotes ]
      }});
    </script>
  </body>
</html>"""
        
        return html
    
    def _generate_slides_html(self, slides: List[Dict[str, Any]]) -> str:
        """生成幻灯片 HTML"""
        html_parts = []
        
        for i, slide in enumerate(slides, 1):
            slide_html = self._generate_single_slide(slide, i)
            html_parts.append(slide_html)
        
        return '\n'.join(html_parts)
    
    def _generate_single_slide(self, slide: Dict[str, Any], index: int) -> str:
        """生成单张幻灯片 HTML"""
        # 获取背景色
        bg_color = slide.get('background', {}).get('fillColor', '#FFFFFF')
        
        # 获取内容
        contents = slide.get('contents', [])
        content_html = self._generate_content_html(contents)
        
        # 获取标题
        title = slide.get('title', '')
        
        # 获取备注
        notes = slide.get('notes', '')
        
        # 获取过渡类型
        transition = slide.get('transition', {}).get('effect', 'fade')
        
        # 生成 HTML
        html = f"""        <section data-background-color="{bg_color}" data-transition="{transition}">
          <h2>{title}</h2>
          {content_html}
          {f'<!-- .notes: {notes} -->' if notes else ''}
        </section>"""
        
        return html
    
    def _generate_content_html(self, contents: List[Dict[str, Any]]) -> str:
        """生成内容 HTML"""
        html_parts = []
        
        # 按类型分组内容
        by_type = {}
        for content in contents:
            content_type = content.get('type', 'body')
            if content_type not in by_type:
                by_type[content_type] = []
            by_type[content_type].append(content)
        
        # 生成标题
        if 'title' in by_type:
            for title in by_type['title']:
                html_parts.append(f'<h3>{title.get("text", "")}</h3>')
        
        # 生成列表
        if 'bullet' in by_type:
            bullets = by_type['bullet']
            level_bullets = {}
            for bullet in bullets:
                level = bullet.get('level', 0)
                if level not in level_bullets:
                    level_bullets[level] = []
                level_bullets[level].append(bullet)
            
            # 按级别排序
            html_parts.append('<ul class="fragment-list">')
            for level in sorted(level_bullets.keys()):
                spaces = "  " * (level + 1)
                li_tag = "<li>"
                li_end = "</li>"
                for bullet in level_bullets[level]:
                    text = bullet.get('text', '')
                    # 检查是否有动画
                    anim = bullet.get('animation', {})
                    anim_class = ''
                    if anim:
                        effect = anim.get('effect', '')
                        if effect == 'fade':
                            anim_class = ' class="fragment fade-in"'
                    html_parts.append(f'{spaces}{li_tag}<span{anim_class}>{text}</span>{li_end}')
            html_parts.append('</ul>')
        
        # 生成普通段落
        if 'body' in by_type:
            for body in by_type['body']:
                text = body.get('text', '')
                html_parts.append(f'<p>{text}</p>')
        
        # 生成引用
        if 'quote' in by_type:
            for quote in by_type['quote']:
                text = quote.get('text', '')
                html_parts.append(f'<blockquote>{text}</blockquote>')
        
        # 生成 CTA 按钮
        if 'cta_button' in by_type:
            for cta in by_type['cta_button']:
                text = cta.get('text', '')
                bg = cta.get('shape', {}).get('fillColor', '#FF6600')
                html_parts.append(f'<div class="cta-button" style="background-color: {bg};">{text}</div>')
        
        return '\n'.join(html_parts)
    
    def _generate_config(self) -> str:
        """生成 Reveal.js 配置"""
        return f"""
      // 自动播放媒体
      Reveal.configure({{
        autoPlayMedia: {str(self.config.auto_play_media).lower()}
      }});
      
      // 笔记
      Reveal.configure({{
        showNotes: {str(self.config.show_notes).lower()}
      }});
    """
    
    def _generate_custom_css(self, metadata: Dict[str, Any], slides: List[Dict[str, Any]]) -> str:
        """生成自定义 CSS"""
        css_parts = []
        
        # 获取配色
        if slides:
            first_slide = slides[0]
            bg = first_slide.get('background', {})
            bg_color = bg.get('fillColor', '#FFFFFF')
            text_color = '#1A1A1A'
            
            # 从内容中查找颜色
            for content in first_slide.get('contents', []):
                if content.get('type') == 'title':
                    style = content.get('style', {})
                    text_color = style.get('color', '#1A1A1A')
                    break
        
        # 添加自定义样式
        css_parts.append(f"""/* 自定义字体 */
.reveal {{
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 24px;
}}

.reveal h1, .reveal h2, .reveal h3 {{
  font-weight: 600;
  text-transform: none;
}}

.reveal h1 {{
  font-size: 2.5em;
  margin-bottom: 0.5em;
}}

.reveal h2 {{
  font-size: 1.8em;
  color: {text_color};
}}

.reveal p, .reveal li {{
  line-height: 1.6;
  color: {text_color};
}}

/* 列表样式 */
.reveal ul {{
  list-style-type: disc;
  margin-left: 1em;
}}

.reveal ul li {{
  margin-bottom: 0.5em;
}}

/* 引用样式 */
.reveal blockquote {{
  border-left: 4px solid {bg_color};
  padding-left: 1em;
  margin: 1em 0;
  font-style: italic;
  background: rgba(0,0,0,0.05);
  padding: 0.5em 1em;
}}

/* CTA 按钮 */
.cta-button {{
  display: inline-block;
  padding: 0.8em 2em;
  border-radius: 4px;
  color: white;
  font-weight: bold;
  margin-top: 1em;
  cursor: pointer;
}}

/* 幻灯片编号 */
.reveal .slide-number {{
  font-size: 14px;
  color: {text_color};
  background: transparent;
}}

/* 进度条 */
.reveal .progress {{
  height: 4px;
  background: rgba(0,0,0,0.1);
}}

.reveal .progress span {{
  background: {bg_color};
}}

/* 响应式 */
@media (max-width: 768px) {{
  .reveal {{
    font-size: 18px;
  }}
  
  .reveal h1 {{
    font-size: 2em;
  }}
  
  .reveal h2 {{
    font-size: 1.5em;
  }}
}}""")
        
        return '\n'.join(css_parts)
    
    def save(self, slides: List[Dict[str, Any]], metadata: Dict[str, Any], filepath: Path) -> Path:
        """
        保存为 HTML 文件
        
        Args:
            slides: 幻灯片数据
            metadata: 元数据
            filepath: 输出文件路径
            
        Returns:
            Path: 保存的文件路径
        """
        html = self.export(slides, metadata)
        
        # 确保扩展名为 .html
        if filepath.suffix.lower() != '.html':
            filepath = filepath.with_suffix('.html')
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return filepath


# 便捷函数
def export_revealjs(slides: List[Dict[str, Any]],
                  metadata: Dict[str, Any],
                  output_path: str,
                  theme: str = 'black') -> str:
    """
    便捷的 Reveal.js 导出函数
    
    Args:
        slides: 幻灯片数据
        metadata: 元数据
        output_path: 输出路径
        theme: 主题
        
    Returns:
        str: 导出的 HTML 内容
    """
    exporter = RevealJSExporter(theme=theme)
    filepath = exporter.save(slides, metadata, Path(output_path))
    return str(filepath)


# CLI 支持
if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path
    
    parser = argparse.ArgumentParser(description="Export to Reveal.js HTML")
    parser.add_argument("input", help="Input JSON file or 'demo'")
    parser.add_argument("--output", "-o", help="Output HTML file")
    parser.add_argument("--theme", "-t", default="black", choices=RevealJSExporter.THEMES,
                       help="Reveal.js theme")
    parser.add_argument("--width", type=int, default=1280, help="Slide width")
    parser.add_argument("--height", type=int, default=720, help="Slide height")
    
    args = parser.parse_args()
    
    # 创建配置
    config = RevealJSConfig(
        width=args.width,
        height=args.height
    )
    
    # 创建导出器
    exporter = RevealJSExporter(theme=args.theme, config=config)
    
    if args.input == 'demo':
        # 创建示例幻灯片
        slides = [
            {
                'title': '欢迎',
                'background': {'fillColor': '#003366'},
                'transition': {'effect': 'fade'},
                'contents': [
                    {'type': 'title', 'text': '演示文稿标题', 'style': {'color': '#FFFFFF'}},
                    {'type': 'body', 'text': '副标题或描述', 'style': {'color': '#CCCCCC'}}
                ]
            },
            {
                'title': '内容',
                'background': {'fillColor': '#FFFFFF'},
                'transition': {'effect': 'slide'},
                'contents': [
                    {'type': 'title', 'text': '主要章节', 'style': {'color': '#003366'}},
                    {'type': 'bullet', 'text': '第一点', 'level': 0},
                    {'type': 'bullet', 'text': '第二点', 'level': 0},
                    {'type': 'bullet', 'text': '第三点', 'level': 0}
                ]
            },
            {
                'title': '结束',
                'background': {'fillColor': '#003366'},
                'transition': {'effect': 'fade'},
                'contents': [
                    {'type': 'title', 'text': '谢谢！', 'style': {'color': '#FFFFFF'}},
                    {'type': 'body', 'text': '提问环节', 'style': {'color': '#CCCCCC'}}
                ]
            }
        ]
        metadata = {
            'title': '演示文稿',
            'author': '作者'
        }
    else:
        # 从文件读取
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
            slides = data.get('slides', [])
            metadata = {
                'title': data.get('metadata', {}).get('title', 'Presentation'),
                'author': data.get('metadata', {}).get('author', '')
            }
    
    # 导出
    if args.output:
        filepath = exporter.save(slides, metadata, Path(args.output))
        print(f"Saved to: {filepath}")
    else:
        html = exporter.export(slides, metadata)
        print(html[:2000] + "..." if len(html) > 2000 else html)
