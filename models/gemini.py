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
from ..i18n import get_translation

# 获取日志记录器
logger = logging.getLogger('calibre_plugins.ask_ai_plugin.models.gemini')

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
        # 基本必需字段（不包括 model，因为在获取模型列表时可能为空）
        required_keys = ['api_key']
        for key in required_keys:
            if not self.config.get(key):
                translations = get_translation(self.config.get('language', 'en'))
                raise ValueError(translations.get('missing_required_config', 'Missing required configuration: {key}').format(key=key))
        
        # 确保 api_base_url 存在，如果不存在则使用默认值
        if 'api_base_url' not in self.config:
            self.config['api_base_url'] = self.DEFAULT_API_BASE_URL
        
        # 如果 model 为空，使用默认值
        if not self.config.get('model'):
            self.config['model'] = self.DEFAULT_MODEL
    
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
        
        # 只进行基本的长度检查
        token = self.get_token()
        if len(token) < 10:  # 只要求基本长度
            translations = get_translation(self.config.get('language', 'en'))
            raise ValueError(translations.get('api_key_too_short', 'API Key is too short. Please check and enter the complete key.'))
        
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
        translations = get_translation(self.config.get('language', 'en'))
        system_message = kwargs.get('system_message', translations.get('default_system_message', 'You are an expert in book analysis. Your task is to help users understand books better by providing insightful questions and analysis.'))
        
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
        generation_config = {}
        
        # 温度参数
        if 'temperature' in kwargs:
            generation_config["temperature"] = kwargs.get('temperature')
        
        # 最大输出令牌数 (如果用户指定了，则覆盖默认值)
        if 'max_tokens' in kwargs:
            generation_config["maxOutputTokens"] = kwargs.get('max_tokens')
        
        # 最大输出令牌数为 128000
        generation_config["maxOutputTokens"] = 128000

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
        
        # 获取流式传输设置（只有明确指定才使用流式）
        use_stream = kwargs.get('stream', False)
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
                                        except json.JSONDecodeError as je:
                                            logger.error(f"JSON解析错误: {str(je)}, 行内容: {line[:50]}...")
                                            continue
                                
                                # 检查是否超过5秒没有收到新数据
                                current_time = time.time()
                                if current_time - last_chunk_time > 15:
                                    logger.warning(f"已经 {current_time - last_chunk_time:.1f} 秒没有收到新数据")
                                
                                # 如果超过15秒没有收到新数据，尝试恢复连接
                                if current_time - last_chunk_time > 60 and full_content:  # 只有在已有内容的情况下才触发
                                    logger.warning("超过15秒无响应，主动触发恢复机制")
                                    raise requests.exceptions.ReadTimeout("流式传输超过15秒没有新内容，可能是连接问题")
                                
                                last_chunk_time = current_time  # 重置计时器避免重复日志
                        except Exception as e:
                            logger.error(f"流式处理异常: {str(e)}")
                            # 记录异常时的状态
                            logger.warning(f"异常发生时状态: 已接收 {chunk_count} 块, 总长度: {len(full_content)}")
                            
                            # 如果已经有内容，尝试恢复连接
                            if full_content:
                                logger.info("尝试恢复连接以获取完整响应...")
                                try:
                                    # 保存当前已接收的内容
                                    current_content = full_content
                                    
                                    # 重新构建请求，添加标记表示这是恢复请求
                                    recovery_data = self.prepare_request_data(prompt, **kwargs)
                                    
                                    # 检查响应是否可能不完整（例如缺少结束标点或代码块未闭合）
                                    unclosed_code_blocks = full_content.count('```') % 2
                                    
                                    # 添加恢复标记，让模型知道这是继续之前的对话
                                    if 'contents' in recovery_data and len(recovery_data['contents']) > 0:
                                        # 如果最后一个内容是用户消息，添加一个系统消息表示继续
                                        translations = get_translation(self.config.get('language', 'en'))
                                        recovery_prompt = translations.get('stream_continue_prompt', 'Please continue your previous answer without repeating content already provided.')
                                        
                                        # 根据不同的不完整情况生成不同的恢复提示
                                        if unclosed_code_blocks:
                                            recovery_prompt += translations.get('stream_continue_code_blocks', 'Your previous answer had unclosed code blocks. Please continue and complete these code blocks.')
                                        
                                        recovery_data['contents'].append({
                                            "role": "user",
                                            "parts": [{"text": recovery_prompt}]
                                        })
                                    
                                    # 设置更长的超时时间
                                    recovery_timeout = kwargs.get('timeout', 300) + 60
                                    
                                    logger.info(f"发起恢复请求，超时时间: {recovery_timeout}秒")
                                    
                                    # 发起恢复请求
                                    with requests.post(
                                        url,
                                        headers=headers,
                                        json=recovery_data,
                                        params=params,
                                        timeout=recovery_timeout,
                                        stream=True
                                    ) as recovery_response:
                                        recovery_response.raise_for_status()
                                        logger.info(f"恢复连接成功，状态码: {recovery_response.status_code}")
                                        
                                        # 处理恢复响应
                                        for line in recovery_response.iter_lines():
                                            if line:
                                                line = line.decode('utf-8')
                                                
                                                if line.startswith('data: '):
                                                    line = line[6:]
                                                    
                                                    if line.strip() == "[DONE]":
                                                        logger.info("恢复请求收到结束标记 [DONE]")
                                                        break
                                                    
                                                    try:
                                                        chunk_data = json.loads(line)
                                                        
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
                                                    except json.JSONDecodeError as je:
                                                        logger.error(f"恢复请求JSON解析错误: {str(je)}")
                                                        continue
                                        
                                        logger.info(f"恢复请求完成，新增内容长度: {len(full_content) - len(current_content)}")
                                except Exception as recovery_e:
                                    logger.error(f"恢复连接失败: {str(recovery_e)}")
                                    logger.warning(f"将返回已接收的 {len(full_content)} 字符内容")
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
                            timeout=kwargs.get('timeout', 300)  # 增加超时时间
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
                        translations = get_translation(self.config.get('language', 'en'))
                        error_msg = translations.get('api_invalid_response', 'Unable to get valid API response')
                        if 'error' in result:
                            error_msg = f"{error_msg}: {result['error'].get('message', translations.get('unknown_error', 'Unknown error'))}"
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
                translations = get_translation(self.config.get('language', 'en'))
                error_msg = translations.get('api_request_failed', 'API request failed: {error}').format(error=str(e))
                
                if hasattr(e, 'response') and e.response is not None:
                    try:
                        error_detail = e.response.json()
                        
                        # 根据错误类型提供更具体的错误信息
                        if e.response.status_code == 404:
                            error_msg = translations.get('api_version_model_error', 'API version or model name error: {message}\n\nPlease update API Base URL to "{base_url}" and model to "{model}" or other available model in settings.').format(
                                message=error_detail.get('error', {}).get('message', ''),
                                base_url=self.DEFAULT_API_BASE_URL,
                                model=self.DEFAULT_MODEL
                            )
                        elif e.response.status_code == 400:
                            error_msg = translations.get('api_format_error', 'API request format error: {message}').format(
                                message=error_detail.get('error', {}).get('message', '')
                            )
                        elif e.response.status_code == 401:
                            error_msg = translations.get('api_key_invalid', 'API Key invalid or unauthorized: {message}\n\nPlease check your API Key and ensure API access is enabled.').format(
                                message=error_detail.get('error', {}).get('message', '')
                            )
                        elif e.response.status_code == 429:
                            error_msg = translations.get('api_rate_limit', 'Request rate limit exceeded, please try again later\n\nYou may have exceeded the free usage quota. This could be due to:\n1. Too many requests per minute\n2. Too many requests per day\n3. Too many input tokens per minute')
                    except:
                        error_msg += f" | 响应内容: {e.response.text[:200] if hasattr(e.response, 'text') else '无法解析响应'}"
                
                raise Exception(error_msg) from e
    
    def get_model_name(self) -> str:
        """
        获取当前模型名称
        
        :return: 模型名称字符串
        """
        return self.config.get('model', self.DEFAULT_MODEL)
    
    def get_provider_name(self) -> str:
        """
        获取提供商名称
        
        :return: 提供商名称字符串
        """
        return "Google Gemini"
    
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
    
    def prepare_models_request_headers(self) -> Dict[str, str]:
        """
        准备获取模型列表的请求头
        Gemini 获取模型列表时不需要在请求头中添加 API key
        API key 通过 URL 参数传递
        
        :return: 请求头字典
        """
        return {
            "Content-Type": "application/json"
        }
    
    def prepare_models_request_url(self, base_url: str, endpoint: str) -> str:
        """
        准备获取模型列表的完整 URL
        Gemini 将 API key 作为 URL 参数
        
        :param base_url: API 基础 URL
        :param endpoint: API 端点路径
        :return: 完整的请求 URL
        """
        api_key = self.config.get('api_key', '')
        return f"{base_url}{endpoint}?key={api_key}"
    
    def parse_models_response(self, data: Dict[str, Any]) -> list:
        """
        解析 Gemini API 的模型列表响应
        Gemini 使用 "models" 字段，且模型名称有 "models/" 前缀需要移除
        
        :param data: API 响应的 JSON 数据
        :return: 模型名称列表
        """
        models = []
        for model in data.get('models', []):
            model_name = model.get('name', '')
            # Remove "models/" prefix if present
            if model_name.startswith('models/'):
                models.append(model_name.replace('models/', ''))
            else:
                models.append(model_name)
        return models
    
    # Gemini 只需重写 URL 格式和响应解析，其他使用基类默认实现
