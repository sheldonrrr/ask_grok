#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Norwegian language translations for Ask AI Plugin.
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
        return 'Kontekst: Du hjelper en bruker av calibre (http://calibre-ebook.com), en kraftig e-bokhåndteringsapplikasjon, gjennom "Ask AI Plugin". Denne plugin-en lar brukere stille spørsmål om bøker i sitt calibre-bibliotek. Merk: Denne plugin-en kan bare svare på spørsmål om den valgte bokens innhold, temaer eller relaterte emner - den kan ikke direkte endre bokmetadata eller utføre calibre-operasjoner. Bokinformasjon: Tittel: "{title}", Forfatter: {author}, Utgiver: {publisher}, Utgivelsesår: {pubyear}, Språk: {language}, Serie: {series}. Brukerens spørsmål: {query}. Vennligst gi et nyttig svar basert på bokinformasjonen og din kunnskap.'

    @property
    def suggestion_template(self) -> str:
        return """Du er en ekspert bokkritiker. For boken "{title}" av {author}, utgivelsesspråk er {language}, generer ETT innsiktsfullt spørsmål som hjelper leserne til å bedre forstå bokens kjerneideer, praktiske anvendelser eller unike perspektiver. Regler: 1. Returner KUN spørsmålet, uten introduksjon eller forklaring 2. Fokuser på bokens innhold, ikke bare tittelen 3. Gjør spørsmålet praktisk og tankevekkende 4. Hold det kortfattet (30-200 ord) 5. Vær kreativ og generer et nytt spørsmål hver gang, selv for samme bok"""

    @property
    def multi_book_default_template(self) -> str:
        return """Her er informasjon om flere bøker: {books_metadata} Brukers spørsmål: {query} Vennligst svar på spørsmålet basert på ovennevnte bokinformasjon."""

    @property
    def translations(self) -> dict:
        return {
            # Plugin information
            'plugin_name': 'Spør AI-plugin',
            'plugin_desc': 'Still spørsmål om en bok ved hjelp av AI',

            # UI - Tabs and sections
            'config_title': 'Konfigurasjon',
            'general_tab': 'Generelt',
            'ai_models': 'AI-leverandører',
            'shortcuts': 'Snarveier',
            'shortcuts_note': "Du kan tilpasse disse snarveiene i calibre: Innstillinger -> Snarveier (søk 'Ask AI').\nDenne siden viser standard/eksempelsnarveier. Hvis du endret dem i Snarveier, har calibre-innstillingene forrang.",
            'prompts_tab': 'Prompts',
            'about': 'Om',
            'metadata': 'Metadata',

            # Section subtitles
            'language_settings': 'Språk',
            'language_subtitle': 'Velg foretrukket grensesnittspråk',
            'ai_providers_subtitle': 'Konfigurer AI-leverandører og velg din standard-AI',
            'prompts_subtitle': 'Tilpass hvordan spørsmål sendes til AI',
            'export_settings_subtitle': 'Angi standardmappe for eksport av PDF-filer',
            'debug_settings_subtitle': 'Aktiver feilsøkingslogging for feilsøking',
            'reset_all_data_subtitle': '⚠️ Advarsel: Dette vil permanent slette alle dine innstillinger og data',

            # Prompts tab
            'language_preference_title': 'Språkpreferanse',
            'language_preference_subtitle': 'Kontroller om AI-svar skal samsvare med grensesnittspråket ditt',
            'prompt_templates_title': 'Prompt-maler',
            'prompt_templates_subtitle': 'Tilpass hvordan bokinformasjon sendes til AI ved hjelp av dynamiske felt som {title}, {author}, {query}',
            'ask_prompts': 'Spør prompts',
            'random_questions_prompts': 'Prompts for tilfeldige spørsmål',
            'multi_book_prompts_label': 'Flere bøker prompts',
            'multi_book_placeholder_hint': 'Bruk {books_metadata} for bokinformasjon, {query} for brukerens spørsmål',
            'dynamic_fields_title': 'Referanse for dynamiske felt',
            'dynamic_fields_subtitle': 'Tilgjengelige felt og eksempelverdier fra "Frankenstein" av Mary Shelley',
            'dynamic_fields_examples': '<b>{title}</b> → Frankenstein<br><b>{author}</b> → Mary Shelley<br><b>{publisher}</b> → Lackington, Hughes, Harding, Mavor & Jones<br><b>{pubyear}</b> → 1818<br><b>{language}</b> → Engelsk<br><b>{series}</b> → (ingen)<br><b>{query}</b> → Din spørsmålstekst',
            'reset_prompts': 'Tilbakestill prompts til standard',
            'reset_prompts_confirm': 'Er du sikker på at du vil tilbakestille alle prompt-maler til standardverdiene? Denne handlingen kan ikke angres.',
            'unsaved_changes_title': 'Ulagrede endringer',
            'unsaved_changes_message': 'Du har ulagrede endringer i Prompts-fanen. Vil du lagre dem?',
            'use_interface_language': 'Be alltid AI om å svare på gjeldende plugin-grensesnittspråk',
            'language_instruction_label': 'Språkinstruksjon lagt til prompts:',
            'language_instruction_text': 'Vennligst svar på {language_name}.',

            # Persona settings
            'persona_title': 'Persona',
            'persona_subtitle': 'Definer din forskningsbakgrunn og mål for å hjelpe AI med å gi mer relevante svar',
            'use_persona': 'Bruk persona',
            'persona_label': 'Persona',
            'persona_placeholder': 'Som forsker ønsker jeg å forske gjennom bokdata.',
            'persona_hint': 'Jo mer AI vet om ditt mål og din bakgrunn, desto bedre blir forskningen eller genereringen.',

            # UI - Buttons and actions
            'ok_button': 'OK',
            'save_button': 'Lagre',
            'send_button': 'Send',
            'stop_button': 'Stopp',
            'suggest_button': 'Tilfeldig spørsmål',
            'copy_response': 'Kopier svar',
            'copy_question_response': 'Kopier S&S',
            'export_pdf': 'Eksporter PDF',
            'export_current_qa': 'Eksporter gjeldende S&S',
            'export_history': 'Eksporter historikk',
            'export_all_history_dialog_title': 'Eksporter all historikk til PDF',
            'export_all_history_title': 'ALL S&S HISTORIKK',
            'export_history_insufficient': 'Trenger minst 2 historikkposter for å eksportere.',
            'history_record': 'Post',
            'question_label': 'Spørsmål',
            'answer_label': 'Svar',
            'default_ai': 'Standard-AI',
            'export_time': 'Eksportert kl.',
            'total_records': 'Totalt antall poster',
            'info': 'Informasjon',
            'yes': 'Ja',
            'no': 'Nei',
            'no_book_selected_title': 'Ingen bok valgt',
            'no_book_selected_message': 'Velg en bok før du stiller spørsmål.',
            'set_default_ai_title': 'Angi standard-AI',
            'set_default_ai_message': 'Du har byttet til "{0}". Vil du angi den som standard-AI for fremtidige spørringer?',
            'set_default_ai_success': 'Standard-AI er satt til "{0}".',
            'default_ai_mismatch_title': 'Standard-AI endret',
            'default_ai_mismatch_message': 'Standard-AI i konfigurasjonen er endret til "{default_ai}",\nmen den aktuelle dialogen bruker "{current_ai}".\n\nVil du bytte til den nye standard-AI?',
            'copied': 'Kopiert!',
            'pdf_exported': 'PDF eksportert!',
            'export_pdf_dialog_title': 'Eksporter til PDF',
            'export_pdf_error': 'Kunne ikke eksportere PDF: {0}',
            'no_question': 'Ingen spørsmål',
            'no_response': 'Ingen svar',
            'saved': 'Lagret',
            'close_button': 'Lukk',
            'open_local_tutorial': 'Åpne lokal veiledning',
            'tutorial_open_failed': 'Kunne ikke åpne veiledning',
            'tutorial': 'Veiledning',

            'model_display_name_perplexity': 'Perplexity',

            # UI - Configuration fields
            'token_label': 'API-nøkkel:',
            'api_key_label': 'API-nøkkel:',
            'model_label': 'Modell:',
            'language_label': 'Språk:',
            'language_label_old': 'Språk',
            'base_url_label': 'Base-URL:',
            'base_url_placeholder': 'Standard: {default_api_base_url}',
            'shortcut': 'Snarveitast',
            'shortcut_open_dialog': 'Åpne dialog',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Modell',
            'action': 'Handling',
            'reset_button': 'Tilbakestill til standard',
            'reset_current_ai': 'Tilbakestill gjeldende AI til standard',
            'reset_ai_confirm_title': 'Bekreft tilbakestilling',
            'reset_ai_confirm_message': 'Er i ferd med å tilbakestille {ai_name} til standardtilstand.\n\nDette vil tømme:\n• API-nøkkel\n• Egendefinert modellnavn\n• Andre konfigurerte parametere\n\nFortsette?',
            'reset_tooltip': 'Tilbakestill gjeldende AI til standardverdier',
            'unsaved_changes_title': 'Ulagrede endringer',
            'unsaved_changes_message': 'Du har ulagrede endringer. Hva vil du gjøre?',
            'save_and_close': 'Lagre og lukk',
            'discard_changes': 'Forkast endringer',
            'cancel': 'Avbryt',
            'yes_button': 'Ja',
            'no_button': 'Nei',
            'cancel_button': 'Avbryt',
            'invalid_default_ai_title': 'Ugyldig standard-AI',
            'invalid_default_ai_message': 'Standard-AI "{default_ai}" er ikke riktig konfigurert.\n\nVil du bytte til "{first_ai}" i stedet?',
            'switch_to_ai': 'Bytt til {ai}',
            'keep_current': 'Behold gjeldende',
            'prompt_template': 'Prompt-mal',
            'ask_prompts': 'Spør prompts',
            'random_questions_prompts': 'Prompts for tilfeldige spørsmål',
            'display': 'Vis',
            'export_settings': 'Eksportinnstillinger',
            'enable_default_export_folder': 'Eksporter til standardmappe',
            'no_folder_selected': 'Ingen mappe valgt',
            'browse': 'Bla gjennom...',
            'select_export_folder': 'Velg eksportmappe',

            # Button text and menu items
            'copy_response_btn': 'Kopier svar',
            'copy_qa_btn': 'Kopier S&S',
            'export_current_btn': 'Eksporter S&S som PDF',
            'export_history_btn': 'Eksporter historikk som PDF',
            'copy_mode_response': 'Svar',
            'copy_mode_qa': 'S&S',
            'copy_format_plain': 'Ren tekst',
            'copy_format_markdown': 'Markdown',
            'export_mode_current': 'Gjeldende S&S',
            'export_mode_history': 'Historikk',

            # PDF Export related
            'model_provider': 'Leverandør',
            'model_name': 'Modell',
            'model_api_url': 'API Base-URL',
            'pdf_model_info': 'AI Modellinformasjon',
            'pdf_software': 'Programvare',

            # UI - Dialog elements
            'input_placeholder': 'Skriv inn spørsmålet ditt...',
            'response_placeholder': 'Svar kommer snart...',

            # UI - Menu items
            'menu_title': 'Spør AI',
            'menu_ask': 'Spør',

            # UI - Status information
            'loading': 'Laster',
            'loading_text': 'Spør',
            'loading_models_text': 'Laster modeller',
            'save_success': 'Innstillinger lagret',
            'sending': 'Sender...',
            'requesting': 'Ber om',
            'formatting': 'Forespørsel vellykket, formaterer',

            # UI - Model list feature
            'load_models': 'Last inn modeller',
            'load_models_list': 'Last inn modelliste',
            'test_current_model': 'Test gjeldende modell',
            'use_custom_model': 'Bruk egendefinert modellnavn',
            'custom_model_placeholder': 'Skriv inn egendefinert modellnavn',
            'model_placeholder': 'Last inn modeller først',
            'models_loaded': 'Vellykket lastet {count} modeller',
            'models_loaded_with_selection': 'Vellykket lastet {count} modeller.\nValgt modell: {model}',
            'load_models_failed': 'Kunne ikke laste modeller: {error}',
            'model_list_not_supported': 'Denne leverandøren støtter ikke automatisk henting av modelliste',
            'api_key_required': 'Vennligst skriv inn API-nøkkel først',
            'invalid_params': 'Ugyldige parametere',
            'warning': 'Advarsel',
            'success': 'Suksess',
            'error': 'Feil',

            # Metadata fields
            'metadata_title': 'Tittel',
            'metadata_authors': 'Forfatter',
            'metadata_publisher': 'Utgiver',
            'metadata_pubdate': 'Publiseringsdato',
            'metadata_pubyear': 'Utgivelsesår',
            'metadata_language': 'Språk',
            'metadata_series': 'Serie',
            'no_metadata': 'Ingen metadata',
            'no_series': 'Ingen serie',
            'unknown': 'Ukjent',

            # Multi-book feature
            'books_unit': ' bøker',
            'new_conversation': 'Ny samtale',
            'single_book': 'Enkelt bok',
            'multi_book': 'Flere bøker',
            'deleted': 'Slettet',
            'history': 'Historikk',
            'no_history': 'Ingen historikkposter',
            'empty_question_placeholder': '(Ingen spørsmål)',
            'history_ai_unavailable': 'Denne AI-en er fjernet fra konfigurasjonen',
            'clear_current_book_history': 'Tøm historikk for gjeldende bok',
            'confirm_clear_book_history': 'Er du sikker på at du vil tømme all historikk for:\n{book_titles}?',
            'confirm': 'Bekreft',
            'history_cleared': '{deleted_count} historikkposter tømt.',
            'multi_book_template_label': 'Flere bøker prompt-mal:',
            'multi_book_placeholder_hint': 'Bruk {books_metadata} for bokinformasjon, {query} for brukerens spørsmål',

            # Error messages (Note: 'error' is already defined above, these are other error types)
            'network_error': 'Tilkoblingsfeil',
            'request_timeout': 'Forespørsel tidsavbrutt',
            'request_failed': 'Forespørsel mislyktes',
            'request_stopped': 'Forespørsel stoppet',
            'question_too_long': 'Spørsmål for langt',
            'auth_token_required_title': 'AI-tjeneste kreves',
            'auth_token_required_message': 'Konfigurer en gyldig AI-tjeneste i plugin-konfigurasjonen.',
            'open_configuration': 'Åpne konfigurasjon',
            'error_preparing_request': 'Forespørselsforberedelse mislyktes',
            'empty_suggestion': 'Tomt forslag',
            'process_suggestion_error': 'Forslagsbehandlingsfeil',
            'unknown_error': 'Ukjent feil',
            'unknown_model': 'Ukjent modell: {model_name}',
            'suggestion_error': 'Forslagsfeil',
            'random_question_success': 'Tilfeldig spørsmål generert vellykket!',
            'book_title_check': 'Boktittel er påkrevd',
            'avoid_repeat_question': 'Vennligst bruk et annet spørsmål',
            'empty_answer': 'Tomt svar',
            'invalid_response': 'Ugyldig svar',
            'auth_error_401': 'Uautorisert',
            'auth_error_403': 'Tilgang nektet',
            'rate_limit': 'For mange forespørsler',
            'empty_response': 'Mottok tomt svar fra API',
            'empty_response_after_filter': 'Svar er tomt etter filtrering av tenk-tagger',
            'no_response': 'Ingen svar',
            'template_error': 'Maloppsettfeil',
            'no_model_configured': 'Ingen AI-modell konfigurert. Konfigurer en AI-modell i innstillingene.',
            'no_ai_configured_title': 'Ingen AI konfigurert',
            'no_ai_configured_message': 'Velkommen! For å begynne å stille spørsmål om bøkene dine, må du først konfigurere en AI-leverandør.\n\nGodt nytt: Denne plugin-en har nå en GRATIS nivå (Nvidia AI Free) som du kan bruke umiddelbart uten konfigurasjon!\n\nAndre anbefalte alternativer:\n• Nvidia AI - Få 6 måneder GRATIS API-tilgang med kun telefonnummeret ditt (ingen kredittkort kreves)\n• Ollama - Kjør AI-modeller lokalt på datamaskinen din (helt gratis og privat)\n\nVil du åpne plugin-konfigurasjonen for å sette opp en AI-leverandør nå?',
            'open_settings': 'Plugin-konfigurasjon',
            'ask_anyway': 'Spør likevel',
            'later': 'Senere',
            'debug_settings': 'Feilsøkingsinnstillinger',
            'enable_debug_logging': 'Aktiver feilsøkingslogging (ask_ai_plugin_debug.log)',
            'debug_logging_hint': 'Når deaktivert, vil feilsøkingslogger ikke bli skrevet til fil. Dette kan forhindre at loggfilen blir for stor.',
            'reset_all_data': 'Tilbakestill alle data',
            'reset_all_data_warning': 'Dette vil slette alle API-nøkler, prompt-maler og lokale historikkposter. Din språkpreferanse vil bli bevart. Vennligst fortsett med forsiktighet.',
            'reset_all_data_confirm_title': 'Bekreft tilbakestilling',
            'reset_all_data_confirm_message': 'Er du sikker på at du vil tilbakestille plugin-en til dens opprinnelige tilstand?\n\nDette vil permanent slette:\n• Alle API-nøkler\n• Alle egendefinerte prompt-maler\n• All samtalehistorikk\n• Alle plugin-innstillinger (språkpreferanse vil bli bevart)\n\nDenne handlingen kan ikke angres!',
            'reset_all_data_success': 'Alle plugindata er tilbakestilt. Start calibre på nytt for at endringene skal tre i kraft.',
            'reset_all_data_failed': 'Kunne ikke tilbakestille plugindata: {error}',
            'random_question_error': 'Feil ved generering av tilfeldig spørsmål',
            'clear_history_failed': 'Kunne ikke tømme historikk',
            'clear_history_not_supported': 'Tømming av historikk for enkeltbok støttes ennå ikke',
            'missing_required_config': 'Mangler nødvendig konfigurasjon: {key}. Kontroller innstillingene dine.',
            'api_key_too_short': 'API-nøkkelen er for kort. Kontroller og skriv inn hele nøkkelen.',

            # API response handling
            'api_request_failed': 'API-forespørsel mislyktes: {error}',
            'api_content_extraction_failed': 'Kunne ikke trekke ut innhold fra API-svar',
            'api_invalid_response': 'Kunne ikke få gyldig API-svar',
            'api_unknown_error': 'Ukjent feil: {error}',

            # Stream response handling
            'stream_response_code': 'Strømmingssvar statuskode: {code}',
            'stream_continue_prompt': 'Vennligst fortsett ditt forrige svar uten å gjenta innhold som allerede er gitt.',
            'stream_continue_code_blocks': 'Ditt forrige svar hadde uavsluttede kodeblokker. Vennligst fortsett og fullfør disse kodeblokkene.',
            'stream_continue_parentheses': 'Ditt forrige svar hadde uavsluttede parenteser. Vennligst fortsett og sørg for at alle parenteser er riktig lukket.',
            'stream_continue_interrupted': 'Ditt forrige svar ser ut til å ha blitt avbrutt. Vennligst fortsett med å fullføre din siste tanke eller forklaring.',
            'stream_timeout_error': 'Strømmeoverføringen har ikke mottatt nytt innhold på 60 sekunder, muligens et tilkoblingsproblem.',

            # API error messages
            'api_version_model_error': 'API-versjon eller modellnavnfeil: {message}\n\nOppdater API Base-URL til "{base_url}" og modell til "{model}" eller annen tilgjengelig modell i innstillingene.',
            'api_format_error': 'API-forespørselsformatfeil: {message}',
            'api_key_invalid': 'API-nøkkel ugyldig eller uautorisert: {message}\n\nKontroller din API-nøkkel og sørg for at API-tilgang er aktivert.',
            'api_rate_limit': 'Forespørselsrate-grense overskredet, prøv igjen senere\n\nDu kan ha overskredet den gratis brukskvoten. Dette kan skyldes:\n1. For mange forespørsler per minutt\n2. For mange forespørsler per dag\n3. For mange inndatatokens per minutt',

            # Configuration errors
            'missing_config_key': 'Mangler påkrevd konfigurasjonsnøkkel: {key}',
            'api_base_url_required': 'API Base-URL er påkrevd',
            'model_name_required': 'Modellnavn er påkrevd',

            # Model list fetching
            'fetching_models_from': 'Henter modeller fra {url}',
            'successfully_fetched_models': 'Vellykket hentet {count} {provider} modeller',
            'failed_to_fetch_models': 'Kunne ikke laste modeller: {error}',
            'api_key_empty': 'API-nøkkelen er tom. Vennligst skriv inn en gyldig API-nøkkel.',

            # Error messages for model fetching
            'error_401': 'API-nøkkelautentisering mislyktes. Kontroller: API-nøkkel er riktig, kontoen har tilstrekkelig saldo, API-nøkkelen er ikke utløpt.',
            'error_403': 'Tilgang nektet. Kontroller: API-nøkkelen har tilstrekkelige tillatelser, ingen regionale tilgangsbegrensninger.',
            'error_404': 'API-endepunkt ikke funnet. Kontroller om konfigurasjonen for API Base-URL er riktig.',
            'error_429': 'For mange forespørsler, rate-limit nådd. Prøv igjen senere.',
            'error_5xx': 'Serverfeil. Prøv igjen senere eller kontroller statusen til tjenesteleverandøren.',
            'error_network': 'Nettverkstilkobling mislyktes. Kontroller nettverkstilkobling, proxy-innstillinger eller brannmurkonfigurasjon.',
            'error_unknown': 'Ukjent feil.',
            'technical_details': 'Tekniske detaljer',
            'ollama_service_not_running': 'Ollama-tjenesten kjører ikke. Start Ollama-tjenesten først.',
            'ollama_service_timeout': 'Ollama-tjenestetilkobling tidsavbrutt. Kontroller om tjenesten kjører riktig.',
            'ollama_model_not_available': 'Modell "{model}" er ikke tilgjengelig. Kontroller:\n1. Er modellen startet? Kjør: ollama run {model}\n2. Er modellnavnet riktig?\n3. Er modellen lastet ned? Kjør: ollama pull {model}',
            'gemini_geo_restriction': 'Gemini API er ikke tilgjengelig i din region. Prøv:\n1. Bruk en VPN for å koble til fra en støttet region\n2. Bruk andre AI-leverandører (OpenAI, Anthropic, DeepSeek, etc.)\n3. Sjekk Google AI Studio for regional tilgjengelighet',
            'model_test_success': 'Modelltest vellykket!',
            'test_model_prompt': 'Modeller lastet inn! Vil du teste den valgte modellen "{model}"?',
            'test_model_button': 'Test modell',
            'skip': 'Hopp over',

            # About information
            'author_name': 'Sheldon',
            'user_manual': 'Brukerveiledning',
            'about_plugin': 'Om Ask AI Plugin',
            'learn_how_to_use': 'Hvordan bruke',
            'email': 'iMessage',

            # Model specific configurations
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Egendefinert',
            'model_enable_streaming': 'Aktiver strømming',

            # AI Switcher
            'current_ai': 'Gjeldende AI',
            'no_configured_models': 'Ingen AI konfigurert - Konfigurer i innstillinger',

            # Provider specific info
            'nvidia_free_info': '💡 Nye brukere får 6 måneder gratis API-tilgang - Ingen kredittkort kreves',

            # Common system messages
            'default_system_message': 'Du er en ekspert i bokenalyse. Din oppgave er å hjelpe brukere med å forstå bøker bedre ved å gi innsiktsfulle spørsmål og analyser.',

            # Request timeout settings
            'request_timeout_label': 'Forespørsel tidsavbrudd:',
            'seconds': 'sekunder',
            'request_timeout_error': 'Forespørsel tidsavbrutt. Gjeldende tidsavbrudd: {timeout} sekunder',

            # Parallel AI settings
            'parallel_ai_count_label': 'Antall parallelle AI-er:',
            'parallel_ai_count_tooltip': 'Antall AI-modeller som skal spørres samtidig (1-2 tilgjengelig, 3-4 kommer snart)',
            'parallel_ai_notice': 'Merk: Dette påvirker kun sending av spørsmål. Tilfeldige spørsmål bruker alltid én enkelt AI.',
            'suggest_maximize': 'Tips: Maksimer vinduet for bedre visning med 3 AI-er',
            'ai_panel_label': 'AI {index}:',
            'no_ai_available': 'Ingen AI tilgjengelig for dette panelet',
            'add_more_ai_providers': 'Legg til flere AI-leverandører i innstillingene',
            'select_ai': '-- Velg AI --',
            'select_model': '-- Velg modell --',
            'request_model_list': 'Be om modelliste',
            'coming_soon': 'Kommer snart',
            'advanced_feature_tooltip': 'Denne funksjonen er under utvikling. Følg med for oppdateringer!',

            # AI Manager Dialog
            'ai_manager_title': 'Administrer AI-leverandører',
            'add_ai_title': 'Legg til AI-leverandør',
            'manage_ai_title': 'Administrer konfigurert AI',
            'configured_ai_list': 'Konfigurert AI',
            'available_ai_list': 'Tilgjengelig for å legge til',
            'ai_config_panel': 'Konfigurasjon',
            'select_ai_to_configure': 'Velg en AI fra listen for å konfigurere',
            'select_provider': 'Velg AI-leverandør',
            'select_provider_hint': 'Velg en leverandør fra listen',
            'select_ai_to_edit': 'Velg en AI fra listen for å redigere',
            'set_as_default': 'Angi som standard',
            'save_ai_config': 'Lagre',
            'remove_ai_config': 'Fjern',
            'delete_ai': 'Slett',
            'add_ai_button': 'Legg til AI',
            'edit_ai_button': 'Rediger AI',
            'manage_configured_ai_button': 'Administrer konfigurert AI',
            'manage_ai_button': 'Administrer AI',
            'no_configured_ai': 'Ingen AI konfigurert ennå',
            'no_configured_ai_hint': 'Ingen AI konfigurert. Plugin-en kan ikke fungere. Klikk "Legg til AI" for å legge til en AI-leverandør.',
            'default_ai_label': 'Standard AI:',
            'default_ai_tag': 'Standard',
            'ai_not_configured_cannot_set_default': 'Denne AI-en er ikke konfigurert ennå. Lagre konfigurasjonen først.',
            'ai_set_as_default_success': '{name} er angitt som standard AI.',
            'ai_config_saved_success': '{name}-konfigurasjonen er lagret.',
            'confirm_remove_title': 'Bekreft fjerning',
            'confirm_remove_ai': 'Er du sikker på at du vil fjerne {name}? Dette vil tømme API-nøkkelen og tilbakestille konfigurasjonen.',
            'confirm_delete_title': 'Bekreft sletting',
            'confirm_delete_ai': 'Er du sikker på at du vil slette {name}?',
            'api_key_required': 'API-nøkkel er påkrevd.',
            'configuration': 'Konfigurasjon',

            # Field descriptions
            'api_key_desc': 'Din API-nøkkel for autentisering. Hold den sikker og ikke del den.',
            'base_url_desc': 'API-endepunktets URL. Bruk standard med mindre du har et egendefinert endepunkt.',
            'model_desc': 'Velg en modell fra listen eller bruk et egendefinert modellnavn.',
            'streaming_desc': 'Aktiver sanntidsstrømming av svar for raskere tilbakemelding.',
            'advanced_section': 'Avansert',

            # Provider-specific notices
            'perplexity_model_notice': 'Merk: Perplexity tilbyr ikke en offentlig API for modellister, så modellene er hardkodet.',
            'ollama_no_api_key_notice': 'Merk: Ollama er en lokal modell som ikke krever en API-nøkkel.',
            'nvidia_free_credits_notice': 'Merk: Nye brukere får gratis API-kreditter - ingen kredittkort kreves.',

            # Nvidia Free error messages
            'free_tier_rate_limit': 'Gratisnivåets rate-limit er overskredet. Prøv igjen senere eller konfigurer din egen Nvidia API-nøkkel.',
            'free_tier_unavailable': 'Gratisnivået er midlertidig utilgjengelig. Prøv igjen senere eller konfigurer din egen Nvidia API-nøkkel.',
            'free_tier_server_error': 'Gratisnivåets serverfeil. Prøv igjen senere.',
            'free_tier_error': 'Gratisnivåfeil',

            # Nvidia Free provider info
            'free': 'Gratis',
            'nvidia_free_provider_name': 'Nvidia AI (Gratis)',
            'nvidia_free_display_name': 'Nvidia AI (Gratis)',
            'nvidia_free_api_key_info': 'Vil bli hentet fra server',
            'nvidia_free_desc': 'Denne tjenesten vedlikeholdes av utvikleren og holdes gratis, men kan være mindre stabil. For mer stabil tjeneste, konfigurer din egen Nvidia API-nøkkel.',

            # Nvidia Free first use reminder
            'nvidia_free_first_use_title': 'Velkommen til Ask AI Plugin',
            'nvidia_free_first_use_message': 'Nå kan du spørre uten konfigurasjon! Utvikleren vedlikeholder en gratisversjon for deg, men den er kanskje ikke så stabil. Kos deg!\n\nDu kan konfigurere dine egne AI-leverandører i innstillingene for bedre stabilitet.',

            # Model buttons
            'refresh_model_list': 'Oppdater',
            'test_current_model': 'Test',
            'testing_text': 'Tester',
            'refresh_success': 'Modellisten ble oppdatert.',
            'refresh_failed': 'Kunne ikke oppdatere modellisten.',
            'test_failed': 'Modelltest mislyktes.',

            # Tooltip
            'manage_ai_disabled_tooltip': 'Legg til en AI-leverandør først.',

            # PDF export section titles
            'pdf_book_metadata': 'BOKMETADATA',
            'pdf_question': 'SPØRSMÅL',
            'pdf_answer': 'SVAR',
            'pdf_ai_model_info': 'AI-MODELLINFORMASJON',
            'pdf_generated_by': 'GENERERT AV',
            'pdf_provider': 'Leverandør',
            'pdf_model': 'Modell',
            'pdf_api_base_url': 'API Base-URL',
            'pdf_panel': 'Panel',
            'pdf_plugin': 'Plugin',
            'pdf_github': 'GitHub',
            'pdf_software': 'Programvare',
            'pdf_generated_time': 'Generert tid',
            'pdf_info_not_available': 'Informasjon ikke tilgjengelig',

            #AI Search v1.4.2
            'library_tab': 'Søk',
            'library_search': 'AI-søk',
            'library_info': 'AI-søk er alltid aktivert. Når du ikke velger noen bøker, kan du søke i hele biblioteket ditt med naturlig språk.',
            'library_enable': 'Aktiver AI-søk',
            'library_enable_tooltip': 'Når aktivert, kan du søke i biblioteket ditt med AI når ingen bøker er valgt',
            'library_update': 'Oppdater bibliotekdata',
            'library_update_tooltip': 'Hent ut boktitler og forfattere fra biblioteket ditt',
            'library_updating': 'Oppdaterer...',
            'library_status': 'Status: {count} bøker, siste oppdatering: {time}',
            'library_status_empty': 'Status: Ingen data. Klikk "Oppdater bibliotekdata" for å starte.',
            'library_status_error': 'Status: Feil ved lasting av data',
            'library_update_success': 'Oppdaterte {count} bøker',
            'library_update_failed': 'Kunne ikke oppdatere bibliotekdata',
            'library_no_gui': 'GUI ikke tilgjengelig',
            'library_init_title': 'Initialiser AI-søk',
            'library_init_message': 'AI-søk krever metadata fra biblioteket for å fungere. Vil du initialisere det nå?\n\nDette vil hente ut boktitler og forfattere fra biblioteket ditt.',
            'library_init_required': 'AI-søk kan ikke aktiveres uten bibliotekdata. Vennligst klikk "Oppdater bibliotekdata" når du er klar.',
            'ai_search_welcome_title': 'Velkommen til AI-søk',
            'ai_search_welcome_message': 'Du har ikke valgt noen bøker, så AI-søk er aktivert!\n\nDu kan nå søke i hele biblioteket med naturlig språk. Prøv for eksempel:\n• "Har du noen bøker om Python?"\n• "Vis meg bøker av Isaac Asimov"\n• "Finn bøker om maskinlæring"\n\nAI vil søke i biblioteket ditt og anbefale relevante bøker.',
            'ai_search_not_enough_books_title': 'Ikke nok bøker',
            'ai_search_not_enough_books_message': 'AI-søk krever minst {min_books} bøker i biblioteket ditt.\n\nDitt nåværende bibliotek har bare {book_count} bok/bøker.\n\nVennligst legg til flere bøker for å bruke AI-søk.',
            'ai_search_mode_info': 'Søker i hele biblioteket',
            'ai_search_privacy_title': 'Personvernerklæring',
            'ai_search_privacy_alert': 'AI-søk bruker bokmetadata (titler og forfattere). Denne informasjonen sendes til AI-leverandøren du har konfigurert for å behandle søkene dine.',
            'ai_search_updated_info': 'Oppdaterte {count} bøker {time_ago}',
            'ai_search_books_info': '{count} bøker indeksert',
            'days_ago': '{n} dager siden',
            'hours_ago': '{n} timer siden',
            'minutes_ago': '{n} minutter siden',
            'just_now': 'akkurat nå',
        }