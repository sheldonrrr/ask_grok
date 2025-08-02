#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging
import copy

# 初始化日志
logger = logging.getLogger(__name__)

def mask_api_key(api_key, visible_chars=4, mask_chars=8):
    """
    隐藏API Key的后8位字符，只保留前几位字符
    
    :param api_key: 原始API Key
    :param visible_chars: 保留可见的前几位字符数
    :param mask_chars: 需要掩码的字符数
    :return: 隐藏后的API Key
    """
    if not api_key or len(api_key) <= visible_chars:
        return api_key
    
    # 保留前visible_chars位，后面的替换为*号
    visible_part = api_key[:visible_chars]
    
    # 确定要掩码的部分长度
    mask_length = min(mask_chars, len(api_key) - visible_chars)
    
    # 构建掩码部分
    mask_part = '*' * mask_length
    
    # 如果API Key长度超过visible_chars + mask_chars，保留剩余部分
    remaining = ''
    if len(api_key) > visible_chars + mask_length:
        remaining = api_key[visible_chars + mask_length:]
    
    return visible_part + mask_part + remaining

def mask_api_key_in_text(text):
    """
    隐藏文本中的API Key
    
    :param text: 包含API Key的文本
    :return: 隐藏API Key后的文本
    """
    if not text:
        return text
    
    # 隐藏URL参数中的API Key
    text = re.sub(r'(key=|api_key=|token=|auth_token=)([A-Za-z0-9_-]{4})([A-Za-z0-9_-]{8})([A-Za-z0-9_-]*)', 
                 r'\1\2********\4', text)
    
    # 隐藏JSON中的API Key
    text = re.sub(r'("api_key"|"key"|"token"|"auth_token")\s*:\s*"([A-Za-z0-9_-]{4})([A-Za-z0-9_-]{8})([A-Za-z0-9_-]*)"', 
                 r'\1:"\\2********\4"', text)
    
    return text

def safe_log_config(config, keys_to_mask=None):
    """
    安全地记录配置信息，隐藏敏感信息
    
    :param config: 配置字典
    :param keys_to_mask: 需要掩码的键列表，默认为['api_key', 'key', 'token', 'auth_token']
    :return: 处理后的配置字典副本
    """
    if config is None:
        return None
    
    if keys_to_mask is None:
        keys_to_mask = ['api_key', 'key', 'token', 'auth_token']
    
    # 创建配置的深拷贝，避免修改原始配置
    safe_config = copy.deepcopy(config)
    
    # 遍历配置，掩码敏感信息
    for key, value in safe_config.items():
        if key in keys_to_mask and isinstance(value, str) and value:
            safe_config[key] = mask_api_key(value)
        elif isinstance(value, dict):
            safe_config[key] = safe_log_config(value, keys_to_mask)
    
    return safe_config
