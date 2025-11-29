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
        return 'Over het boek "{title}": Auteur: {author}, Uitgever: {publisher}, Publicatiejaar: {pubyear}, boek in language: {language}, Serie: {series}, Mijn vraag is: {query}'
    
    @property
    def suggestion_template(self) -> str:
        return """U bent een expert in boekrecensies. Voor het boek "{title}" van {author}, publiceren taal is {language}, genereert u ÉÉN inzichtelijke vraag die lezers helpt om het boek beter te begrijpen. Regels: 1. Retourneer ALLEEN de vraag, zonder inleiding of uitleg 2. Concentreer u op de inhoud van het boek, niet alleen op de titel 3. Maak de vraag praktisch en nadenkend 4. Houd het kort (30-200 woorden) 5. Wees creatief en genereer elke keer een andere vraag, zelfs voor hetzelfde boek"""
    
    @property
    def multi_book_default_template(self) -> str:
        return """Hier is informatie over meerdere boeken: {books_metadata} Gebruikersvraag: {query} Beantwoord de vraag a.u.b. op basis van de bovenstaande boekinformatie."""
    
    @property
    def translations(self) -> dict:
        return {
            # Plugin informatie
            'plugin_name': 'Ask AI Plugin',
            'plugin_desc': 'Stel vragen over een boek met behulp van AI',
            
            # UI - Tabbladen en secties
            'config_title': 'Configuratie',
            'general_tab': 'Algemeen',
            'ai_models': 'AI',
            'shortcuts': 'Sneltoetsen',
            'about': 'Over',
            'metadata': 'Metadata',
            
            # UI - Knoppen en acties
            'ok_button': 'OK',
            'save_button': 'Opslaan',
            'send_button': 'Verzenden',
            'stop_button': 'Stoppen',
            'suggest_button': 'Willekeurige vraag',
            'copy_response': 'Antwoord kopiëren',
            'copy_question_response': 'V&&A kopiëren',
            'export_pdf': 'PDF Exporteren',
            'export_current_qa': 'Huidige V&A Exporteren',
            'export_history': 'Geschiedenis Exporteren',
            
            # Exportinstellingen
            'export_settings': 'Exportinstellingen',
            'enable_default_export_folder': 'Exporteren naar standaardmap',
            'no_folder_selected': 'Geen map geselecteerd',
            'browse': 'Bladeren...',
            'select_export_folder': 'Selecteer Exportmap',
            
            # Knoptekst en menu-items
            'copy_response_btn': 'Antwoord Kopiëren',
            'copy_qa_btn': 'V&A Kopiëren',
            'export_current_btn': 'V&A als PDF Exporteren',
            'export_history_btn': 'Geschiedenis als PDF Exporteren',
            'copy_mode_response': 'Antwoord',
            'copy_mode_qa': 'V&A',
            'export_mode_current': 'Huidige V&A',
            'export_mode_history': 'Geschiedenis',
            
            # PDF-export gerelateerd
            'model_provider': 'Provider',
            'model_name': 'Model',
            'model_api_url': 'API Basis-URL',
            'pdf_model_info': 'AI-Modelinformatie',
            'pdf_software': 'Software',
            
            'export_all_history_dialog_title': 'Volledige Geschiedenis naar PDF Exporteren',
            'export_all_history_title': 'VOLLEDIGE V&A GESCHIEDENIS',
            'export_history_insufficient': 'Minimaal 2 geschiedenisrecords vereist om te exporteren.',
            'history_record': 'Record',
            'question_label': 'Vraag',
            'answer_label': 'Antwoord',
            'default_ai': 'Standaard AI',
            'export_time': 'Geëxporteerd op',
            'total_records': 'Totaal Records',
            'info': 'Informatie',
            'yes': 'Ja',
            'no': 'Nee',
            'no_book_selected_title': 'Geen Boek Geselecteerd',
            'no_book_selected_message': 'Selecteer eerst een boek voordat u vragen stelt.',
            'set_default_ai_title': 'Standaard AI Instellen',
            'set_default_ai_message': 'U bent overgeschakeld naar "{0}". Wilt u deze instellen als standaard AI voor toekomstige vragen?',
            'set_default_ai_success': 'Standaard AI is ingesteld op "{0}".',
            'copied': 'Gekopieerd!',
            'pdf_exported': 'PDF geëxporteerd!',
            'export_pdf_dialog_title': 'Exporteren naar PDF',
            'export_pdf_error': 'Fout bij het exporteren naar PDF: {0}',
            'no_question': 'Geen vraag',
            'no_response': 'Geen antwoord',
            'saved': 'Opgeslagen',
            'close_button': 'Sluiten',
            'open_local_tutorial': 'Open lokale handleiding',
            'tutorial_open_failed': 'Kan handleiding niet openen',
            'tutorial': 'Handleiding',
            
            # UI - Configuratievelden
            'token_label': 'API-sleutel:',
            'api_key_label': 'API-sleutel:',
            'model_label': 'Model:',
            'language_label': 'Taal:',
            'language_label_old': 'Taal',
            'base_url_label': 'Basis-URL:',
            'base_url_placeholder': 'Standaard: {default_api_base_url}',
            'shortcut': 'Sneltoets',
            'shortcut_open_dialog': 'Open dialoog',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Model',
            'action': 'Actie',
            'reset_button': 'Reset',
            'prompt_template': 'Promptsjabloon',
            'ask_prompts': 'Vraagprompts',
            'random_questions_prompts': 'Willekeurige vraagprompts',
            'display': 'Weergave',
            
            # UI - Dialoogelementen
            'input_placeholder': 'Typ je vraag hier...',
            'response_placeholder': 'Antwoord komt eraan...',
            
            # UI - Menu-items
            'menu_title': 'Vraag',
            'menu_ask': 'Vraag',
            
            # UI - Statusberichten
            'loading': 'Laden...',
            'loading_text': 'Vragen',
            'save_success': 'Instellingen opgeslagen',
            'sending': 'Verzenden...',
            'requesting': 'Aanvragen',
            'formatting': 'Aanvraag succesvol, formatteren',
            
            # UI - Modellijst functie
            'load_models': 'Modellen laden',
            'use_custom_model': 'Aangepaste modelnaam gebruiken',
            'custom_model_placeholder': 'Aangepaste modelnaam invoeren',
            'model_placeholder': 'Eerst modellen laden a.u.b.',
            'models_loaded': '{count} modellen succesvol geladen',
            'load_models_failed': 'Laden van modellen mislukt: {error}',
            'model_list_not_supported': 'Deze provider ondersteunt geen automatische model lijst ophalen',
            'api_key_required': 'Eerst API-sleutel invoeren a.u.b.',
            'invalid_params': 'Ongeldige parameters',
            'warning': 'Waarschuwing',
            'success': 'Succes',
            'error': 'Fout',
            
            # Metadata-velden
            'metadata_title': 'Titel',
            'metadata_authors': 'Auteur',
            'metadata_publisher': 'Uitgever',
            'metadata_pubyear': 'Publicatiejaar',
            'metadata_language': 'Taal',
            'metadata_series': 'Serie',
            'no_metadata': 'Geen metadata',
            'no_series': 'Geen serie',
            'unknown': 'Onbekend',
            
            # Meerdere boeken functie
            'books_unit': ' boeken',
            'new_conversation': 'Nieuw gesprek',
            'single_book': 'Enkel boek',
            'multi_book': 'Meerdere boeken',
            'deleted': 'Verwijderd',
            'history': 'Geschiedenis',
            'no_history': 'Geen geschiedenisrecords',
            'empty_question_placeholder': '(Geen vraag)',
            'history_ai_unavailable': 'Deze AI is verwijderd uit de configuratie',
            'clear_current_book_history': 'Wis geschiedenis van huidig boek',
            'confirm_clear_book_history': 'Weet u zeker dat u alle geschiedenis wilt wissen voor:\n{book_titles}?',
            'confirm': 'Bevestigen',
            'history_cleared': '{deleted_count} geschiedenisrecords gewist.',
            'multi_book_template_label': 'Multi-Boek Prompt Sjabloon:',
            'multi_book_placeholder_hint': 'Gebruik {books_metadata} voor boekinformatie, {query} voor de gebruikersvraag',
            
            # Foutmeldingen
            'network_error': 'Netwerkfout',
            'request_timeout': 'Verzoek is verlopen',
            'request_failed': 'Verzoek mislukt',
            'question_too_long': 'Vraag is te lang',
            'auth_token_required_title': 'API-sleutel Vereist',
            'auth_token_required_message': 'Stel een geldige API-sleutel in bij Plugin Configuratie.',
            'open_configuration': 'Configuratie Openen',
            'cancel': 'Annuleren',
            "invalid_default_ai_title": "Ongeldige Standaard AI",
            "invalid_default_ai_message": "De standaard AI \"{default_ai}\" is niet correct geconfigureerd.\n\nWilt u in plaats daarvan overschakelen naar \"{first_ai}\"?",
            "switch_to_ai": "Schakel over naar {ai}",
            "keep_current": "Huidige behouden",
            'error_preparing_request': 'Fout bij voorbereiden verzoek',
            'empty_suggestion': 'Lege suggestie',
            'process_suggestion_error': 'Fout bij verwerken van suggestie',
            'unknown_error': 'Onbekende fout',
            'unknown_model': 'Onbekend model: {model_name}',
            'suggestion_error': 'Suggestiefout',
            'rate_limit': 'Te veel verzoeken',
            'invalid_json': 'Ongeldige JSON',
            'template_error': 'Sjabloonfout',
            'no_model_configured': 'Geen AI-model geconfigureerd. Configureer een AI-model in de instellingen.',
            'no_ai_configured_title': 'Geen AI Geconfigureerd',
            'no_ai_configured_message': 'Welkom! Om vragen over uw boeken te stellen, moet u eerst een AI-provider configureren.\n\nAanbevolen voor beginners:\n• Nvidia AI - Krijg 6 maanden GRATIS API-toegang met alleen uw telefoonnummer (geen creditcard vereist)\n• Ollama - Voer AI-modellen lokaal uit op uw computer (volledig gratis en privé)\n\nWilt u nu de plugin-configuratie openen om een AI-provider in te stellen?',
            'open_settings': 'Plugin Configuratie',
            'ask_anyway': 'Toch Vragen',
            'later': 'Later',
            'reset_all_data': 'Alle Gegevens Resetten',
            'reset_all_data_warning': 'Dit verwijdert alle API-sleutels, promptsjablonen en lokale geschiedenisrecords. Uw taalvoorkeur blijft behouden. Ga voorzichtig te werk.',
            'reset_all_data_confirm_title': 'Reset Bevestigen',
            'reset_all_data_confirm_message': 'Weet u zeker dat u de plugin wilt resetten naar de oorspronkelijke staat?\n\nDit verwijdert permanent:\n• Alle API-sleutels\n• Alle aangepaste promptsjablonen\n• Alle gespreksgeschiedenis\n• Alle plugin-instellingen (taalvoorkeur blijft behouden)\n\nDeze actie kan niet ongedaan worden gemaakt!',
            'reset_all_data_success': 'Alle plugin-gegevens zijn succesvol gereset. Start calibre opnieuw op om de wijzigingen door te voeren.',
            'reset_all_data_failed': 'Resetten van plugin-gegevens mislukt: {error}',
            'random_question_error': 'Fout bij het genereren van willekeurige vraag',
            'clear_history_failed': 'Geschiedenis wissen mislukt',
            'clear_history_not_supported': 'Geschiedenis wissen voor enkel boek wordt nog niet ondersteund',
            'missing_required_config': 'Ontbrekende vereiste configuratie: {key}. Controleer uw instellingen.',
            'api_key_too_short': 'API-sleutel is te kort. Controleer en voer de volledige sleutel in.',
            
            # API antwoordafhandeling
            'api_request_failed': 'API-verzoek mislukt: {error}',
            'api_content_extraction_failed': 'Kon geen inhoud extraheren uit API-antwoord',
            'api_invalid_response': 'Geen geldig API-antwoord ontvangen',
            'api_unknown_error': 'Onbekende fout: {error}',
            
            # Streaming antwoordafhandeling
            'stream_response_code': 'Statuscode streaming antwoord: {code}',
            'stream_continue_prompt': 'Ga verder met je vorige antwoord zonder reeds verstrekte inhoud te herhalen.',
            'stream_continue_code_blocks': 'Uw vorige antwoord had ongesloten codeblokken. Ga verder en voltooi deze codeblokken.',
            'stream_continue_parentheses': 'Uw vorige antwoord had ongesloten haakjes. Ga verder en zorg ervoor dat alle haakjes correct zijn gesloten.',
            'stream_continue_interrupted': 'Uw vorige antwoord lijkt onderbroken te zijn. Ga verder door uw laatste gedachte of uitleg af te maken.',
            'stream_timeout_error': 'Streaming verzending heeft gedurende 60 seconden geen nieuwe inhoud ontvangen, waarschijnlijk een verbindingsprobleem.',
            
            # API foutmeldingen
            'api_version_model_error': 'API-versie of modelnaamfout: {message}\n\nUpdate API-basis-URL naar "{base_url}" en model naar "{model}" of een ander beschikbaar model in de instellingen.',
            'api_format_error': 'API-verzoek formaatfout: {message}',
            'api_key_invalid': 'API-sleutel ongeldig of niet geautoriseerd: {message}\n\nControleer uw API-sleutel en zorg ervoor dat API-toegang is ingeschakeld.',
            'api_rate_limit': 'Verzoek tarieflimiet overschreden, probeer het later opnieuw\n\nU hebt mogelijk het gratis gebruiksquota overschreden. Dit kan te wijten zijn aan:\n1. Te veel verzoeken per minuut\n2. Te veel verzoeken per dag\n3. Te veel invoertokens per minuut',
            
            # Configuratie fouten
            'missing_config_key': 'Ontbrekende vereiste configuratiesleutel: {key}',
            'api_base_url_required': 'API-basis-URL is vereist',
            'model_name_required': 'Modelnaam is vereist',
            'api_key_empty': 'API-sleutel is leeg. Voer een geldige API-sleutel in.',
            
            # Modellijst ophalen
            'fetching_models_from': 'Modellen ophalen van {url}',
            'successfully_fetched_models': '{count} {provider}-modellen opgehaald',
            'failed_to_fetch_models': 'Ophalen van modellen mislukt: {error}',
            
            # Over informatie
            'author_name': 'Sheldon',
            'user_manual': 'Gebruikershandleiding',
            'about_plugin': 'Waarom Ask AI Plugin?',
            'learn_how_to_use': 'Hoe te gebruiken',
            'email': 'iMessage',
            
            # Modelspecifieke configuraties
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Aangepast',
            'model_enable_streaming': 'Streaming inschakelen',
            
            # AI Schakelaar
            'current_ai': 'Huidige AI',
            'no_configured_models': 'Geen AI geconfigureerd - Configureer in instellingen a.u.b.',
            
            # Provider specifieke info
            'nvidia_free_info': '💡 Nieuwe gebruikers krijgen 6 maanden gratis API-toegang - Geen creditcard vereist',
            
            # Algemene systeemberichten
            'default_system_message': 'U bent een expert in boekanalyse. Uw taak is om gebruikers te helpen boeken beter te begrijpen door inzichtelijke vragen en analyse te bieden.',
            
            # Verzoek tijdslimiet instellingen
            'request_timeout_label': 'Verzoek tijdslimiet:',
            'seconds': 'seconden',
            'request_timeout_error': 'Verzoek is verlopen. Huidige tijdslimiet: {timeout} seconden',
            
            # Parallelle AI instellingen
            'parallel_ai_count_label': 'Aantal parallelle AI\'s:',
            'parallel_ai_count_tooltip': 'Aantal AI-modellen dat gelijktijdig wordt opgevraagd (1-2 beschikbaar, 3-4 binnenkort beschikbaar)',
            'parallel_ai_notice': 'Opmerking: Dit heeft alleen invloed op het verzenden van vragen. Willekeurige vragen gebruiken altijd één enkele AI.',
            'suggest_maximize': 'Tip: Maximaliseer venster voor beter zicht met 3 AI\'s',
            'ai_panel_label': 'AI {index}:',
            'no_ai_available': 'Geen AI beschikbaar voor dit paneel',
            'add_more_ai_providers': 'Voeg meer AI-providers toe in de instellingen a.u.b.',
            'select_ai': '-- Selecteer AI --',
            'select_model': '-- Wissel Model --',
            'request_model_list': 'Vraag de modellijst aan a.u.b.',
            'coming_soon': 'Binnenkort beschikbaar',
            'advanced_feature_tooltip': 'Deze functie is in ontwikkeling. Blijf op de hoogte van updates!',
            
            # PDF export sectie titels
            'pdf_book_metadata': 'BOEK METADATA',
            'pdf_question': 'VRAAG',
            'pdf_answer': 'ANTWOORD',
            'pdf_ai_model_info': 'AI MODEL INFORMATIE',
            'pdf_generated_by': 'GEGENEREERD DOOR',
            'pdf_provider': 'Aanbieder',
            'pdf_model': 'Model',
            'pdf_api_base_url': 'API Basis-URL',
            'pdf_panel': 'Paneel',
            'pdf_plugin': 'Plug-in',
            'pdf_github': 'GitHub',
            'pdf_software': 'Software',
            'pdf_generated_time': 'Gegenereerde tijd',
            'default_ai_mismatch_title': 'Standaard AI Gewijzigd',
            'default_ai_mismatch_message': 'De standaard AI in de configuratie is gewijzigd naar "{default_ai}",\nmaar het huidige dialoogvenster gebruikt "{current_ai}".\n\nWilt u overschakelen naar de nieuwe standaard AI?',
            'discard_changes': 'Wijzigingen Verwerpen',
            'empty_response': 'Lege reactie ontvangen van API',
            'empty_response_after_filter': 'Reactie is leeg na het filteren van think-tags',
            'error_401': 'API-sleutelauthenticatie mislukt. Controleer: API-sleutel is correct, account heeft voldoende saldo, API-sleutel is niet verlopen.',
            'error_403': 'Toegang geweigerd. Controleer: API-sleutel heeft voldoende machtigingen, geen regionale toegangsbeperkingen.',
            'error_404': 'API-eindpunt niet gevonden. Controleer of de configuratie van de API-basis-URL correct is.',
            'error_429': 'Te veel verzoeken, tariefslimiet bereikt. Probeer het later opnieuw.',
            'error_5xx': 'Serverfout. Probeer het later opnieuw of controleer de status van de serviceprovider.',
            'error_network': 'Netwerkverbinding mislukt. Controleer netwerkverbinding, proxy-instellingen of firewall-configuratie.',
            'error_unknown': 'Onbekende fout.',
            'gemini_geo_restriction': 'Gemini API is niet beschikbaar in uw regio. Probeer:\n1. Gebruik een VPN om verbinding te maken vanuit een ondersteunde regio\n2. Gebruik andere AI-providers (OpenAI, Anthropic, DeepSeek, enz.)\n3. Controleer Google AI Studio voor regionale beschikbaarheid',
            'load_models_list': 'Modellenlijst Laden',
            'loading_models_text': 'Modellen laden',
            'model_test_success': 'Modeltest succesvol! Configuratie opgeslagen.',
            'models_loaded_with_selection': '{count} modellen succesvol geladen.\nGeselecteerd model: {model}',
            'ollama_model_not_available': 'Model "{model}" is niet beschikbaar. Controleer:\n1. Is het model gestart? Voer uit: ollama run {model}\n2. Is de modelnaam correct?\n3. Is het model gedownload? Voer uit: ollama pull {model}',
            'ollama_service_not_running': 'Ollama-service is niet actief. Start eerst de Ollama-service.',
            'ollama_service_timeout': 'Time-out Ollama-serviceverbinding. Controleer of de service correct werkt.',
            'reset_ai_confirm_message': 'Op het punt om {ai_name} te resetten naar de standaardstatus.\n\nDit zal wissen:\n• API-sleutel\n• Aangepaste modelnaam\n• Andere geconfigureerde parameters\n\nDoorgaan?',
            'reset_ai_confirm_title': 'Reset Bevestigen',
            'reset_current_ai': 'Huidige AI Resetten naar Standaard',
            'reset_tooltip': 'Huidige AI resetten naar standaardwaarden',
            'save_and_close': 'Opslaan en Sluiten',
            'skip': 'Overslaan',
            'technical_details': 'Technische Details',
            'test_current_model': 'Huidig Model Testen',
            'test_model_button': 'Model Testen',
            'test_model_prompt': 'Modellen succesvol geladen! Wilt u het geselecteerde model "{model}" testen?',
            'unsaved_changes_message': 'U heeft niet-opgeslagen wijzigingen. Wat wilt u doen?',
            'unsaved_changes_title': 'Niet-opgeslagen Wijzigingen',


            'pdf_info_not_available': 'Informatie niet beschikbaar',
            'auth_error_401': 'Niet geautoriseerd',
            'avoid_repeat_question': 'Gebruik alstublieft een andere vraag',
            'book_title_check': 'Boektitel vereist',
            'empty_answer': 'Leeg antwoord',
            'invalid_response': 'Ongeldige reactie',
            'random_question_success': 'Willekeurige vraag succesvol gegenereerd!',
            'auth_error_403': 'Toegang geweigerd',

        }