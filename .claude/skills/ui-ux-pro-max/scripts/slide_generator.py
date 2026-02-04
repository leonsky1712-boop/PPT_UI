#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
幻灯片生成器 - 根据推理结果生成幻灯片序列

负责将演示推理结果转换为具体的幻灯片对象，
包括内容、版式、样式、动画和备注。
"""

import csv
import json
from dataclasses import dataclass, field, replace
from typing import Optional, List, Dict, Any, Union
from enum import Enum
from pathlib import Path
from datetime import datetime

# 延迟导入避免循环依赖；运行时由 presentation_generator 先加载 presentation_reasoning
def _get_transition_style():
    from presentation_reasoning import TransitionStyle
    return TransitionStyle


class SlideType(Enum):
    """幻灯片类型"""
    TITLE = "title"
    SECTION_DIVIDER = "section_divider"
    AGENDA = "agenda"
    CONTENT = "content"
    COMPARISON = "comparison"
    CHART = "chart"
    TESTIMONIAL = "testimonial"
    PRICING = "pricing"
    TIMELINE = "timeline"
    QUOTE = "quote"
    CTA = "cta"
    THANK_YOU = "thank_you"
    BLANK = "blank"
    CUSTOM = "custom"


class AnimationTrigger(Enum):
    """动画触发方式"""
    ON_CLICK = "on_click"
    WITH_PREVIOUS = "with_previous"
    AFTER_PREVIOUS = "after_previous"


class AnimationDirection(Enum):
    """动画方向"""
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"
    NONE = "none"


@dataclass
class Position:
    """位置和尺寸"""
    left: float = 0.5  # 英寸
    top: float = 0.5   # 英寸
    width: float = 12   # 英寸
    height: float = 6   # 英寸
    
    def to_dict(self) -> Dict[str, float]:
        return {
            'left': self.left,
            'top': self.top,
            'width': self.width,
            'height': self.height
        }


@dataclass
class TextStyle:
    """文本样式"""
    font_family: str = "Arial"
    font_size: int = 24
    font_weight: str = "normal"
    font_style: str = "normal"
    color: str = "#1A1A1A"
    background_color: Optional[str] = None
    text_align: str = "left"
    line_height: float = 1.5
    letter_spacing: float = 0
    bold: bool = False
    italic: bool = False
    underline: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'fontFamily': self.font_family,
            'fontSize': f"{self.font_size}pt",
            'fontWeight': self.font_weight,
            'fontStyle': self.font_style,
            'color': self.color,
            'backgroundColor': self.background_color,
            'textAlign': self.text_align,
            'lineHeight': self.line_height,
            'letterSpacing': f"{self.letter_spacing}px",
            'bold': self.bold,
            'italic': self.italic,
            'underline': self.underline
        }


@dataclass
class ShapeStyle:
    """形状样式"""
    fill_color: str = "#FFFFFF"
    fill_opacity: float = 1.0
    stroke_color: str = "#E2E8F0"
    stroke_width: float = 0
    stroke_style: str = "solid"
    corner_radius: float = 0
    shadow: bool = False
    shadow_color: str = "rgba(0,0,0,0.1)"
    shadow_offset: float = 4
    shadow_blur: float = 8
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'fillColor': self.fill_color,
            'fillOpacity': self.fill_opacity,
            'strokeColor': self.stroke_color,
            'strokeWidth': self.stroke_width,
            'strokeStyle': self.stroke_style,
            'cornerRadius': self.corner_radius,
            'shadow': self.shadow,
            'shadowColor': self.shadow_color,
            'shadowOffset': self.shadow_offset,
            'shadowBlur': self.shadow_blur
        }


@dataclass
class Animation:
    """动画配置"""
    effect: str = "fade"
    direction: AnimationDirection = AnimationDirection.NONE
    trigger: AnimationTrigger = AnimationTrigger.ON_CLICK
    duration_seconds: float = 0.5
    delay_seconds: float = 0
    order: int = 1
    auto_reverse: bool = False
    repeat_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'effect': self.effect,
            'direction': self.direction.value,
            'trigger': self.trigger.value,
            'duration': f"{self.duration_seconds}s",
            'delay': f"{self.delay_seconds}s",
            'order': self.order,
            'autoReverse': self.auto_reverse,
            'repeatCount': self.repeat_count
        }


@dataclass
class SlideContent:
    """幻灯片内容项"""
    content_id: str
    content_type: str  # title, subtitle, body, bullet, image, chart, quote, etc.
    text: str
    position: Position = field(default_factory=Position)
    text_style: TextStyle = field(default_factory=TextStyle)
    shape_style: Optional[ShapeStyle] = None
    animation: Optional[Animation] = None
    level: int = 0  # 缩进级别（用于列表）
    placeholder: str = ""  # 占位符标识
    data_source: Optional[str] = None  # 数据源引用
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            'id': self.content_id,
            'type': self.content_type,
            'text': self.text,
            'position': self.position.to_dict(),
            'style': self.text_style.to_dict()
        }
        if self.shape_style:
            result['shape'] = self.shape_style.to_dict()
        if self.animation:
            result['animation'] = self.animation.to_dict()
        if self.level > 0:
            result['level'] = self.level
        if self.placeholder:
            result['placeholder'] = self.placeholder
        return result


@dataclass
class Slide:
    """幻灯片数据类"""
    slide_id: str
    slide_type: SlideType
    title: str
    layout: str = ""
    contents: List[SlideContent] = field(default_factory=list)
    notes: str = ""
    background: ShapeStyle = field(default_factory=lambda: ShapeStyle(fill_color="#FFFFFF"))
    transition: Animation = field(default_factory=lambda: Animation(effect="fade"))
    slide_number: int = 0
    aspect_ratio: str = "16:9"
    
    # 元数据
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    modified_at: str = field(default_factory=lambda: datetime.now().isoformat())
    custom_properties: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.slide_id,
            'type': self.slide_type.value,
            'title': self.title,
            'layout': self.layout,
            'slideNumber': self.slide_number,
            'aspectRatio': self.aspect_ratio,
            'background': self.background.to_dict(),
            'transition': self.transition.to_dict(),
            'contents': [c.to_dict() for c in self.contents],
            'notes': self.notes,
            'createdAt': self.created_at,
            'modifiedAt': self.modified_at,
            'customProperties': self.custom_properties
        }


@dataclass
class PresentationMetadata:
    """演示文稿元数据"""
    title: str
    subtitle: Optional[str] = None
    author: Optional[str] = None
    company: Optional[str] = None
    date: str = field(default_factory=lambda: datetime.now().strftime("%B %d, %Y"))
    version: str = "1.0"
    theme: str = "default"
    aspect_ratio: str = "16:9"
    slide_count: int = 0
    estimated_duration_minutes: float = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'title': self.title,
            'subtitle': self.subtitle,
            'author': self.author,
            'company': self.company,
            'date': self.date,
            'version': self.version,
            'theme': self.theme,
            'aspectRatio': self.aspect_ratio,
            'slideCount': self.slide_count,
            'estimatedDurationMinutes': self.estimated_duration_minutes
        }


class SlideGenerator:
    """幻灯片生成器"""
    
    # 版式到幻灯片类型映射
    LAYOUT_TO_TYPE_MAP = {
        'title_slide': SlideType.TITLE,
        'section_divider': SlideType.SECTION_DIVIDER,
        'agenda_slide': SlideType.AGENDA,
        'title_and_content': SlideType.CONTENT,
        'two_content': SlideType.COMPARISON,
        'title_only': SlideType.CONTENT,
        'blank': SlideType.BLANK,
        'picture_with_caption': SlideType.CONTENT,
        'comparison_table': SlideType.COMPARISON,
        'chart_slide': SlideType.CHART,
        'quote_slide': SlideType.QUOTE,
        'testimonial_slide': SlideType.TESTIMONIAL,
        'pricing_slide': SlideType.PRICING,
        'team_grid': SlideType.CONTENT,
        'timeline_slide': SlideType.TIMELINE,
        'testimonial_grid': SlideType.TESTIMONIAL,
        'faq_accordion': SlideType.CONTENT,
        'cta_slide': SlideType.CTA,
        'thank_you_slide': SlideType.THANK_YOU,
        'bio_slide': SlideType.CONTENT,
        'stats_slide': SlideType.CHART,
        'feature_list': SlideType.CONTENT,
        'problem_solution': SlideType.COMPARISON,
        'agenda_with_icons': SlideType.AGENDA,
        'full_image_background': SlideType.TITLE,
        'video_frame': SlideType.CONTENT
    }
    
    # 默认版式配置
    DEFAULT_LAYOUTS = {
        SlideType.TITLE: {
            'title': Position(0.5, 2.5, 12, 1.5),
            'subtitle': Position(0.5, 4, 12, 0.8),
            'background_image': Position(0, 0, 13.33, 7.5)
        },
        SlideType.SECTION_DIVIDER: {
            'title': Position(0.5, 3, 12, 1.5)
        },
        SlideType.AGENDA: {
            'title': Position(0.5, 0.5, 12, 0.8),
            'items': Position(0.5, 1.5, 12, 5)
        },
        SlideType.CONTENT: {
            'title': Position(0.5, 0.3, 12, 0.8),
            'body': Position(0.5, 1.3, 12, 5)
        },
        SlideType.COMPARISON: {
            'title': Position(0.5, 0.3, 12, 0.8),
            'left': Position(0.3, 1.3, 6, 5),
            'right': Position(6.8, 1.3, 6, 5)
        },
        SlideType.CHART: {
            'title': Position(0.5, 0.3, 12, 0.8),
            'chart': Position(0.5, 1.3, 12, 4.5),
            'caption': Position(0.5, 6, 12, 0.8)
        },
        SlideType.QUOTE: {
            'quote': Position(1, 2.5, 11, 2),
            'author': Position(1, 5, 11, 0.5)
        },
        SlideType.CTA: {
            'title': Position(0.5, 2, 12, 1),
            'subtitle': Position(0.5, 3.2, 12, 0.6),
            'cta': Position(4.5, 4.2, 4, 0.8)
        },
        SlideType.THANK_YOU: {
            'title': Position(0.5, 2.5, 12, 1.5),
            'subtitle': Position(0.5, 4.2, 12, 0.6),
            'contact': Position(0.5, 5.2, 12, 0.5)
        }
    }
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        初始化幻灯片生成器
        
        Args:
            data_dir: 数据目录路径
        """
        if data_dir is None:
            self.data_dir = Path(__file__).parent.parent / "data"
        else:
            self.data_dir = Path(data_dir)
        
        # 加载版式数据
        self.layouts = self._load_layouts()
    
    def _load_layouts(self) -> Dict[str, Dict]:
        """加载版式数据"""
        layouts = {}
        layout_file = self.data_dir / "slide-layouts.csv"
        
        if layout_file.exists():
            import csv
            with open(layout_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    layouts[row['Layout_Name']] = row
        
        return layouts
    
    def generate(self, 
                 reasoning: 'PresentationReasoning',
                 slide_plan: List['SlidePlan'],
                 metadata: 'PresentationMetadata') -> List['Slide']:
        """
        根据推理结果和幻灯片规划生成幻灯片序列
        
        Args:
            reasoning: 演示推理结果
            slide_plan: 幻灯片规划列表
            metadata: 演示元数据
            
        Returns:
            List[Slide]: 幻灯片对象列表
        """
        slides = []
        slide_id = 1
        
        # 应用配色方案
        colors = reasoning.colors
        
        # 应用字体方案
        typography = reasoning.typography
        
        # 创建背景样式
        background = ShapeStyle(
            fill_color=colors.get('background', '#FFFFFF'),
            fill_opacity=1.0
        )
        
        # 创建默认标题文本样式
        title_style = TextStyle(
            font_family=typography.get('heading_font', 'Arial'),
            font_size=self._parse_font_size(typography.get('title_size', '44pt')),
            font_weight="bold",
            color=self._hex_to_rgba(colors.get('text', '#1A1A1A')),
            text_align="center"
        )
        
        # 创建默认正文文本样式
        body_style = TextStyle(
            font_family=typography.get('body_font', 'Arial'),
            font_size=self._parse_font_size(typography.get('body_size', '24pt')),
            color=self._hex_to_rgba(colors.get('text', '#1A1A1A')),
            text_align="left"
        )
        
        # 创建CTA样式
        cta_style = TextStyle(
            font_family=typography.get('heading_font', 'Arial'),
            font_size=28,
            font_weight="bold",
            color="#FFFFFF",
            background_color=colors.get('cta', '#FF6600'),
            text_align="center"
        )
        
        # 根据规划生成每张幻灯片
        for plan in slide_plan:
            slide = self._create_slide(
                slide_id= str(slide_id),
                plan=plan,
                reasoning=reasoning,
                colors=colors,
                title_style=title_style,
                body_style=body_style,
                cta_style=cta_style,
                background=background,
                metadata=metadata
            )
            slides.append(slide)
            slide_id += 1
        
        return slides
    
    def _create_slide(self,
                      slide_id: str,
                      plan: 'SlidePlan',
                      reasoning: 'PresentationReasoning',
                      colors: Dict[str, str],
                      title_style: TextStyle,
                      body_style: TextStyle,
                      cta_style: TextStyle,
                      background: ShapeStyle,
                      metadata: 'PresentationMetadata') -> 'Slide':
        """创建单张幻灯片"""
        # 确定幻灯片类型
        slide_type = self.LAYOUT_TO_TYPE_MAP.get(
            plan.layout.replace(' ', '_').lower(),
            SlideType.CONTENT
        )
        
        # 获取版式配置
        layout_config = self.DEFAULT_LAYOUTS.get(slide_type, self.DEFAULT_LAYOUTS[SlideType.CONTENT])
        
        # 创建幻灯片
        slide = Slide(
            slide_id=slide_id,
            slide_type=slide_type,
            title=plan.title,
            layout=plan.layout,
            slide_number=int(slide_id),
            aspect_ratio=metadata.aspect_ratio,
            background=background,
            notes=plan.notes_template,
            transition=self._create_transition(reasoning.transition_style)
        )
        
        # 添加标题
        if slide_type in [SlideType.TITLE, SlideType.SECTION_DIVIDER, SlideType.CTA, SlideType.THANK_YOU]:
            title_pos = layout_config.get('title', Position(0.5, 0.3, 12, 0.8))
            title_style_copy = replace(
                title_style,
                font_size=self._get_title_font_size(slide_type),
                text_align="center"
            )
            
            slide.contents.append(SlideContent(
                content_id=f"{slide_id}_title",
                content_type="title",
                text=plan.title,
                position=title_pos,
                text_style=title_style_copy,
                animation=self._create_animation("fade", AnimationTrigger.ON_CLICK, 0)
            ))
        
        # 根据幻灯片类型添加内容
        if slide_type == SlideType.TITLE:
            self._add_title_content(slide, plan, metadata, body_style, colors, cta_style)
        
        elif slide_type == SlideType.SECTION_DIVIDER:
            self._add_section_content(slide, plan, body_style, colors)
        
        elif slide_type == SlideType.AGENDA:
            self._add_agenda_content(slide, plan, body_style, colors)
        
        elif slide_type in [SlideType.CONTENT, SlideType.CHART]:
            self._add_content_content(slide, plan, body_style, colors)
        
        elif slide_type == SlideType.COMPARISON:
            self._add_comparison_content(slide, plan, body_style, colors)
        
        elif slide_type == SlideType.QUOTE:
            self._add_quote_content(slide, plan, body_style, colors)
        
        elif slide_type == SlideType.CTA:
            self._add_cta_content(slide, plan, cta_style, colors)
        
        elif slide_type == SlideType.THANK_YOU:
            self._add_thankyou_content(slide, plan, body_style, colors)
        
        else:
            # 默认内容处理
            self._add_content_content(slide, plan, body_style, colors)
        
        return slide
    
    def _add_title_content(self, slide: 'Slide', plan: 'SlidePlan', metadata: 'PresentationMetadata',
                          body_style: TextStyle, colors: Dict[str, str], cta_style: TextStyle):
        """添加标题幻灯片内容"""
        # 副标题
        if metadata.subtitle:
            subtitle_pos = Position(0.5, 4, 12, 0.6)
            subtitle_style = replace(body_style, font_size=20, text_align="center")
            subtitle_style.color = self._hex_to_rgba(colors.get('secondary', '#666666'))
            
            slide.contents.append(SlideContent(
                content_id=f"{slide.slide_id}_subtitle",
                content_type="subtitle",
                text=metadata.subtitle,
                position=subtitle_pos,
                text_style=subtitle_style,
                animation=self._create_animation("fade", AnimationTrigger.WITH_PREVIOUS, 0.2)
            ))
        
        # 演讲者信息
        if metadata.author:
            author_pos = Position(0.5, 5.2, 12, 0.5)
            author_style = replace(body_style, font_size=16, text_align="center")
            author_style.color = self._hex_to_rgba(colors.get('secondary', '#666666'))
            
            slide.contents.append(SlideContent(
                content_id=f"{slide.slide_id}_author",
                content_type="body",
                text=metadata.author,
                position=author_pos,
                text_style=author_style,
                animation=self._create_animation("fade", AnimationTrigger.WITH_PREVIOUS, 0.4)
            ))
        
        # 日期
        date_pos = Position(0.5, 5.7, 12, 0.4)
        date_style = replace(body_style, font_size=14, color=self._hex_to_rgba(colors.get('secondary', '#666666')))
        
        slide.contents.append(SlideContent(
            content_id=f"{slide.slide_id}_date",
            content_type="body",
            text=metadata.date,
            position=date_pos,
            text_style=date_style,
            animation=self._create_animation("fade", AnimationTrigger.WITH_PREVIOUS, 0.5)
        ))
    
    def _add_section_content(self, slide: 'Slide', plan: 'SlidePlan', 
                            body_style: TextStyle, colors: Dict[str, str]):
        """添加章节分隔幻灯片内容"""
        # 章节图标或编号
        icon_pos = Position(0.5, 2.5, 12, 0.8)
        icon_style = replace(body_style, font_size=48, font_weight="bold")
        icon_style.color = self._hex_to_rgba(colors.get('primary', '#003366'))
        icon_style.text_align = "center"
        
        slide.contents.append(SlideContent(
            content_id=f"{slide.slide_id}_section_number",
            content_type="icon",
            text="///",
            position=icon_pos,
            text_style=icon_style,
            animation=self._create_animation("fade", AnimationTrigger.ON_CLICK, 0)
        ))
    
    def _add_agenda_content(self, slide: 'Slide', plan: 'SlidePlan',
                            body_style: TextStyle, colors: Dict[str, str]):
        """添加议程幻灯片内容"""
        # 议程项
        items = plan.content_bullets if plan.content_bullets else ["Topic 1", "Topic 2", "Topic 3"]
        
        for i, item in enumerate(items):
            item_pos = Position(0.8, 1.5 + (i * 0.9), 11, 0.7)
            item_style = replace(
                body_style,
                font_size=28,
                color=self._hex_to_rgba(colors.get('text', '#1A1A1A'))
            )
            
            # 为第一项添加编号
            item_text = f"{i + 1}. {item}" if not item.startswith(str(i + 1)) else item
            
            slide.contents.append(SlideContent(
                content_id=f"{slide.slide_id}_agenda_{i}",
                content_type="bullet",
                text=item_text,
                position=item_pos,
                text_style=item_style,
                animation=self._create_animation("fade", AnimationTrigger.ON_CLICK, i * 0.3),
                level=0
            ))
    
    def _add_content_content(self, slide: 'Slide', plan: 'SlidePlan',
                           body_style: TextStyle, colors: Dict[str, str]):
        """添加内容幻灯片内容"""
        # 内容要点
        items = plan.content_bullets if plan.content_bullets else ["Key point 1", "Key point 2", "Key point 3"]
        
        for i, item in enumerate(items):
            item_pos = Position(0.8, 1.8 + (i * 1), 11.5, 0.8)
            item_style = replace(body_style, font_size=26)
            
            slide.contents.append(SlideContent(
                content_id=f"{slide.slide_id}_content_{i}",
                content_type="bullet",
                text=item,
                position=item_pos,
                text_style=item_style,
                animation=self._create_animation("fade", AnimationTrigger.ON_CLICK, i * 0.4),
                level=0
            ))
    
    def _add_comparison_content(self, slide: 'Slide', plan: 'SlidePlan',
                                body_style: TextStyle, colors: Dict[str, str]):
        """添加对比幻灯片内容"""
        # 左侧内容
        left_items = plan.content_bullets[:3] if len(plan.content_bullets) > 3 else ["Left point 1", "Left point 2", "Left point 3"]
        for i, item in enumerate(left_items):
            item_pos = Position(0.5, 1.5 + (i * 0.9), 5.8, 0.7)
            item_style = replace(body_style, font_size=22)
            
            slide.contents.append(SlideContent(
                content_id=f"{slide.slide_id}_left_{i}",
                content_type="bullet",
                text=item,
                position=item_pos,
                text_style=item_style,
                animation=self._create_animation("fade", AnimationTrigger.ON_CLICK, i * 0.3)
            ))
        
        # 右侧内容
        right_items = plan.content_bullets[3:6] if len(plan.content_bullets) > 3 else ["Right point 1", "Right point 2", "Right point 3"]
        for i, item in enumerate(right_items):
            item_pos = Position(6.8, 1.5 + (i * 0.9), 5.8, 0.7)
            item_style = replace(body_style, font_size=22)
            
            slide.contents.append(SlideContent(
                content_id=f"{slide.slide_id}_right_{i}",
                content_type="bullet",
                text=item,
                position=item_pos,
                text_style=item_style,
                animation=self._create_animation("fade", AnimationTrigger.ON_CLICK, (i + 3) * 0.3)
            ))
    
    def _add_quote_content(self, slide: 'Slide', plan: 'SlidePlan',
                          body_style: TextStyle, colors: Dict[str, str]):
        """添加引用幻灯片内容"""
        # 引用文本
        quote_pos = Position(1, 2.5, 11, 2)
        quote_style = replace(
            body_style,
            font_size=32,
            font_style="italic",
            color=self._hex_to_rgba(colors.get('primary', '#003366'))
        )
        quote_style.text_align = "center"
        
        quote_text = plan.content_bullets[0] if plan.content_bullets else "Insert quote here"
        slide.contents.append(SlideContent(
            content_id=f"{slide.slide_id}_quote",
            content_type="quote",
            text=f'"{quote_text}"',
            position=quote_pos,
            text_style=quote_style,
            animation=self._create_animation("fade", AnimationTrigger.ON_CLICK, 0)
        ))
        
        # 署名
        if len(plan.content_bullets) > 1:
            author_pos = Position(1, 5, 11, 0.5)
            author_style = replace(
                body_style,
                font_size=18,
                text_align="center",
                color=self._hex_to_rgba(colors.get('secondary', '#666666'))
            )
            
            slide.contents.append(SlideContent(
                content_id=f"{slide.slide_id}_quote_author",
                content_type="body",
                text=f"- {plan.content_bullets[1]}",
                position=author_pos,
                text_style=author_style,
                animation=self._create_animation("fade", AnimationTrigger.WITH_PREVIOUS, 0.5)
            ))
    
    def _add_cta_content(self, slide: 'Slide', plan: 'SlidePlan',
                        cta_style: TextStyle, colors: Dict[str, str]):
        """添加CTA幻灯片内容"""
        # CTA 按钮区域
        cta_pos = Position(4.5, 4.2, 4, 0.8)
        cta_button_style = ShapeStyle(
            fill_color=colors.get('cta', '#FF6600'),
            fill_opacity=1.0,
            corner_radius=8,
            shadow=True,
            shadow_color="rgba(0,0,0,0.2)"
        )
        
        slide.contents.append(SlideContent(
            content_id=f"{slide.slide_id}_cta_button",
            content_type="cta_button",
            text="Get Started",
            position=cta_pos,
            text_style=cta_style,
            shape_style=cta_button_style,
            animation=self._create_animation("fade", AnimationTrigger.ON_CLICK, 0)
        ))
    
    def _add_thankyou_content(self, slide: 'Slide', plan: 'SlidePlan',
                             body_style: TextStyle, colors: Dict[str, str]):
        """添加感谢幻灯片内容"""
        # 副标题
        subtitle_pos = Position(0.5, 4, 12, 0.6)
        subtitle_style = replace(
            body_style,
            font_size=24,
            text_align="center",
            color=self._hex_to_rgba(colors.get('secondary', '#666666'))
        )
        
        slide.contents.append(SlideContent(
            content_id=f"{slide.slide_id}_subtitle",
            content_type="subtitle",
            text="Questions?",
            position=subtitle_pos,
            text_style=subtitle_style,
            animation=self._create_animation("fade", AnimationTrigger.WITH_PREVIOUS, 0.2)
        ))
        
        # 联系信息
        if plan.content_bullets:
            contact_pos = Position(0.5, 5.2, 12, 0.5)
            contact_style = replace(
                body_style,
                font_size=16,
                text_align="center",
                color=self._hex_to_rgba(colors.get('secondary', '#666666'))
            )
            
            slide.contents.append(SlideContent(
                content_id=f"{slide.slide_id}_contact",
                content_type="body",
                text=plan.content_bullets[0] if plan.content_bullets else "contact@example.com",
                position=contact_pos,
                text_style=contact_style,
                animation=self._create_animation("fade", AnimationTrigger.WITH_PREVIOUS, 0.4)
            ))
    
    def _create_animation(self, effect: str, trigger: AnimationTrigger, delay: float) -> Animation:
        """创建动画配置"""
        return Animation(
            effect=effect,
            direction=AnimationDirection.NONE,
            trigger=trigger,
            duration_seconds=0.5,
            delay_seconds=delay,
            order=1
        )
    
    def _create_transition(self, style: 'TransitionStyle') -> Animation:
        """创建过渡配置"""
        TransitionStyle = _get_transition_style()
        effect_map = {
            TransitionStyle.FADE: "fade",
            TransitionStyle.SLIDE: "slide",
            TransitionStyle.PUSH: "push",
            TransitionStyle.ZOOM: "zoom"
        }
        
        return Animation(
            effect=effect_map.get(style, "fade"),
            direction=AnimationDirection.NONE,
            trigger=AnimationTrigger.ON_CLICK,
            duration_seconds=0.4
        )
    
    def _parse_font_size(self, size_str: str) -> int:
        """解析字体大小字符串"""
        try:
            return int(size_str.replace('pt', '').replace('px', '').split('-')[0])
        except (ValueError, AttributeError):
            return 24
    
    def _get_title_font_size(self, slide_type: SlideType) -> int:
        """根据幻灯片类型获取标题字体大小"""
        size_map = {
            SlideType.TITLE: 54,
            SlideType.SECTION_DIVIDER: 48,
            SlideType.CTA: 44,
            SlideType.THANK_YOU: 44,
            SlideType.AGENDA: 36,
            SlideType.CONTENT: 36,
            SlideType.COMPARISON: 36,
            SlideType.CHART: 36,
            SlideType.QUOTE: 32
        }
        return size_map.get(slide_type, 36)
    
    def _hex_to_rgba(self, hex_color: str, alpha: float = 1.0) -> str:
        """将十六进制颜色转换为RGBA"""
        if not hex_color:
            return f"rgba(0,0,0,{alpha})"
        
        hex_color = hex_color.lstrip('#')
        
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return f"rgba({r},{g},{b},{alpha})"
        elif len(hex_color) == 3:
            r = int(hex_color[0] * 2, 16)
            g = int(hex_color[1] * 2, 16)
            b = int(hex_color[2] * 2, 16)
            return f"rgba({r},{g},{b},{alpha})"
        
        return f"rgba(0,0,0,{alpha})"
    
    def export_to_dict(self, slides: List[Slide]) -> Dict[str, Any]:
        """导出幻灯片列表为字典"""
        return {
            'slides': [slide.to_dict() for slide in slides]
        }
    
    def export_to_json(self, slides: List[Slide], filepath: Optional[Path] = None) -> str:
        """导出幻灯片列表为JSON"""
        data = self.export_to_dict(slides)
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_str)
        
        return json_str


