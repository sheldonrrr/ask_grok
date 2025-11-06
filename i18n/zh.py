#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simplified Chinese language translations for Ask AI Plugin.
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
        return '您是一位专业的书评人。对于{author}的书籍"{title}"，发布语言为{language}，请提出一个富有洞察力的问题，帮助读者更好地理解本书的核心思想、实际应用或独特视角。规则：1. 只返回问题，无需任何引言或解释；2. 关注书籍内容，而不仅仅是标题；3. 问题务实且发人深省；4. 保持简洁（30-200 字）；5. 发挥创意，即使是针对同一本书，每次都要提出不同的问题。'
    
    @property
    def multi_book_default_template(self) -> str:
        return """以下是关于多本书籍的信息：{books_metadata} 用户问题：{query} 请基于以上书籍信息回答问题。"""
    
    @property
    def translations(self) -> dict:
        return {
            # 插件信息
            'plugin_name': 'Ask AI Plugin',
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
            'stop_button': '停止',
            'suggest_button': '随机问题',
            'copy_response': '复制回答',
            'copy_question_response': '复制问答',
            'export_pdf': '导出PDF',
            'export_current_qa': '导出当前问答',
            'export_history': '导出历史',
            'export_all_history_dialog_title': '导出全部历史记录为PDF',
            'export_all_history_title': '全部问答历史记录',
            'export_history_insufficient': '需要至少2条历史记录才能导出。',
            'history_record': '记录',
            'question_label': '问题',
            'answer_label': '回答',
            'default_ai': '默认AI',
            'export_time': '导出时间',
            'total_records': '总记录数',
            'info': '信息',
            'yes': '是',
            'no': '否',
            'no_book_selected_title': '未选择书籍',
            'no_book_selected_message': '请先选择一本书后再进行提问。',
            'set_default_ai_title': '设置默认AI',
            'set_default_ai_message': '您已切换到"{0}"。是否将其设为默认AI以用于未来的查询？',
            'set_default_ai_success': '默认AI已设置为"{0}"。',
            'copied': '已复制！',
            'pdf_exported': 'PDF已导出！',
            'export_pdf_dialog_title': '导出为PDF',
            'export_pdf_error': '导出PDF失败：{0}',
            'no_question': '无问题',
            'no_response': '无回答',
            'saved': '已保存',
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
            'current_ai': '当前AI',
            'action': '操作',
            'reset_button': '重置',
            'reset_current_ai': '重置当前AI为默认值',
            'reset_ai_confirm_title': '确认重置',
            'reset_ai_confirm_message': '即将重置 {ai_name} 到默认状态。\n\n此操作将清空：\n• API Key\n• 自定义模型名称\n• 其他已配置的参数\n\n是否继续？',
            'reset_tooltip': '重置当前AI到默认值',
            'unsaved_changes_title': '未保存的更改',
            'unsaved_changes_message': '您有未保存的更改。您想要：',
            'save_and_close': '保存并关闭',
            'discard_changes': '不保存',
            'cancel': '取消',
            'prompt_template': '提示词模板',
            'ask_prompts': '提问提示词',
            'random_questions_prompts': '随机问题提示词',
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
            
            # UI - 模型列表功能
            'load_models': '加载模型',
            'use_custom_model': '使用自定义模型名称',
            'custom_model_placeholder': '输入自定义模型名称',
            'model_placeholder': '请先加载模型',
            'models_loaded': '成功加载 {count} 个模型',
            'load_models_failed': '加载模型失败：{error}',
            'model_list_not_supported': '此提供商不支持自动获取模型列表',
            'api_key_required': '请先输入 API Key',
            'invalid_params': '无效的参数',
            'warning': '警告',
            'success': '成功',
            'error': '错误',
            
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
            
            # 多书功能
            'books_unit': '本书',
            'new_conversation': '新对话',
            'single_book': '单书',
            'multi_book': '多书',
            'deleted': '已删除',
            'history': '历史记录',
            'no_history': '暂无历史记录',
            'clear_current_book_history': '清空当前书籍历史记录',
            'confirm_clear_book_history': '确定要清空以下书籍的所有历史记录吗？\n{book_titles}',
            'confirm': '确认',
            'success': '成功',
            'history_cleared': '已清空 {deleted_count} 条历史记录。',
            'multi_book_template_label': '多书提示词模板:',
            'multi_book_placeholder_hint': '使用 {books_metadata} 表示书籍信息，{query} 表示用户问题',
            
            # 错误消息（注意：'error' 已在前面定义，这里是其他错误类型）
            'network_error': '连接错误',
            'request_timeout': '请求超时',
            'request_failed': '请求失败',
            'question_too_long': '问题过长',
            'auth_token_required_title': '需要AI服务',
            'auth_token_required_message': '请在插件配置中设置有效的AI服务。',
            'open_configuration': '打开配置',
            'cancel': '取消',
            'error_preparing_request': '请求准备失败',
            'empty_suggestion': '空建议',
            'process_suggestion_error': '处理建议错误',
            'unknown_error': '未知错误',
            'unknown_model': '未知模型: {model_name}',
            'suggestion_error': '建议错误',
            'random_question_success': '随机问题生成成功！',
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
            'no_ai_configured_title': '未配置AI',
            'no_ai_configured_message': '欢迎使用！要开始对书籍提问，您需要先配置一个AI提供商。\n\n推荐新手选择：\n• Nvidia AI - 只需手机号即可获取半年免费API访问权限（无需绑定信用卡）\n• Ollama - 在您的电脑上本地运行AI模型（完全免费且隐私）\n\n是否现在打开插件配置来设置AI提供商？',
            'open_settings': '插件配置',
            'ask_anyway': '仍要询问',
            'later': '稍后',
            'reset_all_data': '重置所有数据',
            'reset_all_data_warning': '这将会删除所有API密钥、提示词模板和本地历史记录。您的语言偏好将被保留。请慎重操作。',
            'reset_all_data_confirm_title': '确认重置',
            'reset_all_data_confirm_message': '您确定要将插件重置为初始状态吗？\n\n这将永久删除：\n• 所有API密钥\n• 所有自定义提示词模板\n• 所有对话历史记录\n• 所有插件设置（会保留当前选中的语言配置信息）\n\n此操作无法撤销！',
            'reset_all_data_success': '所有插件数据已成功重置。请重启calibre以使更改生效。',
            'reset_all_data_failed': '重置插件数据失败：{error}',
            'random_question_error': '生成随机问题时出错',
            'clear_history_failed': '清除历史失败',
            'clear_history_not_supported': '暂不支持清除单本书的历史',
            'missing_required_config': '缺少必要的配置：{key}。请检查您的设置。',
            'api_key_too_short': 'API密钥太短。请检查并输入完整的密钥。',
            
            # API响应处理
            'api_request_failed': 'API请求失败：{error}',
            'api_content_extraction_failed': '无法从 API 响应中提取内容',
            'api_invalid_response': '无法获取有效的API响应',
            'api_unknown_error': '未知错误：{error}',
            
            # 流式响应处理
            'stream_response_code': '流式响应状态码：{code}',
            'stream_continue_prompt': '请继续您的上一个回答，不要重复已提供的内容。',
            'stream_continue_code_blocks': '您的上一个回答有未关闭的代码块。请继续并完成这些代码块。',
            'stream_continue_parentheses': '您的上一个回答有未关闭的括号。请继续并确保所有括号正确关闭。',
            'stream_continue_interrupted': '您的上一个回答似乎被中断了。请继续完成您的最后一个想法或解释。',
            'stream_timeout_error': '流式传输60秒没有收到新内容，可能是连接问题。',
            
            # API错误消息
            'api_version_model_error': 'API版本或模型名称错误：{message}\n\n请在设置中将API基础URL更新为"{base_url}"，并将模型更新为"{model}"或其他可用模型。',
            'api_format_error': 'API请求格式错误：{message}',
            'api_key_invalid': 'API密钥无效或未授权：{message}\n\n请检查您的API密钥并确保已启用API访问。',
            'api_rate_limit': '请求频率超限，请稍后再试\n\n您可能已超过免费使用配额。这可能是由于：\n1. 每分钟请求过多\n2. 每天请求过多\n3. 每分钟输入令牌过多',
            
            # 配置错误
            'missing_config_key': '缺少必要的配置键：{key}',
            'api_base_url_required': '需要API基础URL',
            'model_name_required': '需要模型名称',
            'api_key_empty': 'API密钥为空。请输入有效的API密钥。',
            
            # 模型列表获取
            'fetching_models_from': '正在从 {url} 获取模型',
            'successfully_fetched_models': '成功获取 {count} 个 {provider} 模型',
            'failed_to_fetch_models': '加载模型失败：{error}',
            
            # 模型获取错误信息
            'error_401': 'API Key 验证失败。请检查：API Key 是否正确、账户余额是否充足、API Key 是否已过期。',
            'error_403': '访问被拒绝。请检查：API Key 权限是否足够、是否有地区访问限制。',
            'error_404': 'API 端点不存在。请检查 API Base URL 配置是否正确。',
            'error_429': '请求过于频繁，已达到速率限制。请稍后重试。',
            'error_5xx': '服务器错误。请稍后重试，或检查服务提供商状态。',
            'error_network': '网络连接失败。请检查网络连接、代理设置或防火墙配置。',
            'error_unknown': '未知错误。',
            'technical_details': '技术细节',
            
            # 关于信息
            'author_name': 'Sheldon',
            'user_manual': '用户手册',
            'about_plugin': '关于 Ask AI Plugin',
            'learn_how_to_use': '观看教程视频',
            'email': 'iMessage',
            
            # 模型特定配置
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': '自定义',
            'model_enable_streaming': '启用流式传输',
            
            # AI Switcher
            'current_ai': '当前AI',
            'no_configured_models': '未配置 AI - 请在设置中配置', # 补充缺失
            
            # 提供商特定信息
            'nvidia_free_info': '💡 新用户可获得 6 个月免费 API 访问权限 - 无需信用卡', # 补充缺失的图标和完整信息
            
            # 通用系统消息
            'default_system_message': '您是一位书籍分析专家。您的任务是通过提供有洞察力的问题和分析，帮助用户更好地理解书籍。',
            
            # 请求超时设置
            'request_timeout_label': '请求超时时间：',
            'seconds': '秒',
            'request_timeout_error': '请求超时，当前超时时间为：{timeout} 秒',
            
            # 并行AI设置
            'parallel_ai_count_label': '并行AI数量：',
            'parallel_ai_count_tooltip': '同时请求的AI数量（1-2可用，3-4即将推出）', # 修正tooltip
            'parallel_ai_notice': '注意：这仅影响发送问题。随机问题始终使用单个AI。', # 修正notice
            'suggest_maximize': '提示：使用3个AI时建议最大化窗口以获得更好的显示效果', # 修正
            'ai_panel_label': 'AI {index}：',
            'no_ai_available': '此面板没有可用的AI',
            'add_more_ai_providers': '请添加更多AI服务商',
            'select_ai': '-- 选择AI --',
            'select_model': '-- 切换Model --',
            'request_model_list': '请请求模型列表',
            'coming_soon': '即将推出',
            'advanced_feature_tooltip': '此功能正在开发中，敬请期待！',
            
            # PDF导出章节标题
            'pdf_book_metadata': '书籍元数据',
            'pdf_question': '问题',
            'pdf_answer': '回答',
            'pdf_ai_model_info': 'AI模型信息',
            'pdf_generated_by': '生成信息', # 修正
            'pdf_provider': '提供商',
            'pdf_model': '模型',
            'pdf_api_base_url': 'API基础URL',
            'pdf_panel': '面板',
            'pdf_plugin': '插件',
            'pdf_github': 'GitHub',
            'pdf_software': '软件',
            'pdf_generated_time': '生成时间',
            'pdf_info_not_available': '信息不可用',
        }