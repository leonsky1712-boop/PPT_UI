# -*- coding: utf-8 -*-
"""
JWT 认证模块
"""

import os
from datetime import datetime, timedelta
from functools import wraps
import jwt
import bcrypt
from flask import request, jsonify

# 从环境变量读取，无则禁用认证
JWT_SECRET = os.environ.get('JWT_SECRET_KEY') or os.environ.get('JWT_SECRET')
JWT_ALGORITHM = 'HS256'
ACCESS_EXPIRE_MINUTES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', 1440))


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


def create_access_token(user_id: int, email: str) -> str:
    if not JWT_SECRET:
        return ''
    payload = {
        'sub': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES),
        'iat': datetime.utcnow(),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str):
    if not JWT_SECRET or not token:
        return None
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except Exception:
        return None


def get_token_from_request():
    auth = request.headers.get('Authorization')
    if auth and auth.startswith('Bearer '):
        return auth[7:]
    return request.args.get('token')


def login_required(f):
    """需要登录的接口装饰器（可选：若未配置 JWT_SECRET 则跳过校验）"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not JWT_SECRET:
            return f(*args, **kwargs)
        token = get_token_from_request()
        payload = decode_token(token)
        if not payload:
            return jsonify({'error': '未授权或 token 无效'}), 401
        request.current_user_id = payload.get('sub')
        request.current_user_email = payload.get('email')
        return f(*args, **kwargs)
    return wrapped


def optional_login(f):
    """可选登录：有 token 则解析并注入用户，无则继续"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        request.current_user_id = None
        request.current_user_email = None
        if JWT_SECRET:
            token = get_token_from_request()
            payload = decode_token(token)
            if payload:
                request.current_user_id = payload.get('sub')
                request.current_user_email = payload.get('email')
        return f(*args, **kwargs)
    return wrapped
