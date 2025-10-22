"""
Grok AI 模型实现
"""
import json
import requests
import time
import logging
from typing import Dict, Any, Optional

from .base import BaseAIModel
from ..i18n import get_translation


class GrokModel(BaseAIModel):
    """
    Grok AI 模型实现类
    """
    # 默认模型名称，集中管理便于后续更新
    DEFAULT_MODEL = "grok-4-latest"
    # 默认 API 基础 URL
    DEFAULT_API_BASE_URL = "https://api.x.ai/v1"
    
    def _validate_config(self):
        """
        验证 Grok 模型配置
        
        :raises ValueError: 当配置无效时抛出异常
        """
        # 基本必需字段（不包括 model，因为在获取模型列表时可能为空）
        required_keys = ['auth_token', 'api_base_url']
        for key in required_keys:
            if not self.config.get(key):
                translations = get_translation(self.config.get('language', 'en'))
                raise ValueError(translations.get('missing_required_config', 'Missing required configuration: {key}').format(key=key))
        
        # 如果 model 为空，使用默认值
        if not self.config.get('model'):
            self.config['model'] = self.DEFAULT_MODEL
    
    def get_token(self) -> str:
        """
        获取 Grok 模型的 API Key/Token
        
        :return: API Key/Token 字符串
        """
        return self.config.get('auth_token', '')
    
    def validate_token(self) -> bool:
        """
        验证 Grok 模型的 token 是否有效
        
        :return: 如果 token 有效则返回 True
        :raises ValueError: 当 token 无效时抛出异常
        """
        # 首先调用基类的基本验证
        super().validate_token()
        
        token = self.get_token()
        
        # Grok API Key 格式验证：只验证基本长度
        if len(token) < 10:
            translations = get_translation(self.config.get('language', 'en'))
            raise ValueError(translations.get('api_key_too_short', 'API Key is too short. Please check and enter the complete key.'))
        
        return True
    
    def prepare_headers(self) -> Dict[str, str]:
        """
        准备 Grok API 请求头
        
        :return: 请求头字典
        """
        token = self.get_token()
        
        # 确保 token 有 Bearer 前缀
        if not token.startswith('Bearer '):
            token = f'Bearer {token}'
            
        return {
            "Content-Type": "application/json",
            "Authorization": token
        }
    
    def prepare_request_data(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        准备 Grok API 请求数据
        
        :param prompt: 提示文本
        :param kwargs: 其他参数，如 temperature、stream 等
        :return: 请求数据字典
        """
        translations = get_translation(self.config.get('language', 'en'))
        system_message = kwargs.get('system_message', translations.get('default_system_message', 'You are an expert in book analysis. Your task is to help users understand books better by providing insightful questions and analysis.'))
        
        data = {
            "model": self.config.get('model', self.DEFAULT_MODEL),
            "messages": [
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": kwargs.get('temperature', 0.7),
            "max_tokens": kwargs.get('max_tokens', 128000)
        }
        
        # 添加流式传输支持（只有明确指定 stream=True 才添加）
        if kwargs.get('stream', False):
            data['stream'] = True
            
        return data
    
    def ask(self, prompt: str, **kwargs) -> str:
        """
        向 Grok API 发送提示并获取响应
        
        :param prompt: 提示文本
        :param kwargs: 其他参数，如 temperature、stream、stream_callback 等
        :return: AI 模型的响应文本
        :raises Exception: 当请求失败时抛出异常
        """
        # 准备请求头和数据
        headers = self.prepare_headers()
        data = self.prepare_request_data(prompt, **kwargs)
        
        # 检查是否使用流式传输
        use_stream = kwargs.get('stream', self.config.get('enable_streaming', True))
        stream_callback = kwargs.get('stream_callback', None)
        
        try:
            # 如果使用流式传输
            if use_stream and stream_callback:
                full_content = ""
                chunk_count = 0
                last_chunk_time = time.time()
                logger = logging.getLogger('calibre_plugins.ask_grok.models.grok')
                
                api_url = f"{self.config['api_base_url']}/chat/completions"
                
                try:
                    with requests.post(
                        api_url,
                        headers=headers,
                        json=data,
                        timeout=kwargs.get('timeout', 300),  # 流式传输需要更长的超时时间
                        stream=True,
                        verify=False  # 注意：生产环境应该验证 SSL 证书
                    ) as response:
                        response.raise_for_status()
                        
                        for line in response.iter_lines():
                            if line:
                                line_str = line.decode('utf-8')
                                if line_str.startswith('data: '):
                                    # 处理数据行
                                    try:
                                        line_data = json.loads(line_str[6:])  # 去除 'data: ' 前缀
                                        if 'choices' in line_data and line_data['choices']:
                                            choice = line_data['choices'][0]
                                            if 'delta' in choice and 'content' in choice['delta']:
                                                chunk_text = choice['delta']['content']
                                                if chunk_text:
                                                    full_content += chunk_text
                                                    stream_callback(chunk_text)
                                                    chunk_count += 1
                                                    last_chunk_time = time.time()
                                    except json.JSONDecodeError as je:
                                        logger.error(f"JSON解析错误: {str(je)}, 行内容: {line_str[:50]}...")
                                        continue
                                    
                                # 检查是否超过15秒没有收到新数据
                                current_time = time.time()
                                if current_time - last_chunk_time > 15:
                                    logger.warning(f"已经 {current_time - last_chunk_time:.1f} 秒没有收到新数据")
                                
                                # 如果超过60秒没有收到新数据，尝试恢复连接
                                if current_time - last_chunk_time > 60 and full_content:  # 只有在已有内容的情况下才触发
                                    logger.warning("超过60秒无响应，主动触发恢复机制")
                                    translations = get_translation(self.config.get('language', 'en'))
                                    raise requests.exceptions.ReadTimeout(translations.get('stream_timeout_error', "流式传输超过60秒没有新内容，可能是连接问题"))
                                
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
                            translations = get_translation(self.config.get('language', 'en'))
                            recovery_prompt = translations.get('stream_continue_prompt', 'Please continue your previous answer without repeating content already provided.')
                            
                            # 根据不同的不完整情况生成不同的恢复提示
                            if unclosed_code_blocks:
                                recovery_prompt += " " + translations.get('stream_continue_code_blocks', 'Your previous answer had unclosed code blocks. Please continue and complete these code blocks.')
                            
                            # 为恢复请求添加用户消息
                            recovery_data['messages'].append({
                                "role": "user",
                                "content": recovery_prompt
                            })
                            
                            # 设置更长的超时时间
                            recovery_timeout = kwargs.get('timeout', 300) + 60
                            
                            logger.info(f"发起恢复请求，超时时间: {recovery_timeout}秒")
                            
                            # 发起恢复请求
                            with requests.post(
                                api_url,
                                headers=headers,
                                json=recovery_data,
                                timeout=recovery_timeout,
                                stream=True,
                                verify=False
                            ) as recovery_response:
                                recovery_response.raise_for_status()
                                logger.info(f"恢复连接成功，状态码: {recovery_response.status_code}")
                                
                                # 处理恢复响应
                                for line in recovery_response.iter_lines():
                                    if line:
                                        line_str = line.decode('utf-8')
                                        if line_str.startswith('data: '):
                                            line_data_str = line_str[6:]
                                            
                                            if line_data_str.strip() == "[DONE]":
                                                logger.info("恢复请求收到结束标记 [DONE]")
                                                break
                                            
                                            try:
                                                line_data = json.loads(line_data_str)
                                                if 'choices' in line_data and line_data['choices']:
                                                    choice = line_data['choices'][0]
                                                    if 'delta' in choice and 'content' in choice['delta']:
                                                        chunk_text = choice['delta']['content']
                                                        if chunk_text:
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
                # 非流式请求
                logger = logging.getLogger('calibre_plugins.ask_grok.models.grok')
                
                logger.debug("开始Grok非流式请求")
                try:
                    # 记录请求详情，但隐藏敏感信息
                    api_url = f"{self.config['api_base_url']}/chat/completions"
                    logger.debug(f"请求URL: {api_url}")
                    
                    # 隐藏授权信息的请求头记录
                    safe_headers = {k: '***' if k.lower() == 'authorization' else v for k, v in headers.items()}
                    logger.debug(f"请求头: {json.dumps(safe_headers, ensure_ascii=False)}")
                    
                    # 记录请求数据
                    logger.debug(f"请求数据: {json.dumps(data, ensure_ascii=False)[:500]}...")
                    
                    response = requests.post(
                        api_url,
                        headers=headers,
                        json=data,
                        timeout=kwargs.get('timeout', 300),  # 增加超时时间
                        verify=False  # 注意：生产环境应该验证 SSL 证书
                    )
                    response.raise_for_status()
                    
                    logger.debug(f"Grok响应状态: {response.status_code}, 响应长度: {len(response.text)}")
                    
                    result = response.json()
                    
                    if 'choices' in result and result['choices'] and len(result['choices']) > 0:
                        if 'message' in result['choices'][0] and 'content' in result['choices'][0]['message']:
                            content = result['choices'][0]['message']['content']
                            logger.debug(f"成功获取Grok响应内容，长度: {len(content)}")
                            return content
                        elif 'text' in result['choices'][0]:
                            # 尝试从其他可能的字段获取内容
                            content = result['choices'][0]['text']
                            logger.debug(f"从替代字段获取Grok响应内容，长度: {len(content)}")
                            return content
                    
                    # 如果无法从标准格式提取内容，尝试从整个响应中提取有用信息
                    logger.warning("无法从标准格式提取Grok API响应内容，尝试提取原始响应")
                    
                    # 尝试从响应中提取任何可能的文本内容
                    if isinstance(result, dict):
                        # 尝试从响应中的任何字段提取文本
                        for key, value in result.items():
                            if isinstance(value, str) and len(value) > 10:
                                logger.debug(f"从字段 '{key}' 提取内容，长度: {len(value)}")
                                return value
                            elif isinstance(value, list) and value and isinstance(value[0], dict):
                                # 尝试从列表中的第一个字典提取内容
                                for sub_key, sub_value in value[0].items():
                                    if isinstance(sub_value, str) and len(sub_value) > 10:
                                        logger.debug(f"从子字段 '{key}.{sub_key}' 提取内容，长度: {len(sub_value)}")
                                        return sub_value
                    
                    # 如果仍然无法提取内容，返回响应的字符串表示
                    response_str = json.dumps(result, ensure_ascii=False)
                    if len(response_str) > 10:  # 确保响应不是空的或者太短
                        logger.warning(f"返回原始响应字符串，长度: {len(response_str)}")
                        return response_str[:128000]  # 限制长度以避免过大的响应
                    
                    # 如果响应格式不符合预期且无法提取任何有用内容
                    translations = get_translation(self.config.get('language', 'en'))
                    error_msg = translations.get('api_content_extraction_failed', 'Unable to extract content from Grok API response')
                    logger.error(f"{error_msg}, 响应: {json.dumps(result, ensure_ascii=False)[:200]}...")
                    # 抛出异常而不是返回带有Error:前缀的字符串
                    raise Exception(error_msg)
                except requests.exceptions.RequestException as req_e:
                    translations = get_translation(self.config.get('language', 'en'))
                    error_msg = translations.get('api_request_failed', 'Grok API request failed: {error}').format(error=str(req_e))
                    logger.error(error_msg)
                    if hasattr(req_e, 'response') and req_e.response is not None:
                        try:
                            error_detail = req_e.response.json()
                            logger.error(f"错误详情: {json.dumps(error_detail, ensure_ascii=False)}")
                        except:
                            logger.error(f"响应内容: {req_e.response.text[:500]}")
                    raise Exception(error_msg) from req_e
            
        except requests.exceptions.RequestException as e:
            translations = get_translation(self.config.get('language', 'en'))
            error_msg = translations.get('api_request_failed', 'API request failed: {error}').format(error=str(e))
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    error_msg += f" | {json.dumps(error_detail, ensure_ascii=False)}"
                except:
                    error_msg += f" | {e.response.text}"
            raise Exception(error_msg) from e
    
    def supports_streaming(self) -> bool:
        """
        检查 Grok 模型是否支持流式传输
        
        :return: 始终返回 True，因为 Grok API 支持流式传输
        """
        return True
    
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
        return "x.AI (Grok)"
    
    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """
        获取 Grok 模型的默认配置
        
        :return: 默认配置字典
        """
        return {
            "auth_token": "",
            "api_base_url": cls.DEFAULT_API_BASE_URL,
            "model": cls.DEFAULT_MODEL,
            "enable_streaming": True,  # 默认启用流式传输
        }
    
    # Grok 使用基类的默认实现（OpenAI 兼容格式），无需重写 fetch_available_models
    # 注意：Grok 使用 auth_token 而不是 api_key，但 prepare_headers() 已经处理了这个差异
