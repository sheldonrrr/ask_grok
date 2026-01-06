#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
设备指纹和用户 UUID 管理模块

用于生成和管理设备唯一标识，用于免费 API 通道的用户识别和限流。
"""

import hashlib
import uuid
import platform
import locale
import json
from typing import Dict, Any
from calibre.utils.config import JSONConfig


class DeviceFingerprint:
    """设备指纹管理类"""
    
    @staticmethod
    def get_or_create_user_uuid() -> str:
        """
        获取或创建用户 UUID
        
        如果用户 UUID 不存在，则生成一个新的 UUID 并保存到配置中。
        
        :return: 用户 UUID 字符串
        """
        prefs = JSONConfig('plugins/ask_ai_plugin')
        user_uuid = prefs.get('user_uuid', '')
        
        if not user_uuid:
            # 生成新的 UUID
            user_uuid = str(uuid.uuid4())
            prefs['user_uuid'] = user_uuid
            
        return user_uuid
    
    @staticmethod
    def get_device_info() -> Dict[str, Any]:
        """
        获取设备信息
        
        :return: 包含设备信息的字典
        """
        try:
            # 获取系统信息
            system_info = {
                'system': platform.system(),           # 操作系统名称 (Windows, Linux, Darwin)
                'release': platform.release(),         # 系统版本
                'machine': platform.machine(),         # 机器类型 (x86_64, arm64, etc.)
                'processor': platform.processor(),     # 处理器信息
            }
            
            # 获取语言设置
            try:
                lang_code, encoding = locale.getdefaultlocale()
                system_info['locale'] = lang_code or 'en_US'
                system_info['encoding'] = encoding or 'UTF-8'
            except:
                system_info['locale'] = 'en_US'
                system_info['encoding'] = 'UTF-8'
            
            # 获取 Python 版本
            system_info['python_version'] = platform.python_version()
            
            return system_info
            
        except Exception as e:
            # 如果获取失败，返回基本信息
            return {
                'system': 'unknown',
                'locale': 'en_US',
                'error': str(e)
            }
    
    @staticmethod
    def generate_device_fingerprint() -> str:
        """
        生成设备指纹
        
        基于设备的硬件和系统信息生成唯一的设备指纹。
        
        :return: 设备指纹字符串 (MD5 hash)
        """
        try:
            # 获取机器 MAC 地址（最稳定的硬件标识）
            mac_address = str(uuid.getnode())
            
            # 获取系统信息
            device_info = DeviceFingerprint.get_device_info()
            
            # 组合信息生成指纹
            fingerprint_data = {
                'mac': mac_address,
                'system': device_info.get('system', ''),
                'machine': device_info.get('machine', ''),
            }
            
            # 生成 MD5 hash
            fingerprint_str = json.dumps(fingerprint_data, sort_keys=True)
            fingerprint_hash = hashlib.md5(fingerprint_str.encode()).hexdigest()
            
            return fingerprint_hash
            
        except Exception as e:
            # 如果生成失败，使用随机 UUID
            return hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()
    
    @staticmethod
    def get_client_metadata() -> Dict[str, Any]:
        """
        获取完整的客户端元数据
        
        包含用户 UUID、设备指纹和设备信息，用于发送到服务器。
        
        :return: 客户端元数据字典
        """
        return {
            'user_uuid': DeviceFingerprint.get_or_create_user_uuid(),
            'device_fingerprint': DeviceFingerprint.generate_device_fingerprint(),
            'device_info': DeviceFingerprint.get_device_info(),
            'plugin_version': DeviceFingerprint._get_plugin_version()
        }
    
    @staticmethod
    def _get_plugin_version() -> str:
        """
        获取插件版本号
        
        :return: 版本号字符串
        """
        try:
            from .version import __version__
            return __version__
        except:
            return 'unknown'
