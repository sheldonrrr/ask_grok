#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional
import requests
import json
from calibre_plugins.ask_gpt.config import get_prefs
import logging

# 设置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class XAIClient:
    def __init__(self, auth_token: Optional[str] = None):
        """Initialize X.AI client with authorization token.
        
        Args:
            auth_token: Optional authorization token. If not provided, will be read from preferences.
                      Should be in format "Bearer xai-xxx" or just "xai-xxx"
        """
        prefs = get_prefs()
        self.auth_token = auth_token or prefs.get('auth_token')
        if not self.auth_token:
            raise ValueError("X.AI authorization token not found. Please configure it in plugin settings.")
        
        # 确保 auth_token 格式正确
        self.auth_token = self.auth_token.strip()
        if not self.auth_token.startswith('Bearer '):
            self.auth_token = f"Bearer {self.auth_token}"
        
        self.api_base = prefs.get('api_base_url', 'https://api.x.ai/v1')
        self.model = prefs.get('model', 'grok-2-latest')
        logger.debug(f"Initialized XAIClient with model: {self.model}, api_base: {self.api_base}")

    def ask(self, prompt: str) -> str:
        try:
            logger.debug(f"Sending prompt: {prompt}")
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": self.auth_token
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
                "temperature": 0.7
            }
            
            # 发送请求
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            # 记录响应信息
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response headers: {response.headers}")
            logger.debug(f"Response text: {response.text}")
            
            if response.status_code != 200:
                error_text = response.text
                try:
                    error_json = response.json()
                    if isinstance(error_json, dict):
                        error_text = error_json.get('error', error_text)
                except:
                    pass
                return f"API Error: {error_text}"
            
            # 解析响应
            try:
                result = response.json()
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {str(e)}")
                return f"API Error: Invalid JSON response - {str(e)}"
            
            if not isinstance(result, dict):
                logger.error(f"Unexpected response format: {result}")
                return "Unexpected response format from API"
            
            choices = result.get('choices', [])
            if not choices:
                logger.warning("No choices in response")
                return "No response received"
                
            message = choices[0].get('message', {})
            content = message.get('content')
            
            if not content:
                logger.warning("No content in response message")
                return "Empty response from API"
                
            return content.strip()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {str(e)}", exc_info=True)
            error_msg = str(e)
            
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    if isinstance(error_data, dict):
                        error_msg = error_data.get('error', str(e))
                except:
                    if e.response.text:
                        error_msg = e.response.text
            
            return f"API Error: {error_msg}"
            
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return f"Error: {str(e)}"

def main():
    """Example usage of XAIClient."""
    try:
        client = XAIClient()
        response = client.ask("What is the meaning of life, the universe, and everything?")
        print(f"Final response: {response}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()