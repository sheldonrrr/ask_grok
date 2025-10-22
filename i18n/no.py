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
            'saved': 'Lagret',
            'close_button': 'Lukk',
            
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
            
            # UI - Modellistefunksjon
            'load_models': 'Last modeller',
            'use_custom_model': 'Bruk egendefinert modellnavn',
            'custom_model_placeholder': 'Skriv inn egendefinert modellnavn',
            'model_placeholder': 'Vennligst last modeller først',
            'models_loaded': '{count} modeller lastet',
            'load_models_failed': 'Kunne ikke laste modeller: {error}',
            'model_list_not_supported': 'Denne leverandøren støtter ikke automatisk henting av modellliste',
            'api_key_required': 'Vennligst skriv inn API-nøkkel først',
            'invalid_params': 'Ugyldige parametere',
            'warning': 'Advarsel',
            'success': 'Suksess',
            
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
            'auth_token_required_message': 'Vennligst sett API-nøkkelen i Plugin-konfigurasjonen',
            'error_preparing_request': 'Feil ved forberedelse av forespørsel',
            'empty_suggestion': 'Tom forslag',
            'process_suggestion_error': 'Feil ved behandling av forslag',
            'unknown_error': 'Ukjent feil',
            'unknown_model': 'Ukjent modell: {model_name}',
            'suggestion_error': 'Forslagsfeil',
            'random_question_success': 'Tilfeldig spørsmål generert med suksess!',
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
            'missing_required_config': 'Manglende påkrevd konfigurasjon: {key}. Sjekk innstillingene dine.',
            'api_key_too_short': 'API-nøkkel er for kort. Sjekk og skriv inn hele nøkkelen.',
            
            # API-svarhåndtering
            'api_request_failed': 'API-forespørsel mislyktes: {error}',
            'api_content_extraction_failed': 'Kunne ikke hente innhold fra API-svar',
            'api_invalid_response': 'Mottok ikke et gyldig API-svar',
            'api_unknown_error': 'Ukjent feil: {error}',
            
            # Streaming-svarhåndtering
            'stream_response_code': 'Streaming-svar statuskode: {code}',
            'stream_continue_prompt': 'Fortsett med ditt tidligere svar uten å gjenta allerede levert innhold.',
            'stream_continue_code_blocks': 'Ditt tidligere svar hadde uåpne kodeblokker. Fortsett og fullfør disse kodeblokkene.',
            'stream_continue_parentheses': 'Ditt tidligere svar hadde uåpne parenteser. Fortsett og sørg for at alle parenteser er riktig lukket.',
            'stream_continue_interrupted': 'Ditt tidligere svar ser ut til å ha blitt avbrutt. Fortsett og fullfør din siste tanke eller forklaring.',
            'stream_timeout_error': 'Streaming-overføringen har ikke mottatt nytt innhold på 60 sekunder, muligens et tilkoblingsproblem.',
            
            # API-feilmeldinger
            'api_version_model_error': 'API-versjon eller modellnavn feil: {message}\n\nOppdater API-base-URL til "{base_url}" og modellen til "{model}" eller en annen tilgjengelig modell i innstillingene.',
            'api_format_error': 'API-forespørselsformatfeil: {message}',
            'api_key_invalid': 'API-nøkkel ugyldig eller ikke autorisert: {message}\n\nSjekk API-nøkkelen din og sørg for at API-tilgang er aktivert.',
            'api_rate_limit': 'Forespørselsgrense overskredet, prøv igjen senere\n\nDu har kanskje overskredet din gratis brukskvote. Dette kan skyldes:\n1. For mange forespørsler per minutt\n2. For mange forespørsler per dag\n3. For mange input-tokens per minutt',
            
            # Konfigurasjonsfeil
            'missing_config_key': 'Manglende påkrevd konfigurasjonsnøkkel: {key}',
            'api_base_url_required': 'API-base-URL er påkrevd',
            'model_name_required': 'Modellnavn er påkrevd',
            'api_key_empty': 'API-nøkkel er tom. Skriv inn en gyldig API-nøkkel.',
            
            # Henting av modellliste
            'fetching_models_from': 'Henter modeller fra {url}',
            'successfully_fetched_models': '{count} {provider}-modeller hentet',
            'failed_to_fetch_models': 'Kunne ikke hente modeller: {error}',
            
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
            'model_enable_streaming': 'Aktiver streaming',
            'model_disable_ssl_verify': 'Deaktiver SSL-verifisering',
            
            # Generelle systemmeldinger
            'default_system_message': 'Du er en ekspert på bokanalyse. Din oppgave er å hjelpe brukere med å forstå bøker bedre ved å gi innsiktsfulle spørsmål og analyser.',
        }
