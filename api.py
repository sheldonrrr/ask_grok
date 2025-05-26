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
    
    def ask_stream(self, prompt: str, lang_code: str = 'en') -> str:
        """向 X.AI API 发送问题并获取回答
        
        Args:
            prompt: 问题文本
            lang_code: 语言代码，用于获取相应的翻译文本
            
        Returns:
            str: API 返回的完整回答
        """
        # 确保 token 格式正确：移除可能存在的 Bearer 前缀和多余空格，然后重新添加
        token = self.auth_token.replace('Bearer', '').strip()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        data = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": self.model,
            "stream": False,
            "temperature": 0
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data
            )
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