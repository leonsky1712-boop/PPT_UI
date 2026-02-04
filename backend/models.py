# -*- coding: utf-8 -*-
"""
数据模型 - SQLAlchemy ORM
支持 SQLite / PostgreSQL
"""

import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model):
    """用户表"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), default='')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    presentations = relationship('Presentation', backref='user', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class Presentation(db.Model):
    """演示文稿记录表"""
    __tablename__ = 'presentations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True, index=True)
    title = Column(String(500), nullable=False)
    template_id = Column(String(100), default='modern-elegant')
    presentation_type = Column(String(100), default='business_presentation')
    audience = Column(String(100), default='general_employees')
    duration = Column(Integer, default=15)
    tone = Column(String(50), default='professional')
    industry = Column(String(200), default='')
    output_filename = Column(String(255), default='')
    slide_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'template_id': self.template_id,
            'presentation_type': self.presentation_type,
            'audience': self.audience,
            'duration': self.duration,
            'tone': self.tone,
            'industry': self.industry,
            'output_filename': self.output_filename,
            'slide_count': self.slide_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


def init_db(app):
    """初始化数据库并创建表"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
