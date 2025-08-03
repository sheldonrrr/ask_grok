#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simplified Chinese language translations for Ask Grok plugin.
"""

from ..models.base import BaseTranslation, TranslationRegistry, AIProvider


@TranslationRegistry.register
class SimplifiedChineseTranslation(BaseTranslation):
    """Simplified Chinese language translation."""
    
    @property
    def code(self) -> str:
        return "zh"
    
    @property
    def name(self) -> str:
        return "简体中文"
    
    @property
    def default_template(self) -> str:
        return '关于书籍 "{title}": 作者: {author}, 出版社: {publisher}, 出版年份: {pubyear}, 语言: {language}, 系列: {series}, 我的问题是: {query}'
    
    @property
    def suggestion_template(self) -> str:
        return '您是一位专业的书评人。对于{author}的书籍“{title}”，发布语言为{language}，请提出一个富有洞察力的问题，帮助读者更好地理解本书的核心思想、实际应用或独特视角。规则：1. 只返回问题，无需任何引言或解释；2. 关注书籍内容，而不仅仅是标题；3. 问题务实且发人深省；4. 保持简洁（30-200 字）；5. 发挥创意，即使是针对同一本书，每次都要提出不同的问题。'
    
    @property
    def translations(self) -> dict:
        return {
            # 插件信息
            'plugin_name': 'Ask Grok',
            'plugin_desc': '使用AI回答关于书籍的问题',
            
            # UI - 标签和区域
            'config_title': '配置',
            'general_tab': '常规',
            'ai_models': 'AI',
            'shortcuts': '快捷键',
            'about': '关于',
            'metadata': '元数据',
            
            # UI - 按钮和操作
            'ok_button': '确定',
            'save_button': '保存',
            'send_button': '发送',
            'suggest_button': '随机问题',
            'copy_response': '复制回答',
            'copy_question_response': '复制问答',
            'copied': '已复制！',
            'close_button': '关闭',
            
            # UI - 配置字段
            'token_label': 'API密钥:',
            'api_key_label': 'API密钥:',
            'model_label': '模型:',
            'language_label': '语言:',
            'language_label_old': '语言',
            'base_url_label': '基础URL:',
            'base_url_placeholder': '默认: {default_api_base_url}',
            'shortcut': '快捷键',
            'shortcut_open_dialog': '打开对话框',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': '模型',
            'current_ai': '当前AI:',
            'action': '操作',
            'reset_button': '重置',
            'prompt_template': '提示模板:',
            'ask_prompts': '提问提示:',
            'random_questions_prompts': '随机问题提示:',
            'display': '显示',
            
            # UI - 对话框元素
            'input_placeholder': '输入你的问题...',
            'response_placeholder': '回答即将到来...',
            
            # UI - 菜单项
            'menu_title': '提问',
            'menu_ask': '询问 {model}',
            
            # UI - 状态信息
            'loading': '加载中',
            'loading_text': '提问中',
            'save_success': '设置已保存',
            'sending': '发送中...',
            'requesting': '请求中',
            'formatting': '请求成功，正在格式化',
            
            # 元数据字段
            'metadata_title': '标题',
            'metadata_authors': '作者',
            'metadata_publisher': '出版社',
            'metadata_pubyear': '出版日期',
            'metadata_language': '语言',
            'metadata_series': '系列',
            'no_metadata': '无元数据',
            'no_series': '无系列',
            'unknown': '未知',
            
            # 错误信息
            'error': '错误: ',
            'network_error': '连接错误',
            'request_timeout': '请求超时',
            'request_failed': '请求失败',
            'question_too_long': '问题过长',
            'auth_token_required_title': '需要API密钥',
            'auth_token_required_message': '请在设置中设置API密钥',
            'error_preparing_request': '请求准备失败',
            'empty_suggestion': '空建议',
            'process_suggestion_error': '处理建议错误',
            'unknown_error': '未知错误',
            'unknown_model': '未知模型: {model_name}',
            'suggestion_error': '建议错误',
            'book_title_check': '需要书籍标题',
            'avoid_repeat_question': '请使用不同的问题',
            'empty_answer': '空回答',
            'invalid_response': '无效回应',
            'auth_error_401': '未授权',
            'auth_error_403': '访问被拒绝',
            'rate_limit': '请求过多',
            'invalid_json': '无效JSON',
            'no_response': '无回应',
            'template_error': '模板错误',
            'no_model_configured': '未配置AI模型。请在设置中配置AI模型。',
            'random_question_error': '生成随机问题时出错',
            'clear_history_failed': '清除历史失败',
            'clear_history_not_supported': '暂不支持清除单本书的历史',
            
            # 关于信息
            'author_name': 'Sheldon',
            'user_manual': '用户手册',
            'learn_how_to_use': '观看教程视频',
            'email': 'iMessage',
            'about_plugin': '关于 Ask Grok',
            
            # 模型特定配置
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': '自定义',
        }
