#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示文稿生成器主模块

协调推理引擎和幻灯片生成器，提供完整的演示文稿生成能力。
支持多种输出格式（JSON、PPTX、Reveal.js等）。
"""

import json
import csv
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum


class OutputFormat(Enum):
    """输出格式枚举"""
    JSON = "json"
    DICT = "dict"
    PPTX = "pptx"
    REVEAL_JS = "reveal_js"
    MARKDOWN = "markdown"


class PresentationGenerator:
    """
    演示文稿生成器主类
    
    整合推理引擎和幻灯片生成器，提供完整的演示文稿生成流程。
    """
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        初始化演示文稿生成器
        
        Args:
            data_dir: 数据目录路径，如果为 None 则使用默认路径
        """
        # 导入依赖模块
        from presentation_reasoning import (
            PresentationReasoningEngine,
            PresentationRequest,
            PresentationReasoning
        )
        from slide_generator import (
            SlideGenerator,
            PresentationMetadata,
            Slide
        )
        
        self.PresentationRequest = PresentationRequest
        self.PresentationReasoning = PresentationReasoning
        self.PresentationMetadata = PresentationMetadata
        self.Slide = Slide
        
        # 初始化引擎
        if data_dir is None:
            self.data_dir = Path(__file__).parent.parent / "data"
        else:
            self.data_dir = Path(data_dir)
        
        self.reasoning_engine = PresentationReasoningEngine(self.data_dir)
        self.slide_generator = SlideGenerator(self.data_dir)
    
    def generate(self,
                 title: str,
                 presentation_type: str,
                 audience: str,
                 duration_minutes: int,
                 tone: str = "professional",
                 industry: str = "",
                 key_points: List[str] = None,
                 objectives: List[str] = None,
                 output_format: OutputFormat = OutputFormat.JSON,
                 options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        生成演示文稿
        
        Args:
            title: 演示文稿标题
            presentation_type: 演示类型
            audience: 目标受众
            duration_minutes: 预计时长（分钟）
            tone: 基调
            industry: 行业
            key_points: 关键要点列表
            objectives: 目标列表
            output_format: 输出格式
            options: 额外选项
            
        Returns:
            Dict[str, Any]: 生成结果
        """
        options = options or {}
        
        # 1. 创建请求
        request = self._create_request(
            title=title,
            presentation_type=presentation_type,
            audience=audience,
            duration_minutes=duration_minutes,
            tone=tone,
            industry=industry,
            key_points=key_points or [],
            objectives=objectives or [],
            options=options
        )
        
        # 2. 推理分析
        reasoning = self.reasoning_engine.analyze(request)
        
        # 3. 生成幻灯片规划
        slide_plans = self.reasoning_engine.generate_slide_plan(reasoning, request)
        
        # 4. 创建元数据
        metadata = self._create_metadata(request, reasoning, len(slide_plans), options)
        
        # 5. 生成幻灯片
        slides = self.slide_generator.generate(reasoning, slide_plans, metadata)
        
        # 6. 格式化输出
        result = self._format_output(
            slides=slides,
            reasoning=reasoning,
            metadata=metadata,
            output_format=output_format
        )
        
        return result
    
    def generate_from_request(self,
                               request: 'PresentationRequest',
                               output_format: OutputFormat = OutputFormat.JSON) -> Dict[str, Any]:
        """
        根据请求对象生成演示文稿
        
        Args:
            request: 演示请求对象
            output_format: 输出格式
            
        Returns:
            Dict[str, Any]: 生成结果
        """
        # 1. 推理分析
        reasoning = self.reasoning_engine.analyze(request)
        
        # 2. 生成幻灯片规划
        slide_plans = self.reasoning_engine.generate_slide_plan(reasoning, request)
        
        # 3. 创建元数据
        metadata = self._create_metadata(request, reasoning, len(slide_plans), options=None)
        
        # 4. 生成幻灯片
        slides = self.slide_generator.generate(reasoning, slide_plans, metadata)
        
        # 5. 格式化输出
        result = self._format_output(
            slides=slides,
            reasoning=reasoning,
            metadata=metadata,
            output_format=output_format
        )
        
        return result
    
    def _create_request(self,
                        title: str,
                        presentation_type: str,
                        audience: str,
                        duration_minutes: int,
                        tone: str,
                        industry: str,
                        key_points: List[str],
                        objectives: List[str],
                        options: Dict[str, Any]) -> 'PresentationRequest':
        """创建演示请求"""
        # 导入枚举
        from presentation_reasoning import (
            PresentationType,
            AudienceType,
            Tone
        )
        
        # 转换类型
        try:
            pt = PresentationType(presentation_type)
        except ValueError:
            pt = PresentationType.BUSINESS_PRESENTATION
        
        try:
            at = AudienceType(audience)
        except ValueError:
            at = AudienceType.GENERAL_EMPLOYEES
        
        try:
            t = Tone(tone)
        except ValueError:
            t = Tone.PROFESSIONAL
        
        return self.PresentationRequest(
            title=title,
            presentation_type=pt,
            audience=at,
            duration_minutes=duration_minutes,
            tone=t,
            industry=industry,
            key_points=key_points,
            objectives=objectives,
            aspect_ratio=options.get('aspect_ratio', '16:9'),
            include_animations=options.get('include_animations', True),
            include_transitions=options.get('include_transitions', True)
        )
    
    def _create_metadata(self, request: 'PresentationRequest', 
                        reasoning: 'PresentationReasoning',
                        slide_count: int,
                        options: Optional[Dict[str, Any]] = None) -> 'PresentationMetadata':
        """创建演示元数据"""
        opts = options or {}
        return self.PresentationMetadata(
            title=request.title,
            subtitle=f"Presented by: {request.industry}" if request.industry else None,
            author=opts.get('author', None),
            company=opts.get('company', None),
            version="1.0",
            theme=reasoning.style.get('name', 'default'),
            aspect_ratio=request.aspect_ratio,
            slide_count=slide_count,
            estimated_duration_minutes=request.duration_minutes
        )
    
    def _format_output(self,
                      slides: List['Slide'],
                      reasoning: 'PresentationReasoning',
                      metadata: 'PresentationMetadata',
                      output_format: OutputFormat) -> Dict[str, Any]:
        """格式化输出"""
        if output_format == OutputFormat.DICT:
            return self._to_dict(slides, reasoning, metadata)
        elif output_format == OutputFormat.JSON:
            return json.loads(self._to_json(slides, reasoning, metadata))
        elif output_format == OutputFormat.REVEAL_JS:
            return self._to_reveal_js(slides, reasoning, metadata)
        elif output_format == OutputFormat.MARKDOWN:
            return self._to_markdown(slides, reasoning, metadata)
        else:
            return self._to_dict(slides, reasoning, metadata)
    
    def _to_dict(self,
                slides: List['Slide'],
                reasoning: 'PresentationReasoning',
                metadata: 'PresentationMetadata') -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'metadata': {
                'title': metadata.title,
                'subtitle': metadata.subtitle,
                'author': metadata.author,
                'company': metadata.company,
                'date': metadata.date,
                'version': metadata.version,
                'theme': metadata.theme,
                'aspectRatio': metadata.aspect_ratio,
                'slideCount': metadata.slide_count,
                'estimatedDurationMinutes': metadata.estimated_duration_minutes
            },
            'reasoning': {
                'presentationType': reasoning.presentation_type.value,
                'pattern': reasoning.pattern.get('Pattern_Name', ''),
                'style': reasoning.style.get('name', ''),
                'colors': reasoning.colors.get('name', ''),
                'typography': reasoning.typography.get('name', ''),
                'slideCount': reasoning.slide_count_estimate,
                'timePerSlide': reasoning.time_per_slide_estimate,
                'animationIntensity': reasoning.animation_intensity.value,
                'transitionStyle': reasoning.transition_style.value,
                'toneAdjustment': reasoning.tone_adjustment
            },
            'recommendations': reasoning.recommendations,
            'antiPatterns': reasoning.anti_patterns,
            'slides': [slide.to_dict() for slide in slides]
        }
    
    def _to_json(self,
                slides: List['Slide'],
                reasoning: 'PresentationReasoning',
                metadata: 'PresentationMetadata') -> str:
        """转换为JSON字符串"""
        data = self._to_dict(slides, reasoning, metadata)
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def _to_reveal_js(self,
                      slides: List['Slide'],
                      reasoning: 'PresentationReasoning',
                      metadata: 'PresentationMetadata') -> Dict[str, Any]:
        """转换为Reveal.js格式"""
        reveal_slides = []
        
        for slide in slides:
            slide_html = ""
            
            # 根据幻灯片类型生成HTML
            for content in slide.contents:
                if content.content_type == "title":
                    slide_html += f'<h2>{content.text}</h2>\n'
                elif content.content_type == "subtitle":
                    slide_html += f'<p class="subtitle">{content.text}</p>\n'
                elif content.content_type == "bullet":
                    level = "  " * content.level
                    slide_html += f'{level}<li>{content.text}</li>\n'
                elif content.content_type == "body":
                    slide_html += f'<p>{content.text}</p>\n'
                elif content.content_type == "quote":
                    slide_html += f'<blockquote>{content.text}</blockquote>\n'
                elif content.content_type == "cta_button":
                    slide_html += f'<div class="cta-button">{content.text}</div>\n'
            
            # 背景样式
            bg_color = slide.background.fill_color
            
            reveal_slide = {
                'content': slide_html,
                'background': bg_color,
                'transition': slide.transition.effect,
                'title': slide.title,
                'notes': slide.notes
            }
            
            reveal_slides.append(reveal_slide)
        
        return {
            'title': metadata.title,
            'theme': 'black',
            'config': {
                'controls': True,
                'progress': True,
                'hash': True,
                'transition': reasoning.transition_style.value
            },
            'slides': reveal_slides,
            'metadata': {
                'author': metadata.author,
                'date': metadata.date
            }
        }
    
    def _to_markdown(self,
                     slides: List['Slide'],
                     reasoning: 'PresentationReasoning',
                     metadata: 'PresentationMetadata') -> str:
        """转换为Markdown格式"""
        lines = []
        
        # 标题
        lines.append(f"# {metadata.title}")
        lines.append("")
        lines.append(f"**副标题**: {metadata.subtitle or '无'}")
        lines.append(f"**作者**: {metadata.author or '未知'}")
        lines.append(f"**日期**: {metadata.date}")
        lines.append(f"**幻灯片数**: {metadata.slide_count}")
        lines.append(f"**预计时长**: {metadata.estimated_duration_minutes} 分钟")
        lines.append("")
        
        lines.append("---")
        lines.append("")
        
        # 设计系统摘要
        lines.append("## 设计系统")
        lines.append(f"- **模式**: {reasoning.pattern.get('Pattern_Name', 'Standard')}")
        lines.append(f"- **风格**: {reasoning.style.get('name', 'Minimalism')}")
        lines.append(f"- **配色**: {reasoning.colors.get('name', 'Professional Blue')}")
        lines.append(f"- **字体**: {reasoning.typography.get('name', 'Modern Professional')}")
        lines.append(f"- **动画强度**: {reasoning.animation_intensity.value}")
        lines.append("")
        
        lines.append("---")
        lines.append("")
        
        # 幻灯片列表
        lines.append("## 幻灯片内容")
        lines.append("")
        
        for i, slide in enumerate(slides, 1):
            lines.append(f"### 幻灯片 {i}: {slide.title}")
            lines.append(f"- **类型**: {slide.slide_type.value}")
            lines.append(f"- **版式**: {slide.layout}")
            lines.append("")
            
            for content in slide.contents:
                if content.content_type == "title":
                    lines.append(f"**标题**: {content.text}")
                elif content.content_type == "bullet":
                    prefix = "  " * content.level + "-"
                    lines.append(f"{prefix} {content.text}")
                elif content.content_type == "body":
                    lines.append(f"{content.text}")
            
            if slide.notes:
                lines.append(f"**演讲备注**: {slide.notes}")
            
            lines.append("")
            lines.append("---")
            lines.append("")
        
        # 建议
        lines.append("")
        lines.append("## 演示建议")
        lines.append("")
        for rec in reasoning.recommendations[:5]:
            lines.append(f"- {rec}")
        
        return "\n".join(lines)
    
    def get_available_types(self) -> List[Dict[str, str]]:
        """获取可用的演示类型"""
        return self.reasoning_engine.get_available_presentation_types()
    
    def get_available_audiences(self) -> List[Dict[str, str]]:
        """获取可用的受众类型"""
        return self.reasoning_engine.get_available_audiences()
    
    def get_available_tones(self) -> List[Dict[str, str]]:
        """获取可用的基调"""
        return self.reasoning_engine.get_available_tones()
    
    def quick_generate(self,
                      query: str,
                      duration: int = 20,
                      audience: str = "general") -> Dict[str, Any]:
        """
        快速生成演示文稿
        
        Args:
            query: 查询字符串，将自动检测演示类型
            duration: 时长（分钟）
            audience: 受众
            
        Returns:
            Dict[str, Any]: 生成结果
        """
        # 简单类型检测
        query_lower = query.lower()
        
        if any(kw in query_lower for kw in ['pitch', 'investor', 'vc', 'fundraising']):
            presentation_type = "investor_pitch"
        elif any(kw in query_lower for kw in ['launch', 'product', 'announce']):
            presentation_type = "product_launch"
        elif any(kw in query_lower for kw in ['training', 'workshop', 'learn']):
            presentation_type = "training_workshop"
        elif any(kw in query_lower for kw in ['quarterly', 'review', 'quarter']):
            presentation_type = "quarterly_review"
        elif any(kw in query_lower for kw in ['conference', 'talk', 'speech']):
            presentation_type = "conference_talk"
        elif any(kw in query_lower for kw in ['technical', 'engineering', 'developer']):
            presentation_type = "technical_workshop"
        else:
            presentation_type = "business_presentation"
        
        return self.generate(
            title=query,
            presentation_type=presentation_type,
            audience=audience,
            duration_minutes=duration,
            tone="professional"
        )


# 便捷函数
def create_presentation(title: str,
                       type: str,
                       audience: str,
                       duration: int,
                       tone: str = "professional",
                       data_dir: str = None) -> Dict[str, Any]:
    """
    创建演示文稿的便捷函数
    
    Args:
        title: 标题
        type: 类型
        audience: 受众
        duration: 时长
        tone: 基调
        data_dir: 数据目录
        
    Returns:
        Dict[str, Any]: 生成结果
    """
    generator = PresentationGenerator(Path(data_dir) if data_dir else None)
    return generator.generate(
        title=title,
        presentation_type=type,
        audience=audience,
        duration_minutes=duration,
        tone=tone
    )


def quick_presentation(query: str,
                      duration: int = 20,
                      data_dir: str = None) -> Dict[str, Any]:
    """
    快速创建演示文稿
    
    Args:
        query: 描述
        duration: 时长
        data_dir: 数据目录
        
    Returns:
        Dict[str, Any]: 生成结果
    """
    generator = PresentationGenerator(Path(data_dir) if data_dir else None)
    return generator.quick_generate(query, duration)


# CLI 支持
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Presentation Generator")
    parser.add_argument("title", help="Presentation title")
    parser.add_argument("--type", "-t", default="business_presentation", help="Presentation type")
    parser.add_argument("--audience", "-a", default="general", help="Target audience")
    parser.add_argument("--duration", "-d", type=int, default=20, help="Duration in minutes")
    parser.add_argument("--tone", default="professional", help="Presentation tone")
    parser.add_argument("--output", "-o", help="Output JSON file")
    parser.add_argument("--format", "-f", choices=["json", "markdown", "reveal"], default="json", help="Output format")
    
    args = parser.parse_args()
    
    # 格式化映射
    format_map = {
        "json": OutputFormat.JSON,
        "markdown": OutputFormat.MARKDOWN,
        "reveal": OutputFormat.REVEAL_JS
    }
    
    # 生成
    generator = PresentationGenerator()
    result = generator.generate(
        title=args.title,
        presentation_type=args.type,
        audience=args.audience,
        duration_minutes=args.duration,
        tone=args.tone,
        output_format=format_map.get(args.format, OutputFormat.JSON)
    )
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            if isinstance(result, dict):
                json.dump(result, f, indent=2, ensure_ascii=False)
            else:
                f.write(str(result))
        print(f"Saved to {args.output}")
    else:
        if isinstance(result, dict):
            print(json.dumps(result, indent=2, ensure_ascii=False)[:3000])
        else:
            print(str(result)[:3000])
