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
        }
