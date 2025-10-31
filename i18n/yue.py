#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Cantonese language translations for Ask AI Plugin.
"""

from ..models.base import BaseTranslation, TranslationRegistry, AIProvider


@TranslationRegistry.register
class CantoneseTranslation(BaseTranslation):
    """Cantonese language translation."""
    
    @property
    def code(self) -> str:
        return "yue"
    
    @property
    def name(self) -> str:
        return "粵語"
    
    @property
    def default_template(self) -> str:
        return '關於本書 "{title}": 作者: {author}, 出版社: {publisher}, 出版年份: {pubyear}, 語言: {language}, 系列: {series}, 我嘅問題係: {query}'
    
    @property
    def suggestion_template(self) -> str:
        return """你係一個專業嘅書評家。對於「{title}」這本由{author}寫嘅書，出版語言係{language}，生成一個有見地嘅問題，幫助讀者更加理解這本書嘅核心思想、實踐應用或者獨特觀點。規則：1. 只返回問題本身，唔使介紹或解釋 2. 將焦點放在書嘅內容上，唔係標題 3. 令問題具有實用性同啟發性 4. 保持精簡（30-200字） 5. 發揮創意，就算係同一本書，每次都要生成唔同嘅問題"""
    
    @property
    def multi_book_default_template(self) -> str:
        return """以下係關於多本書嘅信息：{books_metadata} 用戶問題：{query} 請基於以上書籍信息回答問題。"""
    
    @property
    def translations(self) -> dict:
        return {
            # 插件信息
            'plugin_name': 'Ask AI Plugin',
            'plugin_desc': '用AI問書嘅問題',
            
            # UI - 標籤同區域
            'config_title': '設定',
            'general_tab': '一般',
            'ai_models': '人工智能',
            'shortcuts': '快捷鍵',
            'about': '關於',
            'metadata': '元數據',
            
            # UI - 按鈕同操作
            'ok_button': '確定',
            'save_button': '儲存',
            'send_button': '發送',
            'stop_button': '停止',
            'suggest_button': '隨機問題',
            'copy_response': '複製回答',
            'copy_question_response': '複製問答',
            'export_pdf': '導出 PDF',
            'export_current_qa': '導出當前問答',
            'export_history': '導出歷史',
            'export_all_history_dialog_title': '導出全部歷史記錄為PDF',
            'export_all_history_title': '全部問答歷史記錄',
            'export_history_insufficient': '需要至少兩條歷史記錄先可以導出。',
            'history_record': '記錄',
            'question_label': '問題',
            'answer_label': '回答',
            'default_ai': '預設AI',
            'export_time': '導出時間',
            'total_records': '總記錄數',
            'info': '資訊',
            'copied': '已複製！',
            'pdf_exported': 'PDF 已導出！',
            'export_pdf_dialog_title': '導出為 PDF',
            'export_pdf_error': 'PDF 導出錯誤：{0}',
            'no_question': '冇問題',
            'no_response': '冇回應',
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
            'shortcut_open_dialog': '開對話框',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': '模型',
            'action': '操作',
            'reset_button': '重置',
            'prompt_template': '提示模板',
            'ask_prompts': '問題提示',
            'random_questions_prompts': '隨機問題提示',
            'display': '顯示',
            
            # UI - 對話框元素
            'input_placeholder': '輸入你嘅問題...',
            'response_placeholder': '回答即將到來...',
            
            # UI - 選單項目
            'menu_title': '問問題',
            'menu_ask': '問 {model}',
            
            # UI - 狀態消息
            'loading': '載入緊',
            'loading_text': '問緊問題',
            'save_success': '設定已儲存',
            'sending': '發送緊...',
            'requesting': '請求緊',
            'formatting': '請求成功，格式化緊',
            
            # UI - 模型列表功能
            'load_models': '載入模型',
            'use_custom_model': '使用自訂模型名',
            'custom_model_placeholder': '輸入自訂模型名',
            'model_placeholder': '請先載入模型',
            'models_loaded': '成功載入 {count} 個模型',
            'load_models_failed': '載入模型失敗：{error}',
            'model_list_not_supported': '呢個提供商唔支援自動獲取模型列表',
            'api_key_required': '請先輸入 API Key',
            'invalid_params': '無效參數',
            'warning': '警告',
            'success': '成功',
            'error': '錯誤',
            
            # 元數據欄位
            'metadata_title': '標題',
            'metadata_authors': '作者',
            'metadata_publisher': '出版社',
            'metadata_pubyear': '出版年份',
            'metadata_language': '語言',
            'metadata_series': '系列',
            'no_metadata': '冇元數據',
            'no_series': '冇系列',
            'unknown': '未知',

            # 多本書功能
            'books_unit': ' 本書',
            'new_conversation': '新對話',
            'single_book': '單本書',
            'multi_book': '多本書',
            'deleted': '已刪除',
            'history': '歷史記錄',
            'no_history': '暂無歷史記錄',
            'clear_current_book_history': '清空當前書籍歷史記錄',
            'confirm_clear_book_history': '確定要清空以下書籍嘉所有歷史記錄嘅？\n{book_titles}',
            'confirm': '確認',
            'history_cleared': '已清空 {deleted_count} 條歷史記錄。',
            'multi_book_template_label': '多本書提示詞範本:',
            'multi_book_placeholder_hint': '用 {books_metadata} 嚟表示書本信息，{query} 嚟表示用戶問題',
            
            # 錯誤消息
            'error': '錯誤: ',
            'network_error': '網絡錯誤',
            'request_timeout': '請求超時',
            'request_failed': '請求失敗',
            'question_too_long': '問題太長',
            'auth_token_required_title': '需要API金鑰',
            'auth_token_required_message': '請在插件配置內設置API金鑰。',
            'error_preparing_request': '準備請求時出錯',
            'empty_suggestion': '空建議',
            'process_suggestion_error': '處理建議時出錯',
            'unknown_error': '未知錯誤',
            'unknown_model': '未知模型: {model_name}',
            'suggestion_error': '建議錯誤',
            'random_question_success': '隨機問題生成成功！',
            'book_title_check': '需要書名',
            'avoid_repeat_question': '請用唔同嘅問題',
            'empty_answer': '空回答',
            'invalid_response': '無效回應',
            'auth_error_401': '未授權',
            'auth_error_403': '拒絕訪問',
            'rate_limit': '請求太多',
            'invalid_json': '無效嘅JSON',
            'no_response': '冇回應',
            'template_error': '模板錯誤',
            'no_model_configured': '未設置人工智能模型。請在設定內設置人工智能模型。',
            'random_question_error': '生成隨機問題時出錯',
            'clear_history_failed': '清除歷史失敗',
            'clear_history_not_supported': '而家唔支持清除單本書嘅歷史記錄',
            'missing_required_config': '缺少必要嘅設定: {key}。請檢查你嘅設定。',
            'api_key_too_short': 'API金鑰太短。請檢查並輸入完整嘅金鑰。',
            
            # API回應處理
            'api_request_failed': 'API請求失敗: {error}',
            'api_content_extraction_failed': '無法從API回應中提取內容',
            'api_invalid_response': '收到嘅API回應無效',
            'api_unknown_error': '未知錯誤: {error}',
            
            # 流式回應處理
            'stream_response_code': '流式回應狀態碼: {code}',
            'stream_continue_prompt': '繼續你嘅上一個回應，唔使重複已經提供嘅內容。',
            'stream_continue_code_blocks': '你嘅上一個回應有未關閉嘅代碼塊。繼續並完成呢啲代碼塊。',
            'stream_continue_parentheses': '你嘅上一個回應有未關閉嘅括號。繼續並確保所有括號都正確關閉。',
            'stream_continue_interrupted': '你嘅上一個回應似乎被中斷咗。繼續並完成你嘅最後一個思考或解釋。',
            'stream_timeout_error': '流式傳輸喺60秒內冇收到新嘅內容，可能係連接問題。',
            
            # API錯誤消息
            'api_version_model_error': 'API版本或模型名稱錯誤: {message}\n\n請更新API基礎URL為"{base_url}"，以及模型為"{model}"或在設定中添加其他可用模型。',
            'api_format_error': 'API請求格式錯誤: {message}',
            'api_key_invalid': '無效或未授權嘅API金鑰: {message}\n\n請檢查你嘅API金鑰並確保已開啟API訪問。',
            'api_rate_limit': '超出請求限制，請稍後再試\n\n你可能超出咗免費配額。呢可能係因為:\n1. 每分鐘請求太多\n2. 每日請求太多\n3. 每分鐘輸入嘅令牌太多',
            
            # 設定錯誤
            'missing_config_key': '缺少必要嘅設定鍵: {key}',
            'api_base_url_required': '需要API基礎URL',
            'model_name_required': '需要模型名稱',
            'api_key_empty': 'API金鑰為空。請輸入有效嘅API金鑰。',
            
            # 模型列表獲取
            'fetching_models_from': '正在從 {url} 獲取模型',
            'successfully_fetched_models': '成功獲取 {count} 個 {provider} 模型',
            'failed_to_fetch_models': '獲取模型失敗：{error}',
            
            # 關於信息
            'author_name': 'Sheldon',
            'user_manual': '用戶手冊',
            'about_plugin': '點解揀 Ask AI Plugin？',
            'learn_how_to_use': '點樣用',
            'email': 'iMessage',
            
            # 模型特定設定
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': '自訂',
            'model_enable_streaming': '啟用流式傳輸',
            'model_disable_ssl_verify': '禁用 SSL 驗證',

            # AI 切換器
            'current_ai': '當前 AI',
            'no_configured_models': '未配置 AI - 請在設定中配置',
            
            # 提供商特定信息
            'nvidia_free_info': '💡 新用戶有 6 個月免費 API 訪問 - 唔使信用卡',
            
            # 一般系統消息
            'default_system_message': '你係一個書籍分析專家。你嘅任務係通過提供有見地嘅問題同分析，幫助用戶更好咁理解書籍。',

            # 請求超時設定
            'request_timeout_label': '請求超時:',
            'seconds': '秒',
            'request_timeout_error': '請求超時。而家嘅超時時間：{timeout} 秒',
            
            # 並行 AI 設定
            'parallel_ai_count_label': '並行 AI 數量:',
            'parallel_ai_count_tooltip': '同時查詢嘅 AI 模型數量 (1-2 可用，3-4 即將推出)',
            'parallel_ai_notice': '注意：呢個只影響發送問題。隨機問題總係用單個 AI。',
            'suggest_maximize': '貼士：最大化窗口，用 3 個 AI 睇得更好',
            'ai_panel_label': 'AI {index}:',
            'no_ai_available': '呢個面板冇可用嘅 AI',
            'add_more_ai_providers': '請喺設定中添加更多 AI 提供商',
            'select_ai': '-- 選擇 AI --',
            'coming_soon': '即將推出',
            'advanced_feature_tooltip': '呢個功能開發緊。請留意更新！',
            
            # PDF 導出部分標題
            'pdf_book_metadata': '書籍元數據',
            'pdf_question': '問題',
            'pdf_answer': '回答',
            'pdf_ai_model_info': 'AI 模型信息',
            'pdf_generated_by': '由...生成',
            'pdf_provider': '提供商',
            'pdf_model': '模型',
            'pdf_api_base_url': 'API 基礎 URL',
            'pdf_panel': '面板',
            'pdf_plugin': '插件',
            'pdf_github': 'GitHub',
            'pdf_software': '軟件',
            'pdf_generated_time': '生成時間',
            'pdf_info_not_available': '信息不可用',
        }