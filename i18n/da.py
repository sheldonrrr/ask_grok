#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Danish language translations for Ask Grok plugin.
"""

from ..models.base import BaseTranslation, TranslationRegistry, AIProvider


@TranslationRegistry.register
class DanishTranslation(BaseTranslation):
    """Danish language translation."""
    
    @property
    def code(self) -> str:
        return "da"
    
    @property
    def name(self) -> str:
        return "Dansk"
    
    @property
    def default_template(self) -> str:
        return 'Om bogen "{title}": Forfatter: {author}, Forlag: {publisher}, Udgivelsesår: {pubyear}, bog i language: {language}, Serie: {series}, Mit spørgsmål er: {query}'
    
    @property
    def suggestion_template(self) -> str:
        return """Du er en ekspert i boganmeldelser. For bogen "{title}" af {author},publiceringssprog er {language}, generér ÉT indsigtfuldt spørgsmål, der hjælper læserne med at forstå bogen bedre. Regler: 1. Returner KUN spørgsmålet, uden introduktion eller forklaring 2. Fokuser på bogens indhold, ikke kun titlen 3. Gør spørgsmålet praktisk og tankevækkende 4. Hold det kort (30-200 ord) 5. Vær kreativ og generer et andet spørsmål hver gang, selv for samme bog"""
    
    @property
    def translations(self) -> dict:
        return {
            # Plugin information
            'plugin_name': 'Ask Grok',
            'plugin_desc': 'Stil spørgsmål om en bog ved hjælp af AI',
            
            # UI - Tabs and sections
            'config_title': 'Konfiguration',
            'general_tab': 'Generelt',
            'ai_models': 'AI',
            'shortcuts': 'Genveje',
            'about': 'Om',
            'metadata': 'Metadata',
            
            # UI - Buttons and actions
            'ok_button': 'OK',
            'save_button': 'Gem',
            'send_button': 'Send',
            'suggest_button': 'Tilfældigt spørgsmål',
            'copy_response': 'Kopiér svar',
            'copy_question_response': 'Kopiér S&&S',
            'copied': 'Kopieret!',
            
            # UI - Configuration fields
            'token_label': 'API-nøgle:',
            'model_label': 'Model:',
            'language_label': 'Sprog',
            'base_url_label': 'Base-URL:',
            'base_url_placeholder': 'Standard: {default_api_base_url}',
            'shortcut': 'Genvej',
            'shortcut_open_dialog': 'Åbn dialog',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Model',
            'current_ai': 'Nuværende AI:',
            'action': 'Handling',
            'reset_button': 'Nulstil',
            'prompt_template': 'Promptskabelon',
            'ask_prompts': 'Spørgsmålsprompts',
            'random_questions_prompts': 'Tilfældige spørgsmålsprompts',
            'display': 'Visning',
            
            # UI - Dialog elements
            'input_placeholder': 'Skriv dit spørgsmål her...',
            'response_placeholder': 'Svaret kommer snart...',
            
            # UI - Menu options
            'menu_title': 'Spørg',
            'menu_ask': 'Spørg {model}',
            
            # UI - Status messages
            'loading': 'Indlæser',
            'loading_text': 'Stiller spørgsmål',
            'save_success': 'Indstillinger gemt',
            'sending': 'Sender...',
            'requesting': 'Anmoder',
            'formatting': 'Anmodning vellykket, formaterer',
            
            # Metadata fields
            'metadata_title': 'Titel',
            'metadata_authors': 'Forfatter',
            'metadata_publisher': 'Forlag',
            'metadata_pubyear': 'Udgivelsesdato',
            'metadata_language': 'Sprog',
            'metadata_series': 'Serie',
            'no_metadata': 'Ingen metadata',
            'no_series': 'Ingen serie',
            'unknown': 'Ukendt',
            
            # Error messages
            'error': 'Fejl: ',
            'network_error': 'Netværksfejl',
            'request_timeout': 'Anmodning timeout',
            'request_failed': 'Anmodning mislykkedes',
            'question_too_long': 'Spørgsmålet er for langt',
            'auth_token_required_title': 'API-nøgle påkrævet',
            'auth_token_required_message': 'Venligst indstil API-nøglen i indstillingerne',
            'error_preparing_request': 'Fejl ved forberedelse af anmodning',
            'empty_suggestion': 'Tom forslag',
            'process_suggestion_error': 'Fejl ved behandling af forslag',
            'unknown_error': 'Ukendt fejl',
            'unknown_model': 'Ukendt model: {model_name}',
            'suggestion_error': 'Forslagsfejl',
            'book_title_check': 'Bogtitel påkrævet',
            'avoid_repeat_question': 'Venligst brug et andet spørgsmål',
            'empty_answer': 'Tomt svar',
            'invalid_response': 'Ugyldigt svar',
            'auth_error_401': 'Ikke autoriseret',
            'auth_error_403': 'Adgang nægtet',
            'rate_limit': 'For mange anmodninger',
            'invalid_json': 'Ugyldig JSON',
            'no_response': 'Intet svar',
            'template_error': 'Skabelonfejl',
            'no_model_configured': 'Ingen AI-model konfigureret. Venligst konfigurer en AI-model i indstillingerne.',
            'random_question_error': 'Fejl ved generering af tilfældigt spørgsmål',
            'clear_history_failed': 'Kunne ikke rydde historik',
            'clear_history_not_supported': 'Rydning af historik for en enkelt bog understøttes ikke endnu',
            
            # About information
            'author_name': 'Sheldon',
            'user_manual': 'Brugermanual',
            'about_plugin': 'Hvorfor Ask Grok?',
            'learn_how_to_use': 'Sådan bruges',
            'email': 'iMessage',
            
            # Model-specific configurations
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
        }
