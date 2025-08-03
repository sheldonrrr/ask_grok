#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Norwegian language translations for Ask Grok plugin.
"""

from ..models.base import BaseTranslation, TranslationRegistry, AIProvider


@TranslationRegistry.register
class NorwegianTranslation(BaseTranslation):
    """Norwegian language translation."""
    
    @property
    def code(self) -> str:
        return "no"
    
    @property
    def name(self) -> str:
        return "Norsk"
    
    @property
    def default_template(self) -> str:
        return 'Om boken "{title}": Forfatter: {author}, Forlag: {publisher}, Utgivelsesår: {pubyear}, bok i language: {language}, Serie: {series}, Spørsmålet mitt er: {query}'
    
    @property
    def suggestion_template(self) -> str:
        return """Du er en ekspert i bokanmeldelser. For boken "{title}" av {author}, publiceringsspråk er {language}, generer ÉT innsiktsfullt spørsmål som hjelper lesere med å forstå boken bedre. Regler: 1. Returner KUN spørsmålet, uten introduksjon eller forklaring 2. Fokuser på bokens innhold, ikke bare tittelen 3. Gjør spørsmålet praktisk og tankevekkende 4. Hold det kort (30-200 ord) 5. Vær kreativ og generer et annet spørsmål hver gang, selv for samme bok"""
    
    @property
    def translations(self) -> dict:
        return {
            # Plugin informasjon
            'plugin_name': 'Ask Grok',
            'plugin_desc': 'Still spørsmål om en bok ved hjelp av AI',
            
            # UI - Faner og seksjoner
            'config_title': 'Konfigurasjon',
            'general_tab': 'Generelt',
            'ai_models': 'AI',
            'shortcuts': 'Snarveier',
            'about': 'Om',
            'metadata': 'Metadata',
            
            # UI - Knapper og handlinger
            'ok_button': 'OK',
            'save_button': 'Lagre',
            'send_button': 'Send',
            'suggest_button': 'Tilfeldig spørsmål',
            'copy_response': 'Kopier svar',
            'copy_question_response': 'Kopier S&&S',
            'copied': 'Kopiert!',
            
            # UI - Konfigurasjonsfelter
            'token_label': 'API-nøkkel:',
            'model_label': 'Modell:',
            'language_label': 'Språk',
            'base_url_label': 'Base-URL:',
            'base_url_placeholder': 'Standard: {default_api_base_url}',
            'shortcut': 'Snarvei',
            'shortcut_open_dialog': 'Åpne dialog',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Modell',
            'current_ai': 'Nåværende AI:',
            'action': 'Handling',
            'reset_button': 'Tilbakestill',
            'prompt_template': 'Promptmal',
            'ask_prompts': 'Spørsmålsprompts',
            'random_questions_prompts': 'Tilfeldige spørsmålsprompts',
            'display': 'Visning',
            
            # UI - Dialogelementer
            'input_placeholder': 'Skriv inn spørsmålet ditt...',
            'response_placeholder': 'Svar kommer snart...',
            
            # UI - Menyvalg
            'menu_title': 'Spør',
            'menu_ask': 'Spør {model}',
            
            # UI - Statusmeldinger
            'loading': 'Laster',
            'loading_text': 'Stiller spørsmål',
            'save_success': 'Innstillinger lagret',
            'sending': 'Sender...',
            'requesting': 'Forespør',
            'formatting': 'Forespørsel vellykket, formaterer',
            
            # Metadatafelter
            'metadata_title': 'Tittel',
            'metadata_authors': 'Forfatter',
            'metadata_publisher': 'Forlag',
            'metadata_pubyear': 'Utgivelsesdato',
            'metadata_language': 'Språk',
            'metadata_series': 'Serie',
            'no_metadata': 'Ingen metadata',
            'no_series': 'Ingen serie',
            'unknown': 'Ukjent',
            
            # Feilmeldinger
            'error': 'Feil: ',
            'network_error': 'Nettverksfeil',
            'request_timeout': 'Forespørsel tidsavbrudd',
            'request_failed': 'Forespørsel mislyktes',
            'question_too_long': 'Spørsmålet er for langt',
            'auth_token_required_title': 'API-nøkkel påkrevd',
            'auth_token_required_message': 'Vennligst sett API-nøkkelen i innstillingene',
            'error_preparing_request': 'Feil ved forberedelse av forespørsel',
            'empty_suggestion': 'Tom forslag',
            'process_suggestion_error': 'Feil ved behandling av forslag',
            'unknown_error': 'Ukjent feil',
            'unknown_model': 'Ukjent modell: {model_name}',
            'suggestion_error': 'Forslagsfeil',
            'book_title_check': 'Boktittel påkrevd',
            'avoid_repeat_question': 'Vennligst bruk et annet spørsmål',
            'empty_answer': 'Tomt svar',
            'invalid_response': 'Ugyldig svar',
            'auth_error_401': 'Ikke autorisert',
            'auth_error_403': 'Tilgang nektet',
            'rate_limit': 'For mange forespørsler',
            'invalid_json': 'Ugyldig JSON',
            'no_response': 'Ingen svar',
            'template_error': 'Malfeil',
            'no_model_configured': 'Ingen AI-modell konfigurert. Vennligst konfigurer en AI-modell i innstillingene.',
            'random_question_error': 'Feil ved generering av tilfeldig spørsmål',
            'clear_history_failed': 'Kunne ikke slette historikk',
            'clear_history_not_supported': 'Sletting av historikk for en enkelt bok støttes ikke ennå',
            
            # Om informasjon
            'author_name': 'Sheldon',
            'user_manual': 'Brukermanual',
            'about_plugin': 'Hvorfor Ask Grok?',
            'learn_how_to_use': 'Hvordan bruke',
            'email': 'iMessage',
            
            # Modellspesifikke konfigurasjoner
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Tilpasset',
        }
