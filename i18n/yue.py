#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Cantonese language translations for Ask Grok plugin.
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
    def translations(self) -> dict:
        return {
            # 插件信息
            'plugin_name': 'Ask Grok',
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
            'suggest_button': '隨機問題',
            'copy_response': '複製回答',
            'copy_question_response': '複製問答',
            'copied': '已複製！',
            
            # UI - 設定欄位
            'token_label': 'API金鑰:',
            'model_label': '模型:',
            'language_label': '語言',
            'base_url_label': '基礎URL:',
            'base_url_placeholder': '預設: {default_api_base_url}',
            'shortcut': '快捷鍵',
            'shortcut_open_dialog': '開對話框',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': '模型',
            'current_ai': '而家人工智能:',
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
            
            # 元數據欄位
            'metadata_title': '標題',
            'metadata_authors': '作者',
            'metadata_publisher': '出版社',
            'metadata_pubyear': '出版日期',
            'metadata_language': '語言',
            'metadata_series': '系列',
            'no_metadata': '冠元數據',
            'no_series': '冠系列',
            'unknown': '未知',
            
            # 錯誤消息
            'error': '錯誤: ',
            'network_error': '網絡錯誤',
            'request_timeout': '請求逾時',
            'request_failed': '請求失敗',
            'question_too_long': '問題太長',
            'auth_token_required_title': '需要API金鑰',
            'auth_token_required_message': '請在設定內設置API金鑰',
            'error_preparing_request': '準備請求時出錯',
            'empty_suggestion': '空建議',
            'process_suggestion_error': '處理建議時出錯',
            'unknown_error': '未知錯誤',
            'unknown_model': '未知模型: {model_name}',
            'suggestion_error': '建議錯誤',
            'book_title_check': '需要書名',
            'avoid_repeat_question': '請用唔同嘅問題',
            'empty_answer': '空回答',
            'invalid_response': '無效回應',
            'auth_error_401': '未授權',
            'auth_error_403': '拒絕訪問',
            'rate_limit': '請求太多',
            'invalid_json': '無效嘅JSON',
            'no_response': '冠回應',
            'template_error': '模板錯誤',
            'no_model_configured': '未設置人工智能模型。請在設定內設置人工智能模型。',
            'random_question_error': '生成隨機問題時出錯',
            'clear_history_failed': '清除歷史失敗',
            'clear_history_not_supported': '而家不支持清除單本書嘅歷史記錄',
            
            # 關於信息
            'author_name': 'Sheldon',
            'user_manual': '用戶手冊',
            'about_plugin': '為哪 Ask Grok？',
            'learn_how_to_use': '點樣用',
            'email': 'iMessage',
            
            # 模型特定設置
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': '自定義',
            'model_enable_streaming': '開啟流式傳輸',
            'model_disable_ssl_verify': '關閉SSL驗證',
        }
