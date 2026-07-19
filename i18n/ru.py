#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Russian language translations for Ask AI Plugin.
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
        return 'Контекст: Вы помогаете пользователю calibre (http://calibre-ebook.com), мощного приложения для управления электронными книгами, через плагин "Ask AI Plugin". Этот плагин позволяет пользователям задавать вопросы о книгах в их библиотеке calibre. Примечание: Этот плагин может отвечать только на вопросы о содержании, темах или связанных темах выбранной книги - он не может напрямую изменять метаданные книги или выполнять операции calibre. Информация о книге: Название: "{title}", Автор: {author}, Издательство: {publisher}, Год публикации: {pubyear}, Язык: {language}, Серия: {series}. Вопрос пользователя: {query}. Пожалуйста, предоставьте полезный ответ на основе информации о книге и ваших знаний.'

    @property
    def suggestion_template(self) -> str:
        return """Вы эксперт по книжным рецензиям. Для книги "{title}" автора {author}, язык публикации: {language}, сгенерируйте ОДИН проницательный вопрос, который поможет читателям лучше понять основные идеи книги, практические применения или уникальные перспективы. Правила: 1. Возвращайте ТОЛЬКО вопрос, без вступления или объяснения 2. Сосредоточьтесь на содержании книги, а не только на ее названии 3. Сделайте вопрос практичным и заставляющим задуматься 4. Будьте лаконичны (30-200 слов) 5. Проявляйте креативность и генерируйте новый вопрос каждый раз, даже для одной и той же книги"""

    @property
    def multi_book_default_template(self) -> str:
        return """Вот информация о нескольких книгах: {books_metadata} Вопрос пользователя: {query} Пожалуйста, ответьте на вопрос, основываясь на приведенной выше информации о книгах."""

    @property
    def translations(self) -> dict:
        return {
            # Plugin information
            'plugin_name': 'Плагин "Спросить ИИ"',
            'plugin_desc': 'Задавайте вопросы о книге с помощью ИИ',

            # UI - Tabs and sections
            'config_title': 'Настройки',
            'general_tab': 'Общие',
            'ai_models': 'Провайдеры ИИ',
            'shortcuts': 'Горячие клавиши',
            'shortcuts_note': "Вы можете настроить эти горячие клавиши в calibre: Настройки -> Горячие клавиши (поиск 'Ask AI').\nЭта страница показывает горячие клавиши по умолчанию/примеры. Если вы изменили их в Горячих клавишах, настройки calibre имеют приоритет.",
            'prompts_tab': 'Промпты',
            'about': 'О программе',
            'metadata': 'Метаданные',

            # Section subtitles
            'language_settings': 'Язык',
            'language_subtitle': 'Выберите предпочитаемый язык интерфейса',
            'ai_providers_subtitle': 'Настройте провайдеров ИИ и выберите ИИ по умолчанию',
            'prompts_subtitle': 'Настройте способ отправки вопросов в ИИ',
            'export_settings_subtitle': 'Установите папку по умолчанию для экспорта PDF',
            'reset_all_data_subtitle': 'Внимание: Это навсегда удалит все ваши настройки и данные',

            # Prompts tab
            'language_preference_title': 'Языковые предпочтения',
            'language_preference_subtitle': 'Контролировать, должны ли ответы ИИ соответствовать языку вашего интерфейса',
            'prompt_templates_title': 'Шаблоны промптов',
            'prompt_templates_subtitle': 'Настройте, как информация о книге отправляется в ИИ, используя динамические поля, такие как {title}, {author}, {query}',
            'ask_prompts': 'Промпты для вопросов',
            'random_questions_prompts': 'Промпты для случайных вопросов',
            'multi_book_prompts_label': 'Промпты для нескольких книг',
            'multi_book_placeholder_hint': 'Используйте {books_metadata} для информации о книге, {query} для вопроса пользователя',
            'dynamic_fields_title': 'Справочник динамических полей',
            'dynamic_fields_subtitle': 'Доступные поля и примеры значений из "Франкенштейна" Мэри Шелли',
            'dynamic_fields_examples': '<b>{title}</b> → Франкенштейн<br><b>{author}</b> → Мэри Шелли<br><b>{publisher}</b> → Lackington, Hughes, Harding, Mavor & Jones<br><b>{pubyear}</b> → 1818<br><b>{language}</b> → Английский<br><b>{series}</b> → (нет)<br><b>{query}</b> → Ваш текст вопроса',
            'reset_prompts': 'Сбросить промпты до значений по умолчанию',
            'reset_prompts_confirm': 'Вы уверены, что хотите сбросить все шаблоны промптов до их значений по умолчанию? Это действие нельзя отменить.',
            'unsaved_changes_title': 'Несохраненные изменения',
            'unsaved_changes_message': 'У вас есть несохраненные изменения на вкладке "Промпты". Вы хотите их сохранить?',
            'use_interface_language': 'Всегда просить ИИ отвечать на текущем языке интерфейса плагина',
            'language_instruction_label': 'Языковая инструкция, добавленная в промпты:',
            'language_instruction_text': 'Пожалуйста, ответьте на {language_name}.',

            # Persona settings
            'persona_title': 'Персона',
            'persona_subtitle': 'Определите свой исследовательский опыт и цели, чтобы помочь ИИ предоставлять более релевантные ответы',
            'use_persona': 'Использовать персону',
            'persona_label': 'Персона',
            'persona_placeholder': 'Как исследователь, я хочу изучать данные книг.',
            'persona_hint': 'Чем больше ИИ знает о вашей цели и фоне, тем лучше будет исследование или генерация.',

            # UI - Buttons and actions
            'ok_button': 'ОК',
            'save_button': 'Сохранить',
            'send_button': 'Отправить',
            'stop_button': 'Остановить',
            'suggest_button': 'Случайный вопрос',
            'copy_response': 'Копировать ответ',
            'copy_question_response': 'Копировать В&О',
            'export_pdf': 'Экспорт в PDF',
            'export_current_qa': 'Экспорт текущего В&О',
            'export_history': 'Экспорт истории',
            'export_all_history_dialog_title': 'Экспорт всей истории в PDF',
            'export_all_history_title': 'ВСЯ ИСТОРИЯ В&О',
            'export_history_insufficient': 'Требуется не менее 2 записей истории для экспорта.',
            'history_record': 'Запись',
            'question_label': 'Вопрос',
            'answer_label': 'Ответ',
            'default_ai': 'ИИ по умолчанию',
            'export_time': 'Экспортировано в',
            'total_records': 'Всего записей',
            'info': 'Информация',
            'yes': 'Да',
            'no': 'Нет',
            'no_book_selected_title': 'Книга не выбрана',
            'no_book_selected_message': 'Пожалуйста, выберите книгу, прежде чем задавать вопросы.',
            'set_default_ai_title': 'Установить ИИ по умолчанию',
            'set_default_ai_message': 'Вы переключились на "{0}". Хотите установить его в качестве ИИ по умолчанию для будущих запросов?',
            'set_default_ai_success': 'ИИ по умолчанию установлено "{0}".',
            'default_ai_mismatch_title': 'ИИ по умолчанию изменен',
            'default_ai_mismatch_message': 'ИИ по умолчанию в конфигурации был изменен на "{default_ai}",\nно текущий диалог использует "{current_ai}".\n\nВы хотите переключиться на новый ИИ по умолчанию?',
            'copied': 'Скопировано!',
            'pdf_exported': 'PDF экспортирован!',
            'export_pdf_dialog_title': 'Экспорт в PDF',
            'export_pdf_error': 'Не удалось экспортировать PDF: {0}',
            'no_question': 'Нет вопроса',
            'no_response': 'Нет ответа',
            'saved': 'Сохранено',
            'close_button': 'Закрыть',
            'open_local_tutorial': 'Открыть локальное руководство',
            'tutorial_open_failed': 'Не удалось открыть руководство',
            'tutorial': 'Руководство',

            'model_display_name_perplexity': 'Perplexity',

            # UI - Configuration fields
            'token_label': 'Ключ API:',
            'api_key_label': 'Ключ API:',
            'model_label': 'Модель:',
            'language_label': 'Язык:',
            'language_label_old': 'Язык',
            'base_url_label': 'Базовый URL:',
            'base_url_placeholder': 'По умолчанию: {default_api_base_url}',
            'shortcut': 'Горячая клавиша',
            'shortcut_open_dialog': 'Открыть диалог',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Модель',
            'action': 'Действие',
            'reset_button': 'Сбросить до значений по умолчанию',
            'reset_current_ai': 'Сбросить текущий ИИ до значений по умолчанию',
            'reset_ai_confirm_title': 'Подтвердить сброс',
            'reset_ai_confirm_message': 'Будет сброшен {ai_name} до состояния по умолчанию.\n\nЭто очистит:\n• Ключ API\n• Пользовательское имя модели\n• Другие настроенные параметры\n\nПродолжить?',
            'reset_tooltip': 'Сбросить текущий ИИ до значений по умолчанию',
            'unsaved_changes_title': 'Несохраненные изменения',
            'unsaved_changes_message': 'У вас есть несохраненные изменения. Что вы хотите сделать?',
            'save_and_close': 'Сохранить и закрыть',
            'discard_changes': 'Отменить изменения',
            'cancel': 'Отмена',
            'yes_button': 'Да',
            'no_button': 'Нет',
            'cancel_button': 'Отмена',
            'invalid_default_ai_title': 'Неверный ИИ по умолчанию',
            'invalid_default_ai_message': 'ИИ по умолчанию "{default_ai}" настроен неправильно.\n\nХотите переключиться на "{first_ai}"?',
            'switch_to_ai': 'Переключиться на {ai}',
            'keep_current': 'Оставить текущий',
            'prompt_template': 'Шаблон промпта',
            'ask_prompts': 'Промпты для вопросов',
            'random_questions_prompts': 'Промпты для случайных вопросов',
            'display': 'Отображение',
            'export_settings': 'Настройки экспорта',
            'enable_default_export_folder': 'Экспортировать в папку по умолчанию',
            'no_folder_selected': 'Папка не выбрана',
            'browse': 'Обзор...',
            'select_export_folder': 'Выбрать папку для экспорта',

            # Button text and menu items
            'copy_response_btn': 'Копировать ответ',
            'copy_qa_btn': 'Копировать В&О',
            'export_current_btn': 'Экспорт В&О в PDF',
            'export_history_btn': 'Экспорт истории в PDF',
            'copy_mode_response': 'Ответ',
            'copy_mode_qa': 'В&О',
            'copy_format_plain': 'Простой текст',
            'copy_format_markdown': 'Markdown',
            'export_mode_current': 'Текущий В&О',
            'export_mode_history': 'История',

            # PDF Export related
            'model_provider': 'Провайдер',
            'model_name': 'Модель',
            'model_api_url': 'Базовый URL API',
            'pdf_model_info': 'Информация о модели ИИ',
            'pdf_software': 'Программное обеспечение',

            # UI - Dialog elements
            'input_placeholder': 'Введите ваш вопрос...',
            'response_placeholder': 'Ответ скоро...',  # Placeholder for all models

            # UI - Menu items
            'menu_title': 'Спросить ИИ',
            'menu_ask': 'Спросить',

            # UI - Status information
            'loading': 'Загрузка',
            'loading_text': 'Запрашиваю',
            'loading_models_text': 'Загрузка моделей',
            'save_success': 'Настройки сохранены',
            'sending': 'Отправка...',
            'requesting': 'Запрос',
            'formatting': 'Запрос успешен, форматирование',

            # UI - Model list feature
            'load_models': 'Загрузить модели',
            'load_models_list': 'Загрузить список моделей',
            'test_current_model': 'Проверить текущую модель',
            'use_custom_model': 'Использовать пользовательское имя модели',
            'custom_model_placeholder': 'Введите пользовательское имя модели',
            'model_placeholder': 'Пожалуйста, сначала загрузите модели',
            'models_loaded': 'Успешно загружено {count} моделей',
            'models_loaded_with_selection': 'Успешно загружено {count} моделей.\nВыбранная модель: {model}',
            'load_models_failed': 'Не удалось загрузить модели: {error}',
            'model_list_not_supported': 'Этот провайдер не поддерживает автоматическое получение списка моделей',
            'api_key_required': 'Пожалуйста, сначала введите ключ API',
            'invalid_params': 'Неверные параметры',
            'warning': 'Предупреждение',
            'success': 'Успешно',
            'error': 'Ошибка',
            'error_opening_dialog': 'Ошибка при открытии диалога:',
            'skipped_books_warning': 'Пропущено {count} книг(и) из-за ошибок доступа к файлам.\nЭто может быть вызвано недопустимыми символами в путях к файлам или блокировкой файлов другой программой.',
            'failed_to_read_all_books': 'Не удалось прочитать метаданные для всех выбранных книг.\nЭто может быть вызвано недопустимыми символами в путях к файлам или блокировкой файлов другой программой.',
            'error_starting_request': 'Ошибка при запуске запроса',
            'default_ai_mismatch_title': 'ИИ по умолчанию изменён',
            'default_ai_mismatch_message': 'ИИ по умолчанию в настройках был изменён на "{default_ai}",\nно текущий диалог использует "{current_ai}".\n\nХотите переключиться на новый ИИ по умолчанию?',

            # Metadata fields
            'metadata_title': 'Название',
            'metadata_authors': 'Автор',
            'metadata_publisher': 'Издательство',
            'metadata_pubdate': 'Дата публикации',
            'metadata_pubyear': 'Год публикации',
            'metadata_language': 'Язык',
            'metadata_series': 'Серия',
            'no_metadata': 'Нет метаданных',
            'no_series': 'Нет серии',
            'unknown': 'Неизвестно',

            # Multi-book feature
            'books_unit': ' книг',
            'new_conversation': 'Новый разговор',
            'single_book': 'Одна книга',
            'multi_book': 'Несколько книг',
            'deleted': 'Удалено',
            'history': 'История',
            'no_history': 'Нет записей истории',
            'empty_question_placeholder': '(Нет вопроса)',
            'history_ai_unavailable': 'Этот ИИ был удален из конфигурации',
            'clear_current_book_history': 'Очистить историю текущей книги',
            'confirm_clear_book_history': 'Вы уверены, что хотите очистить всю историю для:\n{book_titles}?',
            'confirm': 'Подтвердить',
            'history_cleared': 'Удалено {deleted_count} записей истории.',
            'multi_book_template_label': 'Шаблон промпта для нескольких книг:',
            'multi_book_placeholder_hint': 'Используйте {books_metadata} для информации о книге, {query} для вопроса пользователя',

            # Error messages (Note: 'error' is already defined above, these are other error types)
            'network_error': 'Ошибка соединения',
            'request_timeout': 'Таймаут запроса',
            'request_failed': 'Запрос не выполнен',
            'request_stopped': 'Запрос остановлен',
            'question_too_long': 'Вопрос слишком длинный',
            'question_too_long_detail': (
                'Подсказка слишком длинная ({current} символов, лимит {limit}, превышение на {over}). '
                'Вы выбрали {book_count} книг(и).'
            ),
            'question_too_long_detail_library': (
                'Подсказка слишком длинная ({current} символов, лимит {limit}, превышение на {over}). '
                'В индексе библиотеки {book_count} книг(и).'
            ),
            'question_too_long_hint_ai_search': (
                'Для поиска по всей библиотеке используйте AI Search (задавайте вопрос без выбора книг '
                'или через меню AI Search), а не выбирайте много книг сразу.'
            ),
            'question_too_long_hint_library_search': (
                'Индекс библиотеки превышает текущий лимит подсказки. Включите пользовательский лимит длины '
                'в Настройках плагина → General (рекомендуется: 524288 символов) или задайте более конкретный вопрос.'
            ),
            'question_too_long_reduce_books': (
                'Для глубокого сравнения меньшего набора попробуйте снять выбор примерно с {count} книг(и).'
            ),
            'question_too_long_hint_default': (
                'Текущий лимит по умолчанию: {limit} символов ({mode}). '
                'Для одной книги по умолчанию 128 000; для нескольких — 256 000. '
                'Опытные пользователи могут включить пользовательский лимит в Настройках плагина → General.'
            ),
            'question_too_long_hint_custom': (
                'Вы включили пользовательский лимит подсказки. Если запросы завершаются по таймауту, '
                'уменьшите лимит в Настройках плагина → General или сократите выбор книг / уточните запрос.'
            ),
            'large_selection_dialog_title': 'Выбрано много книг',
            'large_selection_dialog_message': (
                'Вы выбрали {count} книг. Для вопросов по всей библиотеке лучше подходит AI Search — '
                'он ищет по всей библиотеке в компактном формате метаданных.\n\n'
                'Переключиться на AI Search или продолжить с выбранными книгами в компактном формате?'
            ),
            'large_selection_use_ai_search': 'Использовать AI Search',
            'large_selection_continue': 'Продолжить с выбором',
            'multi_book_truncation_note': (
                'Примечание: из-за лимита подсказки включены только первые {included} из {total} выбранных книг. '
                'Используйте AI Search для запроса ко всей библиотеке или увеличьте пользовательский лимит '
                'в Настройках плагина → General.'
            ),
            'library_metadata_truncation_note': (
                'Примечание: из-за лимита подсказки включены только первые {included} из {total} проиндексированных книг. '
                'Результаты могут быть неполными для очень больших библиотек, если не увеличить пользовательский лимит '
                'в Настройках плагина → General.'
            ),
            'auth_token_required_title': 'Требуется служба ИИ',
            'auth_token_required_message': 'Пожалуйста, настройте действующую службу ИИ в конфигурации плагина.',
            'open_configuration': 'Открыть настройки',
            'error_preparing_request': 'Не удалось подготовить запрос',
            'empty_suggestion': 'Пустое предложение',
            'process_suggestion_error': 'Ошибка обработки предложения',
            'unknown_error': 'Неизвестная ошибка',
            'unknown_model': 'Неизвестная модель: {model_name}',
            'suggestion_error': 'Ошибка предложения',
            'random_question_success': 'Случайный вопрос сгенерирован успешно!',
            'book_title_check': 'Требуется название книги',
            'avoid_repeat_question': 'Пожалуйста, используйте другой вопрос',
            'empty_answer': 'Пустой ответ',
            'invalid_json': 'Неверный JSON',
            'invalid_response': 'Неверный ответ',
            'auth_error_401': 'Не авторизован',
            'auth_error_403': 'Доступ запрещен',
            'rate_limit': 'Слишком много запросов',
            'empty_response': 'Получен пустой ответ от API',
            'empty_response_after_filter': 'Ответ пуст после фильтрации тегов мышления',
            'no_response': 'Нет ответа',
            'template_error': 'Ошибка шаблона',
            'no_model_configured': 'Не настроена модель ИИ. Пожалуйста, настройте модель ИИ в настройках.',
            'no_ai_configured_title': 'ИИ не настроен',
            'no_ai_configured_message': 'Добро пожаловать! Чтобы начать задавать вопросы о ваших книгах, вам нужно сначала настроить провайдера ИИ.\n\nХорошие новости: Этот плагин теперь имеет БЕСПЛАТНЫЙ уровень (Nvidia AI Free), который вы можете использовать немедленно без какой-либо настройки!\n\nДругие рекомендуемые варианты:\n• Nvidia AI - Получите 6 месяцев БЕСПЛАТНОГО доступа к API только по номеру телефона (кредитная карта не требуется)\n• Ollama - Запускайте модели ИИ локально на вашем компьютере (полностью бесплатно и конфиденциально)\n\nХотите открыть настройки плагина для настройки провайдера ИИ прямо сейчас?',
            'open_settings': 'Настройки плагина',
            'ask_anyway': 'Все равно спросить',
            'later': 'Позже',
            'reset_all_data': 'Сбросить все данные',
            'reset_all_data_warning': 'Это удалит все ключи API, шаблоны промптов и локальные записи истории. Ваши языковые предпочтения будут сохранены. Пожалуйста, действуйте осторожно.',
            'reset_all_data_confirm_title': 'Подтвердить сброс',
            'reset_all_data_confirm_message': 'Вы уверены, что хотите сбросить плагин в его исходное состояние?\n\nЭто навсегда удалит:\n• Все ключи API\n• Все пользовательские шаблоны промптов\n• Всю историю разговоров\n• Все настройки плагина (языковые предпочтения будут сохранены)\n\nЭто действие нельзя отменить!',
            'reset_all_data_success': 'Все данные плагина успешно сброшены. Пожалуйста, перезапустите calibre, чтобы изменения вступили в силу.',
            'reset_all_data_failed': 'Не удалось сбросить данные плагина: {error}',
            'random_question_error': 'Ошибка при генерации случайного вопроса',
            'clear_history_failed': 'Не удалось очистить историю',
            'clear_history_not_supported': 'Очистка истории для одной книги пока не поддерживается',
            'missing_required_config': 'Отсутствует обязательная конфигурация: {key}. Пожалуйста, проверьте свои настройки.',
            'api_key_too_short': 'Ключ API слишком короткий. Пожалуйста, проверьте и введите полный ключ.',

            # API response handling
            'api_request_failed': 'Запрос API не выполнен: {error}',
            'api_content_extraction_failed': 'Не удалось извлечь содержимое из ответа API',
            'api_invalid_response': 'Не удалось получить действительный ответ API',
            'api_unknown_error': 'Неизвестная ошибка: {error}',

            # Stream response handling
            'stream_response_code': 'Код состояния ответа потока: {code}',
            'stream_continue_prompt': 'Пожалуйста, продолжайте свой предыдущий ответ, не повторяя уже предоставленное содержание.',
            'stream_continue_code_blocks': 'В вашем предыдущем ответе были незакрытые блоки кода. Пожалуйста, продолжайте и завершите эти блоки кода.',
            'stream_continue_parentheses': 'В вашем предыдущем ответе были незакрытые скобки. Пожалуйста, продолжайте и убедитесь, что все скобки правильно закрыты.',
            'stream_continue_interrupted': 'Ваш предыдущий ответ, похоже, был прерван. Пожалуйста, продолжайте завершать свою последнюю мысль или объяснение.',
            'stream_timeout_error': 'Передача потока не получала новый контент в течение 60 секунд, возможно, проблема с соединением.',

            # API error messages
            'api_version_model_error': 'Ошибка версии API или имени модели: {message}\n\nПожалуйста, обновите базовый URL API до "{base_url}" и модель до "{model}" или другой доступной модели в настройках.',
            'api_format_error': 'Ошибка формата запроса API: {message}',
            'api_key_invalid': 'Неверный или неавторизованный ключ API: {message}\n\nПожалуйста, проверьте свой ключ API и убедитесь, что доступ к API включен.',
            'api_rate_limit': 'Превышен лимит запросов, пожалуйста, попробуйте снова позже\n\nВы могли превысить квоту бесплатного использования. Это может быть связано с:\n1. Слишком большим количеством запросов в минуту\n2. Слишком большим количеством запросов в день\n3. Слишком большим количеством входных токенов в минуту',

            # Configuration errors
            'missing_config_key': 'Отсутствует обязательный ключ конфигурации: {key}',
            'api_base_url_required': 'Требуется базовый URL API',
            'model_name_required': 'Требуется имя модели',

            # Model list fetching
            'fetching_models_from': 'Получение моделей с {url}',
            'successfully_fetched_models': 'Успешно получено {count} моделей {provider}',
            'failed_to_fetch_models': 'Не удалось загрузить модели: {error}',
            'api_key_empty': 'Ключ API пуст. Пожалуйста, введите действительный ключ API.',

            # Error messages for model fetching
            'error_401': 'Ошибка аутентификации ключа API. Пожалуйста, проверьте: ключ API верен, на счете достаточно средств, срок действия ключа API не истек.',
            'error_403': 'Доступ запрещен. Пожалуйста, проверьте: ключ API имеет достаточные разрешения, нет региональных ограничений доступа.',
            'error_404': 'Конечная точка API не найдена. Пожалуйста, проверьте правильность настройки базового URL API.',
            'error_429': 'Слишком много запросов, достигнут лимит скорости. Пожалуйста, попробуйте снова позже.',
            'error_5xx': 'Ошибка сервера. Пожалуйста, попробуйте снова позже или проверьте статус поставщика услуг.',
            'error_network': 'Сбой сетевого подключения. Пожалуйста, проверьте сетевое соединение, настройки прокси или конфигурацию брандмауэра.',
            'error_unknown': 'Неизвестная ошибка.',
            'technical_details': 'Технические детали',
            'ollama_service_not_running': 'Служба Ollama не запущена. Пожалуйста, сначала запустите службу Ollama.',
            'ollama_service_timeout': 'Таймаут подключения к службе Ollama. Пожалуйста, проверьте, работает ли служба правильно.',
            'ollama_model_not_available': 'Модель "{model}" недоступна. Пожалуйста, проверьте:\n1. Запущена ли модель? Выполните: ollama run {model}\n2. Правильно ли имя модели?\n3. Загружена ли модель? Выполните: ollama pull {model}',
            'gemini_geo_restriction': 'API Gemini недоступен в вашем регионе. Пожалуйста, попробуйте:\n1. Использовать VPN для подключения из поддерживаемого региона\n2. Использовать других провайдеров ИИ (OpenAI, Anthropic, DeepSeek и т.д.)\n3. Проверить Google AI Studio на наличие региональной доступности',
            'model_test_success': 'Тест модели успешно пройден!',
            'test_model_prompt': 'Модели успешно загружены! Хотите проверить выбранную модель "{model}"?',
            'test_model_button': 'Проверить модель',
            'skip': 'Пропустить',

            # About information
            'author_name': 'Sheldon',
            'user_manual': 'Руководство пользователя',
            'about_plugin': 'О плагине Ask AI',
            'learn_how_to_use': 'Как использовать',
            'email': 'iMessage',

            # Model specific configurations
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Пользовательский',
            'model_display_name_ollama': 'Ollama(Local)',
            'model_display_name_lmstudio': 'LM Studio(Local)',
            'model_display_name_koboldcpp': 'KoboldCpp(Local)',
            'local_openai_compat_no_api_key_notice': 'Note: This local OpenAI-compatible service usually does not require an API key. Start the local server, then refresh the model list.',
            'lmstudio_no_api_key_notice': 'Note: LM Studio uses the OpenAI-compatible API locally and usually does not require an API key.',
            'koboldcpp_no_api_key_notice': 'Note: KoboldCpp uses the OpenAI-compatible API locally and usually does not require an API key.',
            'local_service_not_running': 'Cannot connect to the local AI service. Please confirm it is running and the Base URL is correct.',
            'model_enable_streaming': 'Включить стриминг',

            # AI Switcher
            'current_ai': 'Текущий ИИ',
            'no_configured_models': 'ИИ не настроен - Пожалуйста, настройте в параметрах',

            # Provider specific info
            'nvidia_free_info': '💡 Новые пользователи получают 6 месяцев бесплатного доступа к API - Кредитная карта не требуется',

            # Common system messages
            'default_system_message': 'Вы эксперт по анализу книг. Ваша задача — помочь пользователям лучше понимать книги, предоставляя проницательные вопросы и анализ.',

            # Request timeout settings
            'request_timeout_label': 'Таймаут запроса:',
            'seconds': 'секунд',
            'request_timeout_error': 'Таймаут запроса. Текущий таймаут: {timeout} секунд',
            'enable_custom_prompt_limit_label': 'Пользовательский лимит длины подсказки',
            'enable_custom_prompt_limit_tooltip': (
                'Лимиты по умолчанию: 128 000 символов (одна книга) и 256 000 (несколько книг). '
                'Большинству пользователей менять не нужно. Для поиска по библиотеке используйте AI Search. '
                'Включайте пользовательский лимит только если модель поддерживает гораздо больший контекст и '
                'запросы всё ещё упираются в лимит.'
            ),
            'max_prompt_length_label': 'Макс. длина подсказки:',
            'max_prompt_length_unit': 'символов',
            'max_prompt_length_tooltip': (
                'Применяется при включённом пользовательском лимите. Рекомендуемое значение: 524288 символов. '
                'Ориентир: 1 токен ≈ 3–4 символа. Для Ollama также настройте num_ctx на стороне модели.'
            ),
            'max_prompt_length_normalized_title': 'Лимит подсказки скорректирован',
            'max_prompt_length_normalized': (
                'Длина подсказки нормализована до {value} символов (удалены разделители вроде запятых '
                'или пробелов).'
            ),

            # Parallel AI settings
            'parallel_ai_count_label': 'Количество параллельных ИИ:',
            'parallel_ai_count_tooltip': 'Количество моделей ИИ для одновременного запроса (1-2 доступны, 3-4 скоро)',
            'parallel_ai_notice': 'Примечание: Это влияет только на отправку вопросов. Случайные вопросы всегда используют один ИИ.',
            'suggest_maximize': 'Совет: Разверните окно для лучшего просмотра с 3 ИИ',
            'ai_panel_label': 'ИИ {index}:',
            'no_ai_available': 'ИИ недоступен для этой панели',
            'add_more_ai_providers': 'Пожалуйста, добавьте больше провайдеров ИИ в настройки',
            'select_ai': '-- Выбрать ИИ --',
            'select_model': '-- Выбрать модель --',
            'request_model_list': 'Пожалуйста, запросите список моделей',
            'coming_soon': 'Скоро',
            'advanced_feature_tooltip': 'Эта функция находится в разработке. Следите за обновлениями!',

            # AI Manager Dialog
            'ai_manager_title': 'Управление провайдерами ИИ',
            'add_ai_title': 'Добавить провайдера ИИ',
            'manage_ai_title': 'Управление настроенным ИИ',
            'configured_ai_list': 'Настроенные ИИ',
            'available_ai_list': 'Доступные для добавления',
            'ai_config_panel': 'Конфигурация',
            'select_ai_to_configure': 'Выберите ИИ из списка для настройки',
            'select_provider': 'Выбрать провайдера ИИ',
            'select_provider_hint': 'Выберите провайдера из списка',
            'select_ai_to_edit': 'Выберите ИИ из списка для редактирования',
            'set_as_default': 'Установить как по умолчанию',
            'save_ai_config': 'Сохранить',
            'remove_ai_config': 'Удалить',
            'delete_ai': 'Удалить',
            'add_ai_button': 'Добавить ИИ',
            'ai_manager_window_hint': '«Добавить / Управление» открывает изменяемое окно (можно развернуть). Двойной щелчок по ИИ — редактирование.',
            'edit_ai_button': 'Редактировать ИИ',
            'manage_configured_ai_button': 'Управление настроенным ИИ',
            'manage_ai_button': 'Управление ИИ',
            'no_configured_ai': 'ИИ еще не настроен',
            'no_configured_ai_hint': 'ИИ не настроен. Плагин не может работать. Пожалуйста, нажмите "Добавить ИИ", чтобы добавить провайдера ИИ.',
            'default_ai_label': 'ИИ по умолчанию:',
            'default_ai_tag': 'По умолчанию',
            'ai_not_configured_cannot_set_default': 'Этот ИИ еще не настроен. Пожалуйста, сначала сохраните конфигурацию.',
            'ai_set_as_default_success': '{name} установлен как ИИ по умолчанию.',
            'ai_config_saved_success': 'Конфигурация {name} успешно сохранена.',
            'confirm_remove_title': 'Подтвердить удаление',
            'confirm_remove_ai': 'Вы уверены, что хотите удалить {name}? Это очистит ключ API и сбросит конфигурацию.',
            'confirm_delete_title': 'Подтвердить удаление',
            'confirm_delete_ai': 'Вы уверены, что хотите удалить {name}?',
            'api_key_required': 'Ключ API обязателен.',
            'configuration': 'Конфигурация',

            # Field descriptions
            'api_key_desc': 'Ваш ключ API для аутентификации. Храните его в безопасности и не делитесь им.',
            'base_url_desc': 'URL конечной точки API. Используйте по умолчанию, если у вас нет пользовательской конечной точки.',
            'model_desc': 'Выберите модель из списка или используйте пользовательское имя модели.',
            'streaming_desc': 'Включить потоковую передачу ответов в реальном времени для более быстрой обратной связи.',
            'advanced_section': 'Расширенные',

            # Provider-specific notices
            'perplexity_model_notice': 'Примечание: Perplexity не предоставляет публичный API списка моделей, поэтому модели жестко закодированы.',
            'ollama_no_api_key_notice': 'Note: Ollama uses the OpenAI-compatible API locally and usually does not require an API key.',
            'nvidia_free_credits_notice': 'Примечание: Новые пользователи получают бесплатные кредиты API — кредитная карта не требуется.',

            # Nvidia Free error messages
            'free_tier_rate_limit': 'Превышен лимит запросов для бесплатного уровня. Пожалуйста, попробуйте снова позже или настройте свой собственный ключ API Nvidia.',
            'free_tier_unavailable': 'Бесплатный уровень временно недоступен. Пожалуйста, попробуйте снова позже или настройте свой собственный ключ API Nvidia.',
            'free_tier_server_error': 'Ошибка сервера бесплатного уровня. Пожалуйста, попробуйте снова позже.',
            'free_tier_error': 'Ошибка бесплатного уровня',

            # Nvidia Free provider info
            'free': 'Бесплатно',
            'nvidia_free_provider_name': 'Nvidia AI (Бесплатно)',
            'nvidia_free_display_name': 'Nvidia AI (Бесплатно)',
            'nvidia_free_api_key_info': 'Будет получен с сервера',
            'nvidia_free_desc': 'Этот сервис поддерживается разработчиком и остается бесплатным, но может быть менее стабильным. Для более стабильной работы, пожалуйста, настройте свой собственный ключ API Nvidia.',

            # Nvidia Free first use reminder
            'nvidia_free_first_use_title': 'Добро пожаловать в плагин Ask AI',
            'nvidia_free_first_use_message': 'Теперь вы можете просто спрашивать без какой-либо настройки! Разработчик поддерживает бесплатный уровень для вас, но он может быть не очень стабильным. Наслаждайтесь!\n\nВы можете настроить своих собственных провайдеров ИИ в настройках для повышения стабильности.',

            # Model buttons
            'refresh_model_list': 'Обновить',
            'test_current_model': 'Проверить',
            'testing_text': 'Тестирование',
            'refresh_success': 'Список моделей успешно обновлен.',
            'refresh_failed': 'Не удалось обновить список моделей.',
            'test_failed': 'Проверка модели не удалась.',

            # Tooltip
            'manage_ai_disabled_tooltip': 'Пожалуйста, сначала добавьте провайдера ИИ.',

            # PDF export section titles
            'pdf_book_metadata': 'МЕТАДАННЫЕ КНИГИ',
            'pdf_question': 'ВОПРОС',
            'pdf_answer': 'ОТВЕТ',
            'pdf_ai_model_info': 'ИНФОРМАЦИЯ О МОДЕЛИ ИИ',
            'pdf_generated_by': 'СГЕНЕРИРОВАНО',
            'pdf_provider': 'Провайдер',
            'pdf_model': 'Модель',
            'pdf_api_base_url': 'Базовый URL API',
            'pdf_panel': 'Панель',
            'pdf_plugin': 'Плагин',
            'pdf_github': 'GitHub',
            'pdf_software': 'Программное обеспечение',
            'pdf_generated_time': 'Время создания',
            'pdf_info_not_available': 'Информация недоступна',
            
            # Library Chat feature (v1.4.2)
            'library_tab': 'Поиск',
            'library_search': 'ИИ-поиск',
            'library_info': 'ИИ-поиск всегда включен. Когда вы не выбираете книги, вы можете искать по всей библиотеке на естественном языке.',
            'library_enable': 'Включить ИИ-поиск',
            'library_enable_tooltip': 'При включении вы можете искать в библиотеке с помощью ИИ, когда книги не выбраны',
            'library_update': 'Обновить данные библиотеки',
            'library_update_tooltip': 'Извлечь названия и авторов книг из вашей библиотеки',
            'library_updating': 'Обновление...',
            'library_status': 'Статус: {count} книг, последнее обновление: {time}',
            'library_status_empty': 'Статус: Нет данных. Нажмите "Обновить данные библиотеки" для начала.',
            'library_status_error': 'Статус: Ошибка загрузки данных',
            'library_update_success': 'Успешно обновлено {count} книг',
            'library_update_failed': 'Не удалось обновить данные библиотеки',
            'library_no_gui': 'GUI недоступен',
            'library_init_title': 'Инициализировать ИИ-поиск',
            'library_init_message': 'ИИ-поиску требуются метаданные библиотеки для работы. Хотите инициализировать сейчас?\n\nЭто извлечет названия и авторов книг из вашей библиотеки.',
            'library_init_required': 'ИИ-поиск не может быть включен без данных библиотеки. Пожалуйста, нажмите "Обновить данные библиотеки", когда будете готовы использовать эту функцию.',
            'ai_search_welcome_title': 'Добро пожаловать в ИИ-поиск',
            'ai_search_not_enough_books_title': 'Недостаточно книг',
            'ai_search_not_enough_books_message': 'Для ИИ-поиска требуется не менее {min_books} книг в вашей библиотеке.\n\nВ вашей текущей библиотеке только {book_count} книг(а).\n\nПожалуйста, добавьте больше книг, чтобы использовать ИИ-поиск.',
            'ai_search_welcome_message': 'ИИ-поиск активирован!\n\nСпособы запуска:\n• Сочетание клавиш (настраивается в параметрах)\n• Меню Инструменты → ИИ-поиск\n• Открыть диалог Ask без выбора книг\n\nВы можете искать по всей библиотеке на естественном языке. Например:\n• "Есть ли у вас книги о Python?"\n• "Покажите книги Айзека Азимова"\n• "Найдите книги о машинном обучении"\n\nИИ найдет и порекомендует подходящие книги. Нажмите на название книги, чтобы открыть её напрямую.',
            'ai_search_mode_info': 'Поиск по всей вашей библиотеке',
            'ai_search_feature_title': 'AI Search',
            'ai_search_feature_subtitle': 'Ищите по всей библиотеке на естественном языке',
            'ai_search_feature_description': (
                'AI Search помогает находить книги во всей библиотеке Calibre.\n\n'
                '• Запуск: откройте Ask без выбора книг, используйте Сервис → AI Search или сочетание клавиш\n'
                '• Как работает: плагин отправляет компактные метаданные (ID, название, автор) '
                'всех проиндексированных книг\n'
                '• Большой выбор: при выборе более 50 книг Ask предложит AI Search вместо '
                'встраивания каждой книги в подробном формате\n'
                '• Обновляйте данные: нажимайте «Обновить данные библиотеки» после добавления или удаления книг\n\n'
                'Примеры: «Найди книги о Python», «Покажи книги Айзека Азимова».'
            ),
            'ai_search_usage_hint': (
                'Совет: AI Search лучше всего подходит для поиска по всей библиотеке. Для глубокого сравнения '
                'нескольких книг выберите до 30 книг.'
            ),
            'ai_search_data_title': 'Индекс библиотеки',
            'ai_search_data_subtitle': 'Обновите компактный список книг для AI при добавлении или удалении книг',
            'library_prompt_template': 'У вас есть доступ к библиотеке книг пользователя. Вот все книги: {metadata} Запрос пользователя: {query} Пожалуйста, найдите соответствующие книги в текущей библиотеке и верните их в этом формате (**ВАЖНО**: Используйте формат HTML-ссылки, чтобы пользователи могли нажать на названия книг, чтобы открыть их напрямую): - <a href="calibre://book/BOOK_ID">Название книги</a> - Имя автора Пример: - <a href="calibre://book/123">Изучаем Python</a> - Mark Lutz - <a href="calibre://book/456">Машинное обучение в действии</a> - Peter Harrington Примечание: Некоторые авторы могут быть указаны как "unknown". Это нормальные данные, пожалуйста, верните все соответствующие результаты нормально. Возвращайте только книги, соответствующие запросу. Максимум 5 результатов.',
            'ai_search_privacy_title': 'Уведомление о конфиденциальности',
            'ai_search_privacy_alert': 'AI Поиск использует метаданные книг (названия и авторы). Эта информация будет отправлена ИИ-провайдеру, которого вы настроили для обработки поисковых запросов.',
            'ai_search_updated_info': 'Обновлено {count} книг {time_ago}',
            'ai_search_books_info': 'Индексировано {count} книг',
            'days_ago': '{n} дн. назад',
            'hours_ago': '{n} час. назад',
            'minutes_ago': '{n} мин. назад',
            'just_now': 'только что',
            
            # Statistics tab (v1.4.2)
            'stat_tab': 'Статистика',
            'stat_overview': 'Обзор',
            'stat_overview_subtitle': 'Статистика запросов к AI',
            'stat_days_unit': 'дней',
            'stat_days_label': 'Начало',
            'stat_start_at': 'Начало {date}',
            'stat_replies_unit': 'раз',
            'stat_replies_label': 'Запросы AI',
            'stat_books_unit': 'книг',
            'stat_books_label': 'Библиотека',
            'stat_no_books': 'Обновить во вкладке Поиск',
            'stat_trends': 'Тренды',
            'stat_curious_index': 'Распределение запросов AI на этой неделе',
            'stat_daily_avg': 'В среднем {n} раз в день',
            'stat_sample_data': 'Показаны примерные данные. Переключится на реальные данные после 20+ запросов',
            'stat_heatmap': 'Тепловая карта',
            'stat_heatmap_subtitle': 'Распределение запросов AI в этом месяце',
            'stat_no_data_week': 'Нет данных за эту неделю',
            'stat_no_data_month': 'Нет данных за этот месяц',
            'stat_data_not_enough': 'Недостаточно данных',
            
            # Статистические титулы пользователя (на основе количества запросов)
            'stat_title_curious': 'Листатель',
            'stat_title_explorer': 'Охотник за книгами',
            'stat_title_seeker': 'Заядлый читатель',
            'stat_title_enthusiast': 'Библиофил',
            'stat_title_pursuer': 'Книжный червь',
            
            # Оценки библиотеки (на основе размера коллекции, исторические ссылки)
            'stat_books_impressive': 'Личный кабинет',
            'stat_books_collection': 'Кабинет учёного',
            'stat_books_variety': 'Библиотека Ивана Грозного',
            'stat_books_awesome': 'Российская государственная библиотека',
            'stat_books_unbelievable': 'Александрийская библиотека',
            
            # Links (v1.4.2)
            'online_tutorial': 'Онлайн-руководство',
        }