#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Swedish language translations for Ask Grok plugin.
"""

from ..models.base import BaseTranslation, TranslationRegistry, AIProvider


@TranslationRegistry.register
class SwedishTranslation(BaseTranslation):
    """Swedish language translation."""
    
    @property
    def code(self) -> str:
        return "sv"
    
    @property
    def name(self) -> str:
        return "Svenska"
    
    @property
    def default_template(self) -> str:
        return 'Om boken "{title}": Författare: {author}, Förlag: {publisher}, Utgivningsår: {pubyear}, bok i language: {language}, Serie: {series}, Min fråga är: {query}'
    
    @property
    def suggestion_template(self) -> str:
        return """Du är en expert på bokrecensioner. För boken "{title}" av {author}, publicerings språk är {language}, generera EN insiktsfull fråga som hjälper läsarna att förstå boken bättre. Regler: 1. Returnera ENDAST frågan, utan introduktion eller förklaring 2. Fokusera på bokens innehåll, inte bara titeln 3. Gör frågan praktisk och tankeväckande 4. Håll den kort (30-200 ord) 5. Var kreativ och generera en annan fråga varje gång, även för samma bok"""
    
    @property
    def translations(self) -> dict:
        return {
            # Plugin information
            'plugin_name': 'Ask Grok',
            'plugin_desc': 'Ställ frågor om en bok med hjälp av AI',
            
            # UI - Flikar och sektioner
            'config_title': 'Konfiguration',
            'general_tab': 'Allmänt',
            'ai_models': 'AI',
            'shortcuts': 'Genvägar',
            'about': 'Om',
            'metadata': 'Metadata',
            
            # UI - Knappar och åtgärder
            'ok_button': 'OK',
            'save_button': 'Spara',
            'send_button': 'Skicka',
            'suggest_button': 'Slumpmässig fråga',
            'copy_response': 'Kopiera svar',
            'copy_question_response': 'Kopiera F&&S',
            'copied': 'Kopierad!',
            
            # UI - Konfigurationsfält
            'token_label': 'API-nyckel:',
            'model_label': 'Modell:',
            'language_label': 'Språk',
            'base_url_label': 'Bas-URL:',
            'base_url_placeholder': 'Standard: {default_api_base_url}',
            'shortcut': 'Genväg',
            'shortcut_open_dialog': 'Öppna dialog',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Modell',
            'current_ai': 'Aktuell AI:',
            'action': 'Åtgärd',
            'återställ_button': 'Återställ',
            'prompt_template': 'Promptmall',
            'ask_prompts': 'Frågeprompts',
            'random_questions_prompts': 'Slumpmässiga frågeprompts',
            'display': 'Visa',
            
            # UI - Dialogelement
            'input_placeholder': 'Skriv din fråga...',
            'response_placeholder': 'Svar kommer snart...',
            
            # UI - Menyalternativ
            'menu_title': 'Fråga',
            'menu_ask': 'Fråga {model}',
            
            # UI - Statusmeddelanden
            'loading': 'Laddar',
            'loading_text': 'Ställer fråga',
            'save_success': 'Inställningar sparade',
            'sending': 'Skickar...',
            'requesting': 'Begär',
            'formatting': 'Begäran lyckades, formaterar',
            
            # Metadatafält
            'metadata_title': 'Titel',
            'metadata_authors': 'Författare',
            'metadata_publisher': 'Förlag',
            'metadata_pubyear': 'Utgivningsdatum',
            'metadata_language': 'Språk',
            'metadata_series': 'Serie',
            'no_metadata': 'Ingen metadata',
            'no_series': 'Ingen serie',
            'unknown': 'Okänd',
            
            # Felmeddelanden
            'error': 'Fel: ',
            'network_error': 'Anslutningsfel',
            'request_timeout': 'Begäran timeout',
            'request_failed': 'Begäran misslyckades',
            'question_too_long': 'Frågan är för lång',
            'auth_token_required_title': 'API-nyckel krävs',
            'auth_token_required_message': 'Vänligen ställ in API-nyckeln i inställningarna',
            'error_preparing_request': 'Fel vid förberedelse av begäran',
            'empty_suggestion': 'Tom förslag',
            'process_suggestion_error': 'Fel vid bearbetning av förslag',
            'unknown_error': 'Okänt fel',
            'unknown_model': 'Okänd modell: {model_name}',
            'suggestion_error': 'Förslagsfel',
            'book_title_check': 'Boktitel krävs',
            'avoid_repeat_question': 'Vänligen använd en annan fråga',
            'empty_answer': 'Tomt svar',
            'invalid_response': 'Ogiltigt svar',
            'auth_error_401': 'Ej auktoriserad',
            'auth_error_403': 'Åtkomst nekad',
            'rate_limit': 'För många begäranden',
            'invalid_json': 'Ogiltig JSON',
            'no_response': 'Inget svar',
            'template_error': 'Mallfel',
            'no_model_configured': 'Ingen AI-modell konfigurerad. Vänligen konfigurera en AI-modell i inställningarna.',
            'random_question_error': 'Fel vid generering av slumpmässig fråga',
            'clear_history_failed': 'Kunde inte rensa historik',
            'clear_history_not_supported': 'Rensa historik för en enskild bok stöds ännu inte',
            
            # Om information
            'author_name': 'Sheldon',
            'user_manual': 'Användarmanual',
            'about_plugin': 'Varför Ask Grok?',
            'learn_how_to_use': 'Hur man använder',
            'email': 'iMessage',
            
            # Modellspecifika konfigurationer
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Anpassad',
        }
