#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from typing import Optional, Dict, Any, Tuple
import logging
from .i18n import get_translation

# 添加一个 logger
logger = logging.getLogger(__name__)

class GrokAPIError(Exception):
    """自定义 API 错误异常类"""
    def __init__(self, message: str, status_code: Optional[int] = None, error_type: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.error_type = error_type
        self.message = message

    def __str__(self) -> str:
        if self.status_code:
            return f"{self.message} (Status: {self.status_code})"
        return self.message

class APIClient:
    """X.AI API 客户端"""
    
    def __init__(self, api_base: str = "https://api.x.ai/v1", model: str = "grok-3-latest", auth_token: str = None, i18n: Dict[str, str] = None):
        """初始化 X.AI API 客户端
        
        Args:
            api_base: API 基础 URL
            model: 使用的模型名称
            auth_token: 认证令牌（可选，如果为 None 会从配置中读取）
            i18n: 国际化文本字典
        """
        self._api_base = api_base.rstrip('/')
        self._model = model
        # 存储默认值
        self._default_prefs = {
            'api_base_url': api_base,
            'model': model,
            'auth_token': auth_token or ''
        }
        # 初始化 i18n
        self.i18n = i18n or get_translation('en')
    
    def _prepare_request(self, prompt: str) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """准备 API 请求的共同部分
        
        Args:
            prompt: 问题文本
            
        Returns:
            tuple: (headers, data) 请求头和请求数据
        """
        
        token = self.auth_token

        # 记录原始 token 用于调试（脱敏处理）
        logger.debug(f"Token length: {len(token)}")
        
        # 检查 token 格式
        if not (token.lower().startswith('xai-') or token.lower().startswith('Bearer xai-')):
            error_msg = self.i18n.get(
                'invalid_token_format', 
                'Invalid token format. Token must start with \'xai-\' or \'Bearer xai-\''
            )
            raise GrokAPIError(error_msg, error_type="auth_error")
        
        # 检查 token 长度
        if len(token) < 64:  # 假设最小长度为 64
            error_msg = self.i18n.get(
                'token_too_short_message',
                'Token is too short. Please check and enter the complete token.'
            )
            raise GrokAPIError(error_msg, error_type="auth_error")
        
        # 确保 token 有 Bearer 前缀
        if not token.startswith('Bearer '):
            token = f'Bearer {token}'
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": token
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
    
    def ask(self, prompt: str, lang_code: str = 'en', return_dict: bool = False) -> str:
        """向 X.AI API 发送问题并获取回答（非流式）
        
        Args:
            prompt: 问题文本
            lang_code: 语言代码，用于获取相应的翻译文本
            return_dict: 是否返回字典类型，默认为 False 返回字符串
            
        Returns:
            Union[str, dict]: 默认返回字符串，当 return_dict=True 时返回解析后的字典
            
        Raises:
            GrokAPIError: 当 API 请求失败时抛出
            
        Note:
            这个方法不使用流式请求，更适合处理长文本和需要完整响应的场景
        """
        # 记录请求开始
        logger.info(f"=== 开始处理 API 请求 ===")
        logger.info(f"请求语言代码: {lang_code}")
        logger.info(f"原始提示词: {prompt[:500]}{'...' if len(prompt) > 500 else ''}")
        
        try:
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
            logger.debug(f"API 响应: {result}")
            
            # 提取回答
            if 'choices' in result and len(result['choices']) > 0:
                answer = result['choices'][0].get('message', {}).get('content', '')
                if not answer:
                    raise GrokAPIError(self.i18n.get('empty_answer','API returned an empty answer'))
                
                logger.info(f"成功获取到回答，长度: {len(answer)} 字符")
                logger.debug(f"回答内容 (前500字符): {answer[:500]}{'...' if len(answer) > 500 else ''}")
                
                if return_dict:
                    try:
                        import json
                        return json.loads(answer)
                    except json.JSONDecodeError:
                        logger.warning("返回的内容不是有效的 JSON 格式，返回原始字符串")
                        return answer
                return answer
            else:
                raise GrokAPIError("API 响应中未找到有效的回答")
                
        except requests.exceptions.RequestException as e:
            status_code = None
            error_msg = str(e)
            
            # 尝试从响应中提取更多错误信息
            if hasattr(e, 'response') and e.response is not None:
                status_code = e.response.status_code
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get('error', {}).get('message', str(e))
                    logger.error(f"API 错误详情: {error_data}")
                except:
                    error_msg = e.response.text[:500]  # 限制错误消息长度
                    logger.error(f"API 错误响应: {error_msg}")
            else:
                logger.error(f"请求 API 时发生错误: {error_msg}")
            
            if status_code == 401:
                
                # 支持i18n的提示字段
                error_msg = self.i18n.get('auth_error_401','Unauthorized token')
                raise GrokAPIError(
                    error_msg,
                    status_code=status_code,
                    error_type="auth_error"
                )
            elif status_code == 403:
                error_msg = self.i18n.get('auth_error_403','Forbidden token')
                raise GrokAPIError(
                    error_msg,
                    status_code=status_code,
                    error_type="auth_error"
                )
            elif status_code == 429:
                error_msg = self.i18n.get('rate_limit','Request too frequent, please try again later')
                raise GrokAPIError(
                    error_msg,
                    status_code=status_code,
                    error_type="rate_limit"
                )
            else:
                error_msg = self.i18n.get('Invalid token','Please check your API token validable in the plugin settings.')
                raise GrokAPIError(
                    error_msg,
                    status_code=status_code,
                    error_type="api_error"
                )
            
        except json.JSONDecodeError as e:
            logger.error(f"解析 API 响应时发生 JSON 解码错误: {str(e)}")
            raise GrokAPIError(self.i18n.get('Invalid JSON response','Invalid JSON response'))
            
        except Exception as e:
            logger.error(f"处理 API 请求时发生未知错误: {str(e)}", exc_info=True)
            if not isinstance(e, GrokAPIError):
                raise GrokAPIError(self.i18n.get('Unknown error','Unknown error'))
            raise
            
        finally:
            logger.info("=== API 请求处理完成 ===\n")

    def random_question(self, prompt: str, lang_code: str = 'en', return_dict: bool = False) -> str:
        """向 X.AI API 发送问题并获取回答（非流式请求，适用于短文本）
        
        Args:
            prompt: 问题文本
            lang_code: 语言代码，用于获取相应的翻译文本
            return_dict: 是否返回字典类型，默认为 False 返回字符串
            
        Returns:
            Union[str, dict]: 默认返回字符串，当 return_dict=True 时返回解析后的字典
        
        Note:
            这个方法不使用流式请求，更适合处理短文本和快速响应的场景
        """
        
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
        status_code = None
        
        try:
            # 添加超时设置
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data,
                timeout=10
            )
            
            status_code = response.status_code
            
            # 处理成功响应
            if status_code == 200:
                # 成功响应
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    answer = result['choices'][0].get('message', {}).get('content', '')
                    if not answer:
                        raise GrokAPIError(
                            self.i18n.get('empty_answer', 'API returned an empty answer'),
                            error_type="api_error"
                        )
                    return answer
                else:
                    raise GrokAPIError(
                        self.i18n.get('invalid_response', 'Invalid response format from API'),
                        error_type="api_error"
                    )
            # 处理错误响应
            elif status_code == 401:
                error_msg = self.i18n.get('auth_error_401', 'Unauthorized token')
                raise GrokAPIError(
                    error_msg,
                    status_code=status_code,
                    error_type="auth_error"
                )
            elif status_code == 403:
                error_msg = self.i18n.get('auth_error_403', 'Forbidden token')
                raise GrokAPIError(
                    error_msg,
                    status_code=status_code,
                    error_type="auth_error"
                )
            elif status_code == 429:
                error_msg = self.i18n.get('rate_limit', 'Request too frequent, please try again later')
                raise GrokAPIError(
                    error_msg,
                    status_code=status_code,
                    error_type="rate_limit"
                )
            else:
                error_msg = self.i18n.get('invalid_token_message', 'Please check your API token validable in the plugin settings.')
                raise GrokAPIError(
                    error_msg,
                    status_code=status_code,
                    error_type="api_error"
                )
        except json.JSONDecodeError as e:
            error_msg = self.i18n.get('invalid_json', 'Invalid JSON response')
            raise GrokAPIError(
                error_msg,
                error_type="parse_error"
            )
        
        except Exception as e:
            error_msg = self.i18n.get('unknown_error', 'Unknown error')
            raise GrokAPIError(
                error_msg,
                error_type="unknown_error"
            )
    

    
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