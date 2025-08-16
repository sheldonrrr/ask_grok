#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Russian language translations for Ask Grok plugin.
"""

from ..models.base import BaseTranslation, TranslationRegistry, AIProvider


@TranslationRegistry.register
class RussianTranslation(BaseTranslation):
    """Russian language translation."""
    
    @property
    def code(self) -> str:
        return "ru"
    
    @property
    def name(self) -> str:
        return "Русский"
    
    @property
    def default_template(self) -> str:
        return 'О книге "{title}": Автор: {author}, Издательство: {publisher}, Год издания: {pubyear}, книга на language: {language}, Серия: {series}, Мой вопрос: {query}'
    
    @property
    def suggestion_template(self) -> str:
        return """Вы эксперт в области рецензий на книги. Для книги "{title}" автора {author}, публикация язык {language}, сгенерируйте ОДИН проницательный вопрос, который поможет читателям лучше понять книгу. Правила: 1. Верните ТОЛЬКО вопрос, без введения или объяснения 2. Сосредоточьтесь на содержании книги, а не только на названии 3. Сделайте вопрос практичным и провокационным 4. Сдерживайте его кратким (30-200 слов) 5. Будьте креативны и генерируйте разные вопросы каждый раз, даже для одной и той же книги"""
    
    @property
    def translations(self) -> dict:
        return {
            # Информация о плагине
            'plugin_name': 'Ask Grok',
            'plugin_desc': 'Задавайте вопросы о книге с помощью ИИ',
            
            # UI - Вкладки и разделы
            'config_title': 'Конфигурация',
            'general_tab': 'Общие',
            'ai_models': 'ИИ',
            'shortcuts': 'Горячие клавиши',
            'about': 'О программе',
            'metadata': 'Метаданные',
            
            # UI - Кнопки и действия
            'ok_button': 'OK',
            'save_button': 'Сохранить',
            'send_button': 'Отправить',
            'suggest_button': 'Случайный вопрос',
            'copy_response': 'Копировать ответ',
            'copy_question_response': 'Копировать В&&О',
            'copied': 'Скопировано!',
            'saved': 'Сохранено',
            'close_button': 'Закрыть',
            
            # UI - Поля конфигурации
            'token_label': 'Ключ API:',
            'model_label': 'Модель:',
            'language_label': 'Язык',
            'base_url_label': 'Базовый URL:',
            'base_url_placeholder': 'По умолчанию: {default_api_base_url}',
            'shortcut': 'Горячая клавиша',
            'shortcut_open_dialog': 'Открыть диалог',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Модель',
            'current_ai': 'Текущий ИИ:',
            'action': 'Действие',
            'reset_button': 'Сброс',
            'prompt_template': 'Шаблон подсказки',
            'ask_prompts': 'Подсказки для вопросов',
            'random_questions_prompts': 'Подсказки для случайных вопросов',
            'display': 'Отображение',
            
            # UI - Элементы диалога
            'input_placeholder': 'Введите ваш вопрос...',
            'response_placeholder': 'Ответ скоро появится...',
            
            # UI - Пункты меню
            'menu_title': 'Спросить',
            'menu_ask': 'Спросить {model}',
            
            # UI - Сообщения о состоянии
            'loading': 'Загрузка',
            'loading_text': 'Задаю вопрос',
            'save_success': 'Настройки сохранены',
            'sending': 'Отправка...',
            'requesting': 'Запрос',
            'formatting': 'Запрос успешен, форматирование',
            
            # Поля метаданных
            'metadata_title': 'Название',
            'metadata_authors': 'Автор',
            'metadata_publisher': 'Издательство',
            'metadata_pubyear': 'Дата публикации',
            'metadata_language': 'Язык',
            'metadata_series': 'Серия',
            'no_metadata': 'Нет метаданных',
            'no_series': 'Нет серии',
            'unknown': 'Неизвестно',
            
            # Сообщения об ошибках
            'error': 'Ошибка: ',
            'network_error': 'Ошибка соединения',
            'request_timeout': 'Тайм-аут запроса',
            'request_failed': 'Запрос не удался',
            'question_too_long': 'Вопрос слишком длинный',
            'auth_token_required_title': 'Требуется ключ API',
            'auth_token_required_message': 'Пожалуйста, установите ключ API в настройках',
            'error_preparing_request': 'Ошибка подготовки запроса',
            'empty_suggestion': 'Пустое предложение',
            'process_suggestion_error': 'Ошибка обработки предложения',
            'unknown_error': 'Неизвестная ошибка',
            'unknown_model': 'Неизвестная модель: {model_name}',
            'suggestion_error': 'Ошибка предложения',
            'random_question_success': 'Случайный вопрос успешно сгенерирован!',
            'book_title_check': 'Требуется название книги',
            'avoid_repeat_question': 'Пожалуйста, используйте другой вопрос',
            'empty_answer': 'Пустой ответ',
            'invalid_response': 'Недействительный ответ',
            'auth_error_401': 'Не авторизован',
            'auth_error_403': 'Доступ запрещен',
            'rate_limit': 'Слишком много запросов',
            'invalid_json': 'Недействительный JSON',
            'no_response': 'Нет ответа',
            'template_error': 'Ошибка шаблона',
            'no_model_configured': 'Не настроена модель ИИ. Пожалуйста, настройте модель ИИ в настройках.',
            'random_question_error': 'Ошибка при генерации случайного вопроса',
            'clear_history_failed': 'Не удалось очистить историю',
            'clear_history_not_supported': 'Очистка истории для одной книги пока не поддерживается',
            'missing_required_config': 'Отсутствует обязательная конфигурация: {key}. Проверьте ваши настройки.',
            'api_key_too_short': 'Ключ API слишком короткий. Проверьте и введите полный ключ.',
            
            # Обработка ответов API
            'api_request_failed': 'Запрос API не удался: {error}',
            'api_content_extraction_failed': 'Не удалось извлечь содержимое из ответа API',
            'api_invalid_response': 'Не получен действительный ответ API',
            'api_unknown_error': 'Неизвестная ошибка: {error}',
            
            # Обработка потоковых ответов
            'stream_response_code': 'Код статуса потокового ответа: {code}',
            'stream_continue_prompt': 'Продолжите свой предыдущий ответ, не повторяя уже предоставленное содержимое.',
            'stream_continue_code_blocks': 'В вашем предыдущем ответе были незакрытые блоки кода. Продолжите и завершите эти блоки кода.',
            'stream_continue_parentheses': 'В вашем предыдущем ответе были незакрытые скобки. Продолжите и убедитесь, что все скобки правильно закрыты.',
            'stream_continue_interrupted': 'Кажется, ваш предыдущий ответ был прерван. Продолжите и завершите свою последнюю мысль или объяснение.',
            'stream_timeout_error': 'Потоковая передача не получала нового содержимого в течение 60 секунд, возможно, проблема с соединением.',
            
            # Сообщения об ошибках API
            'api_version_model_error': 'Ошибка версии API или названия модели: {message}\n\nОбновите базовый URL API на "{base_url}" и модель на "{model}" или другую доступную модель в настройках.',
            'api_format_error': 'Ошибка формата запроса API: {message}',
            'api_key_invalid': 'Недействительный или неавторизованный ключ API: {message}\n\nПроверьте свой ключ API и убедитесь, что доступ к API включен.',
            'api_rate_limit': 'Превышен лимит запросов, попробуйте позже\n\nВозможно, вы превысили свою бесплатную квоту использования. Это может быть связано с:\n1. Слишком много запросов в минуту\n2. Слишком много запросов в день\n3. Слишком много входных токенов в минуту',
            
            # Ошибки конфигурации
            'missing_config_key': 'Отсутствует обязательный ключ конфигурации: {key}',
            'api_base_url_required': 'Требуется базовый URL API',
            'model_name_required': 'Требуется название модели',
            'api_key_empty': 'Ключ API пуст. Введите действительный ключ API.',
            
            # Информация о программе
            'author_name': 'Sheldon',
            'user_manual': 'Руководство пользователя',
            'about_plugin': 'Почему Ask Grok?',
            'learn_how_to_use': 'Как пользоваться',
            'email': 'iMessage',
            
            # Конфигурации специфичные для модели
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Пользовательский',
            'model_enable_streaming': 'Включить потоковую передачу',
            'model_disable_ssl_verify': 'Отключить проверку SSL',
            
            # Общие системные сообщения
            'default_system_message': 'Вы эксперт по анализу книг. Ваша задача - помочь пользователям лучше понять книги, предоставляя проницательные вопросы и анализ.',
        }
