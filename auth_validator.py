#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
统一的 Auth Token 验证模块

集中处理所有 AI 模型的 auth token 验证逻辑，避免代码分散在多处。
"""

import logging
from typing import List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


def validate_models_auth(model_ids: List[str], show_dialog_callback=None) -> Tuple[bool, Optional[str]]:
    """
    统一验证多个模型的 auth token
    
    这是整个插件中唯一的 auth token 验证入口点。
    所有需要验证 auth token 的地方都应该调用这个函数。
    
    Args:
        model_ids: 需要验证的模型ID列表（如 ['grok', 'ollama', 'openai_xxxxx']）
        show_dialog_callback: 可选的回调函数，用于显示错误对话框
        
    Returns:
        Tuple[bool, Optional[str]]: (是否通过验证, 错误消息)
            - (True, None): 所有模型都通过验证
            - (False, error_msg): 验证失败，返回错误消息
    """
    from calibre_plugins.ask_ai_plugin.config import get_prefs
    from calibre_plugins.ask_ai_plugin.models import AIModelFactory
    
    if not model_ids:
        logger.warning("validate_models_auth: 没有提供模型ID")
        return True, None
    
    prefs = get_prefs()
    models_config = prefs.get('models', {})
    
    # 去重
    models_to_check = set(model_ids)
    logger.info(f"开始验证 {len(models_to_check)} 个模型的 auth token: {models_to_check}")
    
    # 检查每个模型
    for selected_model in models_to_check:
        model_config = models_config.get(selected_model, {})
        
        if not model_config:
            logger.warning(f"模型 {selected_model} 没有配置信息")
            continue
        
        try:
            # 从 selected_model 中提取 provider_id（取第一个下划线之前的部分）
            provider_id = model_config.get('provider_id')
            if not provider_id:
                provider_id = selected_model.split('_')[0] if '_' in selected_model else selected_model
            
            # 创建临时模型实例来检查是否需要 auth token
            temp_model = AIModelFactory.create_model(provider_id, model_config)
            
            # 使用工厂函数判断模型是否需要 auth token
            if not temp_model.requires_auth_token():
                logger.info(f"模型 {selected_model} 不需要 auth token，跳过验证")
                continue
            
            # 需要 auth token 的模型，检查是否已配置
            # 根据 provider_id 判断使用哪个字段（Grok 使用 auth_token，其他使用 api_key）
            token_field = 'auth_token' if provider_id == 'grok' else 'api_key'
            token = model_config.get(token_field, '')
            
            if not token or not token.strip():
                error_msg = f"模型 {selected_model} 需要配置 API Key"
                logger.error(error_msg)
                
                # 如果提供了对话框回调，调用它
                if show_dialog_callback:
                    show_dialog_callback()
                
                return False, error_msg
            
            logger.info(f"模型 {selected_model} auth token 验证通过")
            
        except Exception as e:
            logger.warning(f"验证模型 {selected_model} 时出错: {str(e)}，使用后备逻辑")
            
            # 后备逻辑：使用 provider_id 判断是否需要 token
            # Ollama 和 Custom 模型不需要 API Key
            if provider_id in ['ollama', 'custom']:
                logger.info(f"模型 {selected_model} (provider: {provider_id}) 使用后备逻辑，不需要 auth token")
                continue
            
            # 其他模型检查 token（根据 provider_id 判断字段名）
            token_field = 'auth_token' if provider_id == 'grok' else 'api_key'
            token = model_config.get(token_field, '')
            
            if not token or not token.strip():
                error_msg = f"模型 {selected_model} 需要配置 API Key"
                logger.error(error_msg)
                
                if show_dialog_callback:
                    show_dialog_callback()
                
                return False, error_msg
    
    logger.info(f"所有模型 auth token 验证通过: {models_to_check}")
    return True, None


def get_models_to_validate(response_panels=None, default_model_id: Optional[str] = None) -> List[str]:
    """
    获取需要验证的模型ID列表
    
    根据不同的场景（单面板、多面板、随机问题等）收集需要验证的模型。
    
    Args:
        response_panels: 响应面板列表（并行AI模式）
        default_model_id: 默认模型ID（单面板模式或随机问题模式）
        
    Returns:
        List[str]: 需要验证的模型ID列表
    """
    from calibre_plugins.ask_ai_plugin.config import get_prefs
    
    models_to_check = []
    
    # 场景1: 并行AI模式 - 检查所有面板选中的 AI
    if response_panels:
        logger.info(f"并行AI模式: 检查 {len(response_panels)} 个面板")
        for panel in response_panels:
            selected_ai = panel.get_selected_ai()
            if selected_ai:
                models_to_check.append(selected_ai)
                logger.debug(f"面板 {panel.panel_index} 选中的AI: {selected_ai}")
    
    # 场景2: 指定了默认模型ID（随机问题或单面板模式）
    if default_model_id:
        logger.info(f"使用指定的模型ID: {default_model_id}")
        models_to_check.append(default_model_id)
    
    # 场景3: 如果没有收集到任何模型，使用全局默认AI
    if not models_to_check:
        prefs = get_prefs()
        default_ai = prefs.get('selected_model', 'grok')
        logger.info(f"使用全局默认AI: {default_ai}")
        models_to_check.append(default_ai)
    
    # 去重并返回
    unique_models = list(set(models_to_check))
    logger.info(f"需要验证的模型: {unique_models}")
    return unique_models


def validate_single_model(model_id: str, show_dialog_callback=None) -> Tuple[bool, Optional[str]]:
    """
    验证单个模型的 auth token（便捷函数）
    
    Args:
        model_id: 模型ID
        show_dialog_callback: 可选的回调函数，用于显示错误对话框
        
    Returns:
        Tuple[bool, Optional[str]]: (是否通过验证, 错误消息)
    """
    return validate_models_auth([model_id], show_dialog_callback)
