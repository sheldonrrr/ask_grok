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
        return 'Om boken "{title}": Författare: {author}, Förlag: {publisher}, Utgivningsår: {pubyear}, bok i language: {language}, Serie: {series}, Min fråga är: {query}'
    
    @property
    def suggestion_template(self) -> str:
        return """Du är en expert på bokrecensioner. För boken "{title}" av {author}, publicerings språk är {language}, generera EN insiktsfull fråga som hjälper läsarna att förstå boken bättre. Regler: 1. Returnera ENDAST frågan, utan introduktion eller förklaring 2. Fokusera på bokens innehåll, inte bara titeln 3. Gör frågan praktisk och tankeväckande 4. Håll den kort (30-200 ord) 5. Var kreativ och generera en annan fråga varje gång, även för samma bok"""
    
    @property
    def multi_book_default_template(self) -> str:
        return """Här är information om flera böcker: {books_metadata} Användarfråga: {query} Vänligen svara på frågan baserat på ovanstående bokinformation."""
    
    @property
    def translations(self) -> dict:
        return {
            # Plugin information
            'plugin_name': 'Ask AI Plugin',
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
            'stop_button': 'Stoppa',
            'suggest_button': 'Slumpmässig fråga',
            'copy_response': 'Kopiera svar',
            'copy_question_response': 'Kopiera F&&S',
            'export_pdf': 'Exportera PDF',
            'export_current_qa': 'Exportera Nuvarande F&S',
            'export_history': 'Exportera Historik',
            
            # Exportinställningar
            'export_settings': 'Exportinställningar',
            'enable_default_export_folder': 'Exportera till standardmapp',
            'no_folder_selected': 'Ingen mapp vald',
            'browse': 'Bläddra...',
            'select_export_folder': 'Välj Exportmapp',
            
            # Knapptext och menyalternativ
            'copy_response_btn': 'Kopiera Svar',
            'copy_qa_btn': 'Kopiera F&S',
            'export_current_btn': 'Exportera F&S som PDF',
            'export_history_btn': 'Exportera Historik som PDF',
            'copy_mode_response': 'Svar',
            'copy_mode_qa': 'F&S',
            'export_mode_current': 'Aktuell F&S',
            'export_mode_history': 'Historik',
            
            # PDF-export relaterat
            'model_provider': 'Leverantör',
            'model_name': 'Modell',
            'model_api_url': 'API Bas-URL',
            'pdf_model_info': 'AI-Modellinformation',
            'pdf_software': 'Programvara',
            
            'export_all_history_dialog_title': 'Exportera Hela Historiken till PDF',
            'export_all_history_title': 'HELA F&S HISTORIK',
            'export_history_insufficient': 'Minst 2 historikposter krävs för att exportera.',
            'history_record': 'Post',
            'question_label': 'Fråga',
            'answer_label': 'Svar',
            'default_ai': 'Standard AI',
            'export_time': 'Exporterad',
            'total_records': 'Totalt Poster',
            'info': 'Information',
            'yes': 'Ja',
            'no': 'Nej',
            'no_book_selected_title': 'Ingen Bok Vald',
            'no_book_selected_message': 'Vänligen välj en bok innan du ställer frågor.',
            'set_default_ai_title': 'Ange Standard AI',
            'set_default_ai_message': 'Du har bytt till "{0}". Vill du ange den som standard AI för framtida frågor?',
            'set_default_ai_success': 'Standard AI har ställts in till "{0}".',
            'copied': 'Kopierad!',
            'pdf_exported': 'PDF exporterad!',
            'export_pdf_dialog_title': 'Exportera till PDF',
            'export_pdf_error': 'Fel vid PDF-export: {0}',
            'no_question': 'Ingen fråga',
            'saved': 'Sparad',
            'close_button': 'Stäng',
            
            # UI - Konfigurationsfält
            'token_label': 'API-nyckel:',
            'api_key_label': 'API-nyckel:',
            'model_label': 'Modell:',
            'language_label': 'Språk:',
            'language_label_old': 'Språk',
            'base_url_label': 'Bas-URL:',
            'base_url_placeholder': 'Standard: {default_api_base_url}',
            'shortcut': 'Genväg',
            'shortcut_open_dialog': 'Öppna dialog',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Modell',
            'action': 'Åtgärd',
            'reset_button': 'Återställ',
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
            
            # UI - Modellistafunktion
            'load_models': 'Ladda modeller',
            'use_custom_model': 'Använd anpassat modellnamn',
            'custom_model_placeholder': 'Ange anpassat modellnamn',
            'model_placeholder': 'Ladda modeller först',
            'models_loaded': '{count} modeller laddade',
            'load_models_failed': 'Kunde inte ladda modeller: {error}',
            'model_list_not_supported': 'Denna leverantör stöder inte automatisk hämtning av modelllista',
            'api_key_required': 'Ange API-nyckel först',
            'invalid_params': 'Ogiltiga parametrar',
            'warning': 'Varning',
            'success': 'Framgång',
            'error': 'Fel',
            'network_error': 'Nätverksfel',
            'question_too_long': 'Fråga är för lång',
            'request_failed': 'Begäran misslyckades',
            'request_timeout': 'Begäran tidsut',
            
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

            # Multi-bok funksjon
            'books_unit': ' böcker',
            'new_conversation': 'Ny konversation',
            'single_book': 'Enkel bok',
            'multi_book': 'Multi-bok',
            'deleted': 'Raderad',
            'history': 'Historik',
            'no_history': 'Inga historikposter',
            'empty_question_placeholder': '(Ingen fråga)',
            'history_ai_unavailable': 'Denna AI har tagits bort från konfigurationen',
            'clear_current_book_history': 'Rensa Nuvarande Bokhistorik',
            'confirm_clear_book_history': 'Är du säker på att du vill rensa all historik för:\n{book_titles}?',
            'confirm': 'Bekräfta',
            'history_cleared': '{deleted_count} historikposter rensade.',
            'multi_book_template_label': 'Flerbok Prompt Mall:',
            'multi_book_placeholder_hint': 'Använd {books_metadata} för bokinformation, {query} för användarfråga',
            
            # Felmeddelanden
            'random_question_success': 'Slumpmässig fråga genererad!',
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
            'no_ai_configured_title': 'Ingen AI Konfigurerad',
            'no_ai_configured_message': 'Välkommen! För att börja ställa frågor om dina böcker måste du först konfigurera en AI-leverantör.\n\nRekommenderas för nybörjare:\n• Nvidia AI - Få 6 månaders GRATIS API-åtkomst med bara ditt telefonnummer (inget kreditkort krävs)\n• Ollama - Kör AI-modeller lokalt på din dator (helt gratis och privat)\n\nVill du öppna plugin-konfigurationen för att ställa in en AI-leverantör nu?',
            'open_settings': 'Plugin-konfiguration',
            'ask_anyway': 'Fråga Ändå',
            'later': 'Senare',
            'reset_all_data': 'Återställ Alla Data',
            'reset_all_data_warning': 'Detta tar bort alla API-nycklar, promptmallar och lokala historikposter. Din språkpreferens kommer att bevaras. Fortsätt med försiktighet.',
            'reset_all_data_confirm_title': 'Bekräfta Återställning',
            'reset_all_data_confirm_message': 'Är du säker på att du vill återställa pluginet till sitt ursprungliga tillstånd?\n\nDetta tar permanent bort:\n• Alla API-nycklar\n• Alla anpassade promptmallar\n• All konversationshistorik\n• Alla plugin-inställningar (språkpreferens kommer att bevaras)\n\nDenna åtgärd kan inte ångras!',
            'reset_all_data_success': 'Alla plugin-data har återställts framgångsrikt. Starta om calibre för att ändringarna ska träda i kraft.',
            'reset_all_data_failed': 'Misslyckades med att återställa plugin-data: {error}',
            'random_question_error': 'Fel vid generering av slumpmässig fråga',
            'clear_history_failed': 'Kunde inte rensa historik',
            'clear_history_not_supported': 'Rensa historik för en enskild bok stöds ännu inte',
            'missing_required_config': 'Nödvändig konfiguration saknas: {key}. Kontrollera dina inställningar.',
            'api_key_too_short': 'API-nyckeln är för kort. Kontrollera och ange den fullständiga nyckeln.',
            
            # API-svarshantering
            'api_request_failed': 'API-begäran misslyckades: {error}',
            'api_content_extraction_failed': 'Kunde inte extrahera innehåll från API-svar',
            'api_invalid_response': 'Fick inget giltigt svar från API',
            'api_unknown_error': 'Okänt fel: {error}',
            
            # Strömningssvarshantering
            'stream_response_code': 'Statuskod för strömningssvar: {code}',
            'stream_continue_prompt': 'Fortsätt med ditt tidigare svar utan att upprepa innehåll som redan tillhandahållits.',
            'stream_continue_code_blocks': 'Ditt tidigare svar hade oöppnade kodblock. Fortsätt och slutför dessa kodblock.',
            'stream_continue_parentheses': 'Ditt tidigare svar hade oöppnade parenteser. Fortsätt och se till att alla parenteser är korrekt stängda.',
            'stream_continue_interrupted': 'Ditt tidigare svar verkar ha avbrutits. Fortsätt och slutför din senaste tanke eller förklaring.',
            'stream_timeout_error': 'Strömningen har inte fått nytt innehåll på 60 sekunder, möjligen ett anslutningsproblem.',
            
            # API-felmeddelanden
            'api_version_model_error': 'API-versions- eller modellnamnsfel: {message}\n\nUppdatera API-bas-URL till "{base_url}" och modellen till "{model}" eller en annan tillgänglig modell i inställningarna.',
            'api_format_error': 'API-begäransformatfel: {message}',
            'api_key_invalid': 'Ogiltig eller obehörig API-nyckel: {message}\n\nKontrollera din API-nyckel och se till att API-åtkomst är aktiverad.',
            'api_rate_limit': 'Begäransgräns överskriden, försök igen senare\n\nDu kan ha överskridit din gratiskvot. Detta kan bero på:\n1. För många begäranden per minut\n2. För många begäranden per dag\n3. För många indatatokens per minut',
            
            # Konfigurationsfel
            'missing_config_key': 'Nödvändig konfigurationsnyckel saknas: {key}',
            'api_base_url_required': 'API-bas-URL krävs',
            'model_name_required': 'Modellnamn krävs',
            'api_key_empty': 'API-nyckeln är tom. Ange en giltig API-nyckel.',
            
            # Hämtning av modelllista
            'fetching_models_from': 'Hämtar modeller från {url}',
            'successfully_fetched_models': '{count} {provider}-modeller hämtade',
            'failed_to_fetch_models': 'Kunde inte hämta modeller: {error}',
            
            # Om information
            'author_name': 'Sheldon',
            'user_manual': 'Användarmanual',
            'about_plugin': 'Varför Ask AI Plugin?',
            'learn_how_to_use': 'Hur man använder',
            'email': 'iMessage',
            
            # Modellspecifika konfigurationer
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Anpassad',
            'model_enable_streaming': 'Aktivera streaming',
            
            # AI Switcher
            'current_ai': 'Aktuell AI',
            'no_configured_models': 'Ingen AI konfigurerad - Vänligen konfigurera i inställningarna',
            
            # Provider specifik info
            'nvidia_free_info': '💡 Nya användare får 6 månaders gratis API-åtkomst - Inget kreditkort krävs',
            
            # Allmänna systemmeddelanden
            'default_system_message': 'Du är en expert på bokanalys. Din uppgift är att hjälpa användare att förstå böcker bättre genom att tillhandahålla insiktsfulla frågor och analyser.',

            # Begäran timeout inställningar
            'request_timeout_label': 'Begäran timeout:',
            'seconds': 'sekunder',
            'request_timeout_error': 'Begäran timeout. Nuvarande timeout: {timeout} sekunder',
            
            # Parallella AI inställningar
            'parallel_ai_count_label': 'Antal parallella AI:er:',
            'parallel_ai_count_tooltip': 'Antal AI-modeller att fråga samtidigt (1-2 tillgängliga, 3-4 kommer snart)',
            'parallel_ai_notice': 'Obs: Detta påverkar endast sändning av frågor. Slumpmässiga frågor använder alltid en enda AI.',
            'suggest_maximize': 'Tips: Maximera fönstret för bättre visning med 3 AI:er',
            'ai_panel_label': 'AI {index}:',
            'no_ai_available': 'Ingen AI tillgänglig för denna panel',
            'add_more_ai_providers': 'Vänligen lägg till fler AI-leverantörer i inställningarna',
            'select_ai': '-- Välj AI --',
            'select_model': '-- Byt Modell --',
            'request_model_list': 'Vänligen begär modelllista',
            'coming_soon': 'Kommer snart',
            'advanced_feature_tooltip': 'Denna funktion är under utveckling. Håll utkik efter uppdateringar!',

            # PDF export sektionstitlar
            'pdf_book_metadata': 'BOK METADATA',
            'pdf_question': 'FRÅGA',
            'pdf_answer': 'SVAR',
            'pdf_ai_model_info': 'AI MODELL INFORMATION',
            'pdf_generated_by': 'GENERERAD AV',
            'pdf_provider': 'Leverantör',
            'pdf_model': 'Modell',
            'pdf_api_base_url': 'API Bas-URL',
            'pdf_panel': 'Panel',
            'pdf_plugin': 'Plugin',
            'pdf_github': 'GitHub',
            'pdf_software': 'Programvara',
            'pdf_generated_time': 'Genererad Tid',
            'default_ai_mismatch_title': 'Standard AI Ändrad',
            'default_ai_mismatch_message': 'Standard AI i konfigurationen har ändrats till "{default_ai}",\nmen den aktuella dialogen använder "{current_ai}".\n\nVill du byta till den nya standard AI?',
            'discard_changes': 'Kassera Ändringar',
            'empty_response': 'Mottog tomt svar från API',
            'empty_response_after_filter': 'Svaret är tomt efter filtrering av think-taggar',
            'error_401': 'API-nyckelautentisering misslyckades. Kontrollera: API-nyckeln är korrekt, kontot har tillräckligt saldo, API-nyckeln har inte löpt ut.',
            'error_403': 'Åtkomst nekad. Kontrollera: API-nyckeln har tillräckliga behörigheter, inga regionala åtkomstbegränsningar.',
            'error_404': 'API-slutpunkt hittades inte. Kontrollera om API Base URL-konfigurationen är korrekt.',
            'error_429': 'För många förfrågningar, hastighetsgräns nådd. Försök igen senare.',
            'error_5xx': 'Serverfel. Försök igen senare eller kontrollera tjänsteleverantörens status.',
            'error_network': 'Nätverksanslutning misslyckades. Kontrollera nätverksanslutning, proxyinställningar eller brandväggskonfiguration.',
            'error_unknown': 'Okänt fel.',
            'gemini_geo_restriction': 'Gemini API är inte tillgängligt i din region. Försök:\n1. Använd en VPN för att ansluta från en region som stöds\n2. Använd andra AI-leverantörer (OpenAI, Anthropic, DeepSeek, etc.)\n3. Kontrollera Google AI Studio för regional tillgänglighet',
            'load_models_list': 'Ladda Modelllista',
            'loading_models_text': 'Laddar modeller',
            'model_test_success': 'Modelltest lyckades! Konfiguration sparad.',
            'models_loaded_with_selection': 'Laddade {count} modeller framgångsrikt.\nVald modell: {model}',
            'ollama_model_not_available': 'Modell "{model}" är inte tillgänglig. Kontrollera:\n1. Är modellen startad? Kör: ollama run {model}\n2. Är modellnamnet korrekt?\n3. Är modellen nedladdad? Kör: ollama pull {model}',
            'ollama_service_not_running': 'Ollama-tjänsten körs inte. Starta Ollama-tjänsten först.',
            'ollama_service_timeout': 'Ollama-tjänstanslutning timeout. Kontrollera om tjänsten körs korrekt.',
            'reset_ai_confirm_message': 'Håller på att återställa {ai_name} till standardläge.\n\nDetta kommer att rensa:\n• API-nyckel\n• Anpassat modellnamn\n• Andra konfigurerade parametrar\n\nFortsätta?',
            'reset_ai_confirm_title': 'Bekräfta Återställning',
            'reset_current_ai': 'Återställ Aktuell AI till Standard',
            'reset_tooltip': 'Återställ aktuell AI till standardvärden',
            'save_and_close': 'Spara och Stäng',
            'skip': 'Hoppa Över',
            'technical_details': 'Tekniska Detaljer',
            'test_current_model': 'Testa Aktuell Modell',
            'test_model_button': 'Testa Modell',
            'test_model_prompt': 'Modeller laddade framgångsrikt! Vill du testa den valda modellen "{model}"?',
            'unsaved_changes_message': 'Du har osparade ändringar. Vad vill du göra?',
            'unsaved_changes_title': 'Osparade Ändringar',


            'pdf_info_not_available': 'Information ej tillgänglig',
            'auth_token_required_message': 'Vänligen konfigurera en giltig AI-tjänst i Plugin-konfiguration.',
            'auth_token_required_title': 'AI-tjänst Krävs',
            'cancel': 'Avbryt',
            "invalid_default_ai_title": "Ogiltig Standard-AI",
            "invalid_default_ai_message": "Standard-AI:n \"{default_ai}\" är inte korrekt konfigurerad.\n\nVill du byta till \"{first_ai}\" istället?",
            "switch_to_ai": "Byt till {ai}",
            "keep_current": "Behåll nuvarande",
            'empty_suggestion': 'Tomt förslag',
            'error_preparing_request': 'Förberedelse av begäran misslyckades',
            'open_configuration': 'Öppna Konfiguration',
            'process_suggestion_error': 'Fel vid bearbetning av förslag',
            'suggestion_error': 'Förslagsfel',
            'unknown_error': 'Okänt fel',
            'unknown_model': 'Okänd modell: {model_name}',


        }