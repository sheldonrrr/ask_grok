#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Swedish language translations for Ask AI Plugin.
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
        return 'Kontext: Du hjälper en användare av calibre (http://calibre-ebook.com), en kraftfull e-bokshanteringsapplikation, genom "Ask AI Plugin". Detta plugin låter användare ställa frågor om böcker i sitt calibre-bibliotek. Observera: Detta plugin kan bara svara på frågor om den valda bokens innehåll, teman eller relaterade ämnen - det kan inte direkt ändra bokmetadata eller utföra calibre-operationer. Bokinformation: Titel: "{title}", Författare: {author}, Förlag: {publisher}, Utgivningsår: {pubyear}, Språk: {language}, Serie: {series}. Användarens fråga: {query}. Vänligen ge ett användbart svar baserat på bokinformationen och din kunskap.'

    @property
    def suggestion_template(self) -> str:
        return """Du är en expert bokrecensent. För boken "{title}" av {author}, publiceringsspråk är {language}, generera EN insiktsfull fråga som hjälper läsarna att bättre förstå bokens kärnidér, praktiska tillämpningar eller unika perspektiv. Regler: 1. Returnera ENDAST frågan, utan introduktion eller förklaring 2. Fokusera på bokens innehåll, inte bara dess titel 3. Gör frågan praktisk och tankeväckande 4. Håll den koncis (30-200 ord) 5. Var kreativ och generera en ny fråga varje gång, även för samma bok"""

    @property
    def multi_book_default_template(self) -> str:
        return """Här är information om flera böcker: {books_metadata} Användarfråga: {query} Vänligen svara på frågan baserat på ovanstående bokinformation."""

    @property
    def translations(self) -> dict:
        return {
            # Plugin information
            'plugin_name': 'Fråga AI-plugin',
            'plugin_desc': 'Ställ frågor om en bok med hjälp av AI',

            # UI - Tabs and sections
            'config_title': 'Konfiguration',
            'general_tab': 'Allmänt',
            'ai_models': 'AI-leverantörer',
            'shortcuts': 'Genvägar',
            'shortcuts_note': "Du kan anpassa dessa genvägar i calibre: Inställningar -> Genvägar (sök 'Ask AI').\nDen här sidan visar standard-/exempelgenvägarna. Om du ändrade dem i Genvägar, har calibres inställningar företräde.",
            'prompts_tab': 'Prompter',
            'about': 'Om',
            'metadata': 'Metadata',

            # Section subtitles
            'language_settings': 'Språk',
            'language_subtitle': 'Välj ditt föredragna gränssnittsspråk',
            'ai_providers_subtitle': 'Konfigurera AI-leverantörer och välj din standard-AI',
            'prompts_subtitle': 'Anpassa hur frågor skickas till AI',
            'export_settings_subtitle': 'Ställ in standardmapp för export av PDF-filer',
            'reset_all_data_subtitle': 'Varning: Detta kommer permanent att radera alla dina inställningar och data',

            # Prompts tab
            'language_preference_title': 'Språkpreferens',
            'language_preference_subtitle': 'Kontrollera om AI-svar ska matcha ditt gränssnittsspråk',
            'prompt_templates_title': 'Promptmallar',
            'prompt_templates_subtitle': 'Anpassa hur bokinformation skickas till AI med dynamiska fält som {title}, {author}, {query}',
            'ask_prompts': 'Frågeprompter',
            'random_questions_prompts': 'Prompter för slumpmässiga frågor',
            'multi_book_prompts_label': 'Flerboksprompter',
            'multi_book_placeholder_hint': 'Använd {books_metadata} för bokinformation, {query} för användarens fråga',
            'dynamic_fields_title': 'Referens för dynamiska fält',
            'dynamic_fields_subtitle': 'Tillgängliga fält och exempelvärden från "Frankenstein" av Mary Shelley',
            'dynamic_fields_examples': '<b>{title}</b> → Frankenstein<br><b>{author}</b> → Mary Shelley<br><b>{publisher}</b> → Lackington, Hughes, Harding, Mavor & Jones<br><b>{pubyear}</b> → 1818<br><b>{language}</b> → Engelska<br><b>{series}</b> → (ingen)<br><b>{query}</b> → Din frågetext',
            'reset_prompts': 'Återställ prompter till standard',
            'reset_prompts_confirm': 'Är du säker på att du vill återställa alla promptmallar till deras standardvärden? Denna åtgärd kan inte ångras.',
            'unsaved_changes_title': 'Osparade ändringar',
            'unsaved_changes_message': 'Du har osparade ändringar i fliken Prompter. Vill du spara dem?',
            'use_interface_language': 'Be alltid AI att svara på aktuellt plugins gränssnittsspråk',
            'language_instruction_label': 'Språkinstruktion tillagd i prompter:',
            'language_instruction_text': 'Vänligen svara på {language_name}.',

            # Persona settings
            'persona_title': 'Persona',
            'persona_subtitle': 'Definiera din forskningsbakgrund och dina mål för att hjälpa AI att ge mer relevanta svar',
            'use_persona': 'Använd persona',
            'persona_label': 'Persona',
            'persona_placeholder': 'Som forskare vill jag forska genom bokdata.',
            'persona_hint': 'Ju mer AI vet om ditt mål och din bakgrund, desto bättre blir forskningen eller genereringen.',

            # UI - Buttons and actions
            'ok_button': 'OK',
            'save_button': 'Spara',
            'send_button': 'Skicka',
            'stop_button': 'Stoppa',
            'suggest_button': 'Slumpmässig fråga',
            'copy_response': 'Kopiera svar',
            'copy_question_response': 'Kopiera F&S',
            'export_pdf': 'Exportera PDF',
            'export_current_qa': 'Exportera aktuell F&S',
            'export_history': 'Exportera historik',
            'export_all_history_dialog_title': 'Exportera all historik till PDF',
            'export_all_history_title': 'ALL F&S HISTORIK',
            'export_history_insufficient': 'Behöver minst 2 historikposter för att exportera.',
            'history_record': 'Post',
            'question_label': 'Fråga',
            'answer_label': 'Svar',
            'default_ai': 'Standard-AI',
            'export_time': 'Exporterades',
            'total_records': 'Totalt antal poster',
            'info': 'Information',
            'yes': 'Ja',
            'no': 'Nej',
            'no_book_selected_title': 'Ingen bok vald',
            'no_book_selected_message': 'Välj en bok innan du ställer frågor.',
            'set_default_ai_title': 'Ställ in standard-AI',
            'set_default_ai_message': 'Du har växlat till "{0}". Vill du ställa in den som standard-AI för framtida frågor?',
            'set_default_ai_success': 'Standard-AI har ställts in till "{0}".',
            'default_ai_mismatch_title': 'Standard-AI ändrad',
            'default_ai_mismatch_message': 'Standard-AI i konfigurationen har ändrats till "{default_ai}",\nmen den aktuella dialogen använder "{current_ai}".\n\nVill du byta till den nya standard-AI?',
            'copied': 'Kopierat!',
            'pdf_exported': 'PDF exporterad!',
            'export_pdf_dialog_title': 'Exportera till PDF',
            'export_pdf_error': 'Misslyckades med att exportera PDF: {0}',
            'no_question': 'Ingen fråga',
            'no_response': 'Inget svar',
            'saved': 'Sparat',
            'close_button': 'Stäng',
            'open_local_tutorial': 'Öppna lokal handledning',
            'tutorial_open_failed': 'Misslyckades med att öppna handledning',
            'tutorial': 'Handledning',

            'model_display_name_perplexity': 'Perplexity',

            # UI - Configuration fields
            'token_label': 'API-nyckel:',
            'api_key_label': 'API-nyckel:',
            'model_label': 'Modell:',
            'language_label': 'Språk:',
            'language_label_old': 'Språk',
            'base_url_label': 'Bas-URL:',
            'base_url_placeholder': 'Standard: {default_api_base_url}',
            'shortcut': 'Genvägstangent',
            'shortcut_open_dialog': 'Öppna dialogruta',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Modell',
            'action': 'Åtgärd',
            'reset_button': 'Återställ till standard',
            'reset_current_ai': 'Återställ aktuell AI till standard',
            'reset_ai_confirm_title': 'Bekräfta återställning',
            'reset_ai_confirm_message': 'Återställer {ai_name} till standardtillstånd.\n\nDetta kommer att rensa:\n• API-nyckel\n• Anpassat modellnamn\n• Andra konfigurerade parametrar\n\nFortsätt?',
            'reset_tooltip': 'Återställ aktuell AI till standardvärden',
            'unsaved_changes_title': 'Osparade ändringar',
            'unsaved_changes_message': 'Du har osparade ändringar. Vad vill du göra?',
            'save_and_close': 'Spara och stäng',
            'discard_changes': 'Kassera ändringar',
            'cancel': 'Avbryt',
            'yes_button': 'Ja',
            'no_button': 'Nej',
            'cancel_button': 'Avbryt',
            'invalid_default_ai_title': 'Ogiltig standard-AI',
            'invalid_default_ai_message': 'Standard-AI "{default_ai}" är inte korrekt konfigurerad.\n\nVill du byta till "{first_ai}" istället?',
            'switch_to_ai': 'Byt till {ai}',
            'keep_current': 'Behåll nuvarande',
            'prompt_template': 'Promptmall',
            'ask_prompts': 'Frågeprompter',
            'random_questions_prompts': 'Prompter för slumpmässiga frågor',
            'display': 'Visa',
            'export_settings': 'Exportinställningar',
            'enable_default_export_folder': 'Exportera till standardmapp',
            'no_folder_selected': 'Ingen mapp vald',
            'browse': 'Bläddra...',
            'select_export_folder': 'Välj exportmapp',

            # Button text and menu items
            'copy_response_btn': 'Kopiera svar',
            'copy_qa_btn': 'Kopiera F&S',
            'export_current_btn': 'Exportera F&S som PDF',
            'export_history_btn': 'Exportera historik som PDF',
            'copy_mode_response': 'Svar',
            'copy_mode_qa': 'F&S',
            'copy_format_plain': 'Ren text',
            'copy_format_markdown': 'Markdown',
            'export_mode_current': 'Aktuell F&S',
            'export_mode_history': 'Historik',

            # PDF Export related
            'model_provider': 'Leverantör',
            'model_name': 'Modell',
            'model_api_url': 'API bas-URL',
            'pdf_model_info': 'AI-modellinformation',
            'pdf_software': 'Programvara',

            # UI - Dialog elements
            'input_placeholder': 'Skriv din fråga...',
            'response_placeholder': 'Svar kommer snart...',  # Used for all models

            # UI - Menu items
            'menu_title': 'Fråga AI',
            'menu_ask': 'Fråga',

            # UI - Status information
            'loading': 'Laddar',
            'loading_text': 'Frågar',
            'loading_models_text': 'Laddar modeller',
            'save_success': 'Inställningar sparade',
            'sending': 'Skickar...',
            'requesting': 'Begär',
            'formatting': 'Begäran lyckades, formaterar',

            # UI - Model list feature
            'load_models': 'Ladda modeller',
            'load_models_list': 'Ladda modelllista',
            'test_current_model': 'Testa aktuell modell',
            'use_custom_model': 'Använd anpassat modellnamn',
            'custom_model_placeholder': 'Ange anpassat modellnamn',
            'model_placeholder': 'Ladda modeller först',
            'models_loaded': 'Lyckades ladda {count} modeller',
            'models_loaded_with_selection': 'Lyckades ladda {count} modeller.\nVald modell: {model}',
            'load_models_failed': 'Misslyckades med att ladda modeller: {error}',
            'model_list_not_supported': 'Denna leverantör stöder inte automatisk hämtning av modelllista',
            'api_key_required': 'Ange API-nyckel först',
            'invalid_params': 'Ogiltiga parametrar',
            'warning': 'Varning',
            'success': 'Framgång',
            'error': 'Fel',
            'error_opening_dialog': 'Fel vid öppning av dialog:',
            'skipped_books_warning': '{count} bok/böcker hoppades över på grund av filåtkomstfel.\nDetta kan orsakas av ogiltiga tecken i filsökvägar eller filer som är låsta av ett annat program.',
            'failed_to_read_all_books': 'Kunde inte läsa metadata för alla valda böcker.\nDetta kan orsakas av ogiltiga tecken i filsökvägar eller filer som är låsta av ett annat program.',
            'error_starting_request': 'Fel vid start av begäran',
            'default_ai_mismatch_title': 'Standard-AI ändrad',
            'default_ai_mismatch_message': 'Standard-AI i konfigurationen har ändrats till "{default_ai}",\nmen den aktuella konversationen använder "{current_ai}".\n\nVill du byta till den nya standard-AI?',

            # Metadata fields
            'metadata_title': 'Titel',
            'metadata_authors': 'Författare',
            'metadata_publisher': 'Förlag',
            'metadata_pubdate': 'Publiceringsdatum',
            'metadata_pubyear': 'Publiceringsår',
            'metadata_language': 'Språk',
            'metadata_series': 'Serie',
            'no_metadata': 'Inga metadata',
            'no_series': 'Ingen serie',
            'unknown': 'Okänd',

            # Multi-book feature
            'books_unit': ' böcker',
            'new_conversation': 'Ny konversation',
            'single_book': 'Enkel bok',
            'multi_book': 'Flerbok',
            'deleted': 'Borttagen',
            'history': 'Historik',
            'no_history': 'Inga historikposter',
            'empty_question_placeholder': '(Ingen fråga)',
            'history_ai_unavailable': 'Denna AI har tagits bort från konfigurationen',
            'clear_current_book_history': 'Rensa aktuell bokhistorik',
            'confirm_clear_book_history': 'Är du säker på att du vill rensa all historik för:\n{book_titles}?',
            'confirm': 'Bekräfta',
            'history_cleared': '{deleted_count} historikposter rensade.',
            'multi_book_template_label': 'Flerboks-promptmall:',
            'multi_book_placeholder_hint': 'Använd {books_metadata} för bokinformation, {query} för användarens fråga',

            # Error messages (Note: 'error' is already defined above, these are other error types)
            'network_error': 'Nätverksfel',
            'request_timeout': 'Begäran tidsinställd',
            'request_failed': 'Begäran misslyckades',
            'request_stopped': 'Begäran stoppad',
            'question_too_long': 'Frågan är för lång',
            'question_too_long_detail': (
                'Prompten är för lång ({current} tecken, gräns {limit}, överskrider med {over}). '
                'Du har valt {book_count} bok/böcker.'
            ),
            'question_too_long_detail_library': (
                'Prompten är för lång ({current} tecken, gräns {limit}, överskrider med {over}). '
                'Ditt biblioteksindex innehåller {book_count} bok/böcker.'
            ),
            'question_too_long_hint_ai_search': (
                'För biblioteksomfattande sökningar, använd AI Search (fråga utan att välja böcker '
                'eller använd AI Search-menyn) i stället för att välja många böcker.'
            ),
            'question_too_long_hint_library_search': (
                'Ditt biblioteksindex överskrider den aktuella promptgränsen. Aktivera anpassad promptlängdsgräns '
                'under Plugin-konfiguration → General (föreslaget: 524288 tecken), '
                'eller ställ en mer specifik fråga.'
            ),
            'question_too_long_reduce_books': (
                'För att jämföra ett mindre urval på djupet, prova att avmarkera cirka {count} bok/böcker.'
            ),
            'question_too_long_hint_default': (
                'Aktuell standardgräns: {limit} tecken ({mode}). '
                'Standard för en bok är 128 000; för flera böcker 256 000. '
                'Avancerade användare kan aktivera en anpassad gräns under Plugin-konfiguration → General.'
            ),
            'question_too_long_hint_custom': (
                'Du har aktiverat en anpassad promptgräns. Om förfrågningar får timeout, sänk gränsen '
                'under Plugin-konfiguration → General, eller minska valda böcker / använd en mer specifik fråga.'
            ),
            'large_selection_dialog_title': 'Många böcker valda',
            'large_selection_dialog_message': (
                'Du har valt {count} böcker. För biblioteksomfattande frågor fungerar AI Search bättre '
                'och söker i hela biblioteket med kompakt metadata.\n\n'
                'Byta till AI Search, eller fortsätta med valda böcker i kompakt format?'
            ),
            'large_selection_use_ai_search': 'Använd AI Search',
            'large_selection_continue': 'Fortsätt med valda',
            'multi_book_truncation_note': (
                'Obs: Endast de första {included} av {total} valda böcker ingår på grund av promptgränsen. '
                'Använd AI Search för att söka i hela biblioteket, eller höj den anpassade gränsen '
                'under Plugin-konfiguration → General.'
            ),
            'library_metadata_truncation_note': (
                'Obs: Endast de första {included} av {total} indexerade böcker ingår på grund av promptgränsen. '
                'Resultat kan vara ofullständiga för mycket stora bibliotek om du inte höjer den anpassade gränsen '
                'under Plugin-konfiguration → General.'
            ),
            'auth_token_required_title': 'AI-tjänst krävs',
            'auth_token_required_message': 'Vänligen konfigurera en giltig AI-tjänst i plugin-konfigurationen.',
            'open_configuration': 'Öppna konfiguration',
            'error_preparing_request': 'Förberedelse av begäran misslyckades',
            'empty_suggestion': 'Tomt förslag',
            'process_suggestion_error': 'Fel vid behandling av förslag',
            'unknown_error': 'Okänt fel',
            'unknown_model': 'Okänd modell: {model_name}',
            'suggestion_error': 'Förslagsfel',
            'random_question_success': 'Slumpmässig fråga genererades framgångsrikt!',
            'book_title_check': 'Boktitel krävs',
            'avoid_repeat_question': 'Använd en annan fråga',
            'empty_answer': 'Tomt svar',
            'invalid_json': 'Ogiltig JSON',
            'invalid_response': 'Ogiltigt svar',
            'auth_error_401': 'Obehörig',
            'auth_error_403': 'Åtkomst nekad',
            'rate_limit': 'För många förfrågningar',
            'empty_response': 'Fick tomt svar från API',
            'empty_response_after_filter': 'Svaret är tomt efter att ha filtrerat tanketiketter',
            'no_response': 'Inget svar',
            'template_error': 'Mallfel',
            'no_model_configured': 'Ingen AI-modell konfigurerad. Vänligen konfigurera en AI-modell i inställningarna.',
            'no_ai_configured_title': 'Ingen AI konfigurerad',
            'no_ai_configured_message': 'Välkommen! För att börja ställa frågor om dina böcker, måste du först konfigurera en AI-leverantör.\n\nGoda nyheter: Detta plugin har nu en GRATIS nivå (Nvidia AI Free) som du kan använda omedelbart utan någon konfiguration!\n\nAndra rekommenderade alternativ:\n• Nvidia AI - Få 6 månaders GRATIS API-åtkomst bara med ditt telefonnummer (inget kreditkort krävs)\n• Ollama - Kör AI-modeller lokalt på din dator (helt gratis och privat)\n\nVill du öppna plugin-konfigurationen för att ställa in en AI-leverantör nu?',
            'open_settings': 'Plugin-konfiguration',
            'ask_anyway': 'Fråga ändå',
            'later': 'Senare',
            'reset_all_data': 'Återställ alla data',
            'reset_all_data_warning': 'Detta kommer att radera alla API-nycklar, promptmallar och lokala historikposter. Din språkpreferens kommer att bevaras. Fortsätt med försiktighet.',
            'reset_all_data_confirm_title': 'Bekräfta återställning',
            'reset_all_data_confirm_message': 'Är du säker på att du vill återställa pluginet till dess ursprungliga tillstånd?\n\nDetta kommer permanent att radera:\n• Alla API-nycklar\n• Alla anpassade promptmallar\n• All konversationshistorik\n• Alla plugin-inställningar (språkpreferens kommer att bevaras)\n\nDenna åtgärd kan inte ångras!',
            'reset_all_data_success': 'Alla plugin-data har återställts framgångsrikt. Vänligen starta om calibre för att ändringarna ska träda i kraft.',
            'reset_all_data_failed': 'Misslyckades med att återställa plugin-data: {error}',
            'random_question_error': 'Fel vid generering av slumpmässig fråga',
            'clear_history_failed': 'Misslyckades med att rensa historik',
            'clear_history_not_supported': 'Att rensa historik för en enskild bok stöds ännu inte',
            'missing_required_config': 'Saknar obligatorisk konfiguration: {key}. Vänligen kontrollera dina inställningar.',
            'api_key_too_short': 'API-nyckeln är för kort. Vänligen kontrollera och ange hela nyckeln.',

            # API response handling
            'api_request_failed': 'API-begäran misslyckades: {error}',
            'api_content_extraction_failed': 'Kunde inte extrahera innehåll från API-svar',
            'api_invalid_response': 'Kunde inte få giltigt API-svar',
            'api_unknown_error': 'Okänt fel: {error}',

            # Stream response handling
            'stream_response_code': 'Stream-svar statuskod: {code}',
            'stream_continue_prompt': 'Vänligen fortsätt ditt tidigare svar utan att upprepa innehåll som redan har tillhandahållits.',
            'stream_continue_code_blocks': 'Ditt tidigare svar hade oavslutade kodblock. Vänligen fortsätt och slutför dessa kodblock.',
            'stream_continue_parentheses': 'Ditt tidigare svar hade oavslutade parenteser. Vänligen fortsätt och se till att alla parenteser är korrekt stängda.',
            'stream_continue_interrupted': 'Ditt tidigare svar verkar ha blivit avbrutet. Vänligen fortsätt att slutföra din sista tanke eller förklaring.',
            'stream_timeout_error': 'Stream-överföringen har inte mottagit nytt innehåll på 60 sekunder, troligen ett anslutningsproblem.',

            # API error messages
            'api_version_model_error': 'API-versions- eller modellnamnsfel: {message}\n\nVänligen uppdatera API:s bas-URL till "{base_url}" och modell till "{model}" eller annan tillgänglig modell i inställningarna.',
            'api_format_error': 'API-begärans formatfel: {message}',
            'api_key_invalid': 'API-nyckel ogiltig eller obehörig: {message}\n\nVänligen kontrollera din API-nyckel och se till att API-åtkomst är aktiverad.',
            'api_rate_limit': 'Begärans frekvensgräns överskriden, försök igen senare\n\nDu kan ha överskridit den fria användningskvoten. Detta kan bero på:\n1. För många förfrågningar per minut\n2. För många förfrågningar per dag\n3. För många inmatningstokens per minut',

            # Configuration errors
            'missing_config_key': 'Saknar obligatorisk konfigurationsnyckel: {key}',
            'api_base_url_required': 'API bas-URL krävs',
            'model_name_required': 'Modellnamn krävs',

            # Model list fetching
            'fetching_models_from': 'Hämtar modeller från {url}',
            'successfully_fetched_models': 'Lyckades hämta {count} {provider} modeller',
            'failed_to_fetch_models': 'Misslyckades med att ladda modeller: {error}',
            'api_key_empty': 'API-nyckeln är tom. Vänligen ange en giltig API-nyckel.',

            # Error messages for model fetching
            'error_401': 'API-nyckelautentisering misslyckades. Kontrollera: API-nyckeln är korrekt, kontot har tillräckligt saldo, API-nyckeln har inte gått ut.',
            'error_403': 'Åtkomst nekad. Kontrollera: API-nyckeln har tillräckliga behörigheter, inga regionala åtkomstbegränsningar.',
            'error_404': 'API-slutpunkt hittades inte. Kontrollera om API bas-URL-konfigurationen är korrekt.',
            'error_429': 'För många förfrågningar, frekvensgräns nådd. Vänligen försök igen senare.',
            'error_5xx': 'Serverfel. Vänligen försök igen senare eller kontrollera tjänsteleverantörens status.',
            'error_network': 'Nätverksanslutningen misslyckades. Vänligen kontrollera nätverksanslutning, proxyinställningar eller brandväggskonfiguration.',
            'error_unknown': 'Okänt fel.',
            'technical_details': 'Tekniska detaljer',
            'ollama_service_not_running': 'Ollama-tjänsten körs inte. Vänligen starta Ollama-tjänsten först.',
            'ollama_service_timeout': 'Ollama-tjänstanslutning tidsinställd. Vänligen kontrollera om tjänsten körs korrekt.',
            'ollama_model_not_available': 'Modell "{model}" är inte tillgänglig. Vänligen kontrollera:\n1. Är modellen startad? Kör: ollama run {model}\n2. Är modellnamnet korrekt?\n3. Är modellen nedladdad? Kör: ollama pull {model}',
            'gemini_geo_restriction': 'Gemini API är inte tillgängligt i din region. Vänligen försök:\n1. Använd en VPN för att ansluta från en region som stöds\n2. Använd andra AI-leverantörer (OpenAI, Anthropic, DeepSeek, etc.)\n3. Kontrollera Google AI Studio för regionstillgänglighet',
            'model_test_success': 'Modelltest lyckades!',
            'test_model_prompt': 'Modeller laddades framgångsrikt! Vill du testa den valda modellen "{model}"?',
            'test_model_button': 'Testa modell',
            'skip': 'Hoppa över',

            # About information
            'author_name': 'Sheldon',
            'user_manual': 'Användarmanual',
            'about_plugin': 'Om Fråga AI-plugin',
            'learn_how_to_use': 'Hur man använder',
            'email': 'iMessage',

            # Model specific configurations
            'model_display_name_grok': 'Grok(SpaceXAI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Anpassad',
            'model_enable_streaming': 'Aktivera strömning',

            # AI Switcher
            'current_ai': 'Aktuell AI',
            'no_configured_models': 'Ingen AI konfigurerad - Vänligen konfigurera i inställningarna',

            # Provider specific info
            'nvidia_free_info': '💡 Nya användare får 6 månaders gratis API-åtkomst - Inget kreditkort krävs',

            # Common system messages
            'default_system_message': 'Du är en expert på bokanalys. Din uppgift är att hjälpa användare att bättre förstå böcker genom att ge insiktsfulla frågor och analyser.',

            # Request timeout settings
            'request_timeout_label': 'Begäran tidsinställning:',
            'seconds': 'sekunder',
            'request_timeout_error': 'Begäran tidsinställd. Aktuell tidsinställning: {timeout} sekunder',
            'enable_custom_prompt_limit_label': 'Anpassad promptlängdsgräns',
            'enable_custom_prompt_limit_tooltip': (
                'Standardgränser är 128 000 tecken (en bok) och 256 000 (flera böcker). '
                'De flesta användare behöver inte ändra detta. För biblioteksomfattande sökningar, använd AI Search. '
                'Aktivera bara en anpassad gräns om din modell stöder mycket större kontext och '
                'förfrågningar fortfarande når gränsen.'
            ),
            'max_prompt_length_label': 'Max. promptlängd:',
            'max_prompt_length_unit': 'tecken',
            'max_prompt_length_tooltip': (
                'Gäller när anpassad gräns är aktiverad. Standardförslag: 524288 tecken. '
                'Ungefärlig regel: 1 token ≈ 3–4 tecken. För Ollama, ställ även in num_ctx på modellsidan.'
            ),
            'max_prompt_length_normalized_title': 'Promptgräns justerad',
            'max_prompt_length_normalized': (
                'Promptlängden normaliserades till {value} tecken (avgränsare som kommatecken '
                'eller mellanslag togs bort).'
            ),

            # Parallel AI settings
            'parallel_ai_count_label': 'Antal parallella AI:',
            'parallel_ai_count_tooltip': 'Antal AI-modeller att fråga samtidigt (1-2 tillgängliga, 3-4 kommer snart)',
            'parallel_ai_notice': 'Obs: Detta påverkar endast sändning av frågor. Slumpmässiga frågor använder alltid en enda AI.',
            'suggest_maximize': 'Tips: Maximera fönstret för bättre visning med 3 AI',
            'ai_panel_label': 'AI {index}:',
            'no_ai_available': 'Ingen AI tillgänglig för denna panel',
            'add_more_ai_providers': 'Lägg till fler AI-leverantörer i inställningarna',
            'select_ai': '-- Välj AI --',
            'select_model': '-- Välj modell --',
            'request_model_list': 'Vänligen begär modellista',
            'coming_soon': 'Kommer snart',
            'advanced_feature_tooltip': 'Denna funktion är under utveckling. Håll utkik efter uppdateringar!',

            # AI Manager Dialog
            'ai_manager_title': 'Hantera AI-leverantörer',
            'add_ai_title': 'Lägg till AI-leverantör',
            'manage_ai_title': 'Hantera konfigurerad AI',
            'configured_ai_list': 'Konfigurerad AI',
            'available_ai_list': 'Tillgängliga att lägga till',
            'ai_config_panel': 'Konfiguration',
            'select_ai_to_configure': 'Välj en AI från listan att konfigurera',
            'select_provider': 'Välj AI-leverantör',
            'select_provider_hint': 'Välj en leverantör från listan',
            'select_ai_to_edit': 'Välj en AI från listan att redigera',
            'set_as_default': 'Ange som standard',
            'save_ai_config': 'Spara',
            'remove_ai_config': 'Ta bort',
            'delete_ai': 'Radera',
            'add_ai_button': 'Lägg till AI',
            'edit_ai_button': 'Redigera AI',
            'manage_configured_ai_button': 'Hantera konfigurerad AI',
            'manage_ai_button': 'Hantera AI',
            'no_configured_ai': 'Ingen AI konfigurerad ännu',
            'no_configured_ai_hint': 'Ingen AI konfigurerad. Pluginet kan inte fungera. Vänligen klicka på "Lägg till AI" för att lägga till en AI-leverantör.',
            'default_ai_label': 'Standard-AI:',
            'default_ai_tag': 'Standard',
            'ai_not_configured_cannot_set_default': 'Denna AI är inte konfigurerad ännu. Vänligen spara konfigurationen först.',
            'ai_set_as_default_success': '{name} har angetts som standard-AI.',
            'ai_config_saved_success': '{name}-konfigurationen sparades framgångsrikt.',
            'confirm_remove_title': 'Bekräfta borttagning',
            'confirm_remove_ai': 'Är du säker på att du vill ta bort {name}? Detta kommer att rensa API-nyckeln och återställa konfigurationen.',
            'confirm_delete_title': 'Bekräfta radering',
            'confirm_delete_ai': 'Är du säker på att du vill radera {name}?',
            'api_key_required': 'API-nyckel krävs.',
            'configuration': 'Konfiguration',

            # Field descriptions
            'api_key_desc': 'Din API-nyckel för autentisering. Håll den säker och dela den inte.',
            'base_url_desc': 'API-slutpunktens URL. Använd standard om du inte har en anpassad slutpunkt.',
            'model_desc': 'Välj en modell från listan eller använd ett anpassat modellnamn.',
            'streaming_desc': 'Aktivera realtidsströmning av svar för snabbare feedback.',
            'advanced_section': 'Avancerat',

            # Provider-specific notices
            'perplexity_model_notice': 'Obs: Perplexity tillhandahåller inte en publik modelllista API, så modeller är hårdkodade.',
            'ollama_no_api_key_notice': 'Obs: Ollama är en lokal modell som inte kräver en API-nyckel.',
            'nvidia_free_credits_notice': 'Obs: Nya användare får gratis API-krediter - Inget kreditkort krävs.',

            # Nvidia Free error messages
            'free_tier_rate_limit': 'Frekvensgräns för gratisnivå överskriden. Vänligen försök igen senare eller konfigurera din egen Nvidia API-nyckel.',
            'free_tier_unavailable': 'Gratisnivån är tillfälligt otillgänglig. Vänligen försök igen senare eller konfigurera din egen Nvidia API-nyckel.',
            'free_tier_server_error': 'Serverfel för gratisnivå. Vänligen försök igen senare.',
            'free_tier_error': 'Fel på gratisnivå',

            # Nvidia Free provider info
            'free': 'Gratis',
            'nvidia_free_provider_name': 'Nvidia AI (Gratis)',
            'nvidia_free_display_name': 'Nvidia AI (Gratis)',
            'nvidia_free_api_key_info': 'Kommer att hämtas från servern',
            'nvidia_free_desc': 'Denna tjänst underhålls av utvecklaren och är gratis, men kan vara mindre stabil. För en stabilare tjänst, vänligen konfigurera din egen Nvidia API-nyckel.',

            # Nvidia Free first use reminder
            'nvidia_free_first_use_title': 'Välkommen till Fråga AI-plugin',
            'nvidia_free_first_use_message': 'Nu kan du bara fråga utan någon konfiguration! Utvecklaren upprätthåller en gratis nivå för dig, men den kanske inte är särskilt stabil. Njut!\n\nDu kan konfigurera dina egna AI-leverantörer i inställningarna för bättre stabilitet.',

            # Model buttons
            'refresh_model_list': 'Uppdatera',
            'test_current_model': 'Testa',
            'testing_text': 'Testar',
            'refresh_success': 'Modellistan uppdaterades framgångsrikt.',
            'refresh_failed': 'Misslyckades med att uppdatera modellistan.',
            'test_failed': 'Modelltest misslyckades.',

            # Tooltip
            'manage_ai_disabled_tooltip': 'Vänligen lägg till en AI-leverantör först.',

            # PDF export section titles
            'pdf_book_metadata': 'BOKMETADATA',
            'pdf_question': 'FRÅGA',
            'pdf_answer': 'SVAR',
            'pdf_ai_model_info': 'AI-MODELLINFORMATION',
            'pdf_generated_by': 'GENERERAD AV',
            'pdf_provider': 'Leverantör',
            'pdf_model': 'Modell',
            'pdf_api_base_url': 'API bas-URL',
            'pdf_panel': 'Panel',
            'pdf_plugin': 'Plugin',
            'pdf_github': 'GitHub',
            'pdf_software': 'Programvara',
            'pdf_generated_time': 'Genererad tid',
            'pdf_info_not_available': 'Information inte tillgänglig',

            #AI Search v1.4.2
            'library_tab': 'Sök',
            'library_search': 'AI-sökning',
            'library_info': 'AI-sökning är alltid aktiverad. När du inte väljer några böcker kan du söka i hela ditt bibliotek med naturligt språk.',
            'library_enable': 'Aktivera AI-sökning',
            'library_enable_tooltip': 'När aktiverad kan du söka i ditt bibliotek med AI när inga böcker är markerade',
            'library_update': 'Uppdatera biblioteksdata',
            'library_update_tooltip': 'Extrahera boktitlar och författare från ditt bibliotek',
            'library_updating': 'Uppdaterar...',
            'library_status': 'Status: {count} böcker, senaste uppdatering: {time}',
            'library_status_empty': 'Status: Ingen data. Klicka på "Uppdatera biblioteksdata" för att starta.',
            'library_status_error': 'Status: Fel vid inläsning av data',
            'library_update_success': 'Uppdaterade {count} böcker',
            'library_update_failed': 'Misslyckades med att uppdatera biblioteksdata',
            'library_no_gui': 'GUI inte tillgängligt',
            'library_init_title': 'Initialisera AI-sökning',
            'library_init_message': 'AI-sökning kräver metadata från biblioteket för att fungera. Vill du initialisera det nu?\n\nDetta kommer att extrahera boktitlar och författare från ditt bibliotek.',
            'library_init_required': 'AI-sökning kan inte aktiveras utan biblioteksdata. Klicka på "Uppdatera biblioteksdata" när du är redo.',
            'ai_search_welcome_title': 'Välkommen till AI-sökning',
            'ai_search_welcome_message': 'AI-sökning är aktiverad!\n\nSå här aktiverar du:\n• Kortkommando (anpassningsbart i inställningar)\n• Verktygsmenyn → AI-sökning\n• Öppna Ask-dialogen utan att välja böcker\n\nDu kan söka i hela ditt bibliotek med naturligt språk. Till exempel:\n• "Har du några böcker om Python?"\n• "Visa mig böcker av Isaac Asimov"\n• "Hitta böcker om maskininlärning"\n\nAI:n söker i ditt bibliotek och rekommenderar relevanta böcker. Klicka på boktitlar för att öppna dem direkt.',
            'ai_search_not_enough_books_title': 'Inte tillräckligt med böcker',
            'ai_search_not_enough_books_message': 'AI-sökning kräver minst {min_books} böcker i ditt bibliotek.\n\nDitt nuvarande bibliotek har bara {book_count} bok/böcker.\n\nLägg till fler böcker för att använda AI-sökning.',
            'ai_search_mode_info': 'Söker i hela biblioteket',
            'ai_search_feature_title': 'AI Search',
            'ai_search_feature_subtitle': 'Sök i hela biblioteket med naturligt språk',
            'ai_search_feature_description': (
                'AI Search hjälper dig hitta böcker i hela ditt Calibre-bibliotek.\n\n'
                '• Utlös: öppna Ask utan att välja böcker, använd Verktyg → AI Search eller genväg\n'
                '• Så fungerar det: pluginet skickar kompakt metadata (bok-ID, titel, författare) '
                'för alla indexerade böcker\n'
                '• Stora val: om du väljer fler än 50 böcker föreslår Ask AI Search i stället för '
                'att bädda in varje bok i detaljerat format\n'
                '• Håll data uppdaterad: klicka "Uppdatera biblioteksdata" efter att ha lagt till eller tagit bort böcker\n\n'
                'Exempel: "Hitta böcker om Python", "Visa böcker av Isaac Asimov".'
            ),
            'ai_search_usage_hint': (
                'Tips: AI Search fungerar bäst för biblioteksomfattande upptäckt. För djupgående '
                'jämförelse av få böcker, välj upp till 30 böcker.'
            ),
            'ai_search_data_title': 'Biblioteksindex',
            'ai_search_data_subtitle': 'Uppdatera den kompakta boklistan som skickas till AI när du lägger till eller tar bort böcker',
            'library_prompt_template': 'Du har tillgång till användarens bokbibliotek. Här är alla böcker: {metadata} Användarfråga: {query} Vänligen hitta matchande böcker i det aktuella biblioteket och returnera dem i detta format (**VIKTIGT**: Använd HTML-länkformat så att användare kan klicka på boktitlar för att öppna dem direkt): - <a href="calibre://book/BOOK_ID">Boktitel</a> - Författarnamn Exempel: - <a href="calibre://book/123">Lär dig Python</a> - Mark Lutz - <a href="calibre://book/456">Machine Learning i praktiken</a> - Peter Harrington Obs: Vissa författare kan listas som "unknown". Detta är normala data, vänligen returnera alla matchande resultat normalt. Returnera endast böcker som matchar frågan. Maximalt 5 resultat.',
            'ai_search_privacy_title': 'Integritetsmeddelande',
            'ai_search_privacy_alert': 'AI-sökning använder bokmetadata (titlar och författare). Denna information skickas till den AI-leverantör du har konfigurerat för att behandla dina sökningar.',
            'ai_search_updated_info': 'Uppdaterade {count} böcker {time_ago}',
            'ai_search_books_info': '{count} böcker indexerade',
            'days_ago': 'för {n} dagar sedan',
            'hours_ago': 'för {n} timmar sedan',
            'minutes_ago': 'för {n} minuter sedan',
            'just_now': 'just nu',
            
            # Statistics tab (v1.4.2)
            'stat_tab': 'Statistik',
            'stat_overview': 'Översikt',
            'stat_overview_subtitle': 'Statistik över AI-förfrågningar',
            'stat_days_unit': 'dagar',
            'stat_days_label': 'Startad',
            'stat_start_at': 'Start {date}',
            'stat_replies_unit': 'gånger',
            'stat_replies_label': 'Fråga AI',
            'stat_books_unit': 'böcker',
            'stat_books_label': 'Bibliotek',
            'stat_no_books': 'Uppdatera i Sök-fliken',
            'stat_trends': 'Trender',
            'stat_curious_index': 'AI-förfrågningar fördelning denna vecka',
            'stat_daily_avg': 'Dagligt genomsnitt {n} gånger',
            'stat_sample_data': 'Exempeldata visas. Växlar till riktig data efter 20+ förfrågningar',
            'stat_heatmap': 'Värmekarta',
            'stat_heatmap_subtitle': 'AI-förfrågningar fördelning denna månad',
            'stat_no_data_week': 'Ingen data denna vecka',
            'stat_no_data_month': 'Ingen data denna månad',
            'stat_data_not_enough': 'Inte tillräckligt med data',
            
            # Statistik användartitlar (baserat på antal förfrågningar)
            'stat_title_curious': 'Bläddrar',
            'stat_title_explorer': 'Bokjägare',
            'stat_title_seeker': 'Ivrig läsare',
            'stat_title_enthusiast': 'Bibliofil',
            'stat_title_pursuer': 'Bokmal',
            
            # Statistik biblioteksomdömen (baserat på samlingsstorlek, historiska referenser)
            'stat_books_impressive': 'Privat läsrum',
            'stat_books_collection': 'Lärdas arbetsrum',
            'stat_books_variety': 'Uppsala universitetsbibliotek',
            'stat_books_awesome': 'Kungliga biblioteket',
            'stat_books_unbelievable': 'Biblioteket i Alexandria',
            
            # Links (v1.4.2)
            'online_tutorial': 'Online handledning',
        }