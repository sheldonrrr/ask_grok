#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional
import openai
from calibre_plugins.ask_gpt.config import get_prefs
import logging

# 设置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class XAIClient:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize X.AI client with API key."""
        prefs = get_prefs()
        self.api_key = api_key or prefs.get('api_key')
        if not self.api_key:
            raise ValueError("X.AI API key not found. Please configure it in plugin settings.")
        
        openai.api_key = self.api_key
        openai.api_base = prefs.get('api_base_url', 'https://api.x.ai/v1')
        self.model = prefs.get('model', 'grok-2-latest')
        logger.debug(f"Initialized XAIClient with model: {self.model}, api_base: {openai.api_base}")

    def ask(self, prompt: str) -> str:
        try:
            logger.debug(f"Sending prompt: {prompt}")
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."},
                    {"role": "user", "content": prompt}
                ],
            )

            # 调试：记录响应类型和内容
            logger.debug(f"Response type: {type(response)}")
            logger.debug(f"Raw response: {repr(response)}")

            # 处理不同类型的响应
            if isinstance(response, str):
                logger.debug("Received string response")
                return response.strip()
            
            elif isinstance(response, dict):
                logger.debug("Received dict response")
                choices = response.get('choices', [])
                if not choices:
                    logger.warning("No choices in response")
                    return "No response received"
                    
                message = choices[0].get('message', {})
                return message.get('content', str(message))
            
            elif hasattr(response, 'choices') and response.choices:
                logger.debug("Received object response")
                message = response.choices[0].message
                return message.content if hasattr(message, 'content') else str(message)
            
            else:
                logger.error("Unknown response format")
                return "Invalid response format"
        
        except openai.error.APIError as e:
            logger.error(f"API error: {str(e)}", exc_info=True)
            logger.debug(f"API error details: {repr(e.http_body)}")
            return f"API Error:{e.http_body or str(e)}"

        except Exception as e:
            logger.error(f"Exception occurred: {str(e)}", exc_info=True)
            raise Exception(f"Failed to call X.AI API: {str(e)}")

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