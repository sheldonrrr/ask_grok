#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Traditional Chinese language translations for Ask AI Plugin.
"""

from ..models.base import BaseTranslation, TranslationRegistry, AIProvider


@TranslationRegistry.register
class TraditionalChineseTranslation(BaseTranslation):
    """Traditional Chinese language translation."""
    
    @property
    def code(self) -> str:
        return "zht"
    
    @property
    def name(self) -> str:
        return "繁體中文"
    
    @property
    def default_template(self) -> str:
        return '關於書籍 "{title}": 作者: {author}, 出版社: {publisher}, 出版年份: {pubyear}, 語言: {language}, 系列: {series}, 我的問題是: {query}'
    
    @property
    def suggestion_template(self) -> str:
        return """您是一位專業的書評家。對於「{title}」這本由{author}所寫的書，出版語言為{language}，請生成一個有見地的問題，幫助讀者更好地理解這本書的核心思想、實踐應用或獨特觀點。規則：1. 只返回問題本身，不需要任何介紹或解釋 2. 將焦點放在書的內容上，而不僅僅是標題 3. 使問題具有實用性和啟發性 4. 保持精簡（30-200字） 5. 請發揮創意，即使是同一本書，每次也要生成不同的問題"""
    
    @property
    def multi_book_default_template(self) -> str:
        return """以下是關於多本書籍的資訊：{books_metadata} 用戶問題：{query} 請基於以上書籍資訊回答問題。"""
    
    @property
    def translations(self) -> dict:
        return {
        # 插件信息
        'plugin_name': 'Ask AI Plugin',
        'plugin_desc': '使用AI提問關於書籍的問題',
        
        # UI - 標籤和區域
        'config_title': '設定',
        'general_tab': '一般',
        'ai_models': '人工智能',
        'shortcuts': '快捷鍵',
        'about': '關於',
        'metadata': '元數據',
        
        # UI - 按鈕和操作
        'ok_button': '確定',
        'save_button': '儲存',
        'send_button': '發送',
        'stop_button': '停止',
        'suggest_button': '隨機問題',
        'copy_response': '複製回答',
        'copy_question_response': '複製問答',
        'export_pdf': '匯出PDF',
        'export_current_qa': '匯出當前問答',
        'export_history': '匯出歷史',
        'export_all_history_dialog_title': '匯出全部歷史記錄為PDF',
        'export_all_history_title': '全部問答歷史記錄',
        'export_history_insufficient': '需要至少2條歷史記錄才能匯出。',
        'history_record': '記錄',
        'question_label': '問題',
        'answer_label': '回答',
        'default_ai': '預設AI',
        'export_time': '匯出時間',
        'total_records': '總記錄數',
        'info': '資訊',
        'copied': '已複製！',
        'pdf_exported': 'PDF已匯出！',
        'export_pdf_dialog_title': '匯出為PDF',
        'export_pdf_error': '匯出PDF失敗：{0}',
        'no_question': '無問題',
        'no_response': '無回答',
        'saved': '已儲存',
        'close_button': '關閉',
        
        # UI - 設定欄位
        'token_label': 'API金鑰:',
        'api_key_label': 'API金鑰:',
        'model_label': '模型:',
        'language_label': '語言:',
        'language_label_old': '語言',
        'base_url_label': '基礎URL:',
        'base_url_placeholder': '預設: {default_api_base_url}',
        'shortcut': '快捷鍵',
        'shortcut_open_dialog': '開啟對話框',
        'shortcut_enter': 'Ctrl + Enter',
        'shortcut_return': 'Command + Return',
        'using_model': '模型',
        'current_ai': '目前AI:',
        'action': '操作',
        'reset_button': '重置',
        'prompt_template': '提示詞模板:',
        'ask_prompts': '提問提示詞:',
        'random_questions_prompts': '隨機問題提示詞:',
        'display': '顯示',
        
        # UI - 對話框元素
        'input_placeholder': '輸入你的問題...',
        'response_placeholder': '回答即將到來...',
        
        # UI - 選單項目
        'menu_title': '提問',
        'menu_ask': '詢問 {model}',
        
        # UI - 狀態消息
        'loading': '載入中',
        'loading_text': '正在提問',
        'save_success': '設定已儲存',
        'sending': '發送中...',
        'requesting': '請求中',
        'formatting': '請求成功，格式化中',
        
        # UI - 模型列表功能
        'load_models': '載入模型',
        'use_custom_model': '使用自訂模型名稱',
        'custom_model_placeholder': '輸入自訂模型名稱',
        'model_placeholder': '請先載入模型',
        'models_loaded': '成功載入 {count} 個模型',
        'load_models_failed': '載入模型失敗：{error}',
        'model_list_not_supported': '此提供商不支援自動獲取模型列表',
        'api_key_required': '請先輸入 API Key',
        'invalid_params': '無效的參數',
        'warning': '警告',
        'success': '成功',
        'error': '錯誤',
        
        # 元數據欄位
        'metadata_title': '標題',
        'metadata_authors': '作者',
        'metadata_publisher': '出版社',
        'metadata_pubyear': '出版日期',
        'metadata_language': '語言',
        'metadata_series': '系列',
        'no_metadata': '無元數據',
        'no_series': '無系列',
        'unknown': '未知',
        
        # 多書功能
        'books_unit': '本書',
        'new_conversation': '新對話',
        'single_book': '單書',
        'multi_book': '多書',
        'deleted': '已刪除',
        'history': '歷史記錄',
        'no_history': '暫無歷史記錄',
        'clear_current_book_history': '清空當前書籍歷史記錄',
        'confirm_clear_book_history': '確定要清空以下書籍的所有歷史記錄嗎？\n{book_titles}',
        'confirm': '確認',
        'history_cleared': '已清空 {deleted_count} 條歷史記錄。',
        'multi_book_template_label': '多書提示詞模板:',
        'multi_book_placeholder_hint': '使用 {books_metadata} 表示書籍資訊，{query} 表示用戶問題',
        
        # 錯誤信息
        'error': '錯誤: ',
        'network_error': '連線錯誤',
        'request_timeout': '請求超時',
        'request_failed': '請求失敗',
        'question_too_long': '問題過長',
        'auth_token_required_title': '需要API金鑰',
        'auth_token_required_message': '請在插件配置中設定API金鑰。',
        'error_preparing_request': '請求準備失敗',
        'empty_suggestion': '空建議',
        'process_suggestion_error': '處理建議錯誤',
        'unknown_error': '未知錯誤',
        'unknown_model': '未知模型: {model_name}',
        'suggestion_error': '建議錯誤',
        'random_question_success': '隨機問題生成成功！',
        'book_title_check': '需要書籍標題',
        'avoid_repeat_question': '請使用不同的問題',
        'empty_answer': '空回答',
        'invalid_response': '無效回應',
        'auth_error_401': '未授權',
        'auth_error_403': '訪問被拒絕',
        'rate_limit': '請求過多',
        'invalid_json': '無效JSON',
        'no_response': '無回應',
        'template_error': '模板錯誤',
        'no_model_configured': '未配置AI模型。請在設定中配置AI模型。',
        'random_question_error': '生成隨機問題時出錯',
        'clear_history_failed': '清除歷史失敗',
        'clear_history_not_supported': '暫不支援清除單本書的歷史記錄',
        'missing_required_config': '缺少必要的配置：{key}。請檢查您的設定。',
        'api_key_too_short': 'API金鑰太短。請檢查並輸入完整的金鑰。',
        
        # API響應處理
        'api_request_failed': 'API請求失敗：{error}',
        'api_content_extraction_failed': '無法從 API 響應中提取內容',
        'api_invalid_response': '無法獲取有效的API響應',
        'api_unknown_error': '未知錯誤：{error}',
        
        # 流式響應處理
        'stream_response_code': '流式響應狀態碼：{code}',
        'stream_continue_prompt': '請繼續您的上一個回答，不要重複已提供的內容。',
        'stream_continue_code_blocks': '您的上一個回答有未關閉的程式碼塊。請繼續並完成這些程式碼塊。',
        'stream_continue_parentheses': '您的上一個回答有未關閉的括號。請繼續並確保所有括號正確關閉。',
        'stream_continue_interrupted': '您的上一個回答似乎被中斷了。請繼續完成您的最後一個想法或解釋。',
        'stream_timeout_error': '流式傳輸60秒沒有收到新內容，可能是連線問題。',
        
        # API錯誤消息
        'api_version_model_error': 'API版本或模型名稱錯誤：{message}\n\n請在設定中將API基礎URL更新為"{base_url}"，並將模型更新為"{model}"或其他可用模型。',
        'api_format_error': 'API請求格式錯誤：{message}',
        'api_key_invalid': 'API金鑰無效或未授權：{message}\n\n請檢查您的API金鑰並確保已啟用API訪問。',
        'api_rate_limit': '請求頻率超限，請稍後再試\n\n您可能已超過免費使用配額。這可能是由於：\n1. 每分鐘請求過多\n2. 每天請求過多\n3. 每分鐘輸入令牌過多',
        
        # 配置錯誤
        'missing_config_key': '缺少必要的配置鍵：{key}',
        'api_base_url_required': '需要API基礎URL',
        'model_name_required': '需要模型名稱',
        'api_key_empty': 'API金鑰為空。請輸入有效的API金鑰。',
        
        # 模型列表獲取
        'fetching_models_from': '正在從 {url} 獲取模型',
        'successfully_fetched_models': '成功獲取 {count} 個 {provider} 模型',
        'failed_to_fetch_models': '獲取模型失敗：{error}',
        
        # 關於信息
        'author_name': 'Sheldon',
        'user_manual': '用戶手冊',
        'about_plugin': '為何使用 Ask AI Plugin？',
        'learn_how_to_use': '如何使用',
        'email': 'iMessage',
        
        # 模型特定配置
        'model_display_name_grok': 'Grok(x.AI)',
        'model_display_name_gemini': 'Gemini(Google)',
        'model_display_name_deepseek': 'Deepseek',
        'model_display_name_custom': '自定義',
        'model_enable_streaming': '啟用流式傳輸',
        'model_disable_ssl_verify': '禁用SSL驗證',
        
        # AI Switcher
        'current_ai': '目前AI',
        'no_configured_models': '未配置AI - 請在設定中配置',
        
        # 提供商特定信息
        'nvidia_free_info': '💡 新用戶可獲得 6 個月免費 API 訪問權限 - 無需信用卡',
        
        # 通用系統消息
        'default_system_message': '您是一位書籍分析專家。您的任務是透過提供有見地的問題和分析，幫助用戶更好地理解書籍。',
        
        # 請求超時設置
        'request_timeout_label': '請求超時時間：',
        'seconds': '秒',
        'request_timeout_error': '請求超時，當前超時時間為：{timeout} 秒',
        
        # 並行AI設置
        'parallel_ai_count_label': '並行AI數量：',
        'parallel_ai_count_tooltip': '同時查詢的AI數量 (1-2可用，3-4即將推出)',
        'parallel_ai_notice': '注意：這只會影響發送問題。隨機問題始終使用單個AI。',
        'suggest_maximize': '提示：使用3個AI時建議最大化視窗以獲得更好的顯示效果',
        'ai_panel_label': 'AI {index}：',
        'no_ai_available': '此面板沒有可用的AI',
        'add_more_ai_providers': '請在設定中添加更多AI服務商',
        'select_ai': '-- 選擇AI --',
        'coming_soon': '即將推出',
        'advanced_feature_tooltip': '此功能正在開發中，敬請期待！',
        
        # PDF導出章節標題
        'pdf_book_metadata': '書籍元數據',
        'pdf_question': '問題',
        'pdf_answer': '回答',
        'pdf_ai_model_info': 'AI模型資訊',
        'pdf_generated_by': '由...生成',
        'pdf_provider': '提供商',
        'pdf_model': '模型',
        'pdf_api_base_url': 'API 基礎URL',
        'pdf_panel': '面板',
        'pdf_plugin': '插件',
        'pdf_github': 'GitHub',
        'pdf_software': '軟體',
        'pdf_generated_time': '生成時間',
        'pdf_info_not_available': '資訊不可用',
    }