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
            'ai_models': 'AI-udbydere',
            'shortcuts': 'Genveje',
            'shortcuts_note': "Du kan tilpasse disse genveje i calibre: Indstillinger -> Genveje (søg 'Ask AI').\nDenne side viser standard-/eksempelgenveje. Hvis du har ændret dem under Genveje, har calibre-indstillingerne forrang.",
            'prompts_tab': 'Prompts',
            'about': 'Om',
            'metadata': 'Metadata',

            # Section subtitles
            'language_settings': 'Sprog',
            'language_subtitle': 'Vælg dit foretrukne sprog til brugerfladen',
            'ai_providers_subtitle': 'Konfigurér AI-udbydere, og vælg din standard-AI',
            'prompts_subtitle': 'Tilpas, hvordan spørgsmål sendes til AI',
            'export_settings_subtitle': 'Indstil standardmappe for eksport af PDF\'er',
            'debug_settings_subtitle': 'Aktivér fejlfindingslogning til fejlfinding',
            'reset_all_data_subtitle': '⚠️ Advarsel: Dette vil permanent slette alle dine indstillinger og data',

            # Prompts tab
            'language_preference_title': 'Sprogpræference',
            'language_preference_subtitle': 'Kontrollér, om AI-svar skal matche dit grænsefladesprog',
            'prompt_templates_title': 'Prompt-skabeloner',
            'prompt_templates_subtitle': 'Tilpas, hvordan boginformation sendes til AI ved hjælp af dynamiske felter som {title}, {author}, {query}',
            'ask_prompts': 'Spørg prompts',
            'random_questions_prompts': 'Prompts for tilfældige spørgsmål',
            'multi_book_prompts_label': 'Multi-bog prompts',
            'multi_book_placeholder_hint': 'Brug {books_metadata} for boginformation, {query} for brugerens spørgsmål',
            'dynamic_fields_title': 'Dynamiske felter reference',
            'dynamic_fields_subtitle': 'Tilgængelige felter og eksempelværdier fra "Frankenstein" af Mary Shelley',
            'dynamic_fields_examples': '<b>{title}</b> → Frankenstein<br><b>{author}</b> → Mary Shelley<br><b>{publisher}</b> → Lackington, Hughes, Harding, Mavor & Jones<br><b>{pubyear}</b> → 1818<br><b>{language}</b> → Engelsk<br><b>{series}</b> → (ingen)<br><b>{query}</b> → Din spørgsmålstekst',
            'reset_prompts': 'Nulstil prompts til standard',
            'reset_prompts_confirm': 'Er du sikker på, at du vil nulstille alle prompt-skabeloner til deres standardværdier? Denne handling kan ikke fortrydes.',
            'unsaved_changes_title': 'Ugemte ændringer',
            'unsaved_changes_message': 'Du har ugemte ændringer i Prompts-fanen. Vil du gemme dem?',
            'use_interface_language': 'Bed altid AI om at svare på det aktuelle plugins grænsefladesprog',
            'language_instruction_label': 'Sproginstruktion tilføjet til prompts:',
            'language_instruction_text': 'Svar venligst på {language_name}.',

            # Persona settings
            'persona_title': 'Persona',
            'persona_subtitle': 'Definér din forskningsbaggrund og mål for at hjælpe AI med at give mere relevante svar',
            'use_persona': 'Brug persona',
            'persona_label': 'Persona',
            'persona_placeholder': 'Som forsker ønsker jeg at researche gennem bogdata.',
            'persona_hint': 'Jo mere AI ved om dit mål og din baggrund, jo bedre bliver forskningen eller genereringen.',

            # UI - Buttons and actions
            'ok_button': 'OK',
            'save_button': 'Gem',
            'send_button': 'Send',
            'stop_button': 'Stop',
            'suggest_button': 'Tilfældigt spørgsmål',
            'copy_response': 'Kopiér svar',
            'copy_question_response': 'Kopiér S&S',
            'export_pdf': 'Eksportér PDF',
            'export_current_qa': 'Eksportér Nuværende S&S',
            'export_history': 'Eksportér Historik',
            'export_all_history_dialog_title': 'Eksporter al historik til PDF',
            'export_all_history_title': 'AL S&S HISTORIK',
            'export_history_insufficient': 'Kræver mindst 2 historikposter for at eksportere.',
            'history_record': 'Post',
            'question_label': 'Spørgsmål',
            'answer_label': 'Svar',
            'default_ai': 'Standard-AI',
            'export_time': 'Eksporteret den',
            'total_records': 'Total antal poster',
            'info': 'Information',
            'yes': 'Ja',
            'no': 'Nej',
            'no_book_selected_title': 'Ingen bog valgt',
            'no_book_selected_message': 'Vælg venligst en bog, før du stiller spørgsmål.',
            'set_default_ai_title': 'Indstil standard-AI',
            'set_default_ai_message': 'Du har skiftet til "{0}". Vil du indstille den som standard-AI for fremtidige forespørgsler?',
            'set_default_ai_success': 'Standard-AI er indstillet til "{0}".',
            'default_ai_mismatch_title': 'Standard-AI ændret',
            'default_ai_mismatch_message': 'Standard-AI i konfigurationen er ændret til "{default_ai}",\nmen den aktuelle dialog bruger "{current_ai}".\n\nVil du skifte til den nye standard-AI?',
            'copied': 'Kopieret!',
            'pdf_exported': 'PDF eksporteret!',
            'export_pdf_dialog_title': 'Eksportér til PDF',
            'export_pdf_error': 'Kunne ikke eksportere PDF: {0}',
            'no_question': 'Intet spørgsmål',
            'no_response': 'Intet svar',
            'saved': 'Gemt',
            'close_button': 'Luk',
            'open_local_tutorial': 'Åbn lokal vejledning',
            'tutorial_open_failed': 'Kunne ikke åbne vejledning',
            'tutorial': 'Vejledning',

            'model_display_name_perplexity': 'Perplexity',

            # UI - Configuration fields
            'token_label': 'API-nøgle:',
            'api_key_label': 'API-nøgle:',
            'model_label': 'Model:',
            'language_label': 'Sprog:',
            'language_label_old': 'Sprog',
            'base_url_label': 'Basis-URL:',
            'base_url_placeholder': 'Standard: {default_api_base_url}',
            'shortcut': 'Genvejstast',
            'shortcut_open_dialog': 'Åbn dialog',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Model',
            'action': 'Handling',
            'reset_button': 'Nulstil til standard',
            'reset_current_ai': 'Nulstil nuværende AI til standard',
            'reset_ai_confirm_title': 'Bekræft nulstilling',
            'reset_ai_confirm_message': 'Er ved at nulstille {ai_name} til standardtilstand.\n\nDette vil rydde:\n• API-nøgle\n• Brugerdefineret modelnavn\n• Andre konfigurerede parametre\n\nFortsæt?',
            'reset_tooltip': 'Nulstil nuværende AI til standardværdier',
            'unsaved_changes_title': 'Ugemte ændringer',
            'unsaved_changes_message': 'Du har ugemte ændringer. Hvad vil du gøre?',
            'save_and_close': 'Gem og luk',
            'discard_changes': 'Kassér ændringer',
            'cancel': 'Annuller',
            'yes_button': 'Ja',
            'no_button': 'Nej',
            'cancel_button': 'Annuller',
            'invalid_default_ai_title': 'Ugyldig standard-AI',
            'invalid_default_ai_message': 'Standard-AI\'en "{default_ai}" er ikke korrekt konfigureret.\n\nVil du skifte til "{first_ai}" i stedet?',
            'switch_to_ai': 'Skift til {ai}',
            'keep_current': 'Behold nuværende',
            'prompt_template': 'Prompt-skabelon',
            'ask_prompts': 'Spørg prompts',
            'random_questions_prompts': 'Prompts for tilfældige spørgsmål',
            'display': 'Vis',
            'export_settings': 'Eksportindstillinger',
            'enable_default_export_folder': 'Eksportér til standardmappe',
            'no_folder_selected': 'Ingen mappe valgt',
            'browse': 'Gennemse...',
            'select_export_folder': 'Vælg eksportmappe',

            # Button text and menu items
            'copy_response_btn': 'Kopiér svar',
            'copy_qa_btn': 'Kopiér S&S',
            'export_current_btn': 'Eksportér S&S som PDF',
            'export_history_btn': 'Eksportér historik som PDF',
            'copy_mode_response': 'Svar',
            'copy_mode_qa': 'S&S',
            'copy_format_plain': 'Ren tekst',
            'copy_format_markdown': 'Markdown',
            'export_mode_current': 'Nuværende S&S',
            'export_mode_history': 'Historik',

            # PDF Export related
            'model_provider': 'Udbyder',
            'model_name': 'Model',
            'model_api_url': 'API Basis-URL',
            'pdf_model_info': 'AI Model Information',
            'pdf_software': 'Software',

            # UI - Dialog elements
            'input_placeholder': 'Skriv dit spørgsmål...',
            'response_placeholder': 'Svar kommer snart...',  # Used for all models
            # UI - Menu items
            'menu_title': 'Spørg AI',
            'menu_ask': 'Spørg',

            # UI - Status information
            'loading': 'Indlæser',
            'loading_text': 'Spørger',
            'loading_models_text': 'Indlæser modeller',
            'save_success': 'Indstillinger gemt',
            'sending': 'Sender...',
            'requesting': 'Anmoder',
            'formatting': 'Anmodning lykkedes, formaterer',

            # UI - Model list feature
            'load_models': 'Indlæs modeller',
            'load_models_list': 'Indlæs modelliste',
            'test_current_model': 'Test nuværende model',
            'use_custom_model': 'Brug brugerdefineret modelnavn',
            'custom_model_placeholder': 'Indtast brugerdefineret modelnavn',
            'model_placeholder': 'Indlæs venligst modeller først',
            'models_loaded': 'Succesfuldt indlæst {count} modeller',
            'models_loaded_with_selection': 'Succesfuldt indlæst {count} modeller.\nValgt model: {model}',
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
            'metadata_pubdate': 'Udgivelsesdato',
            'metadata_pubyear': 'Udgivelsesår',
            'metadata_language': 'Sprog',
            'metadata_series': 'Serie',
            'no_metadata': 'Ingen metadata',
            'no_series': 'Ingen serie',
            'unknown': 'Ukendt',

            # Multi-book feature
            'books_unit': ' bøger',
            'new_conversation': 'Ny samtale',
            'single_book': 'Enkelt bog',
            'multi_book': 'Multi-bog',
            'deleted': 'Slettet',
            'history': 'Historik',
            'no_history': 'Ingen historikposter',
            'empty_question_placeholder': '(Intet spørgsmål)',
            'history_ai_unavailable': 'Denne AI er blevet fjernet fra konfigurationen',
            'clear_current_book_history': 'Ryd nuværende boghistorik',
            'confirm_clear_book_history': 'Er du sikker på, at du vil rydde al historik for:\n{book_titles}?',
            'confirm': 'Bekræft',
            'history_cleared': '{deleted_count} historikposter ryddet.',
            'multi_book_template_label': 'Multi-bog prompt-skabelon:',
            'multi_book_placeholder_hint': 'Brug {books_metadata} for boginformation, {query} for brugerens spørgsmål',

            # Error messages (Note: 'error' is already defined above, these are other error types)
            'network_error': 'Forbindelsesfejl',
            'request_timeout': 'Anmodningstimeout',
            'request_failed': 'Anmodning mislykkedes',
            'request_stopped': 'Anmodning stoppet',
            'question_too_long': 'Spørgsmål for langt',
            'auth_token_required_title': 'AI-tjeneste kræves',
            'auth_token_required_message': 'Konfigurer venligst en gyldig AI-tjeneste i plugin-konfigurationen.',
            'open_configuration': 'Åbn konfiguration',
            'error_preparing_request': 'Forberedelse af anmodning mislykkedes',
            'empty_suggestion': 'Tomt forslag',
            'process_suggestion_error': 'Behandling af forslag mislykkedes',
            'unknown_error': 'Ukendt fejl',
            'unknown_model': 'Ukendt model: {model_name}',
            'suggestion_error': 'Forslagsfejl',
            'random_question_success': 'Tilfældigt spørgsmål genereret med succes!',
            'book_title_check': 'Bogens titel kræves',
            'avoid_repeat_question': 'Brug venligst et andet spørgsmål',
            'empty_answer': 'Tomt svar',
            'invalid_response': 'Ugyldigt svar',
            'auth_error_401': 'Uautoriseret',
            'auth_error_403': 'Adgang nægtet',
            'rate_limit': 'For mange anmodninger',
            'empty_response': 'Modtog tomt svar fra API',
            'empty_response_after_filter': 'Svaret er tomt efter filtrering af think-tags',
            'template_error': 'Skabelonfejl',
            'no_model_configured': 'Ingen AI-model konfigureret. Konfigurer venligst en AI-model i indstillingerne.',
            'no_ai_configured_title': 'Ingen AI konfigureret',
            'no_ai_configured_message': 'Velkommen! For at begynde at stille spørgsmål om dine bøger, skal du først konfigurere en AI-udbyder.\n\nGodt nyt: Dette plugin har nu en GRATIS version (Nvidia AI Free), som du kan bruge med det samme uden nogen konfiguration!\n\nAndre anbefalede muligheder:\n• Nvidia AI - Få 6 måneders GRATIS API-adgang kun med dit telefonnummer (ingen kreditkort påkrævet)\n• Ollama - Kør AI-modeller lokalt på din computer (helt gratis og privat)\n\nVil du åbne plugin-konfigurationen for at opsætte en AI-udbyder nu?',
            'open_settings': 'Plugin-konfiguration',
            'ask_anyway': 'Spørg alligevel',
            'later': 'Senere',
            'debug_settings': 'Fejlfindingsindstillinger',
            'enable_debug_logging': 'Aktivér fejlfindingslogning (ask_ai_plugin_debug.log)',
            'debug_logging_hint': 'Når deaktiveret, vil fejlfindingslogfiler ikke blive skrevet til fil. Dette kan forhindre, at logfilen bliver for stor.',
            'reset_all_data': 'Nulstil alle data',
            'reset_all_data_warning': 'Dette vil slette alle API-nøgler, prompt-skabeloner og lokale historikposter. Din sprogpræference bevares. Fortsæt venligst med forsigtighed.',
            'reset_all_data_confirm_title': 'Bekræft nulstilling',
            'reset_all_data_confirm_message': 'Er du sikker på, at du vil nulstille plugin\'et til dets oprindelige tilstand?\n\nDette vil permanent slette:\n• Alle API-nøgler\n• Alle brugerdefinerede prompt-skabeloner\n• Al samtalelhistorik\n• Alle plugin-indstillinger (sprogpræference bevares)\n\nDenne handling kan ikke fortrydes!',
            'reset_all_data_success': 'Alle plugin-data er blevet nulstillet. Genstart venligst calibre for at ændringerne træder i kraft.',
            'reset_all_data_failed': 'Kunne ikke nulstille plugin-data: {error}',
            'random_question_error': 'Fejl ved generering af tilfældigt spørgsmål',
            'clear_history_failed': 'Kunne ikke rydde historik',
            'clear_history_not_supported': 'Ryd historik for enkelt bog understøttes endnu ikke',
            'missing_required_config': 'Manglende påkrævet konfiguration: {key}. Tjek venligst dine indstillinger.',
            'api_key_too_short': 'API-nøglen er for kort. Tjek venligst og indtast den komplette nøgle.',

            # API response handling
            'api_request_failed': 'API-anmodning mislykkedes: {error}',
            'api_content_extraction_failed': 'Kunne ikke udtrække indhold fra API-svar',
            'api_invalid_response': 'Kunne ikke få gyldigt API-svar',
            'api_unknown_error': 'Ukendt fejl: {error}',

            # Stream response handling
            'stream_response_code': 'Stream-svar statuskode: {code}',
            'stream_continue_prompt': 'Fortsæt venligst dit forrige svar uden at gentage indhold, der allerede er leveret.',
            'stream_continue_code_blocks': 'Dit forrige svar havde uafsluttede kodeblokke. Fortsæt venligst og færdiggør disse kodeblokke.',
            'stream_continue_parentheses': 'Dit forrige svar havde uafsluttede parenteser. Fortsæt venligst og sørg for, at alle parenteser er korrekt lukket.',
            'stream_continue_interrupted': 'Dit forrige svar ser ud til at være blevet afbrudt. Fortsæt venligst med at færdiggøre din sidste tanke eller forklaring.',
            'stream_timeout_error': 'Stream-transmission har ikke modtaget nyt indhold i 60 sekunder, muligvis et forbindelsesproblem.',

            # API error messages
            'api_version_model_error': 'API-version eller modelnavnfejl: {message}\n\nOpdater venligst API Basis-URL til "{base_url}" og model til "{model}" eller anden tilgængelig model i indstillingerne.',
            'api_format_error': 'API-anmodningsformatfejl: {message}',
            'api_key_invalid': 'API-nøgle ugyldig eller uautoriseret: {message}\n\nTjek venligst din API-nøgle, og sørg for, at API-adgang er aktiveret.',
            'api_rate_limit': 'Anmodningsfrekvens overskredet, prøv venligst igen senere\n\nDu har muligvis overskredet den gratis brugskvote. Dette kan skyldes:\n1. For mange anmodninger pr. minut\n2. For mange anmodninger pr. dag\n3. For mange input-tokens pr. minut',

            # Configuration errors
            'missing_config_key': 'Manglende påkrævet konfigurationsnøgle: {key}',
            'api_base_url_required': 'API Basis-URL er påkrævet',
            'model_name_required': 'Modelnavn er påkrævet',

            # Model list fetching
            'fetching_models_from': 'Henter modeller fra {url}',
            'successfully_fetched_models': 'Succesfuldt hentet {count} {provider} modeller',
            'failed_to_fetch_models': 'Kunne ikke indlæse modeller: {error}',
            'api_key_empty': 'API-nøglen er tom. Indtast venligst en gyldig API-nøgle.',

            # Error messages for model fetching
            'error_401': 'API-nøgleautentificering mislykkedes. Kontroller venligst: API-nøgle er korrekt, konto har tilstrækkelig saldo, API-nøgle er ikke udløbet.',
            'error_403': 'Adgang nægtet. Kontroller venligst: API-nøgle har tilstrækkelige tilladelser, ingen regionale adgangsbegrænsninger.',
            'error_404': 'API-slutpunkt ikke fundet. Kontroller venligst, om API Basis-URL-konfigurationen er korrekt.',
            'error_429': 'For mange anmodninger, hastighedsgrænse nået. Prøv venligst igen senere.',
            'error_5xx': 'Serverfejl. Prøv venligst igen senere, eller kontroller tjenesteudbyderens status.',
            'error_network': 'Netværksforbindelse mislykkedes. Kontroller venligst netværksforbindelse, proxyindstillinger eller firewallkonfiguration.',
            'error_unknown': 'Ukendt fejl.',
            'technical_details': 'Tekniske detaljer',
            'ollama_service_not_running': 'Ollama-tjenesten kører ikke. Start venligst Ollama-tjenesten først.',
            'ollama_service_timeout': 'Ollama-tjenesteforbindelse timeout. Kontroller venligst, om tjenesten kører korrekt.',
            'ollama_model_not_available': 'Model "{model}" er ikke tilgængelig. Kontroller venligst:\n1. Er modellen startet? Kør: ollama run {model}\n2. Er modelnavnet korrekt?\n3. Er modellen downloadet? Kør: ollama pull {model}',
            'gemini_geo_restriction': 'Gemini API er ikke tilgængelig i din region. Prøv venligst:\n1. Brug en VPN til at forbinde fra en understøttet region\n2. Brug andre AI-udbydere (OpenAI, Anthropic, DeepSeek osv.)\n3. Tjek Google AI Studio for regions tilgængelighed',
            'model_test_success': 'Modeltest lykkedes!',
            'test_model_prompt': 'Modeller indlæst med succes! Vil du teste den valgte model "{model}"?',
            'test_model_button': 'Test model',
            'skip': 'Spring over',

            # About information
            'author_name': 'Sheldon',
            'user_manual': 'Brugermanual',
            'about_plugin': 'Om Ask AI Plugin',
            'learn_how_to_use': 'Sådan bruges det',
            'email': 'iMessage',

            # Model specific configurations
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Brugerdefineret',
            'model_enable_streaming': 'Aktivér streaming',

            # AI Switcher
            'current_ai': 'Nuværende AI',
            'no_configured_models': 'Ingen AI konfigureret - Konfigurer venligst i indstillinger',

            # Provider specific info
            'nvidia_free_info': '💡 Nye brugere får 6 måneders gratis API-adgang - Ingen kreditkort påkrævet',

            # Common system messages
            'default_system_message': 'Du er en ekspert i bogenanalyse. Din opgave er at hjælpe brugere med at forstå bøger bedre ved at give indsigtsfulde spørgsmål og analyser.',

            # Request timeout settings
            'request_timeout_label': 'Anmodningstimeout:',
            'seconds': 'sekunder',
            'request_timeout_error': 'Anmodningstimeout. Nuværende timeout: {timeout} sekunder',

            # Parallel AI settings
            'parallel_ai_count_label': 'Parallel AI-antal:',
            'parallel_ai_count_tooltip': 'Antal AI-modeller, der skal forespørges samtidigt (1-2 tilgængelige, 3-4 kommer snart)',
            'parallel_ai_notice': 'Bemærk: Dette påvirker kun afsendelse af spørgsmål. Tilfældige spørgsmål bruger altid en enkelt AI.',
            'suggest_maximize': 'Tip: Maksimér vinduet for bedre visning med 3 AI\'er',
            'ai_panel_label': 'AI {index}:',
            'no_ai_available': 'Ingen AI tilgængelig for dette panel',
            'add_more_ai_providers': 'Tilføj venligst flere AI-udbydere i indstillingerne',
            'select_ai': '-- Vælg AI --',
            'select_model': '-- Vælg model --',
            'request_model_list': 'Anmod venligst om modelliste',
            'coming_soon': 'Kommer snart',
            'advanced_feature_tooltip': 'Denne funktion er under udvikling. Følg med for opdateringer!',

            # AI Manager Dialog
            'ai_manager_title': 'Administrer AI-udbydere',
            'add_ai_title': 'Tilføj AI-udbyder',
            'manage_ai_title': 'Administrer konfigurerede AI\'er',
            'configured_ai_list': 'Konfigurerede AI\'er',
            'available_ai_list': 'Tilgængelige tilføjelser',
            'ai_config_panel': 'Konfiguration',
            'select_ai_to_configure': 'Vælg en AI fra listen for at konfigurere',
            'select_provider': 'Vælg AI-udbyder',
            'select_provider_hint': 'Vælg en udbyder fra listen',
            'select_ai_to_edit': 'Vælg en AI fra listen for at redigere',
            'set_as_default': 'Indstil som standard',
            'save_ai_config': 'Gem',
            'remove_ai_config': 'Fjern',
            'delete_ai': 'Slet',
            'add_ai_button': 'Tilføj AI',
            'edit_ai_button': 'Rediger AI',
            'manage_configured_ai_button': 'Administrer konfigurerede AI\'er',
            'manage_ai_button': 'Administrer AI',
            'no_configured_ai': 'Ingen AI konfigureret endnu',
            'no_configured_ai_hint': 'Ingen AI konfigureret. Plugin kan ikke fungere. Klik venligst "Tilføj AI" for at tilføje en AI-udbyder.',
            'default_ai_label': 'Standard-AI:',
            'default_ai_tag': 'Standard',
            'ai_not_configured_cannot_set_default': 'Denne AI er ikke konfigureret endnu. Gem venligst konfigurationen først.',
            'ai_set_as_default_success': '{name} er indstillet som standard-AI.',
            'ai_config_saved_success': '{name} konfiguration er gemt med succes.',
            'confirm_remove_title': 'Bekræft fjernelse',
            'confirm_remove_ai': 'Er du sikker på, at du vil fjerne {name}? Dette vil rydde API-nøglen og nulstille konfigurationen.',
            'confirm_delete_title': 'Bekræft sletning',
            'confirm_delete_ai': 'Er du sikker på, at du vil slette {name}?',
            'api_key_required': 'API-nøgle er påkrævet.',
            'configuration': 'Konfiguration',

            # Field descriptions
            'api_key_desc': 'Din API-nøgle til autentificering. Hold den sikker og del den ikke.',
            'base_url_desc': 'API-slutpunktets URL. Brug standard, medmindre du har et brugerdefineret slutpunkt.',
            'model_desc': 'Vælg en model fra listen, eller brug et brugerdefineret modelnavn.',
            'streaming_desc': 'Aktivér realtidsrespons-streaming for hurtigere feedback.',
            'advanced_section': 'Avanceret',

            # Provider-specific notices
            'perplexity_model_notice': 'Bemærk: Perplexity leverer ikke en offentlig modelliste-API, så modeller er hardkodet.',
            'ollama_no_api_key_notice': 'Bemærk: Ollama er en lokal model, der ikke kræver en API-nøgle.',
            'nvidia_free_credits_notice': 'Bemærk: Nye brugere får gratis API-kreditter - Ingen kreditkort påkrævet.',

            # Nvidia Free error messages
            'free_tier_rate_limit': 'Gratis niveau hastighedsgrænse overskredet. Prøv venligst igen senere, eller konfigurer din egen Nvidia API-nøgle.',
            'free_tier_unavailable': 'Gratis niveau er midlertidigt utilgængeligt. Prøv venligst igen senere, eller konfigurer din egen Nvidia API-nøgle.',
            'free_tier_server_error': 'Gratis niveau serverfejl. Prøv venligst igen senere.',
            'free_tier_error': 'Gratis niveau fejl',

            # Nvidia Free provider info
            'free': 'Gratis',
            'nvidia_free_provider_name': 'Nvidia AI (Gratis)',
            'nvidia_free_display_name': 'Nvidia AI (Gratis)',
            'nvidia_free_api_key_info': 'Vil blive hentet fra serveren',
            'nvidia_free_desc': 'Denne tjeneste vedligeholdes af udvikleren og holdes gratis, men kan være mindre stabil. For en mere stabil tjeneste, konfigurer venligst din egen Nvidia API-nøgle.',

            # Nvidia Free first use reminder
            'nvidia_free_first_use_title': 'Velkommen til Ask AI Plugin',
            'nvidia_free_first_use_message': 'Nu kan du bare spørge uden nogen konfiguration! Udvikleren vedligeholder et gratis niveau for dig, men det er muligvis ikke særlig stabilt. God fornøjelse!\n\nDu kan konfigurere dine egne AI-udbydere i indstillingerne for bedre stabilitet.',

            # Model buttons
            'refresh_model_list': 'Opdatér',
            'test_current_model': 'Test',
            'testing_text': 'Tester',
            'refresh_success': 'Modellisten blev opdateret med succes.',
            'refresh_failed': 'Kunne ikke opdatere modellisten.',
            'test_failed': 'Modeltest mislykkedes.',

            # Tooltip
            'manage_ai_disabled_tooltip': 'Tilføj venligst en AI-udbyder først.',

            # PDF export section titles
            'pdf_book_metadata': 'BOGMETADATA',
            'pdf_question': 'SPØRGSMÅL',
            'pdf_answer': 'SVAR',
            'pdf_ai_model_info': 'AI-MODELINFORMATION',
            'pdf_generated_by': 'GENERERET AF',
            'pdf_provider': 'Udbyder',
            'pdf_model': 'Model',
            'pdf_api_base_url': 'API Basis-URL',
            'pdf_panel': 'Panel',
            'pdf_plugin': 'Plugin',
            'pdf_github': 'GitHub',
            'pdf_software': 'Software',
            'pdf_generated_time': 'Genereringstid',
            'pdf_info_not_available': 'Information ikke tilgængelig',
        }