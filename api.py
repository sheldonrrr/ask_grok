#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import os
import sys
from typing import Generator
import logging

# 添加一个 logger
logger = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from i18n import get_translation

class APIClient:
    """X.AI API 客户端"""
    
    def _prepare_request(self, prompt: str) -> tuple:
        """准备 API 请求的共同部分
        
        Args:
            prompt: 问题文本
            
        Returns:
            tuple: (headers, data) 请求头和请求数据
        """
        # 处理 token
        token = self.auth_token
        token = ''.join(token.split())  # 移除所有空白字符
        token = token.encode('utf-8').decode('utf-8-sig')  # 移除可能的 BOM
        
        # 处理 Bearer 前缀
        if token.startswith('Bearer'):
            token = token[6:]
            
        # 确保 token 以 xai- 开头
        if not token.startswith('xai-'):
            logger.warning(f"Token format warning: token should start with 'xai-', current token: {token}")
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
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
        """向 X.AI API 发送问题并获取回答（非流式）
        
        Args:
            prompt: 问题文本
            lang_code: 语言代码，用于获取相应的翻译文本
            
        Returns:
            str: API 返回的完整回答
            
        Note:
            这个方法不使用流式请求，更适合处理长文本和需要完整响应的场景
        """
        # 确保 token 格式正确：
        # 1. 移除所有空白字符（包括空格、tab、换行符等）
        # 2. 移除 BOM 标记
        # 3. 处理 Bearer 前缀，确保格式正确
        # 记录原始 token
        logger.debug(f"Original token: {self.auth_token}")
        
        token = self.auth_token
        token = ''.join(token.split())  # 移除所有空白字符
        logger.debug(f"After removing whitespace: {token}")
        
        token = token.encode('utf-8').decode('utf-8-sig')  # 移除可能的 BOM
        logger.debug(f"After removing BOM: {token}")
        
        # 处理 Bearer 前缀
        if token.startswith('Bearer'):
            token = token[6:]  # 移除 'Bearer'
            logger.debug(f"After removing Bearer prefix: {token}")
        
        # 准备请求
        headers, data = self._prepare_request(prompt)
        data["stream"] = False  # 非流式请求
        logger.info(f"Request headers: {headers}")
        logger.info(f"Request data: {data}")
        
        try:
            # 添加超时设置
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data,
                timeout=60  # 增加到60秒
            )
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response content: {response.text}")
            
            # 处理常见错误
            if response.status_code == 400:
                error_data = response.json()
                error_message = error_data.get('error', {}).get('message', 'Bad request')
                logger.error(f"API bad request: {error_message}")
                translation = get_translation(lang_code)
                raise Exception(f"{translation.get('error_prefix', 'Error:')} {error_message}")
            
            response.raise_for_status()
            
            result = response.json()
            if result.get("choices") and result["choices"][0].get("message", {}).get("content"):
                return result["choices"][0]["message"]["content"]
            else:
                logger.error(f"Unexpected API response format: {result}")
                translation = get_translation(lang_code)
                error_message = f"{translation.get('error_prefix', 'Error:')} {translation.get('request_failed', 'API request failed')}: Unexpected response format"
                raise Exception(error_message)
                                
        except requests.exceptions.RequestException as e:
            translation = get_translation(lang_code)
            error_message = f"{translation.get('error_prefix', 'Error:')} {translation.get('request_failed', 'API request failed')}: {str(e)}"
            logger.error(error_message)
            raise Exception(error_message)
    
    def ask_stream(self, prompt: str, lang_code: str = 'en') -> str:
        """向 X.AI API 发送问题并获取回答（流式请求，适用于短文本）
        
        Args:
            prompt: 问题文本
            lang_code: 语言代码，用于获取相应的翻译文本
            
        Returns:
            str: API 返回的完整回答
        
        Note:
            这个方法不使用流式请求，更适合处理短文本和快速响应的场景
        """
        
        # 确保 token 格式正确：
        # 1. 移除所有空白字符（包括空格、tab、换行符等）
        # 2. 移除 BOM 标记
        # 3. 处理 Bearer 前缀，确保格式正确
        # 记录原始 token
        logger.debug(f"Original token: {self.auth_token}")
        
        token = self.auth_token
        token = ''.join(token.split())  # 移除所有空白字符
        token = token.encode('utf-8').decode('utf-8-sig')  # 移除可能的 BOM
        
        # 处理 Bearer 前缀
        if token.startswith('Bearer'):
            token = token[6:]
            token = token.strip()
        token = 'Bearer ' + token
        
        # 准备请求
        headers, data = self._prepare_request(prompt)
        data["stream"] = False  # 非流式请求
        headers['Authorization'] = token  # 使用处理后的 token
        
        try:
            # 添加超时设置
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data,
                timeout=60  # 增加到60秒
            )
            
            # 处理常见错误
            if response.status_code == 400:
                error_data = response.json()
                error_message = error_data.get('error', {}).get('message', 'Bad request')
                logger.error(f"API bad request: {error_message}")
                translation = get_translation(lang_code)
                raise Exception(f"{translation.get('error_prefix', 'Error:')} {error_message}")
            
            response.raise_for_status()
            
            result = response.json()
            if result.get("choices") and result["choices"][0].get("message", {}).get("content"):
                return result["choices"][0]["message"]["content"]
            else:
                logger.error(f"Unexpected API response format: {result}")
                translation = get_translation(lang_code)
                error_message = f"{translation.get('error_prefix', 'Error:')} {translation.get('request_failed', 'API request failed')}: Unexpected response format"
                raise Exception(error_message)
                                
        except requests.exceptions.RequestException as e:
            translation = get_translation(lang_code)
            error_message = f"{translation.get('error_prefix', 'Error:')} {translation.get('request_failed', 'API request failed')}: {str(e)}"
            logger.error(error_message)
            raise Exception(error_message)
    
    def __init__(self, auth_token: str, api_base: str = "https://api.x.ai/v1", model: str = "grok-3-latest"):
        """初始化 X.AI API 客户端
        
        Args:
            auth_token: API 认证令牌
            api_base: API 基础 URL
            model: 使用的模型名称
        """
        self.auth_token = auth_token
        self.api_base = api_base.rstrip('/')
        self.model = model