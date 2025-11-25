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
        'export_history': '匯出歷史記錄',
        
        # 匯出設定
        'export_settings': '匯出設定',
        'enable_default_export_folder': '匯出到預設資料夾',
        'no_folder_selected': '未選擇資料夾',
        'browse': '瀏覽...',
        'select_export_folder': '選擇匯出資料夾',
        
        # 按鈕文字和選單項目
        'copy_response_btn': '複製回答',
        'copy_qa_btn': '複製問答',
        'export_current_btn': '匯出問答為PDF',
        'export_history_btn': '匯出歷史記錄為PDF',
        'copy_mode_response': '回答',
        'copy_mode_qa': '問答',
        'export_mode_current': '當前問答',
        'export_mode_history': '歷史記錄',
        
        # PDF匯出相關
        'model_provider': '提供商',
        'model_name': '模型',
        'model_api_url': 'API基礎URL',
        'pdf_model_info': 'AI模型資訊',
        'pdf_software': '軟體',
        
        'export_all_history_dialog_title': '匯出所有歷史記錄為PDF',
        'export_all_history_title': '所有問答歷史記錄',
        'export_history_insufficient': '需要至少2條歷史記錄才能匯出。',
        'history_record': '記錄',
        'question_label': '問題',
        'answer_label': '回答',
        'default_ai': '預設AI',
        'export_time': '匯出時間',
        'total_records': '總記錄數',
        'info': '資訊',
        'yes': '是',
        'no': '否',
        'no_book_selected_title': '未選擇書籍',
        'no_book_selected_message': '請先選擇一本書後再進行提問。',
        'set_default_ai_title': '設定預設AI',
        'set_default_ai_message': '您已切換到「{0}」。是否將其設為預設AI以用於未來的查詢？',
        'set_default_ai_success': '預設AI已設定為「{0}」。',
        'copied': '已複製！',
        'pdf_exported': 'PDF已匯出！',
        'export_pdf_dialog_title': '匯出為PDF',
        'export_pdf_error': '匯出PDF失敗：{0}',
        'no_question': '無問題',
        'saved': '已儲存',
        'close_button': '關閉',
        'open_local_tutorial': '打開本地教學',
        'tutorial_open_failed': '打開教學失敗',
        'tutorial': '教學',
        
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
        'no_history': '無歷史記錄',
        'empty_question_placeholder': '（無問題）',
        'history_ai_unavailable': '此AI已從配置中移除',
        'clear_current_book_history': '清空當前書籍歷史記錄',
        'confirm_clear_book_history': '確定要清空以下書籍的所有歷史記錄嗎？\n{book_titles}',
        'confirm': '確認',
        'history_cleared': '已清空 {deleted_count} 條歷史記錄。',
        'multi_book_template_label': '多書提示詞模板:',
        'multi_book_placeholder_hint': '使用 {books_metadata} 表示書籍資訊，{query} 表示用戶問題',
        
        # 錯誤信息
        'network_error': '連線錯誤',
        'request_timeout': '請求超時',
        'request_failed': '請求失敗',
        'question_too_long': '問題過長',
        'auth_token_required_title': '需要AI服務',
        'auth_token_required_message': '請在外掛程式配置中設定有效的AI服務。',
        'open_configuration': '打開配置',
        'cancel': '取消',
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
        'no_ai_configured_title': '未配置AI',
        'no_ai_configured_message': '歡迎使用！要開始對書籍提問，您需要先配置一個AI提供商。\n\n推薦新手選擇：\n• Nvidia AI - 只需手機號即可獲取半年免費API訪問權限（無需綁定信用卡）\n• Ollama - 在您的電腦上本地執行AI模型（完全免費且隱私）\n\n是否現在打開外掛程式配置來設定AI提供商？',
        'open_settings': '外掛程式配置',
        'ask_anyway': '仍要詢問',
        'later': '稍後',
        'reset_all_data': '重置所有資料',
        'reset_all_data_warning': '這將會刪除所有API密鑰、提示詞模板和本地歷史記錄。您的語言偏好將被保留。請慎重操作。',
        'reset_all_data_confirm_title': '確認重置',
        'reset_all_data_confirm_message': '您確定要將外掛程式重置為初始狀態嗎？\n\n這將永久刪除：\n• 所有API密鑰\n• 所有自定義提示詞模板\n• 所有對話歷史記錄\n• 所有外掛程式設定（語言偏好將被保留）\n\n此操作無法撤銷！',
        'reset_all_data_success': '所有外掛程式資料已成功重置。請重新啟動calibre以使更改生效。',
        'reset_all_data_failed': '重置外掛程式資料失敗：{error}',
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
        'model_enable_streaming': '啟用串流傳輸',
        
        # AI Switcher
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
        'select_model': '-- 切換Model --',
        'request_model_list': '請請求模型列表',
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
            'default_ai_mismatch_title': '預設 AI 已變更',
            'default_ai_mismatch_message': '設定中的預設 AI 已變更為 "{default_ai}",\n但目前的對話框正在使用 "{current_ai}"。\n\n您要切換到新的預設 AI 嗎？',
            'discard_changes': '放棄變更',
            'empty_response': '收到來自 API 的空回應',
            'empty_response_after_filter': '過濾 think 標籤後回應為空',
            'error_401': 'API 金鑰驗證失敗。請檢查：API 金鑰正確、帳戶有足夠餘額、API 金鑰未過期。',
            'error_403': '拒絕存取。請檢查：API 金鑰有足夠權限、無地區存取限制。',
            'error_404': '找不到 API 端點。請檢查 API Base URL 設定是否正確。',
            'error_429': '請求過多，已達速率限制。請稍後再試。',
            'error_5xx': '伺服器錯誤。請稍後再試或檢查服務提供者狀態。',
            'error_network': '網路連線失敗。請檢查網路連線、代理設定或防火牆設定。',
            'error_unknown': '未知錯誤。',
            'gemini_geo_restriction': 'Gemini API 在您的地區無法使用。請嘗試：\n1. 使用 VPN 從支援的地區連線\n2. 使用其他 AI 提供者（OpenAI、Anthropic、DeepSeek 等）\n3. 檢查 Google AI Studio 的地區可用性',
            'load_models_list': '載入模型清單',
            'loading_models_text': '正在載入模型',
            'model_test_success': '模型測試成功！設定已儲存。',
            'models_loaded_with_selection': '成功載入 {count} 個模型。\n已選模型：{model}',
            'ollama_model_not_available': '模型 "{model}" 無法使用。請檢查：\n1. 模型是否已啟動？執行：ollama run {model}\n2. 模型名稱是否正確？\n3. 模型是否已下載？執行：ollama pull {model}',
            'ollama_service_not_running': 'Ollama 服務未執行。請先啟動 Ollama 服務。',
            'ollama_service_timeout': 'Ollama 服務連線逾時。請檢查服務是否正常執行。',
            'reset_ai_confirm_message': '即將將 {ai_name} 重設為預設狀態。\n\n這將清除：\n• API 金鑰\n• 自訂模型名稱\n• 其他已設定參數\n\n繼續？',
            'reset_ai_confirm_title': '確認重設',
            'reset_current_ai': '將目前 AI 重設為預設',
            'reset_tooltip': '將目前 AI 重設為預設值',
            'save_and_close': '儲存並關閉',
            'skip': '略過',
            'technical_details': '技術詳情',
            'test_current_model': '測試目前模型',
            'test_model_button': '測試模型',
            'test_model_prompt': '模型載入成功！您要測試已選模型 "{model}" 嗎？',
            'unsaved_changes_message': '您有未儲存的變更。您要怎麼做？',
            'unsaved_changes_title': '未儲存的變更',
            'invalid_default_ai_title': '預設AI配置無效',
            'invalid_default_ai_message': '預設AI "{default_ai}" 未正確配置。\n\n是否切換到 "{first_ai}"？',
            'switch_to_ai': '切換到 {ai}',
            'keep_current': '保持目前設定',
            'pdf_info_not_available': '資訊不可用',
    }