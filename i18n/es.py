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
            'auth_token_required_message': 'Por favor configura la clave API en ajustes',
            'error_preparing_request': 'Error al preparar la solicitud',
            'empty_suggestion': 'Sugerencia vacía',
            'process_suggestion_error': 'Error al procesar sugerencia',
            'unknown_error': 'Error desconocido',
            'unknown_model': 'Modelo desconocido: {model_name}',
            'suggestion_error': 'Error de sugerencia',
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
        }
