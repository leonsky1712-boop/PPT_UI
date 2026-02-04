#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示推理引擎 - 基于现有设计系统生成器的扩展

提供演示文稿的智能推理能力，包括：
- 演示类型分类
- 风格匹配
- 配色方案选择
- 字体搭配推荐
- 受众适配
- 时间优化
"""

import csv
import json
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum
from pathlib import Path
from datetime import datetime


class PresentationType(Enum):
    """演示类型枚举"""
    BUSINESS_PRESENTATION = "business_presentation"
    PRODUCT_LAUNCH = "product_launch"
    INVESTOR_PITCH = "investor_pitch"
    TRAINING_WORKSHOP = "training_workshop"
    CONFERENCE_TALK = "conference_talk"
    QUARTERLY_REVIEW = "quarterly_review"
    TECHNICAL_WORKSHOP = "technical_workshop"
    CRISIS_COMMUNICATION = "crisis_communication"
    WEBINAR = "webinar"
    CASE_STUDY = "case_study"
    TEAM_MEETING = "team_meeting"
    STRATEGIC_PLANNING = "strategic_planning"
    EXECUTIVE_BRIEFING = "executive_briefing"
    CUSTOMER_PRESENTATION = "customer_presentation"
    DESIGN_REVIEW = "design_review"
    ALL_HANDS = "all_hands"
    PRODUCT_DEMO = "product_demo"
    INNOVATION_WORKSHOP = "innovation_workshop"
    COMPLIANCE_TRAINING = "compliance_training"
    CHANGE_MANAGEMENT = "change_management"


class AudienceType(Enum):
    """受众类型枚举"""
    SENIOR_EXECUTIVES = "senior_executives"
    MIDDLE_MANAGERS = "middle_managers"
    INVESTORS = "investors"
    TECHNICAL_TEAMS = "technical_teams"
    GENERAL_EMPLOYEES = "general_employees"
    CUSTOMERS_PROSPECTS = "customers_prospects"
    CUSTOMERS_EXISTING = "customers_existing"
    PARTNERS = "partners"
    EXTERNAL_GUESTS = "external_guests"
    STUDENTS_TRAINEES = "students_trainees"
    LEADERSHIP_TEAM = "leadership_team"
    BOARD_OF_DIRECTORS = "board_of_directors"
    HR_LD = "hr_ld"
    MARKETING_TEAM = "marketing_team"
    ENGINEERING_TEAM = "engineering_team"
    PRODUCT_TEAM = "product_team"
    LEGAL_COMPLIANCE = "legal_compliance"
    FINANCE_TEAM = "finance_team"


class Tone(Enum):
    """演示基调枚举"""
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    INSPIRING = "inspiring"
    URGENT = "urgent"
    EDUCATIONAL = "educational"
    PERSUASIVE = "persuasive"
    TECHNICAL = "technical"
    SUPPORTIVE = "supportive"
    AUTHORITATIVE = "authoritative"
    EMPATHETIC = "empathetic"


class AnimationIntensity(Enum):
    """动画强度枚举"""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TransitionStyle(Enum):
    """过渡风格枚举"""
    FADE = "fade"
    SLIDE = "slide"
    PUSH = "push"
    ZOOM = "zoom"


@dataclass
class PresentationRequest:
    """演示请求数据类"""
    title: str
    presentation_type: PresentationType
    audience: AudienceType
    duration_minutes: int
    tone: Tone
    industry: str = ""
    key_points: List[str] = field(default_factory=list)
    objectives: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)
    # 额外选项
    aspect_ratio: str = "16:9"
    include_animations: bool = True
    include_transitions: bool = True


@dataclass
class PresentationReasoning:
    """演示推理结果数据类"""
    # 基础信息
    presentation_type: PresentationType
    pattern: Dict[str, Any]
    style: Dict[str, Any]
    colors: Dict[str, Any]
    typography: Dict[str, Any]
    
    # 结构信息
    structure: Dict[str, Any]
    slide_count_estimate: int
    time_per_slide_estimate: float
    
    # 动画和过渡
    animation_intensity: AnimationIntensity
    transition_style: TransitionStyle
    recommended_animations: List[Dict[str, Any]]
    
    # 受众适配
    audience_adaptation: Dict[str, Any]
    tone_adjustment: str
    
    # 建议和反模式
    recommendations: List[str]
    anti_patterns: List[str]
    
    # 元数据
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class SlidePlan:
    """幻灯片规划数据类"""
    slide_type: str
    title: str
    layout: str
    content_bullets: List[str]
    notes_template: str
    estimated_time_seconds: float
    animation: Dict[str, Any] = field(default_factory=dict)


class PresentationReasoningEngine:
    """
    演示推理引擎
    
    基于现有的 UI/UX 推理能力，扩展到演示文稿领域。
    负责分析演示需求，匹配最佳模式、风格、配色和字体。
    """
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        初始化推理引擎
        
        Args:
            data_dir: 数据目录路径，如果为 None 则使用默认路径
        """
        if data_dir is None:
            # 默认路径相对于当前文件
            self.data_dir = Path(__file__).parent.parent / "data"
        else:
            self.data_dir = Path(data_dir)
        
        # 加载所有数据
        self._load_all_data()
        
    def _load_all_data(self):
        """加载所有演示相关数据"""
        # 加载演示模式
        self.patterns = self._load_csv("presentation-patterns.csv")
        
        # 加载演示推理规则
        self.reasoning_rules = self._load_csv("presentation-reasoning.csv")
        
        # 加载幻灯片版式
        self.layouts = self._load_csv("slide-layouts.csv")
        
        # 加载动画效果
        self.animations = self._load_csv("slide-animations.csv")
        
        # 加载模板
        self.templates = self._load_csv("presentation-templates.csv")
        
        # 加载受众指南
        self.audience_guidelines = self._load_csv("audience-guidelines.csv")
        
        # 加载演讲备注
        self.speech_notes = self._load_csv("speech-notes.csv")
        
        # 加载演示专用样式扩展
        self.styles_presentation = self._load_csv("styles_presentation.csv")
        
        # 加载投影安全配色
        self.colors_presentation = self._load_csv("colors_presentation.csv")
        
        # 加载演示字体配置
        self.typography_presentation = self._load_csv("typography_presentation.csv")
        
    def _load_csv(self, filename: str) -> List[Dict[str, str]]:
        """加载 CSV 文件"""
        filepath = self.data_dir / filename
        if not filepath.exists():
            return []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    
    def analyze(self, request: PresentationRequest) -> PresentationReasoning:
        """
        综合分析生成推理结果
        
        Args:
            request: 演示请求
            
        Returns:
            PresentationReasoning: 完整的推理结果
        """
        # 1. 确定演示模式
        pattern = self._match_pattern(request)
        
        # 2. 匹配风格
        style = self._match_style(request, pattern)
        
        # 3. 选择配色方案
        colors = self._select_colors(request, pattern)
        
        # 4. 选择字体搭配
        typography = self._select_typography(request, pattern)
        
        # 5. 规划结构
        structure = self._plan_structure(request, pattern)
        
        # 6. 选择动画配置
        animation_intensity, transition_style, animations = self._select_animations(request, pattern)
        
        # 7. 受众适配
        audience_adaptation = self._adapt_for_audience(request.audience, request.presentation_type)
        
        # 8. 基调调整
        tone_adjustment = self._adjust_tone(request.tone, request.presentation_type, pattern)
        
        # 9. 估算幻灯片数量和时间
        slide_count = self._estimate_slides(request, pattern)
        time_per_slide = request.duration_minutes * 60 / slide_count if slide_count > 0 else 120
        
        # 10. 生成建议和反模式
        recommendations = self._generate_recommendations(request, pattern, audience_adaptation)
        anti_patterns = self._identify_anti_patterns(request, pattern)
        
        return PresentationReasoning(
            presentation_type=request.presentation_type,
            pattern=pattern,
            style=style,
            colors=colors,
            typography=typography,
            structure=structure,
            slide_count_estimate=slide_count,
            time_per_slide_estimate=time_per_slide,
            animation_intensity=animation_intensity,
            transition_style=transition_style,
            recommended_animations=animations,
            audience_adaptation=audience_adaptation,
            tone_adjustment=tone_adjustment,
            recommendations=recommendations,
            anti_patterns=anti_patterns
        )
    
    def _match_pattern(self, request: PresentationRequest) -> Dict[str, Any]:
        """匹配最佳演示模式"""
        best_match = None
        best_score = 0
        
        # 查找匹配的规则
        category = request.presentation_type.value.replace("_", " ")
        
        for pattern in self.patterns:
            score = 0
            
            # 匹配类型（精确匹配）
            pattern_category = pattern.get('Pattern_Category', '').lower()
            if category.lower() in pattern_category or pattern_category in category.lower():
                score += 10
            
            # 匹配时长
            try:
                min_dur = int(pattern.get('Duration_Range_Min', 0))
                max_dur = int(pattern.get('Duration_Range_Max', 100))
                if min_dur <= request.duration_minutes <= max_dur:
                    score += 5
            except (ValueError, TypeError):
                pass
            
            # 匹配基调
            if request.tone.value.lower() in pattern.get('Tone', '').lower():
                score += 3
            
            if score > best_score:
                best_score = score
                best_match = pattern
        
        # 如果没有精确匹配，返回默认模式
        if not best_match:
            best_match = {
                'Pattern_Name': 'Standard Business Presentation',
                'Pattern_Category': 'business',
                'Duration_Range_Min': '15',
                'Duration_Range_Max': '30',
                'Slide_Count_Min': '12',
                'Slide_Count_Max': '20',
                'Structure_Format': 'Opening→Agenda→Content→Q&A→Closing',
                'Tone': 'Professional',
                'Animation_Intensity': 'Low',
                'Transition_Style': 'Push or Fade',
                'Key_Components': 'Opening,Content,Q&A',
                'Common_Pitfalls': 'Text-heavy slides'
            }
        
        return best_match
    
    def _match_style(self, request: PresentationRequest, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """匹配最佳风格"""
        # 从推理规则获取风格优先级
        style_priority = pattern.get('Primary_Style', '').split('+')
        style_priority = [s.strip() for s in style_priority]
        
        # 从演示专用样式扩展中查找
        for ext_style in self.styles_presentation:
            style_name = ext_style.get('Style_Category', '')
            presentation_suitability = ext_style.get('Presentation_Suitability', '')
            
            if presentation_suitability in ['Very High', 'High']:
                for priority in style_priority:
                    if priority.lower() in style_name.lower():
                        return {
                            'name': style_name,
                            'type': ext_style.get('Layout_Category', ''),
                            'applications': ext_style.get('Slide_Applications', ''),
                            'scale': {
                                'title': ext_style.get('Slide_Title_Size', ''),
                                'body': ext_style.get('Slide_Body_Size', ''),
                                'caption': ext_style.get('Slide_Caption_Size', '')
                            },
                            'animation_recommendations': ext_style.get('Animation_Recommendations', ''),
                            'contrast_requirements': ext_style.get('Contrast_Requirements', ''),
                            'projector_safety_score': ext_style.get('Projector_Safety_Score', ''),
                            'accessibility_notes': ext_style.get('Accessibility_Notes', '')
                        }
        
        # 返回默认风格
        return {
            'name': 'Minimalism & Swiss Style',
            'type': 'General',
            'applications': 'All slide types',
            'scale': {
                'title': '44-54pt',
                'body': '24-32pt',
                'caption': '18-20pt'
            },
            'animation_recommendations': 'Fade In, Appear',
            'contrast_requirements': '7:1 minimum',
            'projector_safety_score': '9/10',
            'accessibility_notes': 'Excellent for projection'
        }
    
    def _select_colors(self, request: PresentationRequest, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """选择配色方案"""
        color_mood = pattern.get('Color_Mood', '')
        
        # 从投影安全配色中查找
        for color in self.colors_presentation:
            if color_mood.lower() in color.get('Keywords', '').lower():
                projector_primary = color.get('Projector_Primary', '')
                if projector_primary and projector_primary.strip():
                    return {
                        'name': color.get('Product_Type', 'Custom'),
                        'primary': color.get('Primary_Hex', '#003366'),
                        'secondary': color.get('Secondary_Hex', '#0066CC'),
                        'cta': color.get('CTA_Hex', '#FF6600'),
                        'background': color.get('Projector_Background', '#FFFFFF'),
                        'text': color.get('Projector_Text', '#1A1A1A'),
                        'projector_safe': color.get('Projector_Safety', 'Yes'),
                        'contrast_ratio': color.get('Contrast_Ratio', '7:1'),
                        'notes': color.get('Projector_Notes', '')
                    }
        
        # 检查行业关键词
        industry = request.industry.lower()
        for color in self.colors_presentation:
            keywords = color.get('Keywords', '').lower()
            if industry in keywords:
                return {
                    'name': color.get('Product_Type', 'Custom'),
                    'primary': color.get('Projector_Primary', '#003366'),
                    'secondary': color.get('Secondary_Hex', '#0066CC'),
                    'cta': color.get('CTA_Hex', '#FF6600'),
                    'background': color.get('Projector_Background', '#FFFFFF'),
                    'text': color.get('Projector_Text', '#1A1A1A'),
                    'projector_safe': color.get('Projector_Safety', 'Yes'),
                    'contrast_ratio': color.get('Contrast_Ratio', '7:1'),
                    'notes': color.get('Projector_Notes', '')
                }
        
        # 返回默认商务配色
        return {
            'name': 'Business Professional',
            'primary': '#003366',
            'secondary': '#0066CC',
            'cta': '#FF6600',
            'background': '#FFFFFF',
            'text': '#1A1A1A',
            'projector_safe': 'Yes',
            'contrast_ratio': '15:1',
            'notes': 'Professional and reliable for all business presentations'
        }
    
    def _select_typography(self, request: PresentationRequest, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """选择字体搭配"""
        typography_mood = pattern.get('Typography_Mood', '')
        
        # 从演示字体配置中查找
        for font in self.typography_presentation:
            mood = font.get('Mood_Style_Keywords', '')
            best_for = font.get('Best_For_Presentation', '')
            
            # 匹配基调
            tone_match = any(m in mood.lower() for m in typography_mood.lower().split())
            
            # 匹配用途
            type_match = request.presentation_type.value.replace("_", " ").lower() in best_for.lower()
            
            if tone_match or type_match:
                return {
                    'name': font.get('Font_Pairing_Name', 'Modern Professional'),
                    'heading_font': font.get('Heading_Font', 'Inter'),
                    'body_font': font.get('Body_Font', 'Inter'),
                    'title_size': font.get('Slide_Title_Size', '44-54pt'),
                    'body_size': font.get('Slide_Body_Size', '24-32pt'),
                    'caption_size': font.get('Slide_Caption_Size', '18-20pt'),
                    'google_fonts_url': font.get('Google_Fonts_URL', ''),
                    'css_import': font.get('CSS_Import', ''),
                    'mood': mood,
                    'best_for': best_for,
                    'reading_distance': font.get('Reading_Distance', '15-30ft')
                }
        
        # 返回默认字体
        return {
            'name': 'Modern Professional',
            'heading_font': 'Poppins',
            'body_font': 'Open Sans',
            'title_size': '44-54pt',
            'body_size': '24-32pt',
            'caption_size': '18-20pt',
            'google_fonts_url': 'https://fonts.google.com/share?selection.family=Open+Sans|Poppins',
            'css_import': "@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&family=Poppins:wght@600;700&display=swap');",
            'mood': 'Modern professional clean corporate',
            'best_for': 'Corporate presentations, Business meetings',
            'reading_distance': '15-30ft'
        }
    
    def _plan_structure(self, request: PresentationRequest, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """规划幻灯片结构"""
        structure_str = pattern.get('Structure_Format', '')
        
        # 解析结构
        sections = []
        parts = structure_str.split('→')
        parts = [p.strip() for p in parts if p.strip()]
        
        for part in parts:
            section_info = {
                'name': part,
                'slide_count': 2,  # 默认每部分2张幻灯片
                'layouts': self._suggest_layouts(part)
            }
            sections.append(section_info)
        
        # 确保有开头和结尾
        if not any('opening' in s['name'].lower() or 'title' in s['name'].lower() for s in sections):
            sections.insert(0, {
                'name': 'Opening',
                'slide_count': 1,
                'layouts': ['title_slide']
            })
        
        if not any('closing' in s['name'].lower() or 'thank' in s['name'].lower() for s in sections):
            sections.append({
                'name': 'Closing',
                'slide_count': 1,
                'layouts': ['thank_you_slide']
            })
        
        return {
            'pattern_name': pattern.get('Pattern_Name', 'Standard'),
            'sections': sections,
            'total_parts': len(parts),
            'tone': pattern.get('Tone', 'Professional')
        }
    
    def _suggest_layouts(self, section_name: str) -> List[str]:
        """为章节推荐版式"""
        section_lower = section_name.lower()
        
        layout_mapping = {
            'opening': ['title_slide'],
            'welcome': ['title_slide'],
            'agenda': ['agenda_slide', 'title_and_content'],
            'content': ['title_and_content', 'two_content', 'comparison'],
            'problem': ['title_and_content', 'two_content'],
            'solution': ['title_and_content', 'comparison'],
            'feature': ['title_and_content', 'two_content', 'chart'],
            'demo': ['title_and_content', 'chart'],
            'pricing': ['pricing_slide', 'comparison'],
            'testimonial': ['quote_slide', 'testimonial_slide'],
            'team': ['team_slide', 'title_and_content'],
            'timeline': ['timeline_slide'],
            'question': ['blank'],
            'q&a': ['blank'],
            'cta': ['cta_slide'],
            'closing': ['thank_you_slide', 'cta_slide'],
            'thank': ['thank_you_slide']
        }
        
        for key, layouts in layout_mapping.items():
            if key in section_lower:
                return layouts
        
        return ['title_and_content']
    
    def _select_animations(self, request: PresentationRequest, pattern: Dict[str, Any]) -> tuple:
        """选择动画配置"""
        # 获取动画强度
        intensity_str = pattern.get('Animation_Intensity', 'Low')
        intensity_map = {
            'None': AnimationIntensity.NONE,
            'Low': AnimationIntensity.LOW,
            'Medium': AnimationIntensity.MEDIUM,
            'High': AnimationIntensity.HIGH
        }
        animation_intensity = intensity_map.get(intensity_str, AnimationIntensity.LOW)
        
        # 获取过渡风格
        transition_str = pattern.get('Transition_Style', 'Fade or Push')
        if 'fade' in transition_str.lower():
            transition_style = TransitionStyle.FADE
        elif 'slide' in transition_str.lower():
            transition_style = TransitionStyle.SLIDE
        elif 'push' in transition_str.lower():
            transition_style = TransitionStyle.PUSH
        elif 'zoom' in transition_str.lower():
            transition_style = TransitionStyle.ZOOM
        else:
            transition_style = TransitionStyle.FADE
        
        # 获取推荐的动画
        recommended_animations = []
        for anim in self.animations:
            applicability = anim.get('Applicability_Score', '')
            if animation_intensity in [AnimationIntensity.LOW, AnimationIntensity.MEDIUM]:
                if 'Very High' in applicability or 'High' in applicability:
                    recommended_animations.append({
                        'name': anim.get('Animation_Name', ''),
                        'category': anim.get('Animation_Category', ''),
                        'effect_type': anim.get('Effect_Type', ''),
                        'duration': anim.get('Duration_Seconds_Duration', ''),
                        'best_for': anim.get('Best_For', ''),
                        'avoid_for': anim.get('Avoid_For', '')
                    })
            elif animation_intensity == AnimationIntensity.HIGH:
                if 'High' in applicability or 'Medium' in applicability:
                    recommended_animations.append({
                        'name': anim.get('Animation_Name', ''),
                        'category': anim.get('Animation_Category', ''),
                        'effect_type': anim.get('Effect_Type', ''),
                        'duration': anim.get('Duration_Seconds_Duration', ''),
                        'best_for': anim.get('Best_For', ''),
                        'avoid_for': anim.get('Avoid_For', '')
                    })
        
        # 限制推荐数量
        recommended_animations = recommended_animations[:10]
        
        return animation_intensity, transition_style, recommended_animations
    
    def _adapt_for_audience(self, audience: AudienceType, presentation_type: PresentationType) -> Dict[str, Any]:
        """为特定受众生成适配建议"""
        audience_key = audience.value.replace("_", " ")
        
        for guideline in self.audience_guidelines:
            audience_name = guideline.get('Audience_Name', '').lower()
            if audience_name in audience_key or audience_key in audience_name:
                return {
                    'audience_name': guideline.get('Audience_Name', ''),
                    'characteristics': guideline.get('Key_Characteristics', ''),
                    'attention_span': guideline.get('Attention_Span', ''),
                    'information_preference': guideline.get('Information_Preference', ''),
                    'decision_style': guideline.get('Decision_Making_Style', ''),
                    'motivation_factors': guideline.get('Motivation_Factors', ''),
                    'visual_preference': guideline.get('Visual_Preference', ''),
                    'data_tolerance': guideline.get('Data_Tolerance', ''),
                    'engagement_strategies': guideline.get('Engagement_Strategies', ''),
                    'talking_speed': guideline.get('Talking_Speed', ''),
                    'slide_density': guideline.get('Slide_Density', ''),
                    'content_ratio': guideline.get('Content_Ratio', '')
                }
        
        # 默认受众适配
        return {
            'audience_name': 'General',
            'characteristics': 'Mixed background and expertise',
            'attention_span': 'Medium (10-15 min per topic)',
            'information_preference': 'Clear and actionable',
            'decision_style': 'Varied',
            'motivation_factors': 'Professional growth',
            'visual_preference': 'Clean and professional',
            'data_tolerance': 'Medium',
            'engagement_strategies': 'Interactive elements',
            'talking_speed': 'Medium',
            'slide_density': 'Medium',
            'content_ratio': '50% storytelling; 50% information'
        }
    
    def _adjust_tone(self, base_tone: Tone, presentation_type: PresentationType, pattern: Dict[str, Any]) -> str:
        """调整基调以适应演示类型"""
        pattern_tone = pattern.get('Tone', '').lower()
        base_tone_str = base_tone.value.lower()
        
        # 基调调整映射
        tone_adjustments = {
            'professional': {
                'board_presentation': 'Authoritative + Clear',
                'quarterly_review': 'Analytical + Supportive',
                'all_hands': 'Professional + Inclusive',
                'investor_pitch': 'Confident + Persuasive'
            },
            'educational': {
                'training_workshop': 'Engaging + Supportive',
                'technical_workshop': 'Technical + Clear',
                'webinar': 'Educational + Professional'
            },
            'inspiring': {
                'conference_talk': 'Inspirational + Engaging',
                'all_hands': 'Motivational + United',
                'kickoff': 'Energetic + Visionary'
            }
        }
        
        # 查找调整
        for tone_key, adjustments in tone_adjustments.items():
            if tone_key in base_tone_str:
                for type_key, adjustment in adjustments.items():
                    if type_key in presentation_type.value.lower():
                        return adjustment
        
        # 返回默认
        if 'professional' in pattern_tone:
            return 'Professional + Clear'
        elif 'engaging' in pattern_tone:
            return 'Engaging + Educational'
        elif 'persuasive' in pattern_tone:
            return 'Persuasive + Confident'
        
        return f"{base_tone.value.title()} + Professional"
    
    def _estimate_slides(self, request: PresentationRequest, pattern: Dict[str, Any]) -> int:
        """估算幻灯片数量"""
        # 从模式获取范围
        try:
            min_slides = int(pattern.get('Slide_Count_Min', '10'))
            max_slides = int(pattern.get('Slide_Count_Max', '20'))
        except (ValueError, TypeError):
            min_slides, max_slides = 10, 20
        
        # 基于时长调整
        duration = request.duration_minutes
        
        # 理想节奏：每分钟 0.5-0.8 张幻灯片
        ideal_slides = int(duration * 0.65)
        
        # 限制在范围内
        ideal_slides = max(min_slides, min(ideal_slides, max_slides))
        
        # 根据类型调整
        if request.presentation_type == PresentationType.INVESTOR_PITCH:
            # 投资路演通常更简洁
            ideal_slides = min(ideal_slides, 15)
        elif request.presentation_type == PresentationType.TRAINING_WORKSHOP:
            # 培训可以更详细
            ideal_slides = max(ideal_slides, 25)
        
        return ideal_slides
    
    def _generate_recommendations(self, request: PresentationRequest, pattern: Dict[str, Any], 
                                   audience_adaptation: Dict[str, Any]) -> List[str]:
        """生成演示建议"""
        recommendations = []
        pattern_name = pattern.get('Pattern_Name', '')
        
        # 基于类型的建议
        if request.presentation_type == PresentationType.INVESTOR_PITCH:
            recommendations.extend([
                'Keep slides under 15 for 10-minute pitch',
                'Focus on problem, solution, market size, and ask',
                'Include at least one compelling data visualization',
                'Practice the timing for each section'
            ])
        elif request.presentation_type == PresentationType.PRODUCT_LAUNCH:
            recommendations.extend([
                'Create excitement with strong opening',
                'Show, do not tell - use demos or visuals',
                'End with clear call to action',
                'Prepare for questions about competitors'
            ])
        
        # 基于受众的建议
        audience_name = audience_adaptation.get('audience_name', '')
        if 'Executive' in audience_name:
            recommendations.extend([
                'Lead with key takeaways, not details',
                'Focus on ROI and business impact',
                'Keep slides clean and scannable',
                'Prepare executive summary backup'
            ])
        elif 'Technical' in audience_name:
            recommendations.extend([
                'Include technical depth where appropriate',
                'Use architecture diagrams if relevant',
                'Be prepared for challenging questions',
                'Balance overview with details'
            ])
        
        # 基于基调的建议
        if request.tone == Tone.INSPIRING:
            recommendations.append('Include personal stories or anecdotes')
        elif request.tone == Tone.URGENT:
            recommendations.append('Keep pacing fast and focused')
        
        return recommendations
    
    def _identify_anti_patterns(self, request: PresentationRequest, pattern: Dict[str, Any]) -> List[str]:
        """识别应避免的模式"""
        anti_patterns = []
        common_anti_patterns = pattern.get('Common_Pitfalls', '')
        
        if common_anti_patterns:
            anti_patterns.extend([p.strip() for p in common_anti_patterns.split('+')])
        
        # 通用反模式
        general_anti_patterns = [
            'More than 7 bullets per slide',
            'Full sentences on slides',
            'Unreadable color combinations',
            'No backup slides for Q&A',
            'Small fonts (less than 24pt)'
        ]
        anti_patterns.extend(general_anti_patterns)
        
        return list(set(anti_patterns))
    
    def generate_slide_plan(self, reasoning: PresentationReasoning, request: PresentationRequest) -> List[SlidePlan]:
        """
        生成详细的幻灯片规划
        
        Args:
            reasoning: 推理结果
            request: 原始请求
            
        Returns:
            List[SlidePlan]: 幻灯片规划列表
        """
        slide_plans = []
        slide_id = 1
        
        # 生成开场幻灯片
        slide_plans.append(SlidePlan(
            slide_type='title',
            title=request.title,
            layout='title_slide',
            content_bullets=[],
            notes_template=self._get_notes_template('Title Slide', reasoning.pattern.get('Pattern_Category', '')),
            estimated_time_seconds=60
        ))
        slide_id += 1
        
        # 生成内容幻灯片
        sections = reasoning.structure.get('sections', [])
        for section in sections:
            section_name = section.get('name', '')
            slide_count = section.get('slide_count', 2)
            
            for i in range(slide_count):
                slide_plan = SlidePlan(
                    slide_type='content',
                    title=f"{section_name} - Part {i + 1}",
                    layout=section.get('layouts', ['title_and_content'])[0],
                    content_bullets=self._generate_content_bullets(section_name, i),
                    notes_template=self._get_notes_template('Content Slide', section_name),
                    estimated_time_seconds=reasoning.time_per_slide_estimate,
                    animation=self._get_animation_config(reasoning.animation_intensity, section_name)
                )
                slide_plans.append(slide_plan)
                slide_id += 1
        
        # 生成结束幻灯片
        slide_plans.append(SlidePlan(
            slide_type='closing',
            title='Thank You',
            layout='thank_you_slide',
            content_bullets=['Questions?', f'Contact: {request.constraints.get("email", "your@email.com")}'],
            notes_template=self._get_notes_template('Thank You Slide', ''),
            estimated_time_seconds=60
        ))
        
        return slide_plans
    
    def _generate_content_bullets(self, section_name: str, index: int) -> List[str]:
        """生成内容要点"""
        section_lower = section_name.lower()
        
        bullet_templates = {
            'problem': ['Identify the core challenge', 'Quantify the impact', 'Explain why it matters now'],
            'solution': ['Present the approach', 'Highlight key benefits', 'Show differentiation'],
            'feature': ['Core capability', 'User benefit', 'Example use case'],
            'demo': ['Walk through the flow', 'Highlight key moments', 'Show the result'],
            'pricing': ['Tier overview', 'Key inclusions', 'Call to action'],
            'team': ['Key team members', 'Relevant experience', 'Contact information'],
            'timeline': ['Major milestones', 'Key dates', 'Dependencies'],
            'agenda': ['Main topic 1', 'Main topic 2', 'Main topic 3'],
            'default': [f'Key point {i + 1}' for i in range(3)]
        }
        
        for key, bullets in bullet_templates.items():
            if key in section_lower:
                return bullets
        
        return bullet_templates['default']
    
    def _get_notes_template(self, slide_type: str, context: str) -> str:
        """获取演讲备注模板"""
        for note in self.speech_notes:
            note_type = (note.get('Slide_Type') or '').lower().replace(' ', '_')
            if slide_type.lower().replace(' ', '_') in note_type:
                return note.get('Note_Template', '') or ''
        return ""
    
    def _get_animation_config(self, intensity: AnimationIntensity, section_name: str) -> Dict[str, Any]:
        """获取动画配置"""
        if intensity == AnimationIntensity.NONE:
            return {'entrance': 'none', 'emphasis': 'none'}
        
        # 根据章节类型选择动画
        if 'opening' in section_name.lower() or 'closing' in section_name.lower():
            return {'entrance': 'fade_in', 'emphasis': 'none'}
        elif 'feature' in section_name.lower() or 'demo' in section_name.lower():
            return {'entrance': 'slide_in', 'emphasis': 'pulse'}
        else:
            return {'entrance': 'fade_in', 'emphasis': 'appear'}
    
    def get_available_presentation_types(self) -> List[Dict[str, str]]:
        """获取所有可用的演示类型"""
        return [
            {'value': pt.value, 'name': pt.name.replace('_', ' ').title()}
            for pt in PresentationType
        ]
    
    def get_available_audiences(self) -> List[Dict[str, str]]:
        """获取所有可用的受众类型"""
        return [
            {'value': aud.value, 'name': aud.name.replace('_', ' ').title()}
            for aud in AudienceType
        ]
    
    def get_available_tones(self) -> List[Dict[str, str]]:
        """获取所有可用的基调"""
        return [
            {'value': t.value, 'name': t.value.replace('_', ' ').title()}
            for t in Tone
        ]


# CLI 支持
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Presentation Reasoning Engine")
    parser.add_argument("query", help="Presentation query or type")
    parser.add_argument("--duration", type=int, default=20, help="Duration in minutes")
    parser.add_argument("--audience", default="general", help="Target audience")
    parser.add_argument("--tone", default="professional", help="Presentation tone")
    
    args = parser.parse_args()
    
    # 创建演示请求
    request = PresentationRequest(
        title=args.query,
        presentation_type=PresentationType(args.query.replace(" ", "_").lower() if " " in args.query else "business_presentation"),
        audience=AudienceType(args.audience.replace(" ", "_").lower()),
        duration_minutes=args.duration,
        tone=Tone(args.tone)
    )
    
    # 分析
    engine = PresentationReasoningEngine()
    reasoning = engine.analyze(request)
    
    # 输出结果
    import json
    print(json.dumps({
        'pattern': reasoning.pattern.get('Pattern_Name', ''),
        'style': reasoning.style.get('name', ''),
        'colors': reasoning.colors.get('name', ''),
        'typography': reasoning.typography.get('name', ''),
        'slide_count': reasoning.slide_count_estimate,
        'time_per_slide': reasoning.time_per_slide_estimate,
        'recommendations': reasoning.recommendations[:5]
    }, indent=2, ensure_ascii=False))
