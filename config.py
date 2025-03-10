#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                           QLineEdit, QPushButton)

from calibre.utils.config import JSONConfig

# 全局配置对象
prefs = JSONConfig('plugins/ask_gpt')

# 加载环境变量
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

# 默认配置
prefs.defaults['api_key'] = os.getenv('API_KEY')
prefs.defaults['template'] = '关于{title}这本书，{query}'

def get_prefs():
    """获取插件配置"""
    return prefs

class ConfigWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # OpenAI API Key 配置
        key_label = QLabel('OpenAI API Key:')
        self.layout.addWidget(key_label)
        
        self.api_key_edit = QLineEdit(self)
        self.api_key_edit.setText(prefs['api_key'])
        self.layout.addWidget(self.api_key_edit)
        
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
        prefs['template'] = self.template_edit.text()
