#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys
from typing import Generator

import requests

# 添加一个 logger
logger = logging.getLogger(__name__)

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入 i18n 模块
from i18n import get_translation

# 本页面的 i18n 字典，页面仅显示英文中文，之后会在 i18n.py 中集中校验

# 'en': {
#    'token_format_warning_xai': "Token format warning: token should start with 'xai-', current token: {}",
#     'token_format_warning_gemini': "Gemini token format warning: token should start with 'AI' and end with '-HA'",
#     'request_error': "Request error: {}",
#     'stream_request_error': "Stream request error: {}",
#     'gemini_request_error': "Gemini request error: {}",
#     'gemini_stream_error': "Gemini stream request error: {}",
#     'unsupported_ai_type': "Unsupported AI type: {}",
#     'system_prompt': "You are Grok, an expert in book analysis. Your task is to help users understand books better by providing insightful questions and analysis. Focus on the substance of the books, not just their titles."
# },
# 'zh': {
#     'token_format_warning_xai': "Token 格式警告：Token 应以 'xai-' 开头，当前 Token: {}",
#     'token_format_warning_gemini': "Gemini Token 格式警告：Token 应以 'AI' 开头并以 '-HA' 结尾",
#     'request_error': "请求出错: {}",
#     'stream_request_error': "流式请求出错: {}",
#     'gemini_request_error': "Gemini 请求出错: {}",
#     'gemini_stream_error': "Gemini 流式请求出错: {}",
#     'unsupported_ai_type': "不支持的 AI 类型: {}",
#     'system_prompt': "你是 Grok，一个书籍分析专家。你的任务是通过提供有见地的问题和分析来帮助用户更好地理解书籍。专注于书籍的实质内容，而不仅仅是标题。"
# }
    
class BaseClient:
    """AI 客户端的基类"""
    
    def _normalize_token(self, token: str) -> str:
        """规范化 Token，移除多余的空格和 BOM 标记
        
        Args:
            token: 原始 Token 字符串
            
        Returns:
            str: 规范化后的 Token
        """
        if not token:
            return ""
            
        # 移除所有空白字符
        token = ''.join(token.split())
        # 移除 BOM 标记
        token = token.encode('utf-8').decode('utf-8-sig')
        # 移除 Bearer 前缀（如果存在）
        if token.startswith('Bearer'):
            token = token[6:].strip()
            
        return token
    
    def ask(self, prompt: str, lang_code: str = 'en') -> str:
        """发送请求并获取响应（同步）"""
        raise NotImplementedError("子类必须实现此方法")
    
    def ask_stream(self, prompt: str, lang_code: str = 'en') -> Generator[str, None, None]:
        """发送流式请求并获取响应"""
        raise NotImplementedError("子类必须实现此方法")


class XAIClient(BaseClient):
    """X.AI API 客户端"""
    
    def __init__(self, auth_token: str, model: str = "grok-3-latest", api_base: str = "https://api.x.ai/v1/chat/completions"):
        """初始化 X.AI API 客户端
        
        Args:
            auth_token: X.AI 认证 Token
            model: 使用的模型，默认为 grok-3-latest
            api_base: API 基础 URL
        """
        self.auth_token = auth_token
        self.model = model
        self.api_base = api_base
    
    def _validate_xai_token(self, token: str) -> str:
        """验证 X.AI Token 格式"""
        if not token.startswith('xai-'):
            logger.warning(f"Token 格式警告：Token 应以 'xai-' 开头，当前 Token: {token}")
        return f"Bearer {token}"
    
    def _get_auth_headers(self) -> dict:
        """获取认证头"""
        normalized = self._normalize_token(self.auth_token)
        validated = self._validate_xai_token(normalized)
        return {
            "Content-Type": "application/json",
            "Authorization": validated
        }
    
    def _prepare_request(self, prompt: str) -> tuple:
        """准备 API 请求"""
        headers = self._get_auth_headers()
        data = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are Grok, an expert in book analysis. Your task is to help users understand books better by providing insightful questions and analysis. Focus on the substance of the books, not just their titles."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": self.model,
            "temperature": 0
        }
        return headers, data
    
    def ask(self, prompt: str, lang_code: str = 'en') -> str:
        """发送请求并获取响应（同步）"""
        try:
            headers, data = self._prepare_request(prompt)
            response = requests.post(
                self.api_base,
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"请求出错: {str(e)}")
            raise
    
    def ask_stream(self, prompt: str, lang_code: str = 'en') -> Generator[str, None, None]:
        """发送流式请求并获取响应"""
        try:
            headers, data = self._prepare_request(prompt)
            data["stream"] = True
            with requests.post(
                self.api_base,
                headers=headers,
                json=data,
                stream=True,
                timeout=30
            ) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        yield line.decode('utf-8')
        except Exception as e:
            logger.error(f"流式请求出错: {str(e)}")
            raise


class GeminiClient(BaseClient):
    """Gemini API 客户端"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash", api_base: str = "https://generativelanguage.googleapis.com/v1beta"):
        """初始化 Gemini API 客户端
        
        Args:
            api_key: Gemini API 密钥
            model: 使用的模型，默认为 gemini-2.0-flash
            api_base: API 基础 URL
        """
        self.api_key = api_key
        self.model = model
        self.api_base = api_base
    
    def _validate_gemini_token(self, token: str) -> str:
        """验证 Gemini Token 格式"""
        if not (token.startswith('AI') and token.endswith('-HA')):
            logger.warning("Gemini Token 格式警告：Token 应以 'AI' 开头并以 '-HA' 结尾")
        return token
    
    def _prepare_request(self, prompt: str) -> tuple:
        """准备 API 请求"""
        normalized_token = self._normalize_token(self.api_key)
        validated_token = self._validate_gemini_token(normalized_token)
        
        url = f"{self.api_base}/models/{self.model}:generateContent?key={validated_token}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        return url, headers, data
    
    def ask(self, prompt: str, lang_code: str = 'en') -> str:
        """发送请求并获取响应（同步）"""
        try:
            url, headers, data = self._prepare_request(prompt)
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            if 'candidates' in result and result['candidates']:
                return result['candidates'][0]['content']['parts'][0]['text']
            return ""
        except Exception as e:
            logger.error(f"Gemini 请求出错: {str(e)}")
            raise
    
    def ask_stream(self, prompt: str, lang_code: str = 'en') -> Generator[str, None, None]:
        """发送流式请求并获取响应"""
        try:
            url, headers, data = self._prepare_request(prompt)
            with requests.post(
                url,
                headers=headers,
                json=data,
                stream=True,
                timeout=30
            ) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        yield line.decode('utf-8')
        except Exception as e:
            logger.error(f"Gemini 流式请求出错: {str(e)}")
            raise


def create_client(ai_type: str, **kwargs) -> BaseClient:
    """创建 AI 客户端工厂函数
    
    Args:
        ai_type: AI 类型，支持 'xai' 或 'gemini'
        **kwargs: 传递给客户端的参数
        
    Returns:
        BaseClient: 对应的客户端实例
        
    Raises:
        ValueError: 如果 ai_type 不支持
    """
    if ai_type == 'xai':
        return XAIClient(**kwargs)
    elif ai_type == 'gemini':
        return GeminiClient(**kwargs)
    else:
        raise ValueError(f"不支持的 AI 类型: {ai_type}")