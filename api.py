#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from typing import Generator
import logging

# 添加一个 logger
logger = logging.getLogger(__name__)

class XAIClient:
    """X.AI API 客户端"""
    
    def __init__(self, auth_token: str, api_base: str = "https://api.x.ai/v1", model: str = "grok-2-1212"):
        """初始化 X.AI API 客户端
        
        Args:
            auth_token: API 认证令牌
            api_base: API 基础 URL
            model: 使用的模型名称
        """
        self.auth_token = auth_token
        self.api_base = api_base.rstrip('/')
        self.model = model
    
    def ask_stream(self, prompt: str) -> Generator[str, None, None]:
        """向 X.AI API 发送问题并获取流式回答
        
        Args:
            prompt: 问题文本
            
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
        
        # 添加调试日志
        logger.info(f"Making request to {self.api_base}/chat/completions")
        logger.info(f"Headers: {headers}")
        logger.info(f"Data: {data}")
        
        response = requests.post(
            f"{self.api_base}/chat/completions",
            headers=headers,
            json=data,
            stream=True
        )
        
        if response.status_code != 200:
            yield f"API 请求失败：{response.status_code} - {response.text}"
            return
            
        for line in response.iter_lines():
            if line:
                try:
                    # 移除 "data: " 前缀并解析 JSON
                    line_text = line.decode('utf-8')
                    if line_text.startswith('data: '):
                        json_str = line_text[6:]  # 跳过 "data: "
                        if json_str == '[DONE]':
                            break
                            
                        chunk = json.loads(json_str)
                        if chunk.get('choices') and len(chunk['choices']) > 0:
                            delta = chunk['choices'][0].get('delta', {})
                            if 'content' in delta:
                                yield delta['content']
                                
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    yield f"\n解析错误：{str(e)}"