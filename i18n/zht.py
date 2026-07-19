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
        return '背景說明：你正在通過「Ask AI Plugin」插件協助 calibre (http://calibre-ebook.com) 電子書管理軟體的用戶。該插件允許用戶針對 calibre 書庫中的書籍提問。注意：本插件只能回答關於所選書籍的內容、主題或相關話題的問題，無法直接修改書籍元數據或執行 calibre 操作。書籍資訊：書名：「{title}」，作者：{author}，出版社：{publisher}，出版年份：{pubyear}，語言：{language}，系列：{series}。用戶問題：{query}。請基於書籍資訊和你的知識提供有幫助的回答。'
    
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
        'plugin_name': 'Ask AI 插件',
        'plugin_desc': '使用AI提問關於書籍的問題',
        
        # UI - 標籤和區域
        'config_title': '設定',
        'general_tab': '一般',
        'ai_models': '人工智能',
        'shortcuts': '快捷鍵',
        'shortcuts_note': "快捷鍵可在 calibre：Preferences -> Shortcuts 中自訂（搜尋 'Ask AI'）。\n本頁顯示的是預設快捷鍵/範例，若你已在 Shortcuts 中修改，請以 calibre 設定為準。",
        'prompts_tab': '提示詞',
        'about': '關於',
        'metadata': '元數據',
        
        # 區域字幕
        'language_settings': '語言',
        'language_subtitle': '選擇你喜好的介面語言',
        'ai_providers_subtitle': '配置AI服務商並選擇預設AI',
        'prompts_subtitle': '自定義向AI發送問題的方式',
        'export_settings_subtitle': '設定匯出PDF的預設資料夾',
        'reset_all_data_subtitle': '警告：這將永久刪除所有設定和資料',
        
        # Prompts tab
        'language_preference_title': '語言偏好',
        'language_preference_subtitle': '控制 AI 回答是否與介面語言保持一致',
        'prompt_templates_title': '提示詞範本',
        'prompt_templates_subtitle': '使用動態欄位如 {title}、{author}、{query} 自訂書籍資訊如何發送給 AI',
        'ask_prompts': '提問提示詞',
        'random_questions_prompts': '隨機問題提示詞',
        'multi_book_prompts_label': '多書提示詞',
        'multi_book_placeholder_hint': '使用 {books_metadata} 表示書籍資訊，{query} 表示使用者問題',
        'dynamic_fields_title': '動態欄位參考',
        'dynamic_fields_subtitle': '可用欄位及範例值（以《弗蘭肯斯坦》為例）',
        'dynamic_fields_examples': '<b>{title}</b> → Frankenstein<br><b>{author}</b> → Mary Shelley<br><b>{publisher}</b> → Lackington, Hughes, Harding, Mavor & Jones<br><b>{pubyear}</b> → 1818<br><b>{language}</b> → English<br><b>{series}</b> → (無)<br><b>{query}</b> → 您的問題文本',
        'reset_prompts': '重設為預設提示詞',
        'reset_prompts_confirm': '確定要將所有提示詞範本重設為預設值嗎？此操作無法撤銷。',
        'unsaved_changes_title': '未儲存的更改',
        'unsaved_changes_message': '提示詞標籤頁有未儲存的更改，是否儲存？',
        'use_interface_language': '始終要求AI使用當前外掛程式介面語言回答',
        'language_instruction_label': '已添加到提示詞的語言指令：',
        'language_instruction_text': '請使用{language_name}回答。',
        
        # Persona 設定
        'persona_title': '角色設定',
        'persona_subtitle': '定義您的研究背景和目標，幫助AI提供更相關的回答',
        'use_persona': '使用角色設定',
        'persona_label': '角色設定',
        'persona_placeholder': '作為研究人員，我希望透過書籍資料進行研究。',
        'persona_hint': 'AI越了解您的目標和背景，研究或生成的效果就越好。',
        
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
        'copy_format_plain': '純文字',
        'copy_format_markdown': 'Markdown',
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
        'open_local_tutorial': '打開本地教程',
        'tutorial_open_failed': '打開教程失敗',
        'tutorial': '教程',

        'model_display_name_perplexity': 'Perplexity',
        
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
        'menu_ask': '詢問',
        
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
        'error_opening_dialog': '開啟對話框時發生錯誤:',
        'skipped_books_warning': '由於檔案存取錯誤，已跳過 {count} 本書。\n這可能是由於檔案路徑包含無效字元或檔案被其他程式鎖定。',
        'failed_to_read_all_books': '無法讀取所有選取書籍的元資料。\n這可能是由於檔案路徑包含無效字元或檔案被其他程式鎖定。',
        'error_starting_request': '啟動請求時發生錯誤',
        'default_ai_mismatch_title': '預設 AI 已更改',
        'default_ai_mismatch_message': '偵測到設定中的預設 AI 已更改為 "{default_ai}"，\n但目前對話使用的是 "{current_ai}"。\n\n是否切換到新的預設 AI？',
        
        # 元數據欄位
        'metadata_title': '標題',
        'metadata_authors': '作者',
        'metadata_publisher': '出版社',
        'metadata_pubdate': '出版日期',
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
        'request_stopped': '請求已停止',
        'question_too_long': '問題過長',
        'question_too_long_detail': (
            '提示詞過長（目前 {current} 字元，限制 {limit} 字元，超出 {over} 字元）。'
            '您選取了 {book_count} 本書。'
        ),
        'question_too_long_detail_library': (
            '提示詞過長（目前 {current} 字元，限制 {limit} 字元，超出 {over} 字元）。'
            '書庫索引共 {book_count} 本書。'
        ),
        'question_too_long_hint_ai_search': (
            '書庫級篩選請使用 AI Search（不選書直接提問，或使用 AI Search 選單），'
            '而不是一次選取大量書籍。'
        ),
        'question_too_long_hint_library_search': (
            '書庫索引超出目前提示詞限制。請在「外掛程式配置 → General」中啟用自訂提示詞長度限制'
            '（建議 524288 字元），或提出更具體的問題。'
        ),
        'question_too_long_reduce_books': (
            '若需對少量書深度比對，請嘗試取消選取約 {count} 本書。'
        ),
        'question_too_long_hint_default': (
            '目前預設限制：{limit} 字元（{mode}）。'
            '單書預設 128,000 字元，多書預設 256,000 字元。'
            '進階使用者可在「外掛程式配置 → General」中啟用自訂提示詞長度限制。'
        ),
        'question_too_long_hint_custom': (
            '您已啟用自訂提示詞長度限制。若請求逾時，請在「外掛程式配置 → General」中調低限制，'
            '或減少選取書籍 / 提出更具體的問題。'
        ),
        'large_selection_dialog_title': '選取書籍過多',
        'large_selection_dialog_message': (
            '您選取了 {count} 本書。書庫級問題更適合使用 AI Search，'
            '將以精簡格式搜尋整個書庫。\n\n'
            '是否切換到 AI Search，還是繼續用目前選取書籍（精簡格式）？'
        ),
        'large_selection_use_ai_search': '使用 AI Search',
        'large_selection_continue': '繼續用目前選取',
        'multi_book_truncation_note': (
            '注意：因提示詞長度限制，僅包含前 {included} / {total} 本選取書籍。'
            '請使用 AI Search 搜尋整個書庫，或在「外掛程式配置 → General」中提高自訂限制。'
        ),
        'library_metadata_truncation_note': (
            '注意：因提示詞長度限制，僅包含前 {included} / {total} 本已索引書籍。'
            '超大書庫的結果可能不完整，可在「外掛程式配置 → General」中提高自訂限制。'
        ),
        'auth_token_required_title': '需要AI服務',
        'auth_token_required_message': '請在外掛程式配置中設定有效的AI服務。',
        'open_configuration': '打開配置',
        'cancel': '取消',
        
        # AI Manager Dialog
        'ai_manager_title': '管理 AI 服務商',
        'add_ai_title': '新增 AI 服務商',
        'manage_ai_title': '管理已配置的 AI',
        'configured_ai_list': '已配置的 AI',
        'available_ai_list': '可新增的 AI',
        'ai_config_panel': '配置',
        'select_ai_to_configure': '從清單中選擇一個 AI 進行配置',
        'select_provider': '選擇 AI 服務商',
        'select_provider_hint': '從清單中選擇一個服務商',
        'select_ai_to_edit': '從清單中選擇一個 AI 進行編輯',
        'set_as_default': '設為預設',
        'save_ai_config': '儲存',
        'remove_ai_config': '移除',
        'delete_ai': '刪除',
        'close_button': '關閉',
        'add_ai_button': '新增 AI',
            'ai_manager_window_hint': '「新增 / 管理」會開啟可調整大小的獨立視窗（可最大化）。雙擊已設定的 AI 可直接編輯。',
        'edit_ai_button': '編輯 AI',
        'manage_configured_ai_button': '管理已配置 AI',
        'manage_ai_button': '管理 AI',
        'no_configured_ai': '尚未配置任何 AI',
        'no_configured_ai_hint': '未配置任何 AI，外掛程式無法使用。請點擊「新增 AI」新增一個 AI 服務商。',
        'default_ai_label': '預設 AI:',
        'default_ai_tag': '預設',
        'ai_not_configured_cannot_set_default': '此 AI 尚未配置。請先儲存配置。',
        'ai_set_as_default_success': '{name} 已設為預設 AI。',
        'ai_config_saved_success': '{name} 配置已成功儲存。',
        'confirm_remove_title': '確認移除',
        'confirm_remove_ai': '確定要移除 {name} 嗎？這將清除 API 金鑰並重設配置。',
        'confirm_delete_title': '確認刪除',
        'confirm_delete_ai': '確定要刪除 {name} 嗎？',
        'api_key_required': 'API 金鑰為必填項。',
        'success': '成功',
        'configuration': '配置',
        
        'yes_button': '是',
        'no_button': '否',
        'cancel_button': '取消',
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
        'no_ai_configured_message': '歡迎使用！要開始對書籍提問，您需要先配置一個AI提供商。\n\n好消息：本外掛程式現在提供免費通道（Nvidia AI Free），您可以立即使用，無需任何配置！\n\n其他推薦選擇：\n• Nvidia AI - 只需手機號即可獲取半年免費API訪問權限（無需綁定信用卡）\n• Ollama - 在您的電腦上本地執行AI模型（完全免費且隱私）\n\n是否現在打開外掛程式配置來設定AI提供商？',
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
            'model_display_name_ollama': 'Ollama(本地)',
            'model_display_name_lmstudio': 'LM Studio(本地)',
            'model_display_name_koboldcpp': 'KoboldCpp(本地)',
            'local_openai_compat_no_api_key_notice': '提示：此本地 OpenAI 相容服務通常不需要 API Key。請先啟動本地服務，再重新整理模型清單。',
            'lmstudio_no_api_key_notice': '提示：LM Studio 本地使用 OpenAI 相容介面，通常不需要 API Key。',
            'koboldcpp_no_api_key_notice': '提示：KoboldCpp 本地使用 OpenAI 相容介面，通常不需要 API Key。',
            'local_service_not_running': '無法連線本地 AI 服務。請確認服務已啟動且 Base URL 正確。',
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
        'max_prompt_length_normalized_title': '提示詞長度已調整',
        'max_prompt_length_normalized': '提示詞長度已規範為 {value} 字元（已移除逗號、空格等分隔符）。',
        'enable_custom_prompt_limit_label': '自訂提示詞長度限制',
        'enable_custom_prompt_limit_tooltip': (
            '預設限制為單書 128,000 字元、多書 256,000 字元，大多數使用者無需修改。'
            '書庫級搜尋請使用 AI Search。僅在模型支援更大上下文且仍遇到長度限制時啟用自訂。'
        ),
        'max_prompt_length_label': '最大提示詞長度：',
        'max_prompt_length_unit': '字元',
        'max_prompt_length_tooltip': (
            '啟用自訂限制後生效。建議預設值：524288 字元。'
            '粗略參考：1 token ≈ 3–4 字元。使用 Ollama 時還需在模型側配置 num_ctx。'
        ),
        
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
        'model_test_success': '模型測試成功！',
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
        
        # Field descriptions
        'api_key_desc': '您的API金鑰用於身份驗證。請妥善保管，不要分享。',
        'base_url_desc': 'API端點URL。除非您有自訂端點，否則請使用預設值。',
        'model_desc': '從清單中選擇模型或使用自訂模型名稱。',
        'streaming_desc': '啟用即時回應串流以獲得更快的回饋。',
        'advanced_section': '進階',
        
        # Provider-specific notices
        'perplexity_model_notice': '注意：Perplexity 沒有提供公開的模型清單API，因此模型名稱為硬編碼。',
        'ollama_no_api_key_notice': '提示：Ollama 本地使用 OpenAI 相容介面，通常不需要 API Key。',
        'nvidia_free_credits_notice': '注意：新用戶可獲得免費API額度，無需信用卡。',
        
        # Nvidia Free 錯誤訊息
        'free_tier_rate_limit': '免費通道請求頻率超限。請稍後再試或配置自己的 Nvidia API Key。',
        'free_tier_unavailable': '免費通道暫時不可用。請稍後再試或配置自己的 Nvidia API Key。',
        'free_tier_server_error': '免費通道伺服器錯誤。請稍後再試。',
        'free_tier_error': '免費通道錯誤',
        
        # Nvidia Free 服務商資訊
        'free': '免費',
        'nvidia_free_provider_name': 'Nvidia AI（免費）',
        'nvidia_free_display_name': 'Nvidia AI（免費）',
        'nvidia_free_api_key_info': '將會從伺服器取得',
        'nvidia_free_desc': '此服務由開發者維護，保持免費，但可能不太穩定。如需更穩定的服務，請配置自己的 Nvidia API Key。',
        
        # Nvidia Free 首次使用提醒
        'nvidia_free_first_use_title': '歡迎使用 Ask AI 外掛',
        'nvidia_free_first_use_message': '現在您無需任何配置就可以直接提問！開發者為您維護了一個免費通道，但可能不太穩定。盡情使用吧！\n\n您可以在設定中配置自己的 AI 服務商以獲得更穩定的服務。',
        
        # Model buttons
        'refresh_model_list': '重新整理',
        'testing_text': '測試中',
        'refresh_success': '模型清單重新整理成功。',
        'refresh_failed': '重新整理模型清單失敗。',
        'test_failed': '模型測試失敗。',
        
        # Tooltip
        'manage_ai_disabled_tooltip': '請先新增AI服務商。',

        #AI Search v1.4.2
        'library_tab': '搜尋',
        'library_search': 'AI 搜尋',
        'library_info': 'AI 搜尋功能始終保持啟用。當您未選取任何書籍時，即可使用自然語言搜尋整個書庫。',
        'library_enable': '啟用 AI 搜尋',
        'library_enable_tooltip': '啟用後，在未選取書籍的情況下可以使用 AI 搜尋書庫',
        'library_update': '更新書庫資料',
        'library_update_tooltip': '從書庫中提取書名與作者',
        'library_updating': '更新中...',
        'library_status': '狀態：共有 {count} 本書，上次更新時間：{time}',
        'library_status_empty': '狀態：尚無資料。請點擊「更新書庫資料」開始。',
        'library_status_error': '狀態：載入資料出錯',
        'library_update_success': '成功更新 {count} 本書籍',
        'library_update_failed': '更新書庫資料失敗',
        'library_no_gui': '圖形介面無法使用',
        'library_init_title': '初始化 AI 搜尋',
        'library_init_message': 'AI 搜尋需要書庫元數據才能運作。是否立即進行初始化？\n\n這將會從您的書庫中提取書名與作者。',
        'library_init_required': '若無書庫資料則無法啟用 AI 搜尋。請在準備就緒時點擊「更新書庫資料」。',
        'ai_search_welcome_title': '歡迎使用 AI 搜尋',
        'ai_search_welcome_message': 'AI 搜尋已啟動！\n\n觸發方式：\n• 快捷鍵（可在設定中自訂）\n• 工具選單 → AI 搜尋\n• 不選取任何書籍時開啟 Ask 對話框\n\n您可以用自然語言搜尋整個書庫。例如：\n• 「你有關於 Python 的書嗎？」\n• 「幫我找艾西莫夫寫的書」\n• 「尋找關於機器學習的書」\n\nAI 會搜尋您的書庫並推薦相關書籍，點擊書名即可直接開啟閱讀。',
        'ai_search_not_enough_books_title': '書籍數量不足',
        'ai_search_not_enough_books_message': 'AI 搜尋需要您的書庫中至少有 {min_books} 本書。\n\n您目前的書庫只有 {book_count} 本書。\n\n請新增更多書籍後再使用 AI 搜尋。',
        'ai_search_mode_info': '正在搜尋整個書庫',
        'ai_search_feature_title': 'AI 搜尋',
        'ai_search_feature_subtitle': '用自然語言搜尋整個書庫',
        'ai_search_feature_description': (
            'AI 搜尋幫助您在整本 Calibre 書庫中發現書籍。\n\n'
            '• 觸發方式：不選書開啟 Ask、使用「工具 → AI 搜尋」或快捷鍵\n'
            '• 工作原理：外掛程式以精簡格式（書籍 ID、書名、作者）傳送已索引的全部書籍元數據\n'
            '• 大量選書：選取超過 50 本時，Ask 會建議使用 AI 搜尋，而不是把每本書的詳細元數據塞進提示詞\n'
            '• 保持資料最新：新增或刪除書籍後，請點擊「更新書庫資料」\n\n'
            '範例問題：「有沒有 Python 相關的書？」「給我看看阿西莫夫的書」。'
        ),
        'ai_search_usage_hint': (
            '提示：AI 搜尋最適合書庫級發現。若需深度比對少量書籍，請直接選取不超過 30 本書。'
        ),
        'ai_search_data_title': '書庫索引',
        'ai_search_data_subtitle': '新增或刪除書籍後，請刷新傳送給 AI 的精簡書單',
        'library_prompt_template': '您可以存取使用者的書庫。以下是所有書籍：{metadata} 使用者查詢：{query} 請在當前書庫目錄中找出符合的書籍並以以下格式回傳（**重要**：使用 HTML 連結格式，讓使用者可以點擊書名直接開啟書籍）：- <a href="calibre://book/書籍ID">書名</a> - 作者名 範例：- <a href="calibre://book/123">Python 程式設計</a> - Mark Lutz - <a href="calibre://book/456">機器學習實戰</a> - Peter Harrington 注意：部分作者資訊可能顯示為「unknown」，這是正常資料，請正常回傳所有符合結果，不要被此誤導。只回傳符合查詢的書籍。最多 5 個結果。',
        'ai_search_privacy_title': '隱私權聲明',
        'ai_search_privacy_alert': 'AI 搜尋會使用您書庫中的書籍元數據（書名與作者）。這些資訊將傳送至您設定的 AI 供應商，以處理您的搜尋請求。',
        'ai_search_updated_info': '{time_ago} 更新了 {count} 本書籍',
        'ai_search_books_info': '已索引 {count} 本書籍',
        'days_ago': '{n} 天前',
        'hours_ago': '{n} 小時前',
        'minutes_ago': '{n} 分鐘前',
        'just_now': '剛才',
        
        # 統計標籤頁 (v1.4.2)
        'stat_tab': '統計',
        'stat_overview': '概覽',
        'stat_overview_subtitle': '統計呈現調用AI問詢的次數',
        'stat_days_unit': '天',
        'stat_days_label': '開始使用',
        'stat_start_at': '開始於 {date}',
        'stat_replies_unit': '次',
        'stat_replies_label': '問詢AI',
        'stat_books_unit': '本書',
        'stat_books_label': '書庫藏書',
        'stat_no_books': '在搜尋頁更新',
        'stat_trends': '趨勢',
        'stat_curious_index': '本週的問詢AI次數分布',
        'stat_daily_avg': '日均 {n} 次',
        'stat_sample_data': '當前為示例資料，總的請求次數大於20次之後會切換為正式資料',
        'stat_heatmap': '熱力圖',
        'stat_heatmap_subtitle': '本月的問詢AI次數分布',
        'stat_no_data_week': '暫無本週資料',
        'stat_no_data_month': '暫無本月資料',
        'stat_data_not_enough': '資料不足',
        
        # 統計用戶稱號（基於問詢次數）
        'stat_title_curious': '翻書人',
        'stat_title_explorer': '覓書客',
        'stat_title_seeker': '啃書匠',
        'stat_title_enthusiast': '藏書家',
        'stat_title_pursuer': '書蟲',
        
        # 統計書庫評價（基於藏書數量，使用歷史圖書館典故）
        'stat_books_impressive': '私人書齋',
        'stat_books_collection': '文人書房',
        'stat_books_variety': '翰林書院',
        'stat_books_awesome': '天一閣',
        'stat_books_unbelievable': '亞歷山大圖書館',
        
        # 連結 (v1.4.2)
        'online_tutorial': '線上教程',
        }
