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
        return 'Sobre el libro "{title}": Autor: {author}, Editorial: {publisher}, Año de publicación: {pubyear}, libro en language: {language}, Serie: {series}, Mi pregunta es: {query}'
    
    @property
    def suggestion_template(self) -> str:
        return """Eres un experto en reseñas de libros. Para el libro \"{title}\" de {author}, cuyo idioma de publicación es {language}, genera UNA pregunta perspicaz que ayude a los lectores a comprender mejor las ideas centrales del libro, sus aplicaciones prácticas o perspectivas únicas. Reglas: 1. Devuelve SOLO la pregunta, sin introducción ni explicación 2. Concéntrate en el contenido del libro, no solo en su título 3. Haz que la pregunta sea práctica y estimulante 4. Sé conciso (30-200 palabras) 5. Sé creativo y genera una pregunta diferente cada vez, incluso para el mismo libro"""
    
    @property
    def multi_book_default_template(self) -> str:
        return """Aquí está la información sobre varios libros: {books_metadata} Pregunta del usuario: {query} Por favor, responda a la pregunta basándose en la información de los libros anterior."""
    
    @property
    def translations(self) -> dict:
        return {
            # Información del plugin
            'plugin_name': 'Ask AI Plugin',
            'plugin_desc': 'Haz preguntas sobre un libro usando IA',
            
            # UI - Pestañas y secciones
            'config_title': 'Configuración',
            'general_tab': 'General',
            'ai_models': 'IA',
            'shortcuts': 'Atajos',
            'about': 'Acerca de',
            'metadata': 'Metadatos',
            
            # UI - Botones y acciones
            'ok_button': 'OK',
            'save_button': 'Guardar',
            'send_button': 'Enviar',
            'stop_button': 'Detener',
            'suggest_button': 'Pregunta Aleatoria',
            'copy_response': 'Copiar Respuesta',
            'copy_question_response': 'Copiar P&&R',
            'export_pdf': 'Exportar PDF',
            'export_current_qa': 'Exportar P&R Actual',
            'export_history': 'Exportar Historial',
            
            # Configuración de exportación
            'export_settings': 'Configuración de Exportación',
            'enable_default_export_folder': 'Exportar a carpeta predeterminada',
            'no_folder_selected': 'Ninguna carpeta seleccionada',
            'browse': 'Examinar...',
            'select_export_folder': 'Seleccionar Carpeta de Exportación',
            
            # Texto de botones y elementos de menú
            'copy_response_btn': 'Copiar Respuesta',
            'copy_qa_btn': 'Copiar P&R',
            'export_current_btn': 'Exportar P&R como PDF',
            'export_history_btn': 'Exportar Historial como PDF',
            'copy_mode_response': 'Respuesta',
            'copy_mode_qa': 'P&R',
            'export_mode_current': 'P&R Actual',
            'export_mode_history': 'Historial',
            
            # Relacionado con exportación PDF
            'model_provider': 'Proveedor',
            'model_name': 'Modelo',
            'model_api_url': 'URL Base de API',
            'pdf_model_info': 'Información del Modelo de IA',
            'pdf_software': 'Software',
            
            'export_all_history_dialog_title': 'Exportar Todo el Historial a PDF',
            'export_all_history_title': 'TODO EL HISTORIAL DE P&R',
            'export_history_insufficient': 'Se necesitan al menos 2 registros de historial para exportar.',
            'history_record': 'Registro',
            'question_label': 'Pregunta',
            'answer_label': 'Respuesta',
            'default_ai': 'IA Predeterminada',
            'export_time': 'Exportado el',
            'total_records': 'Registros Totales',
            'info': 'Información',
            'yes': 'Sí',
            'no': 'No',
            'no_book_selected_title': 'Ningún Libro Seleccionado',
            'no_book_selected_message': 'Por favor, seleccione un libro antes de hacer preguntas.',
            'set_default_ai_title': 'Establecer IA Predeterminada',
            'set_default_ai_message': 'Ha cambiado a "{0}". ¿Desea establecerla como IA predeterminada para futuras consultas?',
            'set_default_ai_success': 'La IA predeterminada se ha establecido en "{0}".',
            'copied': '¡Copiado!',
            'pdf_exported': '¡PDF Exportado!',
            'export_pdf_dialog_title': 'Exportar a PDF',
            'export_pdf_error': 'Error al exportar PDF: {0}',
            'no_question': 'Sin pregunta',
            'saved': 'Guardado',
            'close_button': 'Cerrar',
            'open_local_tutorial': 'Abrir tutorial local',
            'tutorial_open_failed': 'Error al abrir el tutorial',
            
            # UI - Campos de configuración
            'token_label': 'Clave API:',
            'api_key_label': 'Clave API:',
            'model_label': 'Modelo:',
            'language_label': 'Idioma:',
            'language_label_old': 'Idioma',
            'base_url_label': 'URL Base:',
            'base_url_placeholder': 'Predeterminado: {default_api_base_url}',
            'shortcut': 'Tecla de Atajo',
            'shortcut_open_dialog': 'Abrir Diálogo',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Modelo',
            'action': 'Acción',
            'reset_button': 'Restablecer',
            'prompt_template': 'Plantilla de Prompt',
            'ask_prompts': 'Prompts de Preguntas',
            'random_questions_prompts': 'Prompts de Preguntas Aleatorias',
            'display': 'Mostrar',
            
            # UI - Elementos de diálogo
            'input_placeholder': 'Escribe tu pregunta...',
            'response_placeholder': 'Respuesta en breve...',
            
            # UI - Elementos de menú
            'menu_title': 'Preguntar',
            'menu_ask': 'Preguntar a {model}',
            
            # UI - Mensajes de estado
            'loading': 'Cargando...',
            'loading_text': 'Preguntando',
            'save_success': 'Configuración guardada',
            'sending': 'Enviando...',
            'requesting': 'Solicitando',
            'formatting': 'Solicitud exitosa, formateando',
            
            # UI - Función de lista de modelos
            'load_models': 'Cargar modelos',
            'use_custom_model': 'Usar nombre de modelo personalizado',
            'custom_model_placeholder': 'Ingrese el nombre del modelo personalizado',
            'model_placeholder': 'Por favor, cargue los modelos primero',
            'models_loaded': '{count} modelos cargados exitosamente',
            'load_models_failed': 'Error al cargar modelos: {error}',
            'model_list_not_supported': 'Este proveedor no admite la obtención automática de la lista de modelos',
            'api_key_required': 'Por favor, ingrese primero la clave API',
            'invalid_params': 'Parámetros inválidos',
            'warning': 'Advertencia',
            'success': 'Éxito',
            'error': 'Error',
            
            # Campos de metadatos
            'metadata_title': 'Título',
            'metadata_authors': 'Autor',
            'metadata_publisher': 'Editorial',
            'metadata_pubyear': 'Fecha de Publicación',
            'metadata_language': 'Idioma',
            'metadata_series': 'Serie',
            'no_metadata': 'Sin metadatos',
            'no_series': 'Sin serie',
            'unknown': 'Desconocido',

            # Multi-book feature
            'books_unit': ' libros',
            'new_conversation': 'Nueva Conversación',
            'single_book': 'Libro Único',
            'multi_book': 'Multi-Libro',
            'deleted': 'Eliminado',
            'history': 'Historial',
            'no_history': 'Sin registros de historial',
            'empty_question_placeholder': '(Sin pregunta)',
            'history_ai_unavailable': 'Esta IA ha sido eliminada de la configuración',
            'clear_current_book_history': 'Borrar Historial del Libro Actual',
            'confirm_clear_book_history': '¿Está seguro de que desea borrar todo el historial de:\n{book_titles}?',
            'confirm': 'Confirmar',
            'history_cleared': '{deleted_count} registros de historial borrados.',
            'multi_book_template_label': 'Plantilla de Prompt Multi-Libro:',
            'multi_book_placeholder_hint': 'Use {books_metadata} para información del libro, {query} para la pregunta del usuario',
            
            # Mensajes de error
            'network_error': 'Error de conexión',
            'request_timeout': 'Tiempo de espera agotado',
            'request_failed': 'Solicitud fallida',
            'question_too_long': 'Pregunta demasiado larga',
            'auth_token_required_title': 'Clave API Requerida',
            'auth_token_required_message': 'Por favor, establezca una clave API válida en la Configuración del Plugin.',
            'open_configuration': 'Abrir Configuración',
            'cancel': 'Cancelar',
            "invalid_default_ai_title": "IA Predeterminada Inválida",
            "invalid_default_ai_message": "La IA predeterminada \"{default_ai}\" no está configurada correctamente.\n\n¿Le gustaría cambiar a \"{first_ai}\" en su lugar?",
            "switch_to_ai": "Cambiar a {ai}",
            "keep_current": "Mantener Actual",
            'error_preparing_request': 'Error al preparar la solicitud',
            'empty_suggestion': 'Sugerencia vacía',
            'process_suggestion_error': 'Error al procesar sugerencia',
            'unknown_error': 'Error desconocido',
            'unknown_model': 'Modelo desconocido: {model_name}',
            'suggestion_error': 'Error de sugerencia',
            'random_question_success': '¡Pregunta aleatoria generada con éxito!',
            'book_title_check': 'Título del libro requerido',
            'avoid_repeat_question': 'Por favor usa una pregunta diferente',
            'empty_answer': 'Respuesta vacía',
            'invalid_response': 'Respuesta inválida',
            'auth_error_401': 'No autorizado',
            'auth_error_403': 'Acceso denegado',
            'rate_limit': 'Demasiadas solicitudes',
            'invalid_json': 'JSON inválido',
            'no_response': 'Sin respuesta',
            'template_error': 'Error de plantilla',
            'no_model_configured': 'No hay modelo de IA configurado. Por favor, configure un modelo de IA en la configuración.',
            'no_ai_configured_title': 'IA No Configurada',
            'no_ai_configured_message': '¡Bienvenido! Para comenzar a hacer preguntas sobre sus libros, primero debe configurar un proveedor de IA.\n\nRecomendado para principiantes:\n• Nvidia AI - Obtenga 6 meses de acceso API GRATIS solo con su número de teléfono (no se requiere tarjeta de crédito)\n• Ollama - Ejecute modelos de IA localmente en su computadora (completamente gratis y privado)\n\n¿Desea abrir la configuración del plugin para configurar un proveedor de IA ahora?',
            'open_settings': 'Configuración del Plugin',
            'ask_anyway': 'Preguntar de Todos Modos',
            'later': 'Más Tarde',
            'reset_all_data': 'Restablecer Todos los Datos',
            'reset_all_data_warning': 'Esto eliminará todas las claves API, plantillas de prompts y registros de historial local. Su preferencia de idioma se conservará. Por favor, proceda con precaución.',
            'reset_all_data_confirm_title': 'Confirmar Restablecimiento',
            'reset_all_data_confirm_message': '¿Está seguro de que desea restablecer el plugin a su estado inicial?\n\nEsto eliminará permanentemente:\n• Todas las claves API\n• Todas las plantillas de prompts personalizadas\n• Todo el historial de conversaciones\n• Toda la configuración del plugin (la preferencia de idioma se conservará)\n\n¡Esta acción no se puede deshacer!',
            'reset_all_data_success': 'Todos los datos del plugin se han restablecido correctamente. Por favor, reinicie calibre para que los cambios surtan efecto.',
            'reset_all_data_failed': 'Error al restablecer los datos del plugin: {error}',
            'random_question_error': 'Error al generar pregunta aleatoria',
            'clear_history_failed': 'Error al borrar historial',
            'clear_history_not_supported': 'Borrar historial para un solo libro aún no está soportado',
            'missing_required_config': 'Falta configuración requerida: {key}. Por favor revisa tus ajustes.',
            'api_key_too_short': 'La clave API es demasiado corta. Por favor revisa e ingresa la clave completa.',
            
            # Manejo de respuestas API
            'api_request_failed': 'Solicitud API fallida: {error}',
            'api_content_extraction_failed': 'No se puede extraer contenido de la respuesta API',
            'api_invalid_response': 'No se puede obtener una respuesta API válida',
            'api_unknown_error': 'Error desconocido: {error}',
            
            # Manejo de respuestas en streaming
            'stream_response_code': 'Código de estado de respuesta en streaming: {code}',
            'stream_continue_prompt': 'Por favor continúa tu respuesta anterior sin repetir el contenido ya proporcionado.',
            'stream_continue_code_blocks': 'Tu respuesta anterior tenía bloques de código sin cerrar. Por favor continúa y completa estos bloques de código.',
            'stream_continue_parentheses': 'Tu respuesta anterior tenía paréntesis sin cerrar. Por favor continúa y asegúrate de que todos los paréntesis estén correctamente cerrados.',
            'stream_continue_interrupted': 'Tu respuesta anterior parece haber sido interrumpida. Por favor continúa completando tu último pensamiento o explicación.',
            'stream_timeout_error': 'La transmisión en streaming no ha recibido nuevo contenido durante 60 segundos, posiblemente un problema de conexión.',
            
            # Mensajes de error API
            'api_version_model_error': 'Error de versión API o nombre de modelo: {message}\n\nPor favor actualiza la URL Base API a "{base_url}" y el modelo a "{model}" u otro modelo disponible en ajustes.',
            'api_format_error': 'Error de formato de solicitud API: {message}',
            'api_key_invalid': 'Clave API inválida o no autorizada: {message}\n\nPor favor revisa tu clave API y asegúrate de que el acceso API esté habilitado.',
            'api_rate_limit': 'Límite de frecuencia de solicitudes excedido, por favor intenta más tarde\n\nEs posible que hayas excedido la cuota de uso gratuito. Esto podría deberse a:\n1. Demasiadas solicitudes por minuto\n2. Demasiadas solicitudes por día\n3. Demasiados tokens de entrada por minuto',
            
            # Errores de configuración
            'missing_config_key': 'Falta clave de configuración requerida: {key}',
            'api_base_url_required': 'Se requiere URL Base API',
            'model_name_required': 'Se requiere nombre de modelo',
            
            # Obtención de lista de modelos
            'fetching_models_from': 'Obteniendo modelos desde {url}',
            'successfully_fetched_models': '{count} modelos {provider} obtenidos exitosamente',
            'failed_to_fetch_models': 'Error al obtener modelos: {error}',
            'api_key_empty': 'La clave API está vacía. Por favor, ingrese una clave API válida.',
            
            # Información de Acerca de
            'author_name': 'Sheldon',
            'user_manual': 'Manual de Usuario',
            'about_plugin': '¿Por qué Ask AI Plugin?',
            'learn_how_to_use': 'Cómo Usar',
            'email': 'iMessage',
            
            # Configuraciones específicas del modelo
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Personalizado',
            'model_enable_streaming': 'Habilitar streaming',
            
            # AI Switcher
            'current_ai': 'IA Actual',
            'no_configured_models': 'No hay IA configurada - Por favor configure en ajustes',
            
            # Provider specific info
            'nvidia_free_info': '💡 Los nuevos usuarios obtienen 6 meses de acceso gratuito a la API - No se requiere tarjeta de crédito',
            
            # Common system messages
            'default_system_message': 'Eres un experto en análisis de libros. Tu tarea es ayudar a los usuarios a entender mejor los libros proporcionando preguntas y análisis perspicaces.',
            
            # Request timeout settings
            'request_timeout_label': 'Tiempo de espera de solicitud:',
            'seconds': 'segundos',
            'request_timeout_error': 'Tiempo de espera de solicitud agotado. Tiempo de espera actual: {timeout} segundos',
            
            # Parallel AI settings
            'parallel_ai_count_label': 'Recuento de IA paralelas:',
            'parallel_ai_count_tooltip': 'Número de modelos de IA a consultar simultáneamente (1-2 disponibles, 3-4 próximamente)',
            'parallel_ai_notice': 'Nota: Esto solo afecta el envío de preguntas. Las preguntas aleatorias siempre usan una sola IA.',
            'suggest_maximize': 'Sugerencia: Maximice la ventana para una mejor visualización con 3 IAs',
            'ai_panel_label': 'IA {index}:',
            'no_ai_available': 'No hay IA disponible para este panel',
            'add_more_ai_providers': 'Por favor, agregue más proveedores de IA en ajustes',
            'select_ai': '-- Seleccionar IA --',
            'select_model': '-- Cambiar Modelo --',
            'request_model_list': 'Por favor, solicite la lista de modelos',
            'coming_soon': 'Próximamente',
            'advanced_feature_tooltip': 'Esta función está en desarrollo. ¡Manténgase atento a las actualizaciones!',
            
            # PDF export section titles
            'pdf_book_metadata': 'METADATOS DEL LIBRO',
            'pdf_question': 'PREGUNTA',
            'pdf_answer': 'RESPUESTA',
            'pdf_ai_model_info': 'INFORMACIÓN DEL MODELO DE IA',
            'pdf_generated_by': 'GENERADO POR',
            'pdf_provider': 'Proveedor',
            'pdf_model': 'Modelo',
            'pdf_api_base_url': 'URL Base de API',
            'pdf_panel': 'Panel',
            'pdf_plugin': 'Plugin',
            'pdf_github': 'GitHub',
            'pdf_software': 'Software',
            'pdf_generated_time': 'Hora de Generación',
            'default_ai_mismatch_title': 'IA Predeterminada Cambiada',
            'default_ai_mismatch_message': 'La IA predeterminada en la configuración ha cambiado a "{default_ai}",\npero el diálogo actual está usando "{current_ai}".\n\n¿Desea cambiar a la nueva IA predeterminada?',
            'discard_changes': 'Descartar Cambios',
            'empty_response': 'Respuesta vacía recibida de la API',
            'empty_response_after_filter': 'La respuesta está vacía después de filtrar las etiquetas think',
            'error_401': 'Falló la autenticación de la clave API. Por favor verifique: La clave API es correcta, la cuenta tiene saldo suficiente, la clave API no ha expirado.',
            'error_403': 'Acceso denegado. Por favor verifique: La clave API tiene permisos suficientes, no hay restricciones de acceso regional.',
            'error_404': 'Punto final de API no encontrado. Por favor verifique si la configuración de la URL base de la API es correcta.',
            'error_429': 'Demasiadas solicitudes, límite de velocidad alcanzado. Por favor intente de nuevo más tarde.',
            'error_5xx': 'Error del servidor. Por favor intente de nuevo más tarde o verifique el estado del proveedor de servicios.',
            'error_network': 'Falló la conexión de red. Por favor verifique la conexión de red, configuración de proxy o configuración de firewall.',
            'error_unknown': 'Error desconocido.',
            'gemini_geo_restriction': 'La API de Gemini no está disponible en su región. Por favor intente:\n1. Use una VPN para conectarse desde una región compatible\n2. Use otros proveedores de IA (OpenAI, Anthropic, DeepSeek, etc.)\n3. Verifique Google AI Studio para disponibilidad regional',
            'load_models_list': 'Cargar Lista de Modelos',
            'loading_models_text': 'Cargando modelos',
            'model_test_success': '¡Prueba de modelo exitosa! Configuración guardada.',
            'models_loaded_with_selection': 'Se cargaron {count} modelos exitosamente.\nModelo seleccionado: {model}',
            'ollama_model_not_available': 'El modelo "{model}" no está disponible. Por favor verifique:\n1. ¿Está iniciado el modelo? Ejecute: ollama run {model}\n2. ¿Es correcto el nombre del modelo?\n3. ¿Está descargado el modelo? Ejecute: ollama pull {model}',
            'ollama_service_not_running': 'El servicio Ollama no está en ejecución. Por favor inicie el servicio Ollama primero.',
            'ollama_service_timeout': 'Tiempo de espera de conexión del servicio Ollama. Por favor verifique si el servicio está funcionando correctamente.',
            'reset_ai_confirm_message': 'A punto de restablecer {ai_name} al estado predeterminado.\n\nEsto borrará:\n• Clave API\n• Nombre de modelo personalizado\n• Otros parámetros configurados\n\n¿Continuar?',
            'reset_ai_confirm_title': 'Confirmar Restablecimiento',
            'reset_current_ai': 'Restablecer IA Actual a Predeterminada',
            'reset_tooltip': 'Restablecer IA actual a valores predeterminados',
            'save_and_close': 'Guardar y Cerrar',
            'skip': 'Omitir',
            'technical_details': 'Detalles Técnicos',
            'test_current_model': 'Probar Modelo Actual',
            'test_model_button': 'Probar Modelo',
            'test_model_prompt': '¡Modelos cargados exitosamente! ¿Desea probar el modelo seleccionado "{model}"?',
            'unsaved_changes_message': 'Tiene cambios sin guardar. ¿Qué desea hacer?',
            'unsaved_changes_title': 'Cambios Sin Guardar',


            'pdf_info_not_available': 'Información no disponible',
        }