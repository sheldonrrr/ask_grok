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
        return 'Om boken "{title}": Forfatter: {author}, Forlag: {publisher}, Utgivelsesår: {pubyear}, bok i language: {language}, Serie: {series}, Spørsmålet mitt er: {query}'
    
    @property
    def suggestion_template(self) -> str:
        return """Du er en ekspert i bokanmeldelser. For boken "{title}" av {author}, publiceringsspråk er {language}, generer ÉT innsiktsfullt spørsmål som hjelper lesere med å forstå boken bedre. Regler: 1. Returner KUN spørsmålet, uten introduksjon eller forklaring 2. Fokuser på bokens innhold, ikke bare tittelen 3. Gjør spørsmålet praktisk og tankevekkende 4. Hold det kort (30-200 ord) 5. Vær kreativ og generer et annet spørsmål hver gang, selv for samme bok"""
    
    @property
    def multi_book_default_template(self) -> str:
        return """Her er informasjon om flere bøker: {books_metadata} Brukerens spørsmål: {query} Vennligst svar på spørsmålet basert på bokinformasjonen ovenfor."""
    
    @property
    def translations(self) -> dict:
        return {
            # Plugin informasjon
            'plugin_name': 'Ask AI Plugin',
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
            'stop_button': 'Stopp',
            'suggest_button': 'Tilfeldig spørsmål',
            'copy_response': 'Kopier svar',
            'copy_question_response': 'Kopier S&&S',
            'export_pdf': 'Eksporter PDF',
            'export_current_qa': 'Eksporter Nåværende S&S',
            'export_history': 'Eksporter Historikk',
            
            # Eksportinnstillinger
            'export_settings': 'Eksportinnstillinger',
            'enable_default_export_folder': 'Eksporter til standardmappe',
            'no_folder_selected': 'Ingen mappe valgt',
            'browse': 'Bla gjennom...',
            'select_export_folder': 'Velg Eksportmappe',
            
            # Knappetekst og menyelementer
            'copy_response_btn': 'Kopier Svar',
            'copy_qa_btn': 'Kopier S&S',
            'export_current_btn': 'Eksporter S&S som PDF',
            'export_history_btn': 'Eksporter Historikk som PDF',
            'copy_mode_response': 'Svar',
            'copy_mode_qa': 'S&S',
            'export_mode_current': 'Gjeldende S&S',
            'export_mode_history': 'Historikk',
            
            # PDF-eksport relatert
            'model_provider': 'Leverandør',
            'model_name': 'Modell',
            'model_api_url': 'API Basis-URL',
            'pdf_model_info': 'AI-Modellinformasjon',
            'pdf_software': 'Programvare',
            
            'export_all_history_dialog_title': 'Eksporter Hele Historikken til PDF',
            'export_all_history_title': 'HELE S&S HISTORIKK',
            'export_history_insufficient': 'Minst 2 historikkoppføringer kreves for å eksportere.',
            'history_record': 'Oppføring',
            'question_label': 'Spørsmål',
            'answer_label': 'Svar',
            'default_ai': 'Standard AI',
            'export_time': 'Eksportert',
            'total_records': 'Totale Oppføringer',
            'info': 'Informasjon',
            'yes': 'Ja',
            'no': 'Nei',
            'no_book_selected_title': 'Ingen Bok Valgt',
            'no_book_selected_message': 'Vennligst velg en bok før du stiller spørsmål.',
            'set_default_ai_title': 'Angi Standard AI',
            'set_default_ai_message': 'Du har byttet til "{0}". Vil du angi den som standard AI for fremtidige forespørsler?',
            'set_default_ai_success': 'Standard AI er satt til "{0}".',
            'copied': 'Kopiert!',
            'pdf_exported': 'PDF eksportert!',
            'export_pdf_dialog_title': 'Eksporter til PDF',
            'export_pdf_error': 'Feil ved PDF-eksport: {0}',
            'no_question': 'Ingen spørsmål',
            'no_response': 'Ingen svar',
            'saved': 'Lagret',
            'close_button': 'Lukk',
            'open_local_tutorial': 'Åpne lokal veiledning',
            'tutorial_open_failed': 'Kunne ikke åpne veiledning',
            
            # UI - Konfigurasjonsfelter
            'token_label': 'API-nøkkel:',
            'api_key_label': 'API-nøkkel:',
            'model_label': 'Modell:',
            'language_label': 'Språk:',
            'language_label_old': 'Språk',
            'base_url_label': 'Base-URL:',
            'base_url_placeholder': 'Standard: {default_api_base_url}',
            'shortcut': 'Snarvei',
            'shortcut_open_dialog': 'Åpne dialog',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Modell',
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
            'loading': 'Laster...',
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
            'error': 'Feil',
            
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

            # Multi-bok funksjon
            'books_unit': ' bøker',
            'new_conversation': 'Ny samtale',
            'single_book': 'Enkel bok',
            'multi_book': 'Multi-bok',
            'deleted': 'Slettet',
            'history': 'Historikk',
            'no_history': 'Ingen historikkoppføringer',
            'empty_question_placeholder': '(Ingen spørsmål)',
            'history_ai_unavailable': 'Denne AI er fjernet fra konfigurasjonen',
            'clear_current_book_history': 'Tøm Nåværende Bokhistorikk',
            'confirm_clear_book_history': 'Er du sikker på at du vil tømme all historikk for:\n{book_titles}?',
            'confirm': 'Bekreft',
            'history_cleared': '{deleted_count} historikkoppføringer tømt.',
            'multi_book_template_label': 'Flerbok Prompt Mal:',
            'multi_book_placeholder_hint': 'Bruk {books_metadata} for bokinformasjon, {query} for brukerens spørsmål',
            
            'network_error': 'Nettverksfeil',
            'request_timeout': 'Forespørsel tidsavbrudd',
            'request_failed': 'Forespørsel mislyktes',
            'question_too_long': 'Spørsmålet er for langt',
            'auth_token_required_title': 'API-nøkkel Påkrevd',
            'auth_token_required_message': 'Vennligst angi en gyldig API-nøkkel i Plugin-konfigurasjon.',
            'open_configuration': 'Åpne Konfigurasjon',
            'cancel': 'Avbryt',
            "invalid_default_ai_title": "Ugyldig Standard-AI",
            "invalid_default_ai_message": "Standard-AI \"{default_ai}\" er ikke riktig konfigurert.\n\nVil du bytte til \"{first_ai}\" i stedet?",
            "switch_to_ai": "Bytt til {ai}",
            "keep_current": "Behold Gjeldende",
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
            'template_error': 'Malfeil',
            'no_model_configured': 'Ingen AI-modell konfigurert. Vennligst konfigurer en AI-modell i innstillingene.',
            'no_ai_configured_title': 'Ingen AI Konfigurert',
            'no_ai_configured_message': 'Velkommen! For å begynne å stille spørsmål om bøkene dine, må du først konfigurere en AI-leverandør.\n\nAnbefalt for nybegynnere:\n• Nvidia AI - Få 6 måneders GRATIS API-tilgang med bare telefonnummeret ditt (ingen kredittkort nødvendig)\n• Ollama - Kjør AI-modeller lokalt på datamaskinen din (helt gratis og privat)\n\nØnsker du å åpne plugin-konfigurasjonen for å sette opp en AI-leverandør nå?',
            'open_settings': 'Plugin-konfigurasjon',
            'ask_anyway': 'Spør Likevel',
            'later': 'Senere',
            'reset_all_data': 'Tilbakestill Alle Data',
            'reset_all_data_warning': 'Dette vil slette alle API-nøkler, promptmaler og lokale historikkoppføringer. Språkinnstillingen din vil bli bevart. Vennligst fortsett med forsiktighet.',
            'reset_all_data_confirm_title': 'Bekreft Tilbakestilling',
            'reset_all_data_confirm_message': 'Er du sikker på at du vil tilbakestille pluginet til sin opprinnelige tilstand?\n\nDette vil permanent slette:\n• Alle API-nøkler\n• Alle tilpassede promptmaler\n• All samtalehistorikk\n• Alle plugin-innstillinger (språkinnstilling vil bli bevart)\n\nDenne handlingen kan ikke angres!',
            'reset_all_data_success': 'Alle plugin-data har blitt tilbakestilt. Vennligst start calibre på nytt for at endringene skal tre i kraft.',
            'reset_all_data_failed': 'Kunne ikke tilbakestille plugin-data: {error}',
            'random_question_error': 'Feil ved generering av tilfeldig spørsmål',
            'clear_history_failed': 'Kunne ikke slette historikk',
            'clear_history_not_supported': 'Sletting av historikk for en enkelt bok støttes ikke ennå',
            'missing_required_config': 'Manglende påkrevd konfigurasjon: {key}. Sjekk innstillingene dine.',
            'api_key_too_short': 'API-nøkkel er for kort. Sjekk og skriv inn hele nøkkelen.',
            
            # API-svarhåndtering
            'api_request_failed': 'API-forespørsel mislyktes: {error}',
            'api_content_extraction_failed': 'Klarte ikke å hente innhold fra API-svar',
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
            'about_plugin': 'Hvorfor Ask AI Plugin?',
            'learn_how_to_use': 'Hvordan bruke',
            'email': 'iMessage',
            
            # Modellspesifikke konfigurasjoner
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Tilpasset',
            'model_enable_streaming': 'Aktiver streaming',
            
            # AI Switcher
            'current_ai': 'Nåværende AI',
            'no_configured_models': 'Ingen AI konfigurert - Vennligst konfigurer i innstillingene',
            
            # Provider spesifikk info
            'nvidia_free_info': '💡 Nye brukere får 6 måneder gratis API-tilgang - Ingen kredittkort kreves',
            
            # Generelle systemmeldinger
            'default_system_message': 'Du er en ekspert på bokanalyse. Din oppgave er å hjelpe brukere med å forstå bøker bedre ved å gi innsiktsfulle spørsmål og analyser.',

            # Forespørsel tidsavbrudd innstillinger
            'request_timeout_label': 'Forespørsel tidsavbrudd:',
            'seconds': 'sekunder',
            'request_timeout_error': 'Forespørsel tidsavbrudd. Nåværende tidsavbrudd: {timeout} sekunder',
            
            # Parallelle AI innstillinger
            'parallel_ai_count_label': 'Antall parallelle AI-er:',
            'parallel_ai_count_tooltip': 'Antall AI-modeller å spørre samtidig (1-2 tilgjengelig, 3-4 kommer snart)',
            'parallel_ai_notice': 'Merk: Dette påvirker bare sending av spørsmål. Tilfeldige spørsmål bruker alltid én enkelt AI.',
            'suggest_maximize': 'Tips: Maksimer vinduet for bedre visning med 3 AI-er',
            'ai_panel_label': 'AI {index}:',
            'no_ai_available': 'Ingen AI tilgjengelig for dette panelet',
            'add_more_ai_providers': 'Vennligst legg til flere AI-leverandører i innstillingene',
            'select_ai': '-- Velg AI --',
            'select_model': '-- Bytt Modell --',
            'request_model_list': 'Vennligst be om modellliste',
            'coming_soon': 'Kommer snart',
            'advanced_feature_tooltip': 'Denne funksjonen er under utvikling. Følg med for oppdateringer!',
            
            # PDF-eksport seksjonstitler
            'pdf_book_metadata': 'BOK METADATA',
            'pdf_question': 'SPØRSMÅL',
            'pdf_answer': 'SVAR',
            'pdf_ai_model_info': 'AI MODELL INFORMASJON',
            'pdf_generated_by': 'GENERERT AV',
            'pdf_provider': 'Leverandør',
            'pdf_model': 'Modell',
            'pdf_api_base_url': 'API Base-URL',
            'pdf_panel': 'Panel',
            'pdf_plugin': 'Plugin',
            'pdf_github': 'GitHub',
            'pdf_software': 'Programvare',
            'pdf_generated_time': 'Generert tid',
            'default_ai_mismatch_title': 'Standard AI Endret',
            'default_ai_mismatch_message': 'Standard AI i konfigurasjonen er endret til "{default_ai}",\nmen gjeldende dialog bruker "{current_ai}".\n\nVil du bytte til den nye standard AI?',
            'discard_changes': 'Forkast Endringer',
            'empty_response': 'Mottok tomt svar fra API',
            'empty_response_after_filter': 'Svaret er tomt etter filtrering av think-tagger',
            'error_401': 'API-nøkkelautentisering mislyktes. Vennligst sjekk: API-nøkkelen er riktig, kontoen har tilstrekkelig saldo, API-nøkkelen har ikke utløpt.',
            'error_403': 'Tilgang nektet. Vennligst sjekk: API-nøkkelen har tilstrekkelige tillatelser, ingen regionale tilgangsbegrensninger.',
            'error_404': 'API-endepunkt ikke funnet. Vennligst sjekk om API Base URL-konfigurasjonen er riktig.',
            'error_429': 'For mange forespørsler, hastighetsbegrensning nådd. Vennligst prøv igjen senere.',
            'error_5xx': 'Serverfeil. Vennligst prøv igjen senere eller sjekk tjenesteleverandørens status.',
            'error_network': 'Nettverkstilkobling mislyktes. Vennligst sjekk nettverkstilkobling, proxy-innstillinger eller brannmur-konfigurasjon.',
            'error_unknown': 'Ukjent feil.',
            'gemini_geo_restriction': 'Gemini API er ikke tilgjengelig i din region. Vennligst prøv:\n1. Bruk en VPN for å koble til fra en støttet region\n2. Bruk andre AI-leverandører (OpenAI, Anthropic, DeepSeek, etc.)\n3. Sjekk Google AI Studio for regional tilgjengelighet',
            'load_models_list': 'Last Modellliste',
            'loading_models_text': 'Laster modeller',
            'model_test_success': 'Modelltest vellykket! Konfigurasjon lagret.',
            'models_loaded_with_selection': 'Lastet {count} modeller vellykket.\nValgt modell: {model}',
            'ollama_model_not_available': 'Modell "{model}" er ikke tilgjengelig. Vennligst sjekk:\n1. Er modellen startet? Kjør: ollama run {model}\n2. Er modellnavnet riktig?\n3. Er modellen lastet ned? Kjør: ollama pull {model}',
            'ollama_service_not_running': 'Ollama-tjenesten kjører ikke. Vennligst start Ollama-tjenesten først.',
            'ollama_service_timeout': 'Ollama-tjenestetilkobling tidsavbrudd. Vennligst sjekk om tjenesten kjører riktig.',
            'reset_ai_confirm_message': 'I ferd med å tilbakestille {ai_name} til standardtilstand.\n\nDette vil fjerne:\n• API-nøkkel\n• Tilpasset modellnavn\n• Andre konfigurerte parametere\n\nFortsette?',
            'reset_ai_confirm_title': 'Bekreft Tilbakestilling',
            'reset_current_ai': 'Tilbakestill Gjeldende AI til Standard',
            'reset_tooltip': 'Tilbakestill gjeldende AI til standardverdier',
            'save_and_close': 'Lagre og Lukk',
            'skip': 'Hopp Over',
            'technical_details': 'Tekniske Detaljer',
            'test_current_model': 'Test Gjeldende Modell',
            'test_model_button': 'Test Modell',
            'test_model_prompt': 'Modeller lastet vellykket! Vil du teste den valgte modellen "{model}"?',
            'unsaved_changes_message': 'Du har ulagrede endringer. Hva vil du gjøre?',
            'unsaved_changes_title': 'Ulagrede Endringer',


            'pdf_info_not_available': 'Informasjon ikke tilgjengelig',
        }