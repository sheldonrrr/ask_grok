#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Spanish language translations for Ask Grok plugin.
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
    def translations(self) -> dict:
        return {
            # Información del plugin
            'plugin_name': 'Ask Grok',
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
            'suggest_button': 'Pregunta Aleatoria',
            'copy_response': 'Copiar Respuesta',
            'copy_question_response': 'Copiar P&&R',
            'copied': '¡Copiado!',
            'saved': 'Guardado',
            'close_button': 'Cerrar',
            
            # UI - Campos de configuración
            'token_label': 'Clave API:',
            'model_label': 'Modelo:',
            'language_label': 'Idioma',
            'base_url_label': 'URL Base:',
            'base_url_placeholder': 'Predeterminado: {default_api_base_url}',
            'shortcut': 'Tecla de Atajo',
            'shortcut_open_dialog': 'Abrir Diálogo',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Modelo',
            'current_ai': 'IA Actual:',
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
            'loading': 'Cargando',
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
            
            # Mensajes de error
            'error': 'Error: ',
            'network_error': 'Error de conexión',
            'request_timeout': 'Tiempo de espera agotado',
            'request_failed': 'Solicitud fallida',
            'question_too_long': 'Pregunta demasiado larga',
            'auth_token_required_title': 'Clave API Requerida',
            'auth_token_required_message': 'Por favor configura la clave API en Configuración del Plugin',
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
            'no_model_configured': 'No hay modelo de IA configurado. Por favor configura un modelo de IA en ajustes.',
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
            'api_key_empty': 'La clave API está vacía. Por favor, ingrese una clave API válida.',
            
            # Obtención de lista de modelos
            'fetching_models_from': 'Obteniendo modelos desde {url}',
            'successfully_fetched_models': '{count} modelos {provider} obtenidos exitosamente',
            'failed_to_fetch_models': 'Error al obtener modelos: {error}',
            
            # Información de Acerca de
            'author_name': 'Sheldon',
            'user_manual': 'Manual de Usuario',
            'about_plugin': '¿Por qué Ask Grok?',
            'learn_how_to_use': 'Cómo Usar',
            'email': 'iMessage',
            
            # Configuraciones específicas del modelo
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Personalizado',
            'model_enable_streaming': 'Habilitar streaming',
            'model_disable_ssl_verify': 'Deshabilitar verificación SSL',
            
            # Mensajes del sistema comunes
            'default_system_message': 'Eres un experto en análisis de libros. Tu tarea es ayudar a los usuarios a entender mejor los libros proporcionando preguntas y análisis perspicaces.',
        }
