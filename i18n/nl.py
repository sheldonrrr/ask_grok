#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dutch language translations for Ask AI Plugin.
"""

from ..models.base import BaseTranslation, TranslationRegistry, AIProvider


@TranslationRegistry.register
class DutchTranslation(BaseTranslation):
    """Dutch language translation."""

    @property
    def code(self) -> str:
        return "nl"

    @property
    def name(self) -> str:
        return "Nederlands"

    @property
    def default_template(self) -> str:
        return 'Over het boek "{title}": Auteur: {author}, Uitgever: {publisher}, Publicatiejaar: {pubyear}, boek in taal: {language}, Serie: {series}, Mijn vraag is: {query}'

    @property
    def suggestion_template(self) -> str:
        return """U bent een deskundige boekenrecensent. Voor het boek "{title}" van {author}, publicatietaal is {language}, genereer EEN inzichtelijke vraag die lezers helpt de kernideeën, praktische toepassingen of unieke perspectieven van het boek beter te begrijpen. Regels: 1. Retourneer ALLEEN de vraag, zonder inleiding of uitleg 2. Concentreer u op de inhoud van het boek, niet alleen op de titel 3. Maak de vraag praktisch en tot nadenken stemmend 4. Houd het beknopt (30-200 woorden) 5. Wees creatief en genereer elke keer een andere vraag, zelfs voor hetzelfde boek"""

    @property
    def multi_book_default_template(self) -> str:
        return """Hier is informatie over meerdere boeken: {books_metadata} Gebruikersvraag: {query} Beantwoord de vraag alstublieft op basis van de bovenstaande boekinformatie."""

    @property
    def translations(self) -> dict:
        return {
            # Plugin information
            'plugin_name': 'Ask AI Plugin',
            'plugin_desc': 'Stel vragen over een boek met behulp van AI',

            # UI - Tabs and sections
            'config_title': 'Configuratie',
            'general_tab': 'Algemeen',
            'ai_models': 'AI-aanbieders',
            'shortcuts': 'Sneltoetsen',
            'shortcuts_note': "U kunt deze sneltoetsen aanpassen in calibre: Voorkeuren -> Sneltoetsen (zoek 'Ask AI').\nDeze pagina toont de standaard/voorbeeld sneltoetsen. Als u ze in Sneltoetsen heeft gewijzigd, hebben de calibre instellingen voorrang.",
            'prompts_tab': 'Prompts',
            'about': 'Over',
            'metadata': 'Metadata',

            # Section subtitles
            'language_settings': 'Taal',
            'language_subtitle': 'Kies uw voorkeurstaal voor de interface',
            'ai_providers_subtitle': 'Configureer AI-aanbieders en selecteer uw standaard-AI',
            'prompts_subtitle': 'Pas aan hoe vragen naar AI worden verzonden',
            'export_settings_subtitle': 'Stel de standaardmap in voor het exporteren van PDF\'s',
            'debug_settings_subtitle': 'Schakel debug-logging in voor probleemoplossing',
            'reset_all_data_subtitle': '⚠️ Waarschuwing: Dit zal al uw instellingen en gegevens permanent verwijderen',

            # Prompts tab
            'language_preference_title': 'Taalvoorkeur',
            'language_preference_subtitle': 'Bepaal of AI-antwoorden moeten overeenkomen met de taal van uw interface',
            'prompt_templates_title': 'Prompt-sjablonen',
            'prompt_templates_subtitle': 'Pas aan hoe boekinformatie naar AI wordt verzonden met dynamische velden zoals {title}, {author}, {query}',
            'ask_prompts': 'Vraagprompts',
            'random_questions_prompts': 'Willekeurige vragen-prompts',
            'multi_book_prompts_label': 'Meerdere boeken-prompts',
            'multi_book_placeholder_hint': 'Gebruik {books_metadata} voor boekinformatie, {query} voor de gebruikersvraag',
            'dynamic_fields_title': 'Referentie dynamische velden',
            'dynamic_fields_subtitle': 'Beschikbare velden en voorbeeldwaarden van "Frankenstein" door Mary Shelley',
            'dynamic_fields_examples': '<b>{title}</b> → Frankenstein<br><b>{author}</b> → Mary Shelley<br><b>{publisher}</b> → Lackington, Hughes, Harding, Mavor & Jones<br><b>{pubyear}</b> → 1818<br><b>{language}</b> → Engels<br><b>{series}</b> → (geen)<br><b>{query}</b> → Uw vraagtekst',
            'reset_prompts': 'Herstel prompts naar standaard',
            'reset_prompts_confirm': 'Weet u zeker dat u alle prompt-sjablonen wilt herstellen naar hun standaardwaarden? Deze actie kan niet ongedaan worden gemaakt.',
            'unsaved_changes_title': 'Niet-opgeslagen wijzigingen',
            'unsaved_changes_message': 'U heeft niet-opgeslagen wijzigingen in het tabblad Prompts. Wilt u deze opslaan?',
            'use_interface_language': 'Vraag AI altijd om te antwoorden in de huidige interface-taal van de plugin',
            'language_instruction_label': 'Taalinstructie toegevoegd aan prompts:',
            'language_instruction_text': 'Antwoord alstublieft in {language_name}.',

            # Persona settings
            'persona_title': 'Persona',
            'persona_subtitle': 'Definieer uw onderzoeksachtergrond en doelen om AI te helpen relevantere antwoorden te geven',
            'use_persona': 'Gebruik persona',
            'persona_label': 'Persona',
            'persona_placeholder': 'Als onderzoeker wil ik onderzoek doen aan de hand van boekgegevens.',
            'persona_hint': 'Hoe meer AI weet over uw doel en achtergrond, hoe beter de resultaten van het onderzoek of de generatie.',

            # UI - Buttons and actions
            'ok_button': 'OK',
            'save_button': 'Opslaan',
            'send_button': 'Verzenden',
            'stop_button': 'Stop',
            'suggest_button': 'Willekeurige vraag',
            'copy_response': 'Kopieer antwoord',
            'copy_question_response': 'Kopieer V&A',
            'export_pdf': 'Exporteer PDF',
            'export_current_qa': 'Exporteer huidige V&A',
            'export_history': 'Exporteer geschiedenis',
            'export_all_history_dialog_title': 'Exporteer alle geschiedenis naar PDF',
            'export_all_history_title': 'ALLE V&A GESCHIEDENIS',
            'export_history_insufficient': 'Minimaal 2 geschiedenisrecords nodig om te exporteren.',
            'history_record': 'Record',
            'question_label': 'Vraag',
            'answer_label': 'Antwoord',
            'default_ai': 'Standaard-AI',
            'export_time': 'Geëxporteerd op',
            'total_records': 'Totaal aantal records',
            'info': 'Informatie',
            'yes': 'Ja',
            'no': 'Nee',
            'no_book_selected_title': 'Geen boek geselecteerd',
            'no_book_selected_message': 'Selecteer een boek voordat u vragen stelt.',
            'set_default_ai_title': 'Stel standaard-AI in',
            'set_default_ai_message': 'U bent overgeschakeld naar "{0}". Wilt u dit instellen als de standaard-AI voor toekomstige vragen?',
            'set_default_ai_success': 'Standaard-AI is ingesteld op "{0}".',
            'default_ai_mismatch_title': 'Standaard-AI gewijzigd',
            'default_ai_mismatch_message': 'De standaard-AI in de configuratie is gewijzigd naar "{default_ai}",\nmaar het huidige dialoogvenster gebruikt "{current_ai}".\n\nWilt u overschakelen naar de nieuwe standaard-AI?',
            'copied': 'Gekopieerd!',
            'pdf_exported': 'PDF geëxporteerd!',
            'export_pdf_dialog_title': 'Exporteren naar PDF',
            'export_pdf_error': 'Exporteren van PDF mislukt: {0}',
            'no_question': 'Geen vraag',
            'no_response': 'Geen antwoord',
            'saved': 'Opgeslagen',
            'close_button': 'Sluiten',
            'open_local_tutorial': 'Open lokale handleiding',
            'tutorial_open_failed': 'Openen handleiding mislukt',
            'tutorial': 'Handleiding',

            'model_display_name_perplexity': 'Perplexity',

            # UI - Configuration fields
            'token_label': 'API-sleutel:',
            'api_key_label': 'API-sleutel:',
            'model_label': 'Model:',
            'language_label': 'Taal:',
            'language_label_old': 'Taal',
            'base_url_label': 'Basis-URL:',
            'base_url_placeholder': 'Standaard: {default_api_base_url}',
            'shortcut': 'Sneltoets',
            'shortcut_open_dialog': 'Dialoogvenster openen',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Model',
            'action': 'Actie',
            'reset_button': 'Herstel naar standaard',
            'reset_current_ai': 'Herstel huidige AI naar standaard',
            'reset_ai_confirm_title': 'Bevestig herstel',
            'reset_ai_confirm_message': 'Staat op het punt om {ai_name} te herstellen naar de standaardstatus.\n\nDit wist:\n• API-sleutel\n• Aangepaste modelnaam\n• Andere geconfigureerde parameters\n\nDoorgaan?',
            'reset_tooltip': 'Herstel huidige AI naar standaardwaarden',
            'unsaved_changes_title': 'Niet-opgeslagen wijzigingen',
            'unsaved_changes_message': 'U heeft niet-opgeslagen wijzigingen. Wat wilt u doen?',
            'save_and_close': 'Opslaan en sluiten',
            'discard_changes': 'Wijzigingen negeren',
            'cancel': 'Annuleren',
            'yes_button': 'Ja',
            'no_button': 'Nee',
            'cancel_button': 'Annuleren',
            'invalid_default_ai_title': 'Ongeldige standaard-AI',
            'invalid_default_ai_message': 'De standaard-AI "{default_ai}" is niet correct geconfigureerd.\n\nWilt u overschakelen naar "{first_ai}"?',
            'switch_to_ai': 'Schakelen naar {ai}',
            'keep_current': 'Huidige behouden',
            'prompt_template': 'Prompt-sjabloon',
            'ask_prompts': 'Vraagprompts',
            'random_questions_prompts': 'Willekeurige vragen-prompts',
            'display': 'Weergave',
            'export_settings': 'Exportinstellingen',
            'enable_default_export_folder': 'Exporteer naar standaardmap',
            'no_folder_selected': 'Geen map geselecteerd',
            'browse': 'Bladeren...',
            'select_export_folder': 'Selecteer exportmap',

            # Button text and menu items
            'copy_response_btn': 'Kopieer antwoord',
            'copy_qa_btn': 'Kopieer V&A',
            'export_current_btn': 'Exporteer V&A als PDF',
            'export_history_btn': 'Exporteer geschiedenis als PDF',
            'copy_mode_response': 'Antwoord',
            'copy_mode_qa': 'V&A',
            'export_mode_current': 'Huidige V&A',
            'export_mode_history': 'Geschiedenis',

            # PDF Export related
            'model_provider': 'Aanbieder',
            'model_name': 'Model',
            'model_api_url': 'API Basis-URL',
            'pdf_model_info': 'AI Model Informatie',
            'pdf_software': 'Software',

            # UI - Dialog elements
            'input_placeholder': 'Typ uw vraag...',
            'response_placeholder': 'Antwoord binnenkort...',

            # UI - Menu items
            'menu_title': 'Vraag AI',
            'menu_ask': 'Vragen',

            # UI - Status information
            'loading': 'Laden',
            'loading_text': 'Vragen',
            'loading_models_text': 'Modellen laden',
            'save_success': 'Instellingen opgeslagen',
            'sending': 'Verzenden...',
            'requesting': 'Aanvragen',
            'formatting': 'Verzoek geslaagd, formatteren',

            # UI - Model list feature
            'load_models': 'Laad modellen',
            'load_models_list': 'Laad modellijst',
            'test_current_model': 'Test huidig model',
            'use_custom_model': 'Gebruik aangepaste modelnaam',
            'custom_model_placeholder': 'Voer aangepaste modelnaam in',
            'model_placeholder': 'Laad eerst modellen',
            'models_loaded': 'Succesvol {count} modellen geladen',
            'models_loaded_with_selection': 'Succesvol {count} modellen geladen.\nGeselecteerd model: {model}',
            'load_models_failed': 'Laden van modellen mislukt: {error}',
            'model_list_not_supported': 'Deze aanbieder ondersteunt geen automatische modellijstophaling',
            'api_key_required': 'Voer eerst de API-sleutel in',
            'invalid_params': 'Ongeldige parameters',
            'warning': 'Waarschuwing',
            'success': 'Succes',
            'error': 'Fout',

            # Metadata fields
            'metadata_title': 'Titel',
            'metadata_authors': 'Auteur',
            'metadata_publisher': 'Uitgever',
            'metadata_pubdate': 'Publicatiedatum',
            'metadata_pubyear': 'Publicatiejaar',
            'metadata_language': 'Taal',
            'metadata_series': 'Serie',
            'no_metadata': 'Geen metadata',
            'no_series': 'Geen serie',
            'unknown': 'Onbekend',

            # Multi-book feature
            'books_unit': ' boeken',
            'new_conversation': 'Nieuw gesprek',
            'single_book': 'Enkel boek',
            'multi_book': 'Meerdere boeken',
            'deleted': 'Verwijderd',
            'history': 'Geschiedenis',
            'no_history': 'Geen geschiedenisrecords',
            'empty_question_placeholder': '(Geen vraag)',
            'history_ai_unavailable': 'Deze AI is verwijderd uit de configuratie',
            'clear_current_book_history': 'Wis huidige boekgeschiedenis',
            'confirm_clear_book_history': 'Weet u zeker dat u alle geschiedenis wilt wissen voor:\n{book_titles}?',
            'confirm': 'Bevestigen',
            'history_cleared': '{deleted_count} geschiedenisrecords gewist.',
            'multi_book_template_label': 'Meerdere boeken-prompt-sjabloon:',
            'multi_book_placeholder_hint': 'Gebruik {books_metadata} voor boekinformatie, {query} voor de gebruikersvraag',

            # Error messages (Note: 'error' is already defined above, these are other error types)
            'network_error': 'Verbindingsfout',
            'request_timeout': 'Verzoektime-out',
            'request_failed': 'Verzoek mislukt',
            'request_stopped': 'Verzoek gestopt',
            'question_too_long': 'Vraag te lang',
            'auth_token_required_title': 'AI-service vereist',
            'auth_token_required_message': 'Configureer alstublieft een geldige AI-service in de Plugin Configuratie.',
            'open_configuration': 'Open configuratie',
            'error_preparing_request': 'Voorbereiding van verzoek mislukt',
            'empty_suggestion': 'Leeg voorstel',
            'process_suggestion_error': 'Fout bij verwerken van voorstel',
            'unknown_error': 'Onbekende fout',
            'unknown_model': 'Onbekend model: {model_name}',
            'suggestion_error': 'Suggestiefout',
            'random_question_success': 'Willekeurige vraag succesvol gegenereerd!',
            'book_title_check': 'Boektitel vereist',
            'avoid_repeat_question': 'Gebruik alstublieft een andere vraag',
            'empty_answer': 'Leeg antwoord',
            'invalid_response': 'Ongeldig antwoord',
            'auth_error_401': 'Ongeautoriseerd',
            'auth_error_403': 'Toegang geweigerd',
            'rate_limit': 'Te veel verzoeken',
            'empty_response': 'Leeg antwoord ontvangen van API',
            'empty_response_after_filter': 'Antwoord is leeg na filteren van gedachtetags',
            'no_response': 'Geen antwoord',
            'template_error': 'Sjabloonfout',
            'no_model_configured': 'Geen AI-model geconfigureerd. Configureer alstublieft een AI-model in de instellingen.',
            'no_ai_configured_title': 'Geen AI geconfigureerd',
            'no_ai_configured_message': 'Welkom! Om vragen over uw boeken te stellen, moet u eerst een AI-aanbieder configureren.\n\nGoed nieuws: Deze plugin heeft nu een GRATIS versie (Nvidia AI Free) die u direct kunt gebruiken zonder enige configuratie!\n\nAndere aanbevolen opties:\n• Nvidia AI - Ontvang 6 maanden GRATIS API-toegang met alleen uw telefoonnummer (geen creditcard vereist)\n• Ollama - Voer AI-modellen lokaal uit op uw computer (volledig gratis en privé)\n\nWilt u nu de plugin-configuratie openen om een AI-aanbieder in te stellen?',
            'open_settings': 'Plugin Configuratie',
            'ask_anyway': 'Vraag toch',
            'later': 'Later',
            'debug_settings': 'Debug-instellingen',
            'enable_debug_logging': 'Schakel debug-logging in (ask_ai_plugin_debug.log)',
            'debug_logging_hint': 'Indien uitgeschakeld, worden debug-logs niet naar een bestand geschreven. Dit kan voorkomen dat het logbestand te groot wordt.',
            'reset_all_data': 'Reset alle gegevens',
            'reset_all_data_warning': 'Dit zal alle API-sleutels, promptsjablonen en lokale geschiedenisrecords verwijderen. Uw taalvoorkeur blijft behouden. Ga voorzichtig te werk.',
            'reset_all_data_confirm_title': 'Bevestig reset',
            'reset_all_data_confirm_message': 'Weet u zeker dat u de plugin wilt herstellen naar de beginstatus?\n\nDit zal permanent verwijderen:\n• Alle API-sleutels\n• Alle aangepaste promptsjablonen\n• Alle conversatiegeschiedenis\n• Alle plugin-instellingen (taalvoorkeur blijft behouden)\n\nDeze actie kan niet ongedaan worden gemaakt!',
            'reset_all_data_success': 'Alle plugingegevens zijn succesvol gereset. Herstart calibre om de wijzigingen door te voeren.',
            'reset_all_data_failed': 'Resetten van plugingegevens mislukt: {error}',
            'random_question_error': 'Fout bij genereren van willekeurige vraag',
            'clear_history_failed': 'Geschiedenis wissen mislukt',
            'clear_history_not_supported': 'Geschiedenis wissen voor enkel boek wordt nog niet ondersteund',
            'missing_required_config': 'Vereiste configuratie ontbreekt: {key}. Controleer uw instellingen.',
            'api_key_too_short': 'API-sleutel is te kort. Controleer en voer de volledige sleutel in.',

            # API response handling
            'api_request_failed': 'API-verzoek mislukt: {error}',
            'api_content_extraction_failed': 'Kan geen inhoud extraheren uit API-antwoord',
            'api_invalid_response': 'Kan geen geldig API-antwoord krijgen',
            'api_unknown_error': 'Onbekende fout: {error}',

            # Stream response handling
            'stream_response_code': 'Stream-antwoordstatuscode: {code}',
            'stream_continue_prompt': 'Vervolg alstublieft uw vorige antwoord zonder reeds verstrekte inhoud te herhalen.',
            'stream_continue_code_blocks': 'Uw vorige antwoord bevatte ongesloten codeblokken. Ga alstublieft verder en voltooi deze codeblokken.',
            'stream_continue_parentheses': 'Uw vorige antwoord bevatte ongesloten haakjes. Ga alstublieft verder en zorg ervoor dat alle haakjes correct zijn gesloten.',
            'stream_continue_interrupted': 'Uw vorige antwoord lijkt te zijn onderbroken. Ga alstublieft verder met het voltooien van uw laatste gedachte of uitleg.',
            'stream_timeout_error': 'Stream-overdracht heeft 60 seconden lang geen nieuwe inhoud ontvangen, mogelijk een verbindingsprobleem.',

            # API error messages
            'api_version_model_error': 'API-versie of modelnaamfout: {message}\n\nWerk alstublieft de API Basis-URL bij naar "{base_url}" en het model naar "{model}" of een ander beschikbaar model in de instellingen.',
            'api_format_error': 'API-verzoekformaatfout: {message}',
            'api_key_invalid': 'API-sleutel ongeldig of ongeautoriseerd: {message}\n\nControleer alstublieft uw API-sleutel en zorg ervoor dat API-toegang is ingeschakeld.',
            'api_rate_limit': 'Verzoeklimiet overschreden, probeer het later opnieuw\n\nU heeft mogelijk de gratis gebruikslimiet overschreden. Dit kan te wijten zijn aan:\n1. Te veel verzoeken per minuut\n2. Te veel verzoeken per dag\n3. Te veel invoer tokens per minuut',

            # Configuration errors
            'missing_config_key': 'Ontbrekende vereiste configuratiesleutel: {key}',
            'api_base_url_required': 'API Basis-URL is vereist',
            'model_name_required': 'Modelnaam is vereist',

            # Model list fetching
            'fetching_models_from': 'Modellen ophalen van {url}',
            'successfully_fetched_models': 'Succesvol {count} {provider} modellen opgehaald',
            'failed_to_fetch_models': 'Laden van modellen mislukt: {error}',
            'api_key_empty': 'API-sleutel is leeg. Voer alstublieft een geldige API-sleutel in.',

            # Error messages for model fetching
            'error_401': 'API-sleutelauthenticatie mislukt. Controleer alstublieft: API-sleutel is correct, account heeft voldoende saldo, API-sleutel is niet verlopen.',
            'error_403': 'Toegang geweigerd. Controleer alstublieft: API-sleutel heeft voldoende rechten, geen regionale toegangsbeperkingen.',
            'error_404': 'API-eindpunt niet gevonden. Controleer alstublieft of de configuratie van de API Basis-URL correct is.',
            'error_429': 'Te veel verzoeken, rate-limit bereikt. Probeer het later opnieuw.',
            'error_5xx': 'Serverfout. Probeer het later opnieuw of controleer de status van de serviceprovider.',
            'error_network': 'Netwerkverbinding mislukt. Controleer alstublieft de netwerkverbinding, proxy-instellingen of firewallconfiguratie.',
            'error_unknown': 'Onbekende fout.',
            'technical_details': 'Technische details',
            'ollama_service_not_running': 'Ollama-service draait niet. Start alstublieft eerst de Ollama-service.',
            'ollama_service_timeout': 'Ollama-serviceverbinding time-out. Controleer alstublieft of de service correct draait.',
            'ollama_model_not_available': 'Model "{model}" is niet beschikbaar. Controleer alstublieft:\n1. Is het model gestart? Voer uit: ollama run {model}\n2. Is de modelnaam correct?\n3. Is het model gedownload? Voer uit: ollama pull {model}',
            'gemini_geo_restriction': 'Gemini API is niet beschikbaar in uw regio. Probeer alstublieft:\n1. Gebruik een VPN om verbinding te maken vanuit een ondersteunde regio\n2. Gebruik andere AI-aanbieders (OpenAI, Anthropic, DeepSeek, etc.)\n3. Controleer Google AI Studio op regionale beschikbaarheid',
            'model_test_success': 'Modeltest succesvol!',
            'test_model_prompt': 'Modellen succesvol geladen! Wilt u het geselecteerde model "{model}" testen?',
            'test_model_button': 'Test model',
            'skip': 'Overslaan',

            # About information
            'author_name': 'Sheldon',
            'user_manual': 'Gebruikershandleiding',
            'about_plugin': 'Over Ask AI Plugin',
            'learn_how_to_use': 'Hoe te gebruiken',
            'email': 'iMessage',

            # Model specific configurations
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Aangepast',
            'model_enable_streaming': 'Streaming inschakelen',

            # AI Switcher
            'current_ai': 'Huidige AI',
            'no_configured_models': 'Geen AI geconfigureerd - Configureer alstublieft in instellingen',

            # Provider specific info
            'nvidia_free_info': '💡 Nieuwe gebruikers krijgen 6 maanden gratis API-toegang - Geen creditcard vereist',

            # Common system messages
            'default_system_message': 'U bent een expert in boekanalyse. Uw taak is om gebruikers te helpen boeken beter te begrijpen door inzichtelijke vragen en analyses te geven.',

            # Request timeout settings
            'request_timeout_label': 'Verzoektime-out:',
            'seconds': 'seconden',
            'request_timeout_error': 'Verzoektime-out. Huidige time-out: {timeout} seconden',

            # Parallel AI settings
            'parallel_ai_count_label': 'Aantal parallelle AI\'s:',
            'parallel_ai_count_tooltip': 'Aantal AI-modellen dat tegelijkertijd wordt bevraagd (1-2 beschikbaar, 3-4 binnenkort beschikbaar)',
            'parallel_ai_notice': 'Opmerking: Dit heeft alleen invloed op het verzenden van vragen. Willekeurige vragen gebruiken altijd één AI.',
            'suggest_maximize': 'Tip: Maximaliseer het venster voor een betere weergave met 3 AI\'s',
            'ai_panel_label': 'AI {index}:',
            'no_ai_available': 'Geen AI beschikbaar voor dit paneel',
            'add_more_ai_providers': 'Voeg meer AI-aanbieders toe in de instellingen',
            'select_ai': '-- Selecteer AI --',
            'select_model': '-- Selecteer model --',
            'request_model_list': 'Vraag modellijst op',
            'coming_soon': 'Binnenkort beschikbaar',
            'advanced_feature_tooltip': 'Deze functie is in ontwikkeling. Blijf op de hoogte van updates!',

            # AI Manager Dialog
            'ai_manager_title': 'Beheer AI-aanbieders',
            'add_ai_title': 'Voeg AI-aanbieder toe',
            'manage_ai_title': 'Beheer geconfigureerde AI',
            'configured_ai_list': 'Geconfigureerde AI',
            'available_ai_list': 'Beschikbaar om toe te voegen',
            'ai_config_panel': 'Configuratie',
            'select_ai_to_configure': 'Selecteer een AI uit de lijst om te configureren',
            'select_provider': 'Selecteer AI-aanbieder',
            'select_provider_hint': 'Selecteer een aanbieder uit de lijst',
            'select_ai_to_edit': 'Selecteer een AI uit de lijst om te bewerken',
            'set_as_default': 'Instellen als standaard',
            'save_ai_config': 'Opslaan',
            'remove_ai_config': 'Verwijderen',
            'delete_ai': 'Verwijderen',
            'add_ai_button': 'AI toevoegen',
            'edit_ai_button': 'AI bewerken',
            'manage_configured_ai_button': 'Beheer geconfigureerde AI',
            'manage_ai_button': 'Beheer AI',
            'no_configured_ai': 'Nog geen AI geconfigureerd',
            'no_configured_ai_hint': 'Geen AI geconfigureerd. Plugin kan niet werken. Klik op "AI toevoegen" om een AI-aanbieder toe te voegen.',
            'default_ai_label': 'Standaard AI:',
            'default_ai_tag': 'Standaard',
            'ai_not_configured_cannot_set_default': 'Deze AI is nog niet geconfigureerd. Sla de configuratie eerst op.',
            'ai_set_as_default_success': '{name} is ingesteld als de standaard AI.',
            'ai_config_saved_success': '{name}-configuratie succesvol opgeslagen.',
            'confirm_remove_title': 'Verwijdering bevestigen',
            'confirm_remove_ai': 'Weet u zeker dat u {name} wilt verwijderen? Dit wist de API-sleutel en reset de configuratie.',
            'confirm_delete_title': 'Verwijdering bevestigen',
            'confirm_delete_ai': 'Weet u zeker dat u {name} wilt verwijderen?',
            'api_key_required': 'API-sleutel is vereist.',
            'configuration': 'Configuratie',

            # Field descriptions
            'api_key_desc': 'Uw API-sleutel voor authenticatie. Houd deze veilig en deel deze niet.',
            'base_url_desc': 'De API-eindpunt-URL. Gebruik standaard tenzij u een aangepast eindpunt heeft.',
            'model_desc': 'Selecteer een model uit de lijst of gebruik een aangepaste modelnaam.',
            'streaming_desc': 'Schakel real-time responsstreaming in voor snellere feedback.',
            'advanced_section': 'Geavanceerd',

            # Provider-specific notices
            'perplexity_model_notice': 'Opmerking: Perplexity biedt geen openbare API voor modellijsten, dus modellen zijn vastgelegd.',
            'ollama_no_api_key_notice': 'Opmerking: Ollama is een lokaal model waarvoor geen API-sleutel nodig is.',
            'nvidia_free_credits_notice': 'Opmerking: Nieuwe gebruikers krijgen gratis API-tegoed - geen creditcard vereist.',

            # Nvidia Free error messages
            'free_tier_rate_limit': 'Limiet voor gratis tier overschreden. Probeer het later opnieuw of configureer uw eigen Nvidia API-sleutel.',
            'free_tier_unavailable': 'Gratis tier is tijdelijk niet beschikbaar. Probeer het later opnieuw of configureer uw eigen Nvidia API-sleutel.',
            'free_tier_server_error': 'Serverfout gratis tier. Probeer het later opnieuw.',
            'free_tier_error': 'Fout in gratis tier',

            # Nvidia Free provider info
            'free': 'Gratis',
            'nvidia_free_provider_name': 'Nvidia AI (Gratis)',
            'nvidia_free_display_name': 'Nvidia AI (Gratis)',
            'nvidia_free_api_key_info': 'Wordt van server verkregen',
            'nvidia_free_desc': 'Deze service wordt onderhouden door de ontwikkelaar en blijft gratis, maar kan minder stabiel zijn. Voor een stabielere service kunt u uw eigen Nvidia API-sleutel configureren.',

            # Nvidia Free first use reminder
            'nvidia_free_first_use_title': 'Welkom bij Ask AI Plugin',
            'nvidia_free_first_use_message': 'U kunt nu direct vragen stellen zonder configuratie! De ontwikkelaar biedt een gratis tier aan, maar deze is mogelijk minder stabiel. Veel plezier!\n\nU kunt uw eigen AI-aanbieders configureren in de instellingen voor meer stabiliteit.',

            # Model buttons
            'refresh_model_list': 'Vernieuwen',
            'test_current_model': 'Testen',
            'testing_text': 'Bezig met testen',
            'refresh_success': 'Modellijst succesvol vernieuwd.',
            'refresh_failed': 'Vernieuwen van modellijst mislukt.',
            'test_failed': 'Modeltest mislukt.',

            # Tooltip
            'manage_ai_disabled_tooltip': 'Voeg eerst een AI-aanbieder toe.',

            # PDF export section titles
            'pdf_book_metadata': 'BOEK METADATA',
            'pdf_question': 'VRAAG',
            'pdf_answer': 'ANTWOORD',
            'pdf_ai_model_info': 'AI MODEL INFORMATIE',
            'pdf_generated_by': 'GEGENEREERD DOOR',
            'pdf_provider': 'Aanbieder',
            'pdf_model': 'Model',
            'pdf_api_base_url': 'API Basis-URL',
            'pdf_panel': 'Paneel',
            'pdf_plugin': 'Plugin',
            'pdf_github': 'GitHub',
            'pdf_software': 'Software',
            'pdf_generated_time': 'Gegenereerde tijd',
            'pdf_info_not_available': 'Informatie niet beschikbaar',
        }