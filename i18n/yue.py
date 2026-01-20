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
        return '背景說明：你正在通過「Ask AI Plugin」插件協助 calibre (http://calibre-ebook.com) 電子書管理軟件嘅用戶。呢個插件允許用戶針對 calibre 書庫中嘅書籍提問。注意：本插件只可以回答關於所選書籍嘅內容、主題或者相關話題嘅問題，無法直接修改書籍元數據或者執行 calibre 操作。書籍資料：書名：「{title}」，作者：{author}，出版社：{publisher}，出版年份：{pubyear}，語言：{language}，系列：{series}。用戶問題：{query}。請基於書籍資料同你嘅知識提供有幫助嘅回答。'

    @property
    def suggestion_template(self) -> str:
        return """你係一個專業嘅書評家。對於「{title}」呢本由{author}寫嘅書，出版語言係{language}，生成一個有見地嘅問題，幫助讀者更加理解呢本書嘅核心思想、實踐應用或者獨特觀點。規則：1. 只返回問題本身，唔使介紹或解釋 2. 將焦點放喺書嘅內容上，唔係標題 3. 令問題具有實用性同啟發性 4. 保持精簡（30-200字） 5. 發揮創意，就算係同一本書，每次都要生成唔同嘅問題"""

    @property
    def multi_book_default_template(self) -> str:
        return """以下係關於幾本書嘅資料：{books_metadata} 用戶問題：{query} 請基於以上書籍資料回答問題。"""

    @property
    def translations(self) -> dict:
        return {
            # 插件信息
            'plugin_name': 'Ask AI 插件',
            'plugin_desc': '用 AI 問書嘅問題', # Ask questions about a book using AI

            # UI - 標籤同區域
            'config_title': '設定', # Configuration
            'general_tab': '一般', # General
            'ai_models': 'AI 服務供應商', # AI Providers
            'shortcuts': '快捷鍵', # Shortcuts
            'shortcuts_note': "快捷鍵可以喺 calibre 入面自訂：偏好設定 -> 快捷鍵（搵 'Ask AI'）。\n呢頁顯示嘅係預設/例子快捷鍵。如果你喺快捷鍵入面改咗佢哋，就以 calibre 嘅設定為準。", # You can customize these shortcuts in calibre: Preferences -> Shortcuts (search 'Ask AI').\nThis page shows the default/example shortcuts. If you changed them in Shortcuts, calibre settings take precedence.
            'prompts_tab': '提示詞', # Prompts
            'about': '關於', # About
            'metadata': '元數據', # Metadata

            # Section subtitles
            'language_settings': '語言', # Language
            'language_subtitle': '揀你鍾意嘅介面語言', # Choose your preferred interface language
            'ai_providers_subtitle': '設定 AI 服務供應商並揀你嘅預設 AI', # Configure AI providers and select your default AI
            'prompts_subtitle': '自訂點樣將問題傳送俾 AI', # Customize how questions are sent to AI
            'export_settings_subtitle': '設定導出 PDF 嘅預設資料夾', # Set default folder for exporting PDFs
            'debug_settings_subtitle': '啟用偵錯日誌嚟排查問題', # Enable debug logging for troubleshooting
            'reset_all_data_subtitle': '⚠️ 警告：呢個操作會永久刪除你所有嘅設定同資料', # ⚠️ Warning: This will permanently delete all your settings and data

            # Prompts tab
            'language_preference_title': '語言偏好', # Language Preference
            'language_preference_subtitle': '控制 AI 回應係咪要同你介面語言一致', # Control whether AI responses should match your interface language
            'prompt_templates_title': '提示詞範本', # Prompt Templates
            'prompt_templates_subtitle': '用 {title}, {author}, {query} 等動態字段嚟自訂書籍資料點樣傳送俾 AI', # Customize how book information is sent to AI using dynamic fields like {title}, {author}, {query}
            'ask_prompts': '發問提示詞', # Ask Prompts
            'random_questions_prompts': '隨機問題提示詞', # Random Questions Prompts
            'multi_book_prompts_label': '多書提示詞', # Multi-Book Prompts
            'multi_book_placeholder_hint': '用 {books_metadata} 代表書籍資料，{query} 代表用戶問題', # Use {books_metadata} for book information, {query} for user question
            'dynamic_fields_title': '動態字段參考', # Dynamic Fields Reference
            'dynamic_fields_subtitle': '可用字段同埋瑪麗·雪萊「科學怪人」嘅例子值', # Available fields and example values from "Frankenstein" by Mary Shelley
            'dynamic_fields_examples': '<b>{title}</b> → 科學怪人<br><b>{author}</b> → 瑪麗·雪萊<br><b>{publisher}</b> → Lackington, Hughes, Harding, Mavor & Jones<br><b>{pubyear}</b> → 1818<br><b>{language}</b> → 英文<br><b>{series}</b> → (無)<br><b>{query}</b> → 你嘅問題內容', # Example values from "Frankenstein" by Mary Shelley
            'reset_prompts': '將提示詞重設為預設值', # Reset Prompts to Default
            'reset_prompts_confirm': '你確定要將所有提示詞範本重設為預設值咩？呢個動作唔可以還原㗎。', # Are you sure you want to reset all prompt templates to their default values? This action cannot be undone.
            'unsaved_changes_title': '未儲存嘅更改', # Unsaved Changes
            'unsaved_changes_message': '提示詞分頁有未儲存嘅更改，係咪要儲存？', # You have unsaved changes in the Prompts tab. Do you want to save them?
            'use_interface_language': '永遠要求 AI 用目前插件介面語言回答', # Always ask AI to respond in current plugin interface language
            'language_instruction_label': '已添加到提示詞嘅語言指令：', # Language instruction added to prompts:
            'language_instruction_text': '請用{language_name}回答。', # Please respond in {language_name}.

            # Persona settings
            'persona_title': '角色設定', # Persona
            'persona_subtitle': '定義你嘅研究背景同目標，等 AI 可以提供更相關嘅答案', # Define your research background and goals to help AI provide more relevant responses
            'use_persona': '使用角色設定', # Use persona
            'persona_label': '角色設定', # Persona
            'persona_placeholder': '作為一個研究人員，我想通過書籍資料進行研究。', # As a researcher, I want to research through book data.
            'persona_hint': 'AI 越了解你嘅目標同背景，研究或者生成嘅效果就越好。', # The more AI knows about your target and background, the better the research or generation.

            # UI - 按钮和操作
            'ok_button': '確定', # OK
            'save_button': '儲存', # Save
            'send_button': '傳送', # Send
            'stop_button': '停止', # Stop
            'suggest_button': '隨機問題', # Random Question
            'copy_response': '複製答案', # Copy Response
            'copy_question_response': '複製問答', # Copy Q&A
            'export_pdf': '導出 PDF', # Export PDF
            'export_current_qa': '導出目前問答', # Export Current Q&A
            'export_history': '導出歷史紀錄', # Export History
            'export_all_history_dialog_title': '導出所有歷史紀錄為 PDF', # Export All History to PDF
            'export_all_history_title': '所有問答歷史紀錄', # ALL Q&A HISTORY
            'export_history_insufficient': '需要至少 2 條歷史紀錄先可以導出。', # Need at least 2 history records to export.
            'history_record': '紀錄', # Record
            'question_label': '問題', # Question
            'answer_label': '答案', # Answer
            'default_ai': '預設 AI', # Default AI
            'export_time': '導出時間', # Exported at
            'total_records': '總紀錄數', # Total Records
            'info': '資訊', # Information
            'yes': '係', # Yes
            'no': '唔係', # No
            'no_book_selected_title': '未揀書', # No Book Selected
            'no_book_selected_message': '請揀咗本書先至好問問題。', # Please select a book before asking questions.
            'set_default_ai_title': '設定預設 AI', # Set Default AI
            'set_default_ai_message': '你已經轉咗去「{0}」。想唔想將佢設為以後查詢嘅預設 AI 呀？', # You have switched to "{0}". Would you like to set it as the default AI for future queries?
            'set_default_ai_success': '預設 AI 已經設定為「{0}」。', # Default AI has been set to "{0}".
            'default_ai_mismatch_title': '預設 AI 已更改', # Default AI Changed
            'default_ai_mismatch_message': '設定中嘅預設 AI 已經改咗做「{default_ai}」，\n但係目前對話用緊「{current_ai}」。\n\n想唔想轉用新嘅預設 AI 呀？', # The default AI in configuration has been changed to "{default_ai}",\nbut the current dialog is using "{current_ai}".\n\nWould you like to switch to the new default AI?
            'copied': '已複製！', # Copied!
            'pdf_exported': 'PDF 已導出！', # PDF Exported!
            'export_pdf_dialog_title': '導出為 PDF', # Export to PDF
            'export_pdf_error': '導出 PDF 失敗：{0}', # Failed to export PDF: {0}
            'no_question': '無問題', # No question
            'no_response': '無答案', # No response
            'saved': '已儲存', # Saved
            'close_button': '關閉', # Close
            'open_local_tutorial': '打開本地教學', # Open Local Tutorial
            'tutorial_open_failed': '打開教學失敗', # Failed to open tutorial
            'tutorial': '教學', # Tutorial

            'model_display_name_perplexity': 'Perplexity',

            # UI - 配置字段
            'token_label': 'API 金鑰：', # API Key:
            'api_key_label': 'API 金鑰：', # API Key:
            'model_label': '模型：', # Model:
            'language_label': '語言：', # Language:
            'language_label_old': '語言', # Language
            'base_url_label': '基礎 URL：', # Base URL:
            'base_url_placeholder': '預設值: {default_api_base_url}', # Default: {default_api_base_url}
            'shortcut': '快捷鍵', # Shortcuts Key
            'shortcut_open_dialog': '打開對話框', # Open Dialog
            'shortcut_enter': 'Ctrl + Enter', # Ctrl + Enter
            'shortcut_return': 'Command + Return', # Command + Return
            'using_model': '模型', # Model
            'action': '動作', # Action
            'reset_button': '重設為預設值', # Reset to Default
            'reset_current_ai': '重設當前 AI 為預設值', # Reset Current AI to Default
            'reset_ai_confirm_title': '確認重設', # Confirm Reset
            'reset_ai_confirm_message': '即將重設 {ai_name} 到預設狀態。\n\n呢個動作會清除：\n• API 金鑰\n• 自訂模型名稱\n• 其他已設定嘅參數\n\n係咪繼續？', # About to reset {ai_name} to default state.\n\nThis will clear:\n• API Key\n• Custom model name\n• Other configured parameters\n\nContinue?
            'reset_tooltip': '重設目前 AI 到預設值', # Reset current AI to default values
            'unsaved_changes_title': '未儲存嘅更改', # Unsaved Changes
            'unsaved_changes_message': '你有未儲存嘅更改。你想點做？', # You have unsaved changes. What would you like to do?
            'save_and_close': '儲存並關閉', # Save and Close
            'discard_changes': '放棄更改', # Discard Changes
            'cancel': '取消', # Cancel
            'yes_button': '係', # Yes
            'no_button': '唔係', # No
            'cancel_button': '取消', # Cancel
            'invalid_default_ai_title': '無效嘅預設 AI', # Invalid Default AI
            'invalid_default_ai_message': '預設 AI「{default_ai}」未有正確設定。\n\n你想唔想轉用「{first_ai}」？', # The default AI "{default_ai}" is not properly configured.\n\nWould you like to switch to "{first_ai}" instead?
            'switch_to_ai': '轉用 {ai}', # Switch to {ai}
            'keep_current': '保持目前', # Keep Current
            'prompt_template': '提示詞範本', # Prompt Template
            'ask_prompts': '發問提示詞', # Ask Prompts
            'random_questions_prompts': '隨機問題提示詞', # Random Questions Prompts
            'display': '顯示', # Display
            'export_settings': '導出設定', # Export Settings
            'enable_default_export_folder': '導出到預設資料夾', # Export to default folder
            'no_folder_selected': '未揀資料夾', # No folder selected
            'browse': '瀏覽...', # Browse...
            'select_export_folder': '揀導出資料夾', # Select Export Folder

            # Button text and menu items
            'copy_response_btn': '複製答案', # Copy Answer
            'copy_qa_btn': '複製問答', # Copy Q&A
            'export_current_btn': '導出問答為 PDF', # Export Q&A as PDF
            'export_history_btn': '導出歷史紀錄為 PDF', # Export History as PDF
            'copy_mode_response': '答案', # Answer
            'copy_mode_qa': '問答', # Q&A
            'copy_format_plain': '純文字', # Plain Text
            'copy_format_markdown': 'Markdown', # Markdown
            'export_mode_current': '目前問答', # Current Q&A
            'export_mode_history': '歷史紀錄', # History

            # PDF Export related
            'model_provider': '服務供應商', # Provider
            'model_name': '模型', # Model
            'model_api_url': 'API 基礎 URL', # API Base URL
            'pdf_model_info': 'AI 模型資訊', # AI Model Information
            'pdf_software': '軟件', # Software

            # UI - 對話框元素
            'input_placeholder': '輸入你嘅問題...', # Type your question...
            'response_placeholder': '答案就嚟喇...', # Response soon... (colloquial)

            # UI - 菜單項
            'menu_title': '問 AI', # Ask
            'menu_ask': '發問', # Ask

            # UI - 狀態信息
            'loading': '載入中', # Loading
            'loading_text': '正在查詢', # Asking
            'loading_models_text': '正在載入模型', # Loading models
            'save_success': '設定已儲存', # Settings saved
            'sending': '傳送中...', # Sending...
            'requesting': '請求中', # Requesting
            'formatting': '請求成功，正在格式化', # Request successful, formatting

            # UI - 模型列表功能
            'load_models': '載入模型', # Load Models
            'load_models_list': '載入模型列表', # Load Model List
            'test_current_model': '測試目前模型', # Test Current Model
            'use_custom_model': '使用自訂模型名稱', # Use custom model name
            'custom_model_placeholder': '輸入自訂模型名稱', # Enter custom model name
            'model_placeholder': '請先載入模型', # Please load models first
            'models_loaded': '成功載入 {count} 個模型', # Successfully loaded {count} models
            'models_loaded_with_selection': '成功載入 {count} 個模型。\n已選模型：{model}', # Successfully loaded {count} models.\nSelected model: {model}
            'load_models_failed': '載入模型失敗：{error}', # Failed to load models: {error}
            'model_list_not_supported': '呢個服務供應商唔支援自動獲取模型列表', # This provider does not support automatic model list fetching
            'api_key_required': '請先輸入 API 金鑰', # Please enter API Key first
            'invalid_params': '無效參數', # Invalid parameters
            'warning': '警告', # Warning
            'success': '成功', # Success
            'error': '錯誤', # Error

            # 元數據字段
            'metadata_title': '標題', # Title
            'metadata_authors': '作者', # Author
            'metadata_publisher': '出版社', # Publisher
            'metadata_pubdate': '出版日期', # Publication Date
            'metadata_pubyear': '出版年份', # Publication Date
            'metadata_language': '語言', # Language
            'metadata_series': '系列', # Series
            'no_metadata': '無元數據', # No metadata
            'no_series': '無系列', # No series
            'unknown': '未知', # Unknown

            # 多書功能
            'books_unit': ' 本書', # books
            'new_conversation': '新對話', # New Conversation
            'single_book': '單本書', # Single Book
            'multi_book': '多本書', # Multi-Book
            'deleted': '已刪除', # Deleted
            'history': '歷史紀錄', # History
            'no_history': '暫無歷史紀錄', # No history records
            'empty_question_placeholder': '（無問題）', # (No question)
            'history_ai_unavailable': '呢個 AI 已經喺設定入面移除咗', # This AI has been removed from configuration
            'clear_current_book_history': '清除目前書籍歷史紀錄', # Clear Current Book History
            'confirm_clear_book_history': '你確定要清除以下書籍嘅所有歷史紀錄咩？\n{book_titles}', # Are you sure you want to clear all history for:\n{book_titles}?
            'confirm': '確認', # Confirm
            'history_cleared': '已清除 {deleted_count} 條歷史紀錄。', # {deleted_count} history records cleared.
            'multi_book_template_label': '多書提示詞範本：', # Multi-Book Prompt Template:
            'multi_book_placeholder_hint': '用 {books_metadata} 代表書籍資料，{query} 代表用戶問題', # Use {books_metadata} for book information, {query} for user question

            # 錯誤消息
            'network_error': '連線錯誤', # Connection error
            'request_timeout': '請求逾時', # Request timeout
            'request_failed': '請求失敗', # Request failed
            'request_stopped': '請求已停止', # Request stopped
            'question_too_long': '問題太長', # Question too long
            'auth_token_required_title': '需要 AI 服務', # AI Service Required
            'auth_token_required_message': '請喺插件設定中設定有效嘅 AI 服務。', # Please configure a valid AI service in Plugin Configuration.
            'open_configuration': '打開設定', # Open Configuration
            'error_preparing_request': '準備請求失敗', # Request preparation failed
            'empty_suggestion': '空白建議', # Empty suggestion
            'process_suggestion_error': '處理建議時出錯', # Suggestion processing error
            'unknown_error': '未知錯誤', # Unknown error
            'unknown_model': '未知模型: {model_name}', # Unknown model: {model_name}
            'suggestion_error': '建議錯誤', # Suggestion error
            'random_question_success': '隨機問題生成成功！', # Random question generated successfully!
            'book_title_check': '需要書籍標題', # Book title required
            'avoid_repeat_question': '請用唔同嘅問題', # Please use a different question
            'empty_answer': '空白答案', # Empty answer
            'invalid_response': '無效回應', # Invalid response
            'auth_error_401': '未授權', # Unauthorized
            'auth_error_403': '存取被拒絕', # Access denied
            'rate_limit': '太多請求', # Too many requests
            'empty_response': '從 API 收到空白回應', # Received empty response from API
            'empty_response_after_filter': '過濾後回應為空白', # Response is empty after filtering think tags
            'no_response': '無回應', # No response
            'template_error': '範本錯誤', # Template error
            'no_model_configured': '未設定 AI 模型。請喺設定中設定 AI 模型。', # No AI model configured. Please configure an AI model in settings.
            'no_ai_configured_title': '未設定 AI', # No AI Configured
            'no_ai_configured_message': '歡迎使用！要開始問書嘅問題，你首先要設定一個 AI 服務供應商。\n\n好消息：呢個插件而家有免費方案（Nvidia AI Free），你可以即刻用，唔使任何設定！\n\n其他推薦選項：\n• Nvidia AI - 只要有手機號碼就可以免費試用 6 個月 API（唔使信用卡）\n• Ollama - 喺你部電腦度本地運行 AI 模型（完全免費同私隱）\n\n你而家想唔想打開插件設定嚟設定 AI 服務供應商呀？', # No AI Configured message (colloquial)
            'open_settings': '插件設定', # Plugin Configuration
            'ask_anyway': '照問', # Ask Anyway
            'later': '稍後', # Later
            'debug_settings': '偵錯設定', # Debug Settings
            'enable_debug_logging': '啟用偵錯日誌 (ask_ai_plugin_debug.log)', # Enable debug logging (ask_ai_plugin_debug.log)
            'debug_logging_hint': '禁用後，偵錯日誌將唔會寫入文件。咁樣可以防止日誌文件變得太大。', # When disabled, debug logs will not be written to file. This can prevent the log file from growing too large.
            'reset_all_data': '重設所有資料', # Reset All Data
            'reset_all_data_warning': '呢個操作會刪除所有 API 金鑰、提示詞範本同本地歷史紀錄。你嘅語言偏好會保留。請小心操作。', # This will delete all API Keys, prompt templates, and local history records. Your language preference will be preserved. Please proceed with caution.
            'reset_all_data_confirm_title': '確認重設', # Confirm Reset
            'reset_all_data_confirm_message': '你確定要將插件重設為初始狀態咩？\n\n呢個操作會永久刪除：\n• 所有 API 金鑰\n• 所有自訂提示詞範本\n• 所有對話歷史紀錄\n• 所有插件設定（語言偏好會保留）\n\n呢個動作唔可以還原㗎！', # Are you sure you want to reset the plugin to its initial state?\n\nThis will permanently delete:\n• All API Keys\n• All custom prompt templates\n• All conversation history\n• All plugin settings (language preference will be preserved)\n\nThis action cannot be undone!
            'reset_all_data_success': '所有插件資料已成功重設。請重新啟動 calibre 咁啲更改先會生效。', # All plugin data has been reset successfully. Please restart calibre for changes to take effect.
            'reset_all_data_failed': '重設插件資料失敗：{error}', # Failed to reset plugin data: {error}
            'random_question_error': '生成隨機問題時出錯', # Error generating random question
            'clear_history_failed': '清除歷史失敗', # Failed to clear history
            'clear_history_not_supported': '暫時唔支援清除單本書嘅歷史紀錄', # Clear history for single book is not supported yet
            'missing_required_config': '缺少必要嘅設定：「{key}」。請檢查你嘅設定。', # Missing required configuration: {key}. Please check your settings.
            'api_key_too_short': 'API 金鑰太短。請檢查並輸入完整嘅金鑰。', # API Key is too short. Please check and enter the complete key.

            # API響應處理
            'api_request_failed': 'API 請求失敗：{error}', # API request failed: {error}
            'api_content_extraction_failed': '無法從 API 回應中提取內容', # Unable to extract content from API response
            'api_invalid_response': '無法獲取有效嘅 API 回應', # Unable to get valid API response
            'api_unknown_error': '未知錯誤：{error}', # Unknown error: {error}

            # 流式響應處理
            'stream_response_code': '串流回應狀態碼：{code}', # Stream response status code: {code}
            'stream_continue_prompt': '請繼續你上一個答案，唔好重複已經講過嘅內容。', # Please continue your previous answer without repeating content already provided.
            'stream_continue_code_blocks': '你上一個答案有啲未關閉嘅程式碼區塊。請繼續並完成呢啲程式碼區塊。', # Your previous answer had unclosed code blocks. Please continue and complete these code blocks.
            'stream_continue_parentheses': '你上一個答案有啲未關閉嘅括號。請繼續並確保所有括號都正確關閉。', # Your previous answer had unclosed parentheses. Please continue and ensure all parentheses are properly closed.
            'stream_continue_interrupted': '你上一個答案好似俾人打斷咗。請繼續完成你最後一個諗法或者解釋。', # Your previous answer seems to have been interrupted. Please continue completing your last thought or explanation.
            'stream_timeout_error': '串流傳輸 60 秒都無收到新內容，可能係連線問題。', # Stream transmission has not received new content for 60 seconds, possibly a connection issue.

            # API錯誤消息
            'api_version_model_error': 'API 版本或模型名稱錯誤：{message}\n\n請喺設定中將 API 基礎 URL 更新為「{base_url}」，並將模型更新為「{model}」或者其他可用嘅模型。', # API version or model name error: {message}\n\nPlease update API Base URL to "{base_url}" and model to "{model}" or other available model in settings.
            'api_format_error': 'API 請求格式錯誤：{message}', # API request format error: {message}
            'api_key_invalid': 'API 金鑰無效或未授權：{message}\n\n請檢查你嘅 API 金鑰並確保已啟用 API 存取。', # API Key invalid or unauthorized: {message}\n\nPlease check your API Key and ensure API access is enabled.
            'api_rate_limit': '請求頻率超限，請稍後再試\n\n你可能已經超出咗免費使用配額。呢個可能係因為：\n1. 每分鐘請求太多\n2. 每日請求太多\n3. 每分鐘輸入令牌太多', # Request rate limit exceeded, please try again later\n\nYou may have exceeded the free usage quota. This could be due to:\n1. Too many requests per minute\n2. Too many requests per day\n3. Too many input tokens per minute

            # 配置錯誤
            'missing_config_key': '缺少必要嘅設定金鑰：「{key}」', # Missing required config key: {key}
            'api_base_url_required': '需要 API 基礎 URL', # API Base URL is required
            'model_name_required': '需要模型名稱', # Model name is required

            # 模型列表獲取
            'fetching_models_from': '正在從 {url} 獲取模型', # Fetching models from {url}
            'successfully_fetched_models': '成功獲取 {count} 個 {provider} 模型', # Successfully fetched {count} {provider} models
            'failed_to_fetch_models': '載入模型失敗：{error}', # Failed to load models: {error}
            'api_key_empty': 'API 金鑰為空白。請輸入有效嘅 API 金鑰。', # API Key is empty. Please enter a valid API Key.

            # 模型獲取錯誤信息
            'error_401': 'API 金鑰驗證失敗。請檢查：API 金鑰是否正確、帳戶餘額是否充足、API 金鑰是否已過期。', # API Key authentication failed. Please check: API Key is correct, account has sufficient balance, API Key has not expired.
            'error_403': '存取被拒絕。請檢查：API 金鑰權限是否足夠、是否有地區存取限制。', # Access denied. Please check: API Key has sufficient permissions, no regional access restrictions.
            'error_404': 'API 端點唔存在。請檢查 API 基礎 URL 設定是否正確。', # API endpoint not found. Please check if the API Base URL configuration is correct.
            'error_429': '請求過於頻繁，已達到速率限制。請稍後重試。', # Too many requests, rate limit reached. Please try again later.
            'error_5xx': '伺服器錯誤。請稍後重試，或者檢查服務供應商狀態。', # Server error. Please try again later or check the service provider status.
            'error_network': '網路連線失敗。請檢查：網路連線是否正常、代理設定是否正確、防火牆設定是否允許存取。', # Network connection failed. Please check network connection, proxy settings, or firewall configuration.
            'error_unknown': '未知錯誤。', # Unknown error.
            'technical_details': '技術細節', # Technical Details
            'ollama_service_not_running': 'Ollama 服務未運行。請先啟動 Ollama 服務。', # Ollama service is not running. Please start Ollama service first.
            'ollama_service_timeout': 'Ollama 服務連線逾時。請檢查服務是否正常運行。', # Ollama service connection timeout. Please check if the service is running properly.
            'ollama_model_not_available': '模型「{model}」不可用。請檢查：\n1. 模型是否已啟動？運行：ollama run {model}\n2. 模型名稱是否正確？\n3. 模型是否已下載？運行：ollama pull {model}', # Model "{model}" is not available. Please check:\n1. Is the model started? Run: ollama run {model}\n2. Is the model name correct?\n3. Is the model downloaded? Run: ollama pull {model}
            'gemini_geo_restriction': 'Gemini API 在你所在嘅地區不可用。請嘗試：\n1. 使用 VPN 從支援嘅地區連線\n2. 使用其他 AI 服務供應商（OpenAI、Anthropic、DeepSeek 等）\n3. 喺 Google AI Studio 查看地區可用性', # Gemini API is not available in your region. Please try:\n1. Use a VPN to connect from a supported region\n2. Use other AI providers (OpenAI, Anthropic, DeepSeek, etc.)\n3. Check Google AI Studio for region availability
            'model_test_success': '模型測試成功！', # Model test successful!
            'test_model_prompt': '模型列表載入成功！你想唔想測試選中嘅模型「{model}」呀？', # Models loaded successfully! Would you like to test the selected model "{model}"?
            'test_model_button': '測試模型', # Test Model
            'skip': '跳過', # Skip

            # 關於信息
            'author_name': 'Sheldon', # Sheldon
            'user_manual': '用戶手冊', # User Manual
            'about_plugin': '關於 Ask AI 插件', # Why Ask AI Plugin?
            'learn_how_to_use': '點樣用', # How to Use
            'email': 'iMessage', # iMessage

            # 模型特定配置
            'model_display_name_grok': 'Grok(x.AI)', # Grok(x.AI)
            'model_display_name_gemini': 'Gemini(Google)', # Gemini(Google)
            'model_display_name_deepseek': 'Deepseek', # Deepseek
            'model_display_name_custom': '自訂', # Custom
            'model_enable_streaming': '啟用串流', # Enable Streaming

            # AI Switcher
            'current_ai': '目前 AI', # Current AI
            'no_configured_models': '未設定 AI - 請喺設定中設定', # No AI configured - Please configure in settings

            # 服務供應商特定資訊
            'nvidia_free_info': '💡 新用戶有 6 個月免費 API 試用 - 唔使信用卡', # New users get 6 months free API access - No credit card required

            # 通用系統消息
            'default_system_message': '你係一個書籍分析專家。你嘅任務係通過提供有見地嘅問題同分析，幫助用戶更好地理解書籍。', # You are an expert in book analysis. Your task is to help users understand books better by providing insightful questions and analysis.

            # 請求逾時設定
            'request_timeout_label': '請求逾時：', # Request Timeout:
            'seconds': '秒', # seconds
            'request_timeout_error': '請求逾時。目前逾時時間：{timeout} 秒', # Request timeout. Current timeout: {timeout} seconds

            # 並行 AI 設定
            'parallel_ai_count_label': '並行 AI 數量：', # Parallel AI Count:
            'parallel_ai_count_tooltip': '同時查詢嘅 AI 模型數量（1-2 個可用，3-4 個就嚟有）', # Number of AI models to query simultaneously (1-2 available, 3-4 coming soon)
            'parallel_ai_notice': '注意：呢個只會影響傳送問題。隨機問題永遠只會用一個 AI。', # Note: This only affects sending questions. Random questions always use a single AI.
            'suggest_maximize': '提示：最大化視窗可以更好咁睇到 3 個 AI 嘅畫面', # Tip: Maximize window for better viewing with 3 AIs
            'ai_panel_label': 'AI {index}：', # AI {index}:
            'no_ai_available': '呢個面板無可用 AI', # No AI available for this panel
            'add_more_ai_providers': '請喺設定入面添加更多 AI 服務供應商', # Please add more AI providers in settings
            'select_ai': '-- 揀 AI --', # -- Select AI --
            'select_model': '-- 揀模型 --', # -- Select Model --
            'request_model_list': '請請求模型列表', # Please request model list
            'coming_soon': '就嚟有', # Coming Soon
            'advanced_feature_tooltip': '呢個功能開發緊。請留意更新！', # This feature is under development. Stay tuned for updates!

            # AI 管理對話框
            'ai_manager_title': '管理 AI 服務供應商', # Manage AI Providers
            'add_ai_title': '新增 AI 服務供應商', # Add AI Provider
            'manage_ai_title': '管理已設定嘅 AI', # Manage Configured AI
            'configured_ai_list': '已設定嘅 AI', # Configured AI
            'available_ai_list': '可新增嘅 AI', # Available to Add
            'ai_config_panel': '設定', # Configuration
            'select_ai_to_configure': '從列表中揀一個 AI 嚟設定', # Select an AI from the list to configure
            'select_provider': '揀 AI 服務供應商', # Select AI Provider
            'select_provider_hint': '從列表中揀一個服務供應商', # Select a provider from the list
            'select_ai_to_edit': '從列表中揀一個 AI 嚟編輯', # Select an AI from the list to edit
            'set_as_default': '設為預設', # Set as Default
            'save_ai_config': '儲存', # Save
            'remove_ai_config': '移除', # Remove
            'delete_ai': '刪除', # Delete
            'add_ai_button': '新增 AI', # Add AI
            'edit_ai_button': '編輯 AI', # Edit AI
            'manage_configured_ai_button': '管理已設定嘅 AI', # Manage Configured AI
            'manage_ai_button': '管理 AI', # Manage AI
            'no_configured_ai': '未有設定任何 AI', # No AI configured yet
            'no_configured_ai_hint': '未有設定 AI，插件用唔到。請點擊「新增 AI」嚟添加一個 AI 服務供應商。', # No AI configured. Plugin cannot work. Please click "Add AI" to add an AI provider.
            'default_ai_label': '預設 AI：', # Default AI:
            'default_ai_tag': '預設', # Default
            'ai_not_configured_cannot_set_default': '呢個 AI 未設定好。請先儲存設定。', # This AI is not configured yet. Please save the configuration first.
            'ai_set_as_default_success': '「{name}」已設為預設 AI。', # {name} has been set as the default AI.
            'ai_config_saved_success': '「{name}」設定已成功儲存。', # {name} configuration saved successfully.
            'confirm_remove_title': '確認移除', # Confirm Remove
            'confirm_remove_ai': '你確定要移除「{name}」咩？呢個會清除 API 金鑰並重設設定。', # Are you sure you want to remove {name}? This will clear the API key and reset the configuration.
            'confirm_delete_title': '確認刪除', # Confirm Delete
            'confirm_delete_ai': '你確定要刪除「{name}」咩？', # Are you sure you want to delete {name}?
            'api_key_required': 'API 金鑰係必需嘅。', # API Key is required.
            'configuration': '設定', # Configuration

            # 字段說明
            'api_key_desc': '你用於身份驗證嘅 API 金鑰。請妥善保管，唔好分享。', # Your API key for authentication. Keep it secure and do not share.
            'base_url_desc': 'API 端點 URL。除非你有自訂端點，否則用預設值。', # The API endpoint URL. Use default unless you have a custom endpoint.
            'model_desc': '從列表中揀一個模型，或者用自訂模型名稱。', # Select a model from the list or use a custom model name.
            'streaming_desc': '啟用實時回應串流，可以更快咁得到回覆。', # Enable real-time response streaming for faster feedback.
            'advanced_section': '進階', # Advanced

            # 服務供應商特定提示
            'perplexity_model_notice': '注意：Perplexity 冇提供公開嘅模型列表 API，所以模型係硬編碼嘅。', # Note: Perplexity does not provide a public model list API, so models are hardcoded.
            'ollama_no_api_key_notice': '注意：Ollama 係一個本地模型，唔需要 API 金鑰。', # Note: Ollama is a local model that does not require an API key.
            'nvidia_free_credits_notice': '注意：新用戶有免費 API 額度 - 唔使信用卡。', # Note: New users get free API credits - No credit card required.

            # Nvidia 免費方案錯誤消息
            'free_tier_rate_limit': '免費方案請求頻率超限。請稍後再試或者設定你自己嘅 Nvidia API 金鑰。', # Free tier rate limit exceeded. Please try again later or configure your own Nvidia API Key.
            'free_tier_unavailable': '免費方案暫時不可用。請稍後再試或者設定你自己嘅 Nvidia API 金鑰。', # Free tier is temporarily unavailable. Please try again later or configure your own Nvidia API Key.
            'free_tier_server_error': '免費方案伺服器錯誤。請稍後再試。', # Free tier server error. Please try again later.
            'free_tier_error': '免費方案錯誤', # Free tier error

            # Nvidia 免費方案供應商資訊
            'free': '免費', # Free
            'nvidia_free_provider_name': 'Nvidia AI（免費）', # Nvidia AI (Free)
            'nvidia_free_display_name': 'Nvidia AI（免費）', # Nvidia AI (Free)
            'nvidia_free_api_key_info': '將會從伺服器獲取', # Will be obtained from server
            'nvidia_free_desc': '呢個服務由開發者維護，保持免費，但可能冇咁穩定。如果想要更穩定嘅服務，請設定你自己嘅 Nvidia API 金鑰。', # This service is maintained by the developer and kept free, but may be less stable. For more stable service, please configure your own Nvidia API Key.

            # Nvidia 免費方案首次使用提醒
            'nvidia_free_first_use_title': '歡迎使用 Ask AI 插件', # Welcome to Ask AI Plugin
            'nvidia_free_first_use_message': '而家你可以唔使任何設定就咁問問題！開發者為你提供咗一個免費方案，但可能冇咁穩定。享受啦！\n\n你可以喺設定入面設定你自己嘅 AI 服務供應商，以獲得更穩定嘅服務。', # Now you can just ask without any configuration! The developer maintains a free tier for you, but it may not be very stable. Enjoy!\n\nYou can configure your own AI providers in the settings for better stability.

            # 模型按鈕
            'refresh_model_list': '刷新', # Refresh
            'test_current_model': '測試', # Test
            'testing_text': '測試中', # Testing
            'refresh_success': '模型列表刷新成功。', # Model list refreshed successfully.
            'refresh_failed': '刷新模型列表失敗。', # Failed to refresh model list.
            'test_failed': '模型測試失敗。', # Model test failed.

            # 工具提示
            'manage_ai_disabled_tooltip': '請先新增 AI 服務供應商。', # Please add an AI provider first.

            # PDF 導出部分標題
            'pdf_book_metadata': '書籍元數據', # BOOK METADATA
            'pdf_question': '問題', # QUESTION
            'pdf_answer': '答案', # ANSWER
            'pdf_ai_model_info': 'AI 模型資訊', # AI MODEL INFORMATION
            'pdf_generated_by': '生成自', # GENERATED BY
            'pdf_provider': '服務供應商', # Provider
            'pdf_model': '模型', # Model
            'pdf_api_base_url': 'API 基礎 URL', # API Base URL
            'pdf_panel': '面板', # Panel
            'pdf_plugin': '插件', # Plugin
            'pdf_github': 'GitHub', # GitHub
            'pdf_software': '軟件', # Software
            'pdf_generated_time': '生成時間', # Generated Time
            'pdf_info_not_available': '資訊不可用', # Information not available
        }