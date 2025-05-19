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
    
    def ask_stream(self, prompt: str, lang_code: str = 'en') -> Generator[str, None, None]:
        """向 X.AI API 发送问题并获取流式回答
        
        Args:
            prompt: 问题文本
            lang_code: 语言代码，用于获取相应的翻译文本
            
        Yields:
            str: API 返回的每个文本片段
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}" if not self.auth_token.startswith('Bearer ') else self.auth_token
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
            "stream": True
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data,
                stream=True
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    if line.strip() == b"data: [DONE]":
                        break
                    if line.startswith(b"data: "):
                        try:
                            chunk = json.loads(line[6:])
                            if chunk.get("choices") and chunk["choices"][0].get("delta", {}).get("content"):
                                yield chunk["choices"][0]["delta"]["content"]
                        except json.JSONDecodeError:
                            logger.error(f"Failed to decode JSON: {line[6:]}")
                            continue
                                
        except requests.exceptions.RequestException as e:
            translation = get_translation(lang_code)
            error_message = f"{translation.get('error_prefix', 'Error:')} {translation.get('request_failed', 'API request failed')}: {str(e)}"
            logger.error(error_message)
            raise Exception(error_message)