# 辅助类
from presentation_reasoning import PresentationReasoning, SlidePlan


# CLI 支持
if __name__ == "__main__":
    import argparse
    from presentation_reasoning import PresentationReasoningEngine, PresentationRequest, PresentationType, AudienceType, Tone
    
    parser = argparse.ArgumentParser(description="Slide Generator")
    parser.add_argument("--title", default="My Presentation", help="Presentation title")
    parser.add_argument("--type", default="business_presentation", help="Presentation type")
    parser.add_argument("--audience", default="general", help="Target audience")
    parser.add_argument("--duration", type=int, default=20, help="Duration in minutes")
    parser.add_argument("--tone", default="professional", help="Presentation tone")
    parser.add_argument("--output", help="Output JSON file")
    
    args = parser.parse_args()
    
    # 创建推理引擎
    engine = PresentationReasoningEngine()
    
    # 创建请求
    request = PresentationRequest(
        title=args.title,
        presentation_type=PresentationType(args.type),
        audience=AudienceType(args.audience),
        duration_minutes=args.duration,
        tone=Tone(args.tone)
    )
    
    # 分析并生成幻灯片规划
    reasoning = engine.analyze(request)
    slide_plans = engine.generate_slide_plan(reasoning, request)
    
    # 创建幻灯片
    generator = SlideGenerator()
    
    metadata = PresentationMetadata(
        title=args.title,
        subtitle="Subtitle here",
        author="Your Name"
    )
    
    slides = generator.generate(reasoning, slide_plans, metadata)
    
    # 导出
    output_path = Path(args.output) if args.output else None
    json_str = generator.export_to_json(slides, output_path)
    
    print(f"Generated {len(slides)} slides")
    print(json_str[:2000] + "..." if len(json_str) > 2000 else json_str)
