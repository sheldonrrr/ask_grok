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
            'export_current_qa': 'Eksportér Nuværende S&S',
            'export_history': 'Eksporter Historik',
            
            # Eksportindstillinger
            'export_settings': 'Eksportindstillinger',
            'enable_default_export_folder': 'Eksporter til standardmappe',
            'no_folder_selected': 'Ingen mappe valgt',
            'browse': 'Gennemse...',
            'select_export_folder': 'Vælg Eksportmappe',
            
            # Knaptekst og menupunkter
            'copy_response_btn': 'Kopier Svar',
            'copy_qa_btn': 'Kopier S&S',
            'export_current_btn': 'Eksporter S&S som PDF',
            'export_history_btn': 'Eksporter Historik som PDF',
            'copy_mode_response': 'Svar',
            'copy_mode_qa': 'S&S',
            'export_mode_current': 'Nuværende S&S',
            'export_mode_history': 'Historik',
            
            # PDF-eksport relateret
            'model_provider': 'Udbyder',
            'model_name': 'Model',
            'model_api_url': 'API Basis-URL',
            'pdf_model_info': 'AI-Modelinformation',
            'pdf_software': 'Software',
            
            'export_all_history_dialog_title': 'Eksporter Hele Historikken til PDF',
            'export_all_history_title': 'HELE S&S HISTORIK',
            'export_history_insufficient': 'Mindst 2 historikposter kræves for at eksportere.',
            'history_record': 'Post',
            'question_label': 'Spørgsmål',
            'answer_label': 'Svar',
            'default_ai': 'Standard AI',
            'export_time': 'Eksporteret',
            'total_records': 'Samlede Poster',
            'info': 'Information',
            'yes': 'Ja',
            'no': 'Nej',
            'no_book_selected_title': 'Ingen Bog Valgt',
            'no_book_selected_message': 'Vælg venligst en bog før du stiller spørgsmål.',
            'set_default_ai_title': 'Indstil Standard AI',
            'set_default_ai_message': 'Du har skiftet til "{0}". Vil du indstille den som standard AI til fremtidige forespørgsler?',
            'set_default_ai_success': 'Standard AI er blevet indstillet til "{0}".',
            'copied': 'Kopieret!',
            'pdf_exported': 'PDF Eksporteret!',
            'export_pdf_dialog_title': 'Eksportér til PDF',
            'export_pdf_error': 'Fejl ved eksport af PDF: {0}',
            'no_question': 'Intet spørgsmål',
            'no_response': 'Intet svar',
            'saved': 'Gemt',
            'close_button': 'Luk',
            'open_local_tutorial': 'Åbn lokal vejledning',
            'tutorial_open_failed': 'Kunne ikke åbne vejledning',
            'tutorial': 'Vejledning',
            
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
            'no_history': 'Ingen historieposter',
            'empty_question_placeholder': '(Intet spørgsmål)',
            'history_ai_unavailable': 'Denne AI er blevet fjernet fra konfigurationen',
            'clear_current_book_history': 'Ryd Nuværende Boghistorik',
            'confirm_clear_book_history': 'Er du sikker på, at du vil rydde al historik for:\n{book_titles}?',
            'confirm': 'Bekræft',
            'history_cleared': '{deleted_count} historikposter ryddet.',
            'multi_book_template_label': 'Promptskabelon for Flere bøger:',
            'multi_book_placeholder_hint': 'Brug {books_metadata} for boginformation, {query} for brugerens spørgsmål',
            
            # Error messages
            'network_error': 'Forbindelsesfejl',
            'request_timeout': 'Anmodning timeout',
            'request_failed': 'Anmodning mislykkedes',
            'question_too_long': 'Spørgsmål for langt',
            'auth_token_required_title': 'API-nøgle påkrævet',
            'auth_token_required_message': 'Indstil venligst en gyldig API-nøgle i Plugin-konfiguration.',
            'open_configuration': 'Åbn Konfiguration',
            'cancel': 'Annuller',
            'invalid_default_ai_title': 'Ugyldig Standard AI',
            'invalid_default_ai_message': 'Standard AI \"{default_ai}\" er ikke korrekt konfigureret.\n\nVil du skifte til \"{first_ai}\" i stedet?',
            'switch_to_ai': 'Skift til {ai}',
            'keep_current': 'Behold Nuværende',
            'error_preparing_request': 'Fejl ved forberedelse af anmodning',
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
            'template_error': 'Skabelonfejl',
            'no_model_configured': 'Ingen AI-model konfigureret. Konfigurer venligst en AI-model i indstillingerne.',
            'no_ai_configured_title': 'Ingen AI Konfigureret',
            'no_ai_configured_message': 'Velkommen! For at begynde at stille spørgsmål om dine bøger skal du først konfigurere en AI-udbyder.\n\nAnbefalet til begyndere:\n• Nvidia AI - Få 6 måneders GRATIS API-adgang med kun dit telefonnummer (intet kreditkort krævet)\n• Ollama - Kør AI-modeller lokalt på din computer (helt gratis og privat)\n\nØnsker du at åbne plugin-konfigurationen for at opsætte en AI-udbyder nu?',
            'open_settings': 'Plugin-konfiguration',
            'ask_anyway': 'Spørg Alligevel',
            'later': 'Senere',
            'reset_all_data': 'Nulstil Alle Data',
            'reset_all_data_warning': 'Dette vil slette alle API-nøgler, promptskabeloner og lokale historikposter. Din sprogpræference vil blive bevaret. Fortsæt venligst med forsigtighed.',
            'reset_all_data_confirm_title': 'Bekræft Nulstilling',
            'reset_all_data_confirm_message': 'Er du sikker på, at du vil nulstille pluginet til dets oprindelige tilstand?\n\nDette vil permanent slette:\n• Alle API-nøgler\n• Alle tilpassede promptskabeloner\n• Al samtalehistorik\n• Alle plugin-indstillinger (sprogpræference vil blive bevaret)\n\nDenne handling kan ikke fortrydes!',
            'reset_all_data_success': 'Alle plugin-data er blevet nulstillet. Genstart venligst calibre for at ændringerne træder i kraft.',
            'reset_all_data_failed': 'Kunne ikke nulstille plugin-data: {error}',
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
            'model_display_name_custom': 'Tilpasset',
            'model_enable_streaming': 'Aktivér streaming',
            
            # AI Switcher
            'current_ai': 'Nuværende AI',
            'no_configured_models': 'Ingen AI konfigureret - Venligst konfigurer i indstillinger',
            
            # Provider specific info
            'nvidia_free_info': '💡 Nye brugere får 6 måneders gratis API-adgang - Intet kreditkort påkrævet',
            
            # Common system messages
            'default_system_message': 'Du er en ekspert i boganalyse. Din opgave er at hjælpe brugere med at forstå bøger bedre ved at give indsigtsfulde spørgsmål og analyser.',
            
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
            'select_model': '-- Skift Model --',
            'request_model_list': 'Anmod venligst om modelliste',
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
            'default_ai_mismatch_title': 'Standard AI Ændret',
            'default_ai_mismatch_message': 'Standard AI i konfigurationen er ændret til "{default_ai}",\nmen den aktuelle dialog bruger "{current_ai}".\n\nVil du skifte til den nye standard AI?',
            'discard_changes': 'Kassér Ændringer',
            'empty_response': 'Modtog tomt svar fra API',
            'empty_response_after_filter': 'Svar er tomt efter filtrering af think tags',
            'error_401': 'API-nøgle godkendelse mislykkedes. Tjek venligst: API-nøgle er korrekt, konto har tilstrækkelig saldo, API-nøgle er ikke udløbet.',
            'error_403': 'Adgang nægtet. Tjek venligst: API-nøgle har tilstrækkelige tilladelser, ingen regionale adgangsbegrænsninger.',
            'error_404': 'API-endepunkt ikke fundet. Tjek venligst om API Base URL konfigurationen er korrekt.',
            'error_429': 'For mange anmodninger, hastighedsgrænse nået. Prøv venligst igen senere.',
            'error_5xx': 'Serverfejl. Prøv venligst igen senere eller tjek tjenesteudbyderens status.',
            'error_network': 'Netværksforbindelse mislykkedes. Tjek venligst netværksforbindelse, proxy-indstillinger eller firewall-konfiguration.',
            'error_unknown': 'Ukendt fejl.',
            'gemini_geo_restriction': 'Gemini API er ikke tilgængelig i din region. Prøv venligst:\n1. Brug en VPN til at forbinde fra en understøttet region\n2. Brug andre AI-udbydere (OpenAI, Anthropic, DeepSeek osv.)\n3. Tjek Google AI Studio for regional tilgængelighed',
            'load_models_list': 'Indlæs Modelliste',
            'loading_models_text': 'Indlæser modeller',
            'model_test_success': 'Modeltest vellykket! Konfiguration gemt.',
            'models_loaded_with_selection': 'Indlæste {count} modeller med succes.\nValgt model: {model}',
            'ollama_model_not_available': 'Model "{model}" er ikke tilgængelig. Tjek venligst:\n1. Er modellen startet? Kør: ollama run {model}\n2. Er modelnavnet korrekt?\n3. Er modellen downloadet? Kør: ollama pull {model}',
            'ollama_service_not_running': 'Ollama-tjeneste kører ikke. Start venligst Ollama-tjenesten først.',
            'ollama_service_timeout': 'Ollama-tjeneste forbindelse timeout. Tjek venligst om tjenesten kører korrekt.',
            'reset_ai_confirm_message': 'Ved at nulstille {ai_name} til standardtilstand.\n\nDette vil rydde:\n• API-nøgle\n• Brugerdefineret modelnavn\n• Andre konfigurerede parametre\n\nFortsæt?',
            'reset_ai_confirm_title': 'Bekræft Nulstilling',
            'reset_current_ai': 'Nulstil Nuværende AI til Standard',
            'reset_tooltip': 'Nulstil nuværende AI til standardværdier',
            'save_and_close': 'Gem og Luk',
            'skip': 'Spring Over',
            'technical_details': 'Tekniske Detaljer',
            'test_current_model': 'Test Nuværende Model',
            'test_model_button': 'Test Model',
            'test_model_prompt': 'Modeller indlæst med succes! Vil du teste den valgte model "{model}"?',
            'unsaved_changes_message': 'Du har ugemte ændringer. Hvad vil du gøre?',
            'unsaved_changes_title': 'Ugemte Ændringer',


            'pdf_info_not_available': 'Information ikke tilgængelig',
        }