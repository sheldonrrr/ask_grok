#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
English language translations for Ask AI Plugin.
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
    def multi_book_default_template(self) -> str:
        return """Here is information about multiple books: {books_metadata} User question: {query} Please answer the question based on the above book information."""
    
    @property
    def translations(self) -> dict:
        return {
            # Plugin information
            'plugin_name': 'Ask AI Plugin',
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
            'stop_button': 'Stop',
            'suggest_button': 'Random Question',
            'copy_response': 'Copy Response',
            'copy_question_response': 'Copy Q&&A',
            'export_pdf': 'Export PDF',
            'export_current_qa': 'Export Current Q&A',
            'export_history': 'Export History',
            'export_all_history_dialog_title': 'Export All History to PDF',
            'export_all_history_title': 'ALL Q&A HISTORY',
            'export_history_insufficient': 'Need at least 2 history records to export.',
            'history_record': 'Record',
            'question_label': 'Question',
            'answer_label': 'Answer',
            'default_ai': 'Default AI',
            'export_time': 'Exported at',
            'total_records': 'Total Records',
            'info': 'Information',
            'yes': 'Yes',
            'no': 'No',
            'no_book_selected_title': 'No Book Selected',
            'no_book_selected_message': 'Please select a book before asking questions.',
            'set_default_ai_title': 'Set Default AI',
            'set_default_ai_message': 'You have switched to "{0}". Would you like to set it as the default AI for future queries?',
            'set_default_ai_success': 'Default AI has been set to "{0}".',
            'copied': 'Copied!',
            'pdf_exported': 'PDF Exported!',
            'export_pdf_dialog_title': 'Export to PDF',
            'export_pdf_error': 'Failed to export PDF: {0}',
            'no_question': 'No question',
            'no_response': 'No response',
            'saved': 'Saved',
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
            'action': 'Action',
            'reset_button': 'Reset to Default',
            'reset_current_ai': 'Reset Current AI to Default',
            'reset_ai_confirm_title': 'Confirm Reset',
            'reset_ai_confirm_message': 'About to reset {ai_name} to default state.\n\nThis will clear:\n• API Key\n• Custom model name\n• Other configured parameters\n\nContinue?',
            'reset_tooltip': 'Reset current AI to default values',
            'unsaved_changes_title': 'Unsaved Changes',
            'unsaved_changes_message': 'You have unsaved changes. What would you like to do?',
            'save_and_close': 'Save and Close',
            'discard_changes': 'Discard Changes',
            'cancel': 'Cancel',
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
            'loading': 'Loading...',
            'loading_text': 'Asking',
            'save_success': 'Settings saved',
            'sending': 'Sending...',
            'requesting': 'Requesting',
            'formatting': 'Request successful, formatting',
            
            # UI - Model list feature
            'load_models': 'Load Model List',
            'test_current_model': 'Test Current Model',
            'use_custom_model': 'Use custom model name',
            'custom_model_placeholder': 'Enter custom model name',
            'model_placeholder': 'Please load models first',
            'models_loaded': 'Successfully loaded {count} models',
            'load_models_failed': 'Failed to load models: {error}',
            'model_list_not_supported': 'This provider does not support automatic model list fetching',
            'api_key_required': 'Please enter API Key first',
            'invalid_params': 'Invalid parameters',
            'warning': 'Warning',
            'success': 'Success',
            'error': 'Error',
            
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
            
            # Multi-book feature
            'books_unit': ' books',
            'new_conversation': 'New Conversation',
            'single_book': 'Single Book',
            'multi_book': 'Multi-Book',
            'deleted': 'Deleted',
            'history': 'History',
            'no_history': 'No history records',
            'clear_current_book_history': 'Clear Current Book History',
            'confirm_clear_book_history': 'Are you sure you want to clear all history for:\n{book_titles}?',
            'confirm': 'Confirm',
            'success': 'Success',
            'history_cleared': '{deleted_count} history records cleared.',
            'multi_book_template_label': 'Multi-Book Prompt Template:',
            'multi_book_placeholder_hint': 'Use {books_metadata} for book information, {query} for user question',
            
            # Error messages (Note: 'error' is already defined above, these are other error types)
            'network_error': 'Connection error',
            'request_timeout': 'Request timeout',
            'request_failed': 'Request failed',
            'question_too_long': 'Question too long',
            'auth_token_required_title': 'AI Service Required',
            'auth_token_required_message': 'Please configure a valid AI service in Plugin Configuration.',
            'open_configuration': 'Open Configuration',
            'cancel': 'Cancel',
            'error_preparing_request': 'Request preparation failed',
            'empty_suggestion': 'Empty suggestion',
            'process_suggestion_error': 'Suggestion processing error',
            'unknown_error': 'Unknown error',
            'unknown_model': 'Unknown model: {model_name}',
            'suggestion_error': 'Suggestion error',
            'random_question_success': 'Random question generated successfully!',
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
            'no_ai_configured_title': 'No AI Configured',
            'no_ai_configured_message': 'Welcome! To start asking questions about your books, you need to configure an AI provider first.\n\nRecommended for Beginners:\n• Nvidia AI - Get 6 months FREE API access with just your phone number (no credit card required)\n• Ollama - Run AI models locally on your computer (completely free and private)\n\nWould you like to open the plugin configuration to set up an AI provider now?',
            'open_settings': 'Plugin Configuration',
            'ask_anyway': 'Ask Anyway',
            'later': 'Later',
            'reset_all_data': 'Reset All Data',
            'reset_all_data_warning': 'This will delete all API Keys, prompt templates, and local history records. Your language preference will be preserved. Please proceed with caution.',
            'reset_all_data_confirm_title': 'Confirm Reset',
            'reset_all_data_confirm_message': 'Are you sure you want to reset the plugin to its initial state?\n\nThis will permanently delete:\n• All API Keys\n• All custom prompt templates\n• All conversation history\n• All plugin settings (language preference will be preserved)\n\nThis action cannot be undone!',
            'reset_all_data_success': 'All plugin data has been reset successfully. Please restart calibre for changes to take effect.',
            'reset_all_data_failed': 'Failed to reset plugin data: {error}',
            'random_question_error': 'Error generating random question',
            'clear_history_failed': 'Failed to clear history',
            'clear_history_not_supported': 'Clear history for single book is not supported yet',
            'missing_required_config': 'Missing required configuration: {key}. Please check your settings.',
            'api_key_too_short': 'API Key is too short. Please check and enter the complete key.',
            
            # API response handling
            'api_request_failed': 'API request failed: {error}',
            'api_content_extraction_failed': 'Unable to extract content from API response',
            'api_invalid_response': 'Unable to get valid API response',
            'api_unknown_error': 'Unknown error: {error}',
            
            # Stream response handling
            'stream_response_code': 'Stream response status code: {code}',
            'stream_continue_prompt': 'Please continue your previous answer without repeating content already provided.',
            'stream_continue_code_blocks': 'Your previous answer had unclosed code blocks. Please continue and complete these code blocks.',
            'stream_continue_parentheses': 'Your previous answer had unclosed parentheses. Please continue and ensure all parentheses are properly closed.',
            'stream_continue_interrupted': 'Your previous answer seems to have been interrupted. Please continue completing your last thought or explanation.',
            'stream_timeout_error': 'Stream transmission has not received new content for 60 seconds, possibly a connection issue.',
            
            # API error messages
            'api_version_model_error': 'API version or model name error: {message}\n\nPlease update API Base URL to "{base_url}" and model to "{model}" or other available model in settings.',
            'api_format_error': 'API request format error: {message}',
            'api_key_invalid': 'API Key invalid or unauthorized: {message}\n\nPlease check your API Key and ensure API access is enabled.',
            'api_rate_limit': 'Request rate limit exceeded, please try again later\n\nYou may have exceeded the free usage quota. This could be due to:\n1. Too many requests per minute\n2. Too many requests per day\n3. Too many input tokens per minute',
            
            # Configuration errors
            'missing_config_key': 'Missing required config key: {key}',
            'api_base_url_required': 'API Base URL is required',
            'model_name_required': 'Model name is required',
            
            # Model list fetching
            'fetching_models_from': 'Fetching models from {url}',
            'successfully_fetched_models': 'Successfully fetched {count} {provider} models',
            'failed_to_fetch_models': 'Failed to load models: {error}',
            'api_key_empty': 'API Key is empty. Please enter a valid API Key.',
            
            # Error messages for model fetching
            'error_401': 'API Key authentication failed. Please check: API Key is correct, account has sufficient balance, API Key has not expired.',
            'error_403': 'Access denied. Please check: API Key has sufficient permissions, no regional access restrictions.',
            'error_404': 'API endpoint not found. Please check if the API Base URL configuration is correct.',
            'error_429': 'Too many requests, rate limit reached. Please try again later.',
            'error_5xx': 'Server error. Please try again later or check the service provider status.',
            'error_network': 'Network connection failed. Please check network connection, proxy settings, or firewall configuration.',
            'error_unknown': 'Unknown error.',
            'technical_details': 'Technical Details',
            'ollama_service_not_running': 'Ollama service is not running. Please start Ollama service first.',
            'ollama_service_timeout': 'Ollama service connection timeout. Please check if the service is running properly.',
            'ollama_model_not_available': 'Model "{model}" is not available. Please check:\n1. Is the model started? Run: ollama run {model}\n2. Is the model name correct?\n3. Is the model downloaded? Run: ollama pull {model}',
            'model_test_success': 'Model test successful! Configuration saved.',
            'test_model_prompt': 'Models loaded successfully! Would you like to test the selected model "{model}"?',
            'test_model_button': 'Test Model',
            'skip': 'Skip',
            
            # About information
            'author_name': 'Sheldon',
            'user_manual': 'User Manual',
            'about_plugin': 'Why Ask AI Plugin?',
            'learn_how_to_use': 'How to Use',
            'email': 'iMessage',
            
            # Model specific configurations
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Custom',
            'model_enable_streaming': 'Enable Streaming',
            
            # AI Switcher
            'current_ai': 'Current AI',
            'no_configured_models': 'No AI configured - Please configure in settings',
            
            # Provider specific info
            'nvidia_free_info': '💡 New users get 6 months free API access - No credit card required',
            
            # Common system messages
            'default_system_message': 'You are an expert in book analysis. Your task is to help users understand books better by providing insightful questions and analysis.',
            
            # Request timeout settings
            'request_timeout_label': 'Request Timeout:',
            'seconds': 'seconds',
            'request_timeout_error': 'Request timeout. Current timeout: {timeout} seconds',
            
            # Parallel AI settings
            'parallel_ai_count_label': 'Parallel AI Count:',
            'parallel_ai_count_tooltip': 'Number of AI models to query simultaneously (1-2 available, 3-4 coming soon)',
            'parallel_ai_notice': 'Note: This only affects sending questions. Random questions always use a single AI.',
            'suggest_maximize': 'Tip: Maximize window for better viewing with 3 AIs',
            'ai_panel_label': 'AI {index}:',
            'no_ai_available': 'No AI available for this panel',
            'add_more_ai_providers': 'Please add more AI providers in settings',
            'select_ai': '-- Select AI --',
            'select_model': '-- Select Model --',
            'request_model_list': 'Please request model list',
            'coming_soon': 'Coming Soon',
            'advanced_feature_tooltip': 'This feature is under development. Stay tuned for updates!',
            
            # PDF export section titles
            'pdf_book_metadata': 'BOOK METADATA',
            'pdf_question': 'QUESTION',
            'pdf_answer': 'ANSWER',
            'pdf_ai_model_info': 'AI MODEL INFORMATION',
            'pdf_generated_by': 'GENERATED BY',
            'pdf_provider': 'Provider',
            'pdf_model': 'Model',
            'pdf_api_base_url': 'API Base URL',
            'pdf_panel': 'Panel',
            'pdf_plugin': 'Plugin',
            'pdf_github': 'GitHub',
            'pdf_software': 'Software',
            'pdf_generated_time': 'Generated Time',
            'pdf_info_not_available': 'Information not available',
        }
