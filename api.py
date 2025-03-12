#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional
import openai
from calibre_plugins.ask_gpt.config import get_prefs

class XAIClient:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize X.AI client with API key.
        
        The API key is read in the following order:
        1. Passed api_key parameter
        2. Plugin settings (via get_prefs)
        3. Environment variable 'OPENAI_API_KEY'
        """
        prefs = get_prefs()
        self.api_key = api_key or prefs.get('api_key')
        if not self.api_key:
            raise ValueError("X.AI API key not found. Please configure it in plugin settings.")
        
        # 设置 API 配置
        openai.api_key = self.api_key
        openai.api_base = prefs.get('api_base_url', 'https://api.x.ai/v1')
        self.model = prefs.get('model', 'grok-2-latest')

    def ask(self, prompt: str) -> str:
        """
        Send a question to X.AI Grok model and get the response
        
        Args:
            prompt: The question text
            
        Returns:
            str: Grok's response
            
        Raises:
            Exception: If API call fails
        """
        try:
            completion = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."},
                    {"role": "user", "content": prompt}
                ],
            )
            return completion.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Failed to call X.AI API: {str(e)}")

def main():
    """Example usage of XAIClient."""
    try:
        client = XAIClient()
        response = client.ask("What is the meaning of life, the universe, and everything?")
        print(response)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
