#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import openai
from calibre_plugins.ask_gpt.config import get_prefs

class ChatGPTAPI:
    def __init__(self):
        self.api_key = get_prefs()['api_key']
        
    def ask(self, prompt):
        """
        向 ChatGPT 发送问题并获取回答
        
        Args:
            prompt: 问题文本
            
        Returns:
            str: ChatGPT 的回答
        """
        if not self.api_key:
            raise ValueError("请先在插件设置中配置 OpenAI API Key")
            
        openai.api_key = self.api_key
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一个专业的读书专家，擅长回答关于书中知识和关于书籍的问题。"},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"调用 ChatGPT API 失败：{str(e)}")
