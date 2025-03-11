#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                           QLineEdit, QPushButton)
import os
from calibre.utils.config import JSONConfig

# 全局配置对象
prefs = JSONConfig('plugins/ask_gpt')

# 默认配置
prefs.defaults['api_key'] = os.environ.get('OPENAI_API_KEY', '')
prefs.defaults['template'] = '关于{title}这本书，{query}'
prefs.defaults['api_base_url'] = 'https://api.x.ai/v1'
prefs.defaults['model'] = 'grok-2-latest'

def get_prefs():
    # 如果配置中没有 API key，尝试从环境变量获取
    if not prefs['api_key'] and os.environ.get('OPENAI_API_KEY'):
        prefs['api_key'] = os.environ.get('OPENAI_API_KEY')
    return prefs

class ConfigWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # X.AI API Key 配置
        key_label = QLabel('X.AI API Key:')
        self.layout.addWidget(key_label)
        
        self.api_key_edit = QLineEdit(self)
        self.api_key_edit.setText(prefs['api_key'])
        self.layout.addWidget(self.api_key_edit)
        
        # API Base URL 配置
        base_url_label = QLabel('API Base URL:')
        self.layout.addWidget(base_url_label)
        
        self.base_url_edit = QLineEdit(self)
        self.base_url_edit.setText(prefs['api_base_url'])
        self.base_url_edit.setPlaceholderText('Default: https://api.x.ai/v1')
        self.layout.addWidget(self.base_url_edit)
        
        # Model 配置
        model_label = QLabel('Model:')
        self.layout.addWidget(model_label)
        
        self.model_edit = QLineEdit(self)
        self.model_edit.setText(prefs['model'])
        self.model_edit.setPlaceholderText('Default: grok-2-latest')
        self.layout.addWidget(self.model_edit)
        
        # 提示词模板配置
        template_label = QLabel('提示词模板:')
        self.layout.addWidget(template_label)
        
        self.template_edit = QLineEdit(self)
        self.template_edit.setText(prefs['template'])
        self.template_edit.setPlaceholderText('使用 {title} 表示书名，{query} 表示问题')
        self.layout.addWidget(self.template_edit)
        
        self.layout.addStretch()
    
    def save_settings(self):
        """保存配置到 calibre 配置文件"""
        prefs['api_key'] = self.api_key_edit.text()
        prefs['api_base_url'] = self.base_url_edit.text()
        prefs['model'] = self.model_edit.text()
        prefs['template'] = self.template_edit.text()
