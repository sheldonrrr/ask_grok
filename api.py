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

from calibre_plugins.ask_grok.i18n import get_translation

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
        # 记录请求开始
        logger.info(f"=== 开始处理 API 请求 ===")
        logger.info(f"请求语言代码: {lang_code}")
        logger.info(f"原始提示词: {prompt[:500]}{'...' if len(prompt) > 500 else ''}")
        
        # 确保 token 格式正确：
        # 1. 移除所有空白字符（包括空格、tab、换行符等）
        # 2. 移除 BOM 标记
        # 3. 处理 Bearer 前缀，确保格式正确
        # 记录原始 token
        logger.debug(f"原始 Token: {self.auth_token}")
        
        token = self.auth_token
        token = ''.join(token.split())  # 移除所有空白字符
        logger.debug(f"移除空白字符后: {token}")
        
        token = token.encode('utf-8').decode('utf-8-sig')  # 移除可能的 BOM
        logger.debug(f"移除 BOM 后: {token}")
        
        # 处理 Bearer 前缀
        if token.startswith('Bearer'):
            token = token[6:]  # 移除 'Bearer'
            logger.debug(f"移除 Bearer 前缀后: {token}")
        
        # 准备请求
        logger.info("准备请求头和请求数据...")
        headers, data = self._prepare_request(prompt)
        data["stream"] = False  # 非流式请求
        
        # 记录请求详情（敏感信息已脱敏）
        safe_headers = headers.copy()
        if 'Authorization' in safe_headers:
            auth = safe_headers['Authorization']
            if len(auth) > 20:  # 只显示前10个和后5个字符
                safe_headers['Authorization'] = f"{auth[:10]}...{auth[-5:]}"
        
        logger.info(f"请求头: {safe_headers}")
        logger.info(f"请求数据 (前500字符): {str(data)[:500]}{'...' if len(str(data)) > 500 else ''}")
        logger.info(f"请求数据大小: {len(str(data))} 字节")
        
        # 记录完整的系统提示词
        if 'messages' in data and len(data['messages']) > 0:
            for i, msg in enumerate(data['messages']):
                if msg.get('role') == 'system':
                    logger.info(f"系统提示词: {msg.get('content', '')[:500]}{'...' if len(msg.get('content', '')) > 500 else ''}")
                elif msg.get('role') == 'user':
                    logger.info(f"用户提示词: {msg.get('content', '')[:500]}{'...' if len(msg.get('content', '')) > 500 else ''}")
        
        # 发送请求
        try:
            logger.info("正在发送请求到 API...")
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            logger.info(f"收到 API 响应，状态码: {response.status_code}")
            
            # 检查响应状态
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            
            # 记录完整的响应（敏感信息已脱敏）
            logger.debug(f"完整 API 响应: {result}")
            
            # 提取回答
            if 'choices' in result and len(result['choices']) > 0:
                answer = result['choices'][0].get('message', {}).get('content', '')
                logger.info(f"成功获取到回答，长度: {len(answer)} 字符")
                logger.debug(f"回答内容 (前500字符): {answer[:500]}{'...' if len(answer) > 500 else ''}")
                return answer
            else:
                logger.error(f"API 响应中未找到有效的回答: {result}")
                raise ValueError("API 响应中未找到有效的回答")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"请求 API 时发生错误: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    logger.error(f"API 错误详情: {error_detail}")
                except:
                    logger.error(f"API 错误响应内容: {e.response.text[:1000]}")
            raise
            
        except Exception as e:
            logger.error(f"处理 API 响应时发生错误: {str(e)}", exc_info=True)
            raise
            
        finally:
            logger.info("=== API 请求处理完成 ===\n")
        
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
    
    def __init__(self, api_base: str = "https://api.x.ai/v1", model: str = "grok-3-latest"):
        """初始化 X.AI API 客户端
        
        Args:
            api_base: API 基础 URL
            model: 使用的模型名称
        """
        self._api_base = api_base.rstrip('/')
        self._model = model
        # 存储默认值
        self._default_prefs = {
            'api_base_url': api_base,
            'model': model,
            'auth_token': ''
        }
    
    @property
    def api_base(self):
        """动态获取最新的 API 基础 URL"""
        prefs = self._get_latest_prefs()
        return prefs.get('api_base_url', self._default_prefs['api_base_url']).rstrip('/')
    
    @property
    def model(self):
        """动态获取最新的模型名称"""
        prefs = self._get_latest_prefs()
        return prefs.get('model', self._default_prefs['model'])
    
    @property
    def auth_token(self):
        """动态获取最新的 auth_token"""
        prefs = self._get_latest_prefs()
        return prefs.get('auth_token', self._default_prefs['auth_token'])
    
    def _get_latest_prefs(self):
        """直接从配置文件读取最新的配置"""
        from calibre.utils.config import JSONConfig
        try:
            # 直接创建一个新的 JSONConfig 实例，确保获取最新的配置
            prefs = JSONConfig('plugins/ask_grok')
            # 确保所有必要的键都存在
            for key, default in self._default_prefs.items():
                if key not in prefs:
                    prefs[key] = default
            return prefs
        except Exception as e:
            logger.error(f"Error loading preferences: {str(e)}")
            return self._default_prefs