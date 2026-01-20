#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Spanish language translations for Ask AI Plugin.
"""

from ..models.base import BaseTranslation, TranslationRegistry, AIProvider


@TranslationRegistry.register
class SpanishTranslation(BaseTranslation):
    """Spanish language translation."""
    
    @property
    def code(self) -> str:
        return "es"
    
    @property
    def name(self) -> str:
        return "Español"
    
    @property
    def default_template(self) -> str:
        return 'Contexto: Está asistiendo a un usuario de calibre (http://calibre-ebook.com), una potente aplicación de gestión de libros electrónicos, a través del plugin "Ask AI Plugin". Este plugin permite a los usuarios hacer preguntas sobre los libros de su biblioteca de calibre. Nota: Este plugin solo puede responder preguntas sobre el contenido, temas o tópicos relacionados del libro seleccionado - no puede modificar directamente los metadatos del libro ni realizar operaciones de calibre. Información del libro: Título: "{title}", Autor: {author}, Editorial: {publisher}, Año de publicación: {pubyear}, Idioma: {language}, Serie: {series}. Pregunta del usuario: {query}. Por favor, proporcione una respuesta útil basada en la información del libro y su conocimiento.'
    
    @property
    def suggestion_template(self) -> str:
        return """Eres un crítico de libros experto. Para el libro "{title}" de {author}, el idioma de publicación es {language}, genera UNA pregunta perspicaz que ayude a los lectores a comprender mejor las ideas centrales del libro, las aplicaciones prácticas o las perspectivas únicas. Reglas: 1. Devuelve SÓLO la pregunta, sin ninguna introducción o explicación 2. Concéntrate en la sustancia del libro, no solo en su título 3. Haz que la pregunta sea práctica y que invite a la reflexión 4. Mantenla concisa (30-200 palabras) 5. Sé creativo y genera una pregunta diferente cada vez, incluso para el mismo libro"""
    
    @property
    def multi_book_default_template(self) -> str:
        return """Aquí hay información sobre varios libros: {books_metadata} Pregunta del usuario: {query} Por favor, responde a la pregunta basándote en la información de los libros anterior."""
    
    @property
    def translations(self) -> dict:
        return {
            # Plugin information
            'plugin_name': 'Plugin Preguntar a la IA',
            'plugin_desc': 'Haz preguntas sobre un libro usando IA',
            
            # UI - Tabs and sections
            'config_title': 'Configuración',
            'general_tab': 'General',
            'ai_models': 'Proveedores de IA',
            'shortcuts': 'Atajos',
            'shortcuts_note': "Puedes personalizar estos atajos en calibre: Preferencias -> Atajos (busca 'Ask AI').\nEsta página muestra los atajos predeterminados/ejemplo. Si los cambiaste en Atajos, la configuración de calibre tiene prioridad.",
            'prompts_tab': 'Prompts',
            'about': 'Acerca de',
            'metadata': 'Metadatos',
            
            # Section subtitles
            'language_settings': 'Idioma',
            'language_subtitle': 'Elige tu idioma de interfaz preferido',
            'ai_providers_subtitle': 'Configura los proveedores de IA y selecciona tu IA predeterminada',
            'prompts_subtitle': 'Personaliza cómo se envían las preguntas a la IA',
            'export_settings_subtitle': 'Establece la carpeta predeterminada para exportar PDFs',
            'debug_settings_subtitle': 'Habilitar el registro de depuración para solucionar problemas',
            'reset_all_data_subtitle': '⚠️ Advertencia: Esto eliminará permanentemente todos tus ajustes y datos',
            
            # Prompts tab
            'language_preference_title': 'Preferencia de idioma',
            'language_preference_subtitle': 'Controla si las respuestas de la IA deben coincidir con el idioma de tu interfaz',
            'prompt_templates_title': 'Plantillas de Prompt',
            'prompt_templates_subtitle': 'Personaliza cómo se envía la información del libro a la IA usando campos dinámicos como {title}, {author}, {query}',
            'ask_prompts': 'Prompts de pregunta',
            'random_questions_prompts': 'Prompts de preguntas aleatorias',
            'multi_book_prompts_label': 'Prompts de varios libros',
            'multi_book_placeholder_hint': 'Usa {books_metadata} para la información del libro, {query} para la pregunta del usuario',
            'dynamic_fields_title': 'Referencia de campos dinámicos',
            'dynamic_fields_subtitle': 'Campos disponibles y valores de ejemplo de "Frankenstein" de Mary Shelley',
            'dynamic_fields_examples': '<b>{title}</b> → Frankenstein<br><b>{author}</b> → Mary Shelley<br><b>{publisher}</b> → Lackington, Hughes, Harding, Mavor & Jones<br><b>{pubyear}</b> → 1818<br><b>{language}</b> → Inglés<br><b>{series}</b> → (ninguno)<br><b>{query}</b> → Tu texto de pregunta',
            'reset_prompts': 'Restablecer prompts a los valores predeterminados',
            'reset_prompts_confirm': '¿Estás seguro de que quieres restablecer todas las plantillas de prompts a sus valores predeterminados? Esta acción no se puede deshacer.',
            'unsaved_changes_title': 'Cambios sin guardar',
            'unsaved_changes_message': 'Tienes cambios sin guardar en la pestaña Prompts. ¿Quieres guardarlos?',
            'use_interface_language': 'Pedir siempre a la IA que responda en el idioma actual de la interfaz del plugin',
            'language_instruction_label': 'Instrucción de idioma añadida a los prompts:',
            'language_instruction_text': 'Por favor, responde en {language_name}.',
            
            # Persona settings
            'persona_title': 'Persona',
            'persona_subtitle': 'Define tus antecedentes y objetivos de investigación para ayudar a la IA a proporcionar respuestas más relevantes',
            'use_persona': 'Usar persona',
            'persona_label': 'Persona',
            'persona_placeholder': 'Como investigador, quiero investigar a través de los datos del libro.',
            'persona_hint': 'Cuanto más sepa la IA sobre tu objetivo y antecedentes, mejor será la investigación o generación.',
            
            # UI - Buttons and actions
            'ok_button': 'OK',
            'save_button': 'Guardar',
            'send_button': 'Enviar',
            'stop_button': 'Detener',
            'suggest_button': 'Pregunta aleatoria',
            'copy_response': 'Copiar respuesta',
            'copy_question_response': 'Copiar P&R',
            'export_pdf': 'Exportar PDF',
            'export_current_qa': 'Exportar P&R actual',
            'export_history': 'Exportar historial',
            'export_all_history_dialog_title': 'Exportar todo el historial a PDF',
            'export_all_history_title': 'TODO EL HISTORIAL DE P&R',
            'export_history_insufficient': 'Se necesitan al menos 2 registros de historial para exportar.',
            'history_record': 'Registro',
            'question_label': 'Pregunta',
            'answer_label': 'Respuesta',
            'default_ai': 'IA predeterminada',
            'export_time': 'Exportado el',
            'total_records': 'Registros totales',
            'info': 'Información',
            'yes': 'Sí',
            'no': 'No',
            'no_book_selected_title': 'Ningún libro seleccionado',
            'no_book_selected_message': 'Por favor, selecciona un libro antes de hacer preguntas.',
            'set_default_ai_title': 'Establecer IA predeterminada',
            'set_default_ai_message': 'Has cambiado a "{0}". ¿Quieres establecerlo como la IA predeterminada para futuras consultas?',
            'set_default_ai_success': 'La IA predeterminada se ha establecido en "{0}".',
            'default_ai_mismatch_title': 'IA predeterminada cambiada',
            'default_ai_mismatch_message': 'La IA predeterminada en la configuración ha cambiado a "{default_ai}",\npero el diálogo actual está usando "{current_ai}".\n\n¿Quieres cambiar a la nueva IA predeterminada?',
            'copied': '¡Copiado!',
            'pdf_exported': '¡PDF exportado!',
            'export_pdf_dialog_title': 'Exportar a PDF',
            'export_pdf_error': 'Error al exportar PDF: {0}',
            'no_question': 'Ninguna pregunta',
            'no_response': 'Ninguna respuesta',
            'saved': 'Guardado',
            'close_button': 'Cerrar',
            'open_local_tutorial': 'Abrir tutorial local',
            'tutorial_open_failed': 'Error al abrir el tutorial',
            'tutorial': 'Tutorial',
            
            'model_display_name_perplexity': 'Perplexity',
            
            # UI - Configuration fields
            'token_label': 'Clave API:',
            'api_key_label': 'Clave API:',
            'model_label': 'Modelo:',
            'language_label': 'Idioma:',
            'language_label_old': 'Idioma',
            'base_url_label': 'URL base:',
            'base_url_placeholder': 'Predeterminado: {default_api_base_url}',
            'shortcut': 'Tecla de atajo',
            'shortcut_open_dialog': 'Abrir diálogo',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Modelo',
            'action': 'Acción',
            'reset_button': 'Restablecer a valores predeterminados',
            'reset_current_ai': 'Restablecer la IA actual a valores predeterminados',
            'reset_ai_confirm_title': 'Confirmar restablecimiento',
            'reset_ai_confirm_message': 'A punto de restablecer {ai_name} al estado predeterminado.\n\nEsto borrará:\n• Clave API\n• Nombre de modelo personalizado\n• Otros parámetros configurados\n\n¿Continuar?',
            'reset_tooltip': 'Restablecer la IA actual a valores predeterminados',
            'unsaved_changes_title': 'Cambios sin guardar',
            'unsaved_changes_message': 'Tienes cambios sin guardar. ¿Qué te gustaría hacer?',
            'save_and_close': 'Guardar y cerrar',
            'discard_changes': 'Descartar cambios',
            'cancel': 'Cancelar',
            'yes_button': 'Sí',
            'no_button': 'No',
            'cancel_button': 'Cancelar',
            'invalid_default_ai_title': 'IA predeterminada no válida',
            'invalid_default_ai_message': 'La IA predeterminada "{default_ai}" no está configurada correctamente.\n\n¿Te gustaría cambiar a "{first_ai}" en su lugar?',
            'switch_to_ai': 'Cambiar a {ai}',
            'keep_current': 'Mantener actual',
            'prompt_template': 'Plantilla de prompt',
            'ask_prompts': 'Prompts de pregunta',
            'random_questions_prompts': 'Prompts de preguntas aleatorias',
            'display': 'Mostrar',
            'export_settings': 'Configuración de exportación',
            'enable_default_export_folder': 'Exportar a carpeta predeterminada',
            'no_folder_selected': 'Ninguna carpeta seleccionada',
            'browse': 'Explorar...',
            'select_export_folder': 'Seleccionar carpeta de exportación',
            
            # Button text and menu items
            'copy_response_btn': 'Copiar respuesta',
            'copy_qa_btn': 'Copiar P&R',
            'export_current_btn': 'Exportar P&R como PDF',
            'export_history_btn': 'Exportar historial como PDF',
            'copy_mode_response': 'Respuesta',
            'copy_mode_qa': 'P&R',
            'copy_format_plain': 'Texto plano',
            'copy_format_markdown': 'Markdown',
            'export_mode_current': 'P&R actual',
            'export_mode_history': 'Historial',
            
            # PDF Export related
            'model_provider': 'Proveedor',
            'model_name': 'Modelo',
            'model_api_url': 'URL base de la API',
            'pdf_model_info': 'Información del modelo de IA',
            'pdf_software': 'Software',
            
            # UI - Dialog elements
            'input_placeholder': 'Escribe tu pregunta...',
            'response_placeholder': 'Respuesta pronto...',  # Placeholder for all models
            
            # UI - Menu items
            'menu_title': 'Preguntar a la IA',
            'menu_ask': 'Preguntar',
            
            # UI - Status information
            'loading': 'Cargando',
            'loading_text': 'Preguntando',
            'loading_models_text': 'Cargando modelos',
            'save_success': 'Configuración guardada',
            'sending': 'Enviando...',
            'requesting': 'Solicitando',
            'formatting': 'Solicitud exitosa, formateando',
            
            # UI - Model list feature
            'load_models': 'Cargar modelos',
            'load_models_list': 'Cargar lista de modelos',
            'test_current_model': 'Probar modelo actual',
            'use_custom_model': 'Usar nombre de modelo personalizado',
            'custom_model_placeholder': 'Introduce el nombre del modelo personalizado',
            'model_placeholder': 'Por favor, carga los modelos primero',
            'models_loaded': 'Se cargaron {count} modelos con éxito',
            'models_loaded_with_selection': 'Se cargaron {count} modelos con éxito.\nModelo seleccionado: {model}',
            'load_models_failed': 'Error al cargar modelos: {error}',
            'model_list_not_supported': 'Este proveedor no admite la obtención automática de la lista de modelos',
            'api_key_required': 'Por favor, introduce la clave API primero',
            'invalid_params': 'Parámetros no válidos',
            'warning': 'Advertencia',
            'success': 'Éxito',
            'error': 'Error',
            
            # Metadata fields
            'metadata_title': 'Título',
            'metadata_authors': 'Autor',
            'metadata_publisher': 'Editorial',
            'metadata_pubdate': 'Fecha de publicación',
            'metadata_pubyear': 'Año de publicación',
            'metadata_language': 'Idioma',
            'metadata_series': 'Serie',
            'no_metadata': 'Sin metadatos',
            'no_series': 'Sin serie',
            'unknown': 'Desconocido',
            
            # Multi-book feature
            'books_unit': ' libros',
            'new_conversation': 'Nueva conversación',
            'single_book': 'Libro único',
            'multi_book': 'Varios libros',
            'deleted': 'Eliminado',
            'history': 'Historial',
            'no_history': 'Sin registros de historial',
            'empty_question_placeholder': '(Sin pregunta)',
            'history_ai_unavailable': 'Esta IA ha sido eliminada de la configuración',
            'clear_current_book_history': 'Borrar historial del libro actual',
            'confirm_clear_book_history': '¿Estás seguro de que quieres borrar todo el historial para:\n{book_titles}?',
            'confirm': 'Confirmar',
            'history_cleared': '{deleted_count} registros de historial borrados.',
            'multi_book_template_label': 'Plantilla de prompt para varios libros:',
            'multi_book_placeholder_hint': 'Usa {books_metadata} para la información del libro, {query} para la pregunta del usuario',
            
            # Error messages (Note: 'error' is already defined above, these are other error types)
            'network_error': 'Error de conexión',
            'request_timeout': 'Tiempo de espera de la solicitud agotado',
            'request_failed': 'La solicitud falló',
            'request_stopped': 'Solicitud detenida',
            'question_too_long': 'Pregunta demasiado larga',
            'auth_token_required_title': 'Servicio de IA requerido',
            'auth_token_required_message': 'Por favor, configura un servicio de IA válido en la Configuración del Plugin.',
            'open_configuration': 'Abrir configuración',
            'error_preparing_request': 'Error al preparar la solicitud',
            'empty_suggestion': 'Sugerencia vacía',
            'process_suggestion_error': 'Error al procesar la sugerencia',
            'unknown_error': 'Error desconocido',
            'unknown_model': 'Modelo desconocido: {model_name}',
            'suggestion_error': 'Error de sugerencia',
            'random_question_success': '¡Pregunta aleatoria generada con éxito!',
            'book_title_check': 'Se requiere el título del libro',
            'avoid_repeat_question': 'Por favor, usa una pregunta diferente',
            'empty_answer': 'Respuesta vacía',
            'invalid_response': 'Respuesta no válida',
            'auth_error_401': 'No autorizado',
            'auth_error_403': 'Acceso denegado',
            'rate_limit': 'Demasiadas solicitudes',
            'empty_response': 'Se recibió una respuesta vacía de la API',
            'empty_response_after_filter': 'La respuesta está vacía después de filtrar las etiquetas de pensamiento',
            'no_response': 'Sin respuesta',
            'template_error': 'Error de plantilla',
            'no_model_configured': 'No hay ningún modelo de IA configurado. Por favor, configura un modelo de IA en los ajustes.',
            'no_ai_configured_title': 'Ninguna IA configurada',
            'no_ai_configured_message': '¡Bienvenido! Para empezar a hacer preguntas sobre tus libros, primero necesitas configurar un proveedor de IA.\n\nBuenas noticias: ¡Este plugin ahora tiene un nivel GRATUITO (Nvidia AI Free) que puedes usar inmediatamente sin ninguna configuración!\n\nOtras opciones recomendadas:\n• Nvidia AI - Obtén 6 meses de acceso GRATUITO a la API solo con tu número de teléfono (no se requiere tarjeta de crédito)\n• Ollama - Ejecuta modelos de IA localmente en tu ordenador (completamente gratis y privado)\n\n¿Quieres abrir la configuración del plugin para configurar un proveedor de IA ahora?',
            'open_settings': 'Configuración del plugin',
            'ask_anyway': 'Preguntar de todos modos',
            'later': 'Más tarde',
            'debug_settings': 'Ajustes de depuración',
            'enable_debug_logging': 'Habilitar registro de depuración (ask_ai_plugin_debug.log)',
            'debug_logging_hint': 'Cuando está deshabilitado, los registros de depuración no se escribirán en un archivo. Esto puede evitar que el archivo de registro crezca demasiado.',
            'reset_all_data': 'Restablecer todos los datos',
            'reset_all_data_warning': 'Esto eliminará todas las claves API, plantillas de prompts y registros de historial locales. Tu preferencia de idioma se conservará. Procede con precaución.',
            'reset_all_data_confirm_title': 'Confirmar restablecimiento',
            'reset_all_data_confirm_message': '¿Estás seguro de que quieres restablecer el plugin a su estado inicial?\n\nEsto eliminará permanentemente:\n• Todas las claves API\n• Todas las plantillas de prompts personalizadas\n• Todo el historial de conversaciones\n• Todos los ajustes del plugin (la preferencia de idioma se conservará)\n\n¡Esta acción no se puede deshacer!',
            'reset_all_data_success': 'Todos los datos del plugin se han restablecido con éxito. Por favor, reinicia calibre para que los cambios surtan efecto.',
            'reset_all_data_failed': 'Error al restablecer los datos del plugin: {error}',
            'random_question_error': 'Error al generar una pregunta aleatoria',
            'clear_history_failed': 'Error al borrar el historial',
            'clear_history_not_supported': 'Borrar historial para un solo libro aún no es compatible',
            'missing_required_config': 'Falta la configuración requerida: {key}. Por favor, revisa tus ajustes.',
            'api_key_too_short': 'La clave API es demasiado corta. Por favor, verifica e introduce la clave completa.',
            
            # API response handling
            'api_request_failed': 'La solicitud de API falló: {error}',
            'api_content_extraction_failed': 'No se pudo extraer el contenido de la respuesta de la API',
            'api_invalid_response': 'No se pudo obtener una respuesta de API válida',
            'api_unknown_error': 'Error desconocido: {error}',
            
            # Stream response handling
            'stream_response_code': 'Código de estado de la respuesta del stream: {code}',
            'stream_continue_prompt': 'Por favor, continúa tu respuesta anterior sin repetir el contenido ya proporcionado.',
            'stream_continue_code_blocks': 'Tu respuesta anterior tenía bloques de código sin cerrar. Por favor, continúa y completa estos bloques de código.',
            'stream_continue_parentheses': 'Tu respuesta anterior tenía paréntesis sin cerrar. Por favor, continúa y asegúrate de que todos los paréntesis estén correctamente cerrados.',
            'stream_continue_interrupted': 'Tu respuesta anterior parece haber sido interrumpida. Por favor, continúa completando tu última idea o explicación.',
            'stream_timeout_error': 'La transmisión en stream no ha recibido contenido nuevo durante 60 segundos, posiblemente un problema de conexión.',
            
            # API error messages
            'api_version_model_error': 'Error de versión de API o nombre de modelo: {message}\n\nPor favor, actualiza la URL base de la API a "{base_url}" y el modelo a "{model}" u otro modelo disponible en los ajustes.',
            'api_format_error': 'Error de formato de la solicitud de API: {message}',
            'api_key_invalid': 'Clave API no válida o no autorizada: {message}\n\nPor favor, verifica tu clave API y asegúrate de que el acceso a la API esté habilitado.',
            'api_rate_limit': 'Límite de frecuencia de solicitudes excedido, por favor, inténtalo de nuevo más tarde\n\nPuedes haber excedido la cuota de uso gratuito. Esto podría deberse a:\n1. Demasiadas solicitudes por minuto\n2. Demasiadas solicitudes por día\n3. Demasiados tokens de entrada por minuto',
            
            # Configuration errors
            'missing_config_key': 'Falta la clave de configuración requerida: {key}',
            'api_base_url_required': 'Se requiere la URL base de la API',
            'model_name_required': 'Se requiere el nombre del modelo',
            
            # Model list fetching
            'fetching_models_from': 'Obteniendo modelos de {url}',
            'successfully_fetched_models': 'Se obtuvieron {count} modelos de {provider} con éxito',
            'failed_to_fetch_models': 'Error al cargar modelos: {error}',
            'api_key_empty': 'La clave API está vacía. Por favor, introduce una clave API válida.',
            
            # Error messages for model fetching
            'error_401': 'La autenticación de la clave API falló. Por favor, comprueba: que la clave API sea correcta, que la cuenta tenga saldo suficiente, que la clave API no haya caducado.',
            'error_403': 'Acceso denegado. Por favor, comprueba: que la clave API tenga los permisos suficientes, que no haya restricciones de acceso regional.',
            'error_404': 'El punto final de la API no se encontró. Por favor, comprueba si la configuración de la URL base de la API es correcta.',
            'error_429': 'Demasiadas solicitudes, se alcanzó el límite de frecuencia. Por favor, inténtalo de nuevo más tarde.',
            'error_5xx': 'Error del servidor. Por favor, inténtalo de nuevo más tarde o comprueba el estado del proveedor del servicio.',
            'error_network': 'La conexión de red falló. Por favor, comprueba la conexión de red, la configuración del proxy o la configuración del firewall.',
            'error_unknown': 'Error desconocido.',
            'technical_details': 'Detalles técnicos',
            'ollama_service_not_running': 'El servicio de Ollama no se está ejecutando. Por favor, inicia el servicio de Ollama primero.',
            'ollama_service_timeout': 'Tiempo de espera de conexión del servicio de Ollama agotado. Por favor, comprueba si el servicio se está ejecutando correctamente.',
            'ollama_model_not_available': 'El modelo "{model}" no está disponible. Por favor, comprueba:\n1. ¿Está el modelo iniciado? Ejecuta: ollama run {model}\n2. ¿Es correcto el nombre del modelo?\n3. ¿Está descargado el modelo? Ejecuta: ollama pull {model}',
            'gemini_geo_restriction': 'La API de Gemini no está disponible en tu región. Por favor, intenta:\n1. Usar una VPN para conectarte desde una región compatible\n2. Usar otros proveedores de IA (OpenAI, Anthropic, DeepSeek, etc.)\n3. Comprobar Google AI Studio para la disponibilidad regional',
            'model_test_success': '¡Prueba de modelo exitosa!',
            'test_model_prompt': '¡Modelos cargados con éxito! ¿Quieres probar el modelo seleccionado "{model}"?',
            'test_model_button': 'Probar modelo',
            'skip': 'Omitir',
            
            # About information
            'author_name': 'Sheldon',
            'user_manual': 'Manual de usuario',
            'about_plugin': 'Acerca del Plugin Ask AI',
            'learn_how_to_use': 'Cómo usarlo',
            'email': 'iMessage',
            
            # Model specific configurations
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Personalizado',
            'model_enable_streaming': 'Habilitar streaming',
            
            # AI Switcher
            'current_ai': 'IA actual',
            'no_configured_models': 'Ninguna IA configurada - Por favor, configura en los ajustes',
            
            # Provider specific info
            'nvidia_free_info': '💡 Los nuevos usuarios obtienen 6 meses de acceso gratuito a la API - No se requiere tarjeta de crédito',
            
            # Common system messages
            'default_system_message': 'Eres un experto en análisis de libros. Tu tarea es ayudar a los usuarios a comprender mejor los libros proporcionando preguntas y análisis perspicaces.',
            
            # Request timeout settings
            'request_timeout_label': 'Tiempo de espera de la solicitud:',
            'seconds': 'segundos',
            'request_timeout_error': 'Tiempo de espera de la solicitud agotado. Tiempo de espera actual: {timeout} segundos',
            
            # Parallel AI settings
            'parallel_ai_count_label': 'Cantidad de IA paralelas:',
            'parallel_ai_count_tooltip': 'Número de modelos de IA a consultar simultáneamente (1-2 disponibles, 3-4 próximamente)',
            'parallel_ai_notice': 'Nota: Esto solo afecta el envío de preguntas. Las preguntas aleatorias siempre usan una sola IA.',
            'suggest_maximize': 'Consejo: Maximiza la ventana para una mejor visualización con 3 IA',
            'ai_panel_label': 'IA {index}:',
            'no_ai_available': 'Ninguna IA disponible para este panel',
            'add_more_ai_providers': 'Por favor, añade más proveedores de IA en los ajustes',
            'select_ai': '-- Seleccionar IA --',
            'select_model': '-- Seleccionar modelo --',
            'request_model_list': 'Por favor, solicita la lista de modelos',
            'coming_soon': 'Próximamente',
            'advanced_feature_tooltip': 'Esta función está en desarrollo. ¡Mantente atento a las actualizaciones!',
            
            # AI Manager Dialog
            'ai_manager_title': 'Administrar proveedores de IA',
            'add_ai_title': 'Añadir proveedor de IA',
            'manage_ai_title': 'Administrar IA configurada',
            'configured_ai_list': 'IA configurada',
            'available_ai_list': 'Disponible para añadir',
            'ai_config_panel': 'Configuración',
            'select_ai_to_configure': 'Selecciona una IA de la lista para configurar',
            'select_provider': 'Seleccionar proveedor de IA',
            'select_provider_hint': 'Selecciona un proveedor de la lista',
            'select_ai_to_edit': 'Selecciona una IA de la lista para editar',
            'set_as_default': 'Establecer como predeterminado',
            'save_ai_config': 'Guardar',
            'remove_ai_config': 'Eliminar',
            'delete_ai': 'Borrar',
            'add_ai_button': 'Añadir IA',
            'edit_ai_button': 'Editar IA',
            'manage_configured_ai_button': 'Administrar IA configurada',
            'manage_ai_button': 'Administrar IA',
            'no_configured_ai': 'Ninguna IA configurada aún',
            'no_configured_ai_hint': 'Ninguna IA configurada. El plugin no puede funcionar. Por favor, haz clic en "Añadir IA" para añadir un proveedor de IA.',
            'default_ai_label': 'IA predeterminada:',
            'default_ai_tag': 'Predeterminado',
            'ai_not_configured_cannot_set_default': 'Esta IA aún no está configurada. Por favor, guarda la configuración primero.',
            'ai_set_as_default_success': '{name} se ha establecido como la IA predeterminada.',
            'ai_config_saved_success': 'La configuración de {name} se guardó con éxito.',
            'confirm_remove_title': 'Confirmar eliminación',
            'confirm_remove_ai': '¿Estás seguro de que quieres eliminar {name}? Esto borrará la clave API y restablecerá la configuración.',
            'confirm_delete_title': 'Confirmar eliminación',
            'confirm_delete_ai': '¿Estás seguro de que quieres eliminar {name}?',
            'api_key_required': 'La clave API es obligatoria.',
            'configuration': 'Configuración',
            
            # Field descriptions
            'api_key_desc': 'Tu clave API para autenticación. Mantenla segura y no la compartas.',
            'base_url_desc': 'La URL del punto final de la API. Usa el valor predeterminado a menos que tengas un punto final personalizado.',
            'model_desc': 'Selecciona un modelo de la lista o usa un nombre de modelo personalizado.',
            'streaming_desc': 'Habilitar el streaming de respuestas en tiempo real para una retroalimentación más rápida.',
            'advanced_section': 'Avanzado',
            
            # Provider-specific notices
            'perplexity_model_notice': 'Nota: Perplexity no proporciona una API pública de lista de modelos, por lo que los modelos están codificados.',
            'ollama_no_api_key_notice': 'Nota: Ollama es un modelo local que no requiere una clave API.',
            'nvidia_free_credits_notice': 'Nota: Los nuevos usuarios obtienen créditos de API gratuitos - No se requiere tarjeta de crédito.',
            
            # Nvidia Free error messages
            'free_tier_rate_limit': 'Límite de frecuencia del nivel gratuito excedido. Por favor, inténtalo de nuevo más tarde o configura tu propia clave API de Nvidia.',
            'free_tier_unavailable': 'El nivel gratuito no está disponible temporalmente. Por favor, inténtalo de nuevo más tarde o configura tu propia clave API de Nvidia.',
            'free_tier_server_error': 'Error del servidor del nivel gratuito. Por favor, inténtalo de nuevo más tarde.',
            'free_tier_error': 'Error del nivel gratuito',
            
            # Nvidia Free provider info
            'free': 'Gratis',
            'nvidia_free_provider_name': 'Nvidia AI (Gratis)',
            'nvidia_free_display_name': 'Nvidia AI (Gratis)',
            'nvidia_free_api_key_info': 'Se obtendrá del servidor',
            'nvidia_free_desc': 'Este servicio es mantenido por el desarrollador y se mantiene gratuito, pero puede ser menos estable. Para un servicio más estable, por favor, configura tu propia clave API de Nvidia.',
            
            # Nvidia Free first use reminder
            'nvidia_free_first_use_title': 'Bienvenido al Plugin Ask AI',
            'nvidia_free_first_use_message': '¡Ahora puedes preguntar sin ninguna configuración! El desarrollador mantiene un nivel gratuito para ti, pero puede que no sea muy estable. ¡Disfrútalo!\n\nPuedes configurar tus propios proveedores de IA en los ajustes para una mayor estabilidad.',
            
            # Model buttons
            'refresh_model_list': 'Actualizar',
            'test_current_model': 'Probar',
            'testing_text': 'Probando',
            'refresh_success': 'Lista de modelos actualizada con éxito.',
            'refresh_failed': 'Error al actualizar la lista de modelos.',
            'test_failed': 'La prueba del modelo falló.',
            
            # Tooltip
            'manage_ai_disabled_tooltip': 'Por favor, añade un proveedor de IA primero.',
            
            # PDF export section titles
            'pdf_book_metadata': 'METADATOS DEL LIBRO',
            'pdf_question': 'PREGUNTA',
            'pdf_answer': 'RESPUESTA',
            'pdf_ai_model_info': 'INFORMACIÓN DEL MODELO DE IA',
            'pdf_generated_by': 'GENERADO POR',
            'pdf_provider': 'Proveedor',
            'pdf_model': 'Modelo',
            'pdf_api_base_url': 'URL base de la API',
            'pdf_panel': 'Panel',
            'pdf_plugin': 'Plugin',
            'pdf_github': 'GitHub',
            'pdf_software': 'Software',
            'pdf_generated_time': 'Hora de generación',
            'pdf_info_not_available': 'Información no disponible',
        }