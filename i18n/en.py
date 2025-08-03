#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
English language translations for Ask Grok plugin.
"""

from ..models.base import BaseTranslation, TranslationRegistry, AIProvider


@TranslationRegistry.register
class EnglishTranslation(BaseTranslation):
    """English language translation."""
    
    @property
    def code(self) -> str:
        return "en"
    
    @property
    def name(self) -> str:
        return "English"
    
    @property
    def default_template(self) -> str:
        return 'About the book "{title}": Author: {author}, Publisher: {publisher}, Publication Year: {pubyear}, book in language: {language}, Series: {series}, My question is: {query}'
    
    @property
    def suggestion_template(self) -> str:
        return """You are an expert book reviewer. For the book "{title}" by {author}, publish language is {language}, generate ONE insightful question that helps readers better understand the book's core ideas, practical applications, or unique perspectives. Rules: 1. Return ONLY the question, without any introduction or explanation 2. Focus on the book's substance, not just its title 3. Make the question practical and thought-provoking 4. Keep it concise (30-200 words) 5. Be creative and generate a different question each time, even for the same book"""
    
    @property
    def translations(self) -> dict:
        return {
            # Plugin information
            'plugin_name': 'Ask Grok',
            'plugin_desc': 'Ask questions about a book using AI',
            
            # UI - Tabs and sections
            'config_title': 'Configuration',
            'general_tab': 'General',
            'ai_models': 'AI',
            'shortcuts': 'Shortcuts',
            'about': 'About',
            'metadata': 'Metadata',
            
            # UI - Buttons and actions
            'ok_button': 'OK',
            'save_button': 'Save',
            'send_button': 'Send',
            'suggest_button': 'Random Question',
            'copy_response': 'Copy Response',
            'copy_question_response': 'Copy Q&&A',
            'copied': 'Copied!',
            'close_button': 'Close',
            
            # UI - Configuration fields
            'token_label': 'API Key:',
            'api_key_label': 'API Key:',
            'model_label': 'Model:',
            'language_label': 'Language:',
            'language_label_old': 'Language',
            'base_url_label': 'Base URL:',
            'base_url_placeholder': 'Default: {default_api_base_url}',
            'shortcut': 'Shortcuts Key',
            'shortcut_open_dialog': 'Open Dialog',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Model',
            'current_ai': 'Current AI:',
            'action': 'Action',
            'reset_button': 'Reset',
            'prompt_template': 'Prompt Template',
            'ask_prompts': 'Ask Prompts',
            'random_questions_prompts': 'Random Questions Prompts',
            'display': 'Display',
            
            # UI - Dialog elements
            'input_placeholder': 'Type your question...',
            'response_placeholder': 'Response soon...',  # 用于所有模型的占位符
            
            # UI - Menu items
            'menu_title': 'Ask',
            'menu_ask': 'Ask {model}',  # 用于所有模型的菜单项
            
            # UI - Status messages
            'loading': 'Loading',
            'loading_text': 'Asking',
            'save_success': 'Settings saved',
            'sending': 'Sending...',
            'requesting': 'Requesting',
            'formatting': 'Request successful, formatting',
            
            # Metadata fields
            'metadata_title': 'Title',
            'metadata_authors': 'Author',
            'metadata_publisher': 'Publisher',
            'metadata_pubyear': 'Publication Date',
            'metadata_language': 'Language',
            'metadata_series': 'Series',
            'no_metadata': 'No metadata',
            'no_series': 'No series',
            'unknown': 'Unknown',
            
            # Error messages
            'error': 'Error: ',  # 同时用于error_prefix
            'network_error': 'Connection error',
            'request_timeout': 'Request timeout',
            'request_failed': 'Request failed',
            'question_too_long': 'Question too long',
            'auth_token_required_title': 'API Key Required',
            'auth_token_required_message': 'Please set API key in settings',
            'error_preparing_request': 'Request preparation failed',
            'empty_suggestion': 'Empty suggestion',
            'process_suggestion_error': 'Suggestion processing error',
            'unknown_error': 'Unknown error',
            'unknown_model': 'Unknown model: {model_name}',
            'suggestion_error': 'Suggestion error',
            'book_title_check': 'Book title required',
            'avoid_repeat_question': 'Please use a different question',
            'empty_answer': 'Empty answer',
            'invalid_response': 'Invalid response',
            'auth_error_401': 'Unauthorized',
            'auth_error_403': 'Access denied',
            'rate_limit': 'Too many requests',
            'invalid_json': 'Invalid JSON',
            'no_response': 'No response',
            'template_error': 'Template error',
            'no_model_configured': 'No AI model configured. Please configure an AI model in settings.',
            'random_question_error': 'Error generating random question',
            'clear_history_failed': 'Failed to clear history',
            'clear_history_not_supported': 'Clear history for single book is not supported yet',
            
            # About information
            'author_name': 'Sheldon',
            'user_manual': 'User Manual',
            'about_plugin': 'Why Ask Grok?',
            'learn_how_to_use': 'How to Use',
            'email': 'iMessage',
            
            # Model specific configurations
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Custom',
        }
