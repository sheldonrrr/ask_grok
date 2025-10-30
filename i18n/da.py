#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Danish language translations for Ask AI Plugin.
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
        return """Du er en ekspert i boganmeldelser. For bogen "{title}" af {author},publiceringssprog er {language}, generér ÉT indsigtfuldt spørgsmål, der hjælper læserne med at forstå bogen bedre. Regler: 1. Returner KUN spørgsmålet, uden introduktion eller forklaring 2. Fokuser på bogens indhold, ikke kun titlen 3. Gør spørgsmålet praktisk og tankevækkende 4. Hold det kort (30-200 ord) 5. Vær kreativ og generer et andet spørgsmål hver gang, selv for samme bog"""
    
    @property
    def multi_book_default_template(self) -> str:
        return """Her er information om flere bøger: {books_metadata} Brugerens spørgsmål: {query} Besvar venligst spørgsmålet baseret på ovenstående boginformation."""
    
    @property
    def translations(self) -> dict:
        return {
            # Plugin information
            'plugin_name': 'Ask AI Plugin',
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
            'stop_button': 'Stop',
            'suggest_button': 'Tilfældigt spørgsmål',
            'copy_response': 'Kopiér svar',
            'copy_question_response': 'Kopiér S&&S',
            'export_pdf': 'Eksportér PDF',
            'copied': 'Kopieret!',
            'pdf_exported': 'PDF Eksporteret!',
            'export_pdf_dialog_title': 'Eksportér til PDF',
            'export_pdf_error': 'Fejl ved eksport af PDF: {0}',
            'no_question': 'Intet spørgsmål',
            'no_response': 'Intet svar',
            'saved': 'Gemt',
            'close_button': 'Luk',
            
            # UI - Configuration fields
            'token_label': 'API-nøgle:',
            'api_key_label': 'API-nøgle:',
            'model_label': 'Model:',
            'language_label': 'Sprog:',
            'language_label_old': 'Sprog',
            'base_url_label': 'Base-URL:',
            'base_url_placeholder': 'Standard: {default_api_base_url}',
            'shortcut': 'Genvejstast',
            'shortcut_open_dialog': 'Åbn dialog',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Model',
            'action': 'Handling',
            'reset_button': 'Nulstil',
            'prompt_template': 'Promptskabelon',
            'ask_prompts': 'Spørgsmålsprompts',
            'random_questions_prompts': 'Tilfældige spørgsmålsprompts',
            'display': 'Visning',
            
            # UI - Dialog elements
            'input_placeholder': 'Skriv dit spørgsmål her...',
            'response_placeholder': 'Svaret kommer snart...',
            
            # UI - Menu items
            'menu_title': 'Spørg',
            'menu_ask': 'Spørg {model}',
            
            # UI - Status messages
            'loading': 'Indlæser...',
            'loading_text': 'Stiller spørgsmål',
            'save_success': 'Indstillinger gemt',
            'sending': 'Sender...',
            'requesting': 'Anmoder',
            'formatting': 'Anmodning lykkedes, formaterer',
            
            # UI - Model list feature
            'load_models': 'Indlæs modeller',
            'use_custom_model': 'Brug brugerdefineret modelnavn',
            'custom_model_placeholder': 'Indtast brugerdefineret modelnavn',
            'model_placeholder': 'Indlæs venligst modeller først',
            'models_loaded': 'Succesfuldt indlæst {count} modeller',
            'load_models_failed': 'Kunne ikke indlæse modeller: {error}',
            'model_list_not_supported': 'Denne udbyder understøtter ikke automatisk hentning af modelliste',
            'api_key_required': 'Indtast venligst API-nøgle først',
            'invalid_params': 'Ugyldige parametre',
            'warning': 'Advarsel',
            'success': 'Succes',
            'error': 'Fejl',
            
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
            
            # Multi-book feature
            'books_unit': ' bøger',
            'new_conversation': 'Ny samtale',
            'single_book': 'Enkelt bog',
            'multi_book': 'Flere bøger',
            'deleted': 'Slettet',
            'history': 'Historik',
            'multi_book_template_label': 'Promptskabelon for Flere bøger:',
            'multi_book_placeholder_hint': 'Brug {books_metadata} for boginformation, {query} for brugerens spørgsmål',
            
            # Error messages
            'error': 'Fejl: ',
            'network_error': 'Forbindelsesfejl',
            'request_timeout': 'Anmodning timeout',
            'request_failed': 'Anmodning mislykkedes',
            'question_too_long': 'Spørgsmål for langt',
            'auth_token_required_title': 'API-nøgle påkrævet',
            'auth_token_required_message': 'Venligst indstil API-nøgle i Plugin-konfigurationen.',
            'error_preparing_request': 'Anmodningsforberedelse mislykkedes',
            'empty_suggestion': 'Tomt forslag',
            'process_suggestion_error': 'Forslagsbehandlingsfejl',
            'unknown_error': 'Ukendt fejl',
            'unknown_model': 'Ukendt model: {model_name}',
            'suggestion_error': 'Forslagsfejl',
            'random_question_success': 'Tilfældigt spørgsmål genereret med succes!',
            'book_title_check': 'Bogtitel påkrævet',
            'avoid_repeat_question': 'Brug venligst et andet spørgsmål',
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
            'missing_required_config': 'Manglende påkrævet konfiguration: {key}. Tjek venligst dine indstillinger.',
            'api_key_too_short': 'API-nøgle er for kort. Tjek venligst og indtast den fulde nøgle.',
            
            # API response handling
            'api_request_failed': 'API-anmodning mislykkedes: {error}',
            'api_content_extraction_failed': 'Kunne ikke udtrække indhold fra API-svar',
            'api_invalid_response': 'Kunne ikke få et gyldigt API-svar',
            'api_unknown_error': 'Ukendt fejl: {error}',
            
            # Stream response handling
            'stream_response_code': 'Streaming-svar statuskode: {code}',
            'stream_continue_prompt': 'Fortsæt venligst dit tidligere svar uden at gentage allerede leveret indhold.',
            'stream_continue_code_blocks': 'Dit tidligere svar havde uåbne kodeblokke. Fortsæt venligst og færdiggør disse kodeblokke.',
            'stream_continue_parentheses': 'Dit tidligere svar havde uåbne parenteser. Fortsæt venligst og sørg for, at alle parenteser er korrekt lukket.',
            'stream_continue_interrupted': 'Dit tidligere svar ser ud til at være blevet afbrudt. Fortsæt venligst med at færdiggøre din sidste tanke eller forklaring.',
            'stream_timeout_error': 'Streaming-overførslen har ikke modtaget nyt indhold i 60 sekunder, muligvis et forbindelsesproblem.',
            
            # API error messages
            'api_version_model_error': 'API-version eller modelnavn fejl: {message}\n\nOpdater venligst API Base URL til "{base_url}" og modellen til "{model}" eller anden tilgængelig model i indstillingerne.',
            'api_format_error': 'API-anmodningsformatfejl: {message}',
            'api_key_invalid': 'API-nøgle ugyldig eller ikke autoriseret: {message}\n\nTjek venligst din API-nøgle og sørg for, at API-adgang er aktiveret.',
            'api_rate_limit': 'Anmodningsgrænse overskredet, prøv igen senere\n\nDu har måske overskredet den gratis brugskvote. Dette kan skyldes:\n1. For mange anmodninger pr. minut\n2. For mange anmodninger pr. dag\n3. For mange input-tokens pr. minut',
            
            # Configuration errors
            'missing_config_key': 'Manglende påkrævet konfigurationsnøgle: {key}',
            'api_base_url_required': 'API Base URL er påkrævet',
            'model_name_required': 'Modelnavn er påkrævet',
            
            # Model list fetching
            'fetching_models_from': 'Henter modeller fra {url}',
            'successfully_fetched_models': 'Succesfuldt hentet {count} {provider}-modeller',
            'failed_to_fetch_models': 'Kunne ikke hente modeller: {error}',
            'api_key_empty': 'API-nøglen er tom. Indtast venligst en gyldig API-nøgle.',
            
            # About information
            'author_name': 'Sheldon',
            'user_manual': 'Brugermanual',
            'about_plugin': 'Hvorfor Ask AI Plugin?',
            'learn_how_to_use': 'Sådan bruges',
            'email': 'iMessage',
            
            # Model specific configurations
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Brugerdefineret',
            'model_enable_streaming': 'Aktiver Streaming',
            
            # AI Switcher
            'current_ai': 'Nuværende AI',
            'no_configured_models': 'Ingen AI konfigureret - Venligst konfigurer i indstillinger',
            
            # Provider specific info
            'nvidia_free_info': '💡 Nye brugere får 6 måneders gratis API-adgang - Intet kreditkort påkrævet',
            
            # Common system messages
            'default_system_message': 'Du er en ekspert i boganalyse. Din opgave er at hjælpe brugere med at forstå bøger bedre ved at give indsigtsfulde spørgsmål og analyser.',
            'api_content_extraction_failed': 'Kunne ikke udtrække indhold fra API-svar',
            
            # Request timeout settings
            'request_timeout_label': 'Anmodningstimeout:',
            'seconds': 'sekunder',
            'request_timeout_error': 'Anmodningstimeout. Nuværende timeout: {timeout} sekunder',
            
            # Parallel AI settings
            'parallel_ai_count_label': 'Antal parallelle AI:',
            'parallel_ai_count_tooltip': 'Antal AI-modeller, der skal forespørges samtidigt (1-2 tilgængelige, 3-4 kommer snart)',
            'parallel_ai_notice': 'Bemærk: Dette påvirker kun afsendelse af spørgsmål. Tilfældige spørgsmål bruger altid en enkelt AI.',
            'suggest_maximize': 'Tip: Maksimer vinduet for bedre visning med 3 AI\'er',
            'ai_panel_label': 'AI {index}:',
            'no_ai_available': 'Ingen AI tilgængelig for dette panel',
            'add_more_ai_providers': 'Tilføj venligst flere AI-udbydere i indstillingerne',
            'select_ai': '-- Vælg AI --',
            'coming_soon': 'Kommer snart',
            'advanced_feature_tooltip': 'Denne funktion er under udvikling. Følg med for opdateringer!',
            
            # PDF export section titles
            'pdf_book_metadata': 'BOG METADATA',
            'pdf_question': 'SPØRGSMÅL',
            'pdf_answer': 'SVAR',
            'pdf_ai_model_info': 'AI MODEL INFORMATION',
            'pdf_generated_by': 'GENERERET AF',
            'pdf_provider': 'Udbyder',
            'pdf_model': 'Model',
            'pdf_api_base_url': 'API Base URL',
            'pdf_panel': 'Panel',
            'pdf_plugin': 'Plugin',
            'pdf_github': 'GitHub',
            'pdf_software': 'Software',
            'pdf_generated_time': 'Genereret tid',
            'pdf_info_not_available': 'Information ikke tilgængelig',
        }