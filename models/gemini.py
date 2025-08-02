"""
Google Gemini 模型实现
"""
import json
import re
import time
import requests
from typing import Dict, Any, Optional
import logging

from .base import BaseAIModel

# 获取日志记录器
logger = logging.getLogger('calibre_plugins.ask_grok.models.gemini')

class GeminiModel(BaseAIModel):
    """
    Google Gemini 模型实现类
    """
    # 默认模型名称，集中管理便于后续更新
    DEFAULT_MODEL = "gemini-2.5-flash"
    # 默认 API 基础 URL
    DEFAULT_API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
    
    def _validate_config(self):
        """
        验证 Gemini 模型配置
        
        :raises ValueError: 当配置无效时抛出异常
        """
        required_keys = ['api_key', 'model']
        for key in required_keys:
            if not self.config.get(key):
                raise ValueError(f"Missing required config key: {key}")
        
        # 确保 api_base_url 存在，如果不存在则使用默认值
        if 'api_base_url' not in self.config:
            self.config['api_base_url'] = self.DEFAULT_API_BASE_URL
    
    def get_token(self) -> str:
        """
        获取 Gemini 模型的 API Key/Token
        
        :return: API Key/Token 字符串
        """
        return self.config.get('api_key', '')
    
    def validate_token(self) -> bool:
        """
        验证 Gemini 模型的 token 是否有效
        
        :return: 如果 token 有效则返回 True
        :raises ValueError: 当 token 无效时抛出异常
        """
        # 首先调用基类的基本验证
        super().validate_token()
        
        # Gemini API Key 格式验证（可选）
        # 注意：我们不对 Gemini API Key 做特定格式验证，因为它的格式可能会变化
        # 只进行基本的长度检查
        token = self.get_token()
        if len(token) < 10:  # 只要求基本长度
            raise ValueError("API Key is too short. Please check and enter the complete key.")
        
        return True
    
    def prepare_headers(self) -> Dict[str, str]:
        """
        准备 Gemini API 请求头
        
        :return: 请求头字典
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        # 在这里直接添加 API Key，而不是在 ask 方法中
        api_key = self.get_token()
        if api_key:
            headers["x-goog-api-key"] = api_key
            
        return headers
    
    def prepare_request_data(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        准备 Gemini API 请求数据
        
        :param prompt: 提示文本
        :param kwargs: 其他参数，如 temperature 等
        :return: 请求数据字典
        """
        system_message = kwargs.get('system_message', "You are an expert in book analysis. Your task is to help users understand books better by providing insightful questions and analysis.")
        
        # 构建基本请求数据结构，严格按照 Gemini API 要求格式化
        data = {
            "contents": []
        }
        
        # 如果有系统消息，添加为第一条消息
        if system_message and system_message.strip():
            data["contents"].append({
                "role": "user",  # Gemini 2.5 支持 role，但使用 user 而非 system
                "parts": [
                    {"text": system_message}
                ]
            })
        
        # 添加用户提示
        data["contents"].append({
            "role": "user",  # 明确指定角色
            "parts": [
                {"text": prompt}
            ]
        })
        
        # 添加生成配置
        generation_config = {
            # 设置默认的最大输出令牌数为 8192，这是 Gemini 2.5 Pro 支持的最大值
            # 这将允许模型生成更长的回复
            "maxOutputTokens": 65536
        }
        
        # 温度参数
        if 'temperature' in kwargs:
            generation_config["temperature"] = kwargs.get('temperature')
        
        # 最大输出令牌数 (如果用户指定了，则覆盖默认值)
        if 'max_tokens' in kwargs:
            generation_config["maxOutputTokens"] = kwargs.get('max_tokens')
        
        # 采样参数
        if 'top_p' in kwargs:
            generation_config["topP"] = kwargs.get('top_p')
        
        if 'top_k' in kwargs:
            generation_config["topK"] = kwargs.get('top_k')
        
        # 添加生成配置 (现在总是会添加，因为我们有默认的 maxOutputTokens)
        data['generationConfig'] = generation_config
            
        return data
    
    def mask_api_key(self, text: str) -> str:
        """
        隐藏文本中的 API Key
        
        :param text: 原始文本
        :return: 隐藏 API Key 后的文本
        """
        # 隐藏 URL 参数中的 API Key
        text = re.sub(r'key=[A-Za-z0-9_-]+', 'key=********', text)
        
        # 隐藏 JSON 中的 API Key
        text = re.sub(r'"api_key"\s*:\s*"[^"]+"', '"api_key":"********"', text)
        
        return text
    
    def ask(self, prompt: str, **kwargs) -> str:
        """向 Gemini API 发送请求并获取回复
        
        Args:
            prompt: 用户提问
            **kwargs: 其他参数，包括：
                system_message: 系统消息
                temperature: 温度
                max_tokens: 最大令牌数
                top_p: Top-p 采样
                top_k: Top-k 采样
                stream: 是否使用流式传输
                stream_callback: 流式回调函数
                
        Returns:
            模型回复的文本
        """
        # 获取模型名称和API基础URL
        model_name = kwargs.get('model', self.DEFAULT_MODEL)
        api_base_url = kwargs.get('api_base_url', self.DEFAULT_API_BASE_URL)
        
        # 准备请求头和请求体
        headers = self.prepare_headers()
        data = self.prepare_request_data(prompt, **kwargs)
        
        # 获取流式传输设置
        use_stream = kwargs.get('stream', self.config.get('enable_streaming', True))
        stream_callback = kwargs.get('stream_callback', None)
        
        # 根据是否使用流式传输构建不同的URL
        params = {}
        if use_stream:
            url = f"{api_base_url}/models/{model_name}:streamGenerateContent"
            params["alt"] = "sse"  # 使用 Server-Sent Events 格式
        else:
            url = f"{api_base_url}/models/{model_name}:generateContent"
            params = {}
        
        logger.debug(f"请求URL: {url}, 参数: {params}")
        
        # 重试设置
        max_retries = 3
        retry_delay = 2  # 秒
        
        for attempt in range(max_retries):
            try:
                if use_stream and stream_callback:
                    # 流式请求处理
                    full_content = ""
                    chunk_count = 0
                    last_chunk_time = time.time()
                    
                    logger.debug("开始流式请求")
                    # 增加超时时间到 300 秒，避免长回复时请求超时
                    with requests.post(
                        url,
                        headers=headers,
                        json=data,
                        params=params,
                        timeout=kwargs.get('timeout', 300),  # 增加默认超时时间到 300 秒
                        stream=True
                    ) as response:
                        response.raise_for_status()
                        logger.debug(f"流式响应状态码: {response.status_code}")
                        
                        try:
                            for line in response.iter_lines():
                                if line:
                                    line = line.decode('utf-8')
                                    logger.debug(f"收到流式响应行: {line[:50]}...")
                                    
                                    # 处理 SSE 格式，必须以 'data: ' 开头
                                    if line.startswith('data: '):
                                        line = line[6:]  # 去除 'data: ' 前缀
                                        
                                        # 特殊情况处理：如果是 [DONE] 标记
                                        if line.strip() == "[DONE]":
                                            logger.debug("收到流式响应结束标记 [DONE]")
                                            break
                                        
                                        try:
                                            chunk_data = json.loads(line)
                                            logger.debug(f"解析JSON数据: {json.dumps(chunk_data, ensure_ascii=False)[:100]}...")
                                            
                                            # 解析 Gemini 流式响应格式
                                            if 'candidates' in chunk_data and chunk_data['candidates']:
                                                candidate = chunk_data['candidates'][0]
                                                if 'content' in candidate:
                                                    content = candidate['content']
                                                    if 'parts' in content and content['parts']:
                                                        for part in content['parts']:
                                                            if 'text' in part and part['text']:
                                                                chunk_text = part['text']
                                                                full_content += chunk_text
                                                                stream_callback(chunk_text)
                                                                chunk_count += 1
                                                                last_chunk_time = time.time()
                                                                logger.debug(f"处理流式块 #{chunk_count}, 长度: {len(chunk_text)}, 累计长度: {len(full_content)}")
                                        except json.JSONDecodeError as e:
                                            logger.error(f"JSON解析错误: {str(e)}, 行内容: {line[:50]}...")
                                            continue
                                    
                                # 检查是否长时间没有收到新内容
                                if time.time() - last_chunk_time > 10:  # 10秒没有新内容，记录日志
                                    logger.warning(f"流式传输超过10秒没有新内容, 当前已收到 {chunk_count} 块, 总长度: {len(full_content)}")
                                    last_chunk_time = time.time()  # 重置计时器避免重复日志
                        except Exception as e:
                            logger.error(f"流式处理异常: {str(e)}")
                            # 如果已经有内容，不抛出异常，返回已收到的内容
                            if full_content:
                                logger.warning(f"尽管有异常，但返回已收到的 {len(full_content)} 字符内容")
                            else:
                                raise  # 如果没有内容，抛出异常
                    
                    logger.debug(f"流式请求完成, 总内容长度: {len(full_content)}字符")
                    return full_content
                else:
                    # 普通请求处理
                    logger.debug("开始普通请求，禁用流式传输")
                    try:
                        logger.debug(f"请求URL: {url}")
                        logger.debug(f"请求头: {json.dumps({k: '***' if k.lower() in ['authorization', 'x-goog-api-key'] else v for k, v in headers.items()}, ensure_ascii=False)}")
                        logger.debug(f"请求数据: {json.dumps(data, ensure_ascii=False)[:500]}...")
                        
                        response = requests.post(
                            url,
                            headers=headers,
                            json=data,
                            params=params,
                            timeout=kwargs.get('timeout', 60)  # 增加超时时间
                        )
                        response.raise_for_status()
                        
                        logger.debug(f"响应状态码: {response.status_code}")
                        result = response.json()
                        logger.debug(f"普通响应: {json.dumps(result, ensure_ascii=False)[:200]}...")
                        
                        # 解析 Gemini API 响应
                        if 'candidates' in result and result['candidates']:
                            candidate = result['candidates'][0]
                            if 'content' in candidate and 'parts' in candidate['content']:
                                text_parts = [part['text'] for part in candidate['content']['parts'] if 'text' in part]
                                content = ''.join(text_parts)
                                logger.debug(f"成功解析响应内容，长度: {len(content)}")
                                return content
                        
                        # 如果无法获取响应内容，返回错误信息
                        error_msg = "无法获取有效的 Gemini API 响应"
                        if 'error' in result:
                            error_msg = f"{error_msg}: {result['error'].get('message', '未知错误')}"
                        logger.error(f"Gemini API 响应解析失败: {error_msg}")
                        logger.debug(f"完整响应: {json.dumps(result, ensure_ascii=False)}")
                        raise Exception(error_msg)
                    except requests.exceptions.RequestException as req_e:
                        logger.error(f"Gemini API 请求异常: {str(req_e)}")
                        if hasattr(req_e, 'response') and req_e.response is not None:
                            try:
                                error_detail = req_e.response.json()
                                logger.error(f"错误详情: {json.dumps(error_detail, ensure_ascii=False)}")
                            except:
                                logger.error(f"响应内容: {req_e.response.text[:500]}")
                        raise
            
            except requests.exceptions.RequestException as e:
                logger.error(f"请求异常: {str(e)}")
                
                if attempt < max_retries - 1:
                    # 如果不是最后一次尝试，则等待后重试
                    retry_wait = retry_delay * (2 ** attempt)  # 指数退避
                    logger.info(f"第 {attempt+1} 次请求失败，{retry_wait} 秒后重试")
                    time.sleep(retry_wait)
                    continue
                
                # 最后一次尝试失败，提供详细错误信息
                error_msg = f"API 请求失败: {str(e)}"
                
                if hasattr(e, 'response') and e.response is not None:
                    try:
                        error_detail = e.response.json()
                        
                        # 根据错误类型提供更具体的错误信息
                        if e.response.status_code == 404:
                            error_msg = f"API 版本或模型名称错误: {error_detail.get('error', {}).get('message', '')}"
                            error_msg += f"\n\n请在设置中更新 API Base URL 为 '{self.DEFAULT_API_BASE_URL}' 并将模型更新为 '{self.DEFAULT_MODEL}' 或其他可用模型。"
                        elif e.response.status_code == 400:
                            error_msg = f"API 请求格式错误: {error_detail.get('error', {}).get('message', '')}"
                        elif e.response.status_code == 401:
                            error_msg = f"API Key 无效或未授权: {error_detail.get('error', {}).get('message', '')}"
                            error_msg += "\n\n请检查您的 API Key 是否正确，并确保已启用 Gemini API 访问权限。"
                        elif e.response.status_code == 429:
                            error_msg = "请求频率超限，请稍后再试"
                            error_msg += "\n\n您可能已超过 Google Gemini API 的免费使用配额。这可能是因为："
                            error_msg += "\n1. 每分钟请求次数超限"
                            error_msg += "\n2. 每天请求次数超限"
                            error_msg += "\n3. 每分钟输入令牌数超限"
                    except:
                        error_msg += f" | 响应内容: {e.response.text[:200] if hasattr(e.response, 'text') else '无法解析响应'}"
                
                raise Exception(error_msg) from e
    
    def supports_streaming(self) -> bool:
        """
        检查 Gemini 模型是否支持流式传输
        
        :return: 始终返回 True，因为 Gemini API 支持流式传输
        """
        return True
        
    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """
        获取 Gemini 模型的默认配置
        
        :return: 默认配置字典
        """
        return {
            "api_key": "",
            "api_base_url": cls.DEFAULT_API_BASE_URL,
            "model": cls.DEFAULT_MODEL,
            "enable_streaming": True,  # 默认启用流式传输
        }
