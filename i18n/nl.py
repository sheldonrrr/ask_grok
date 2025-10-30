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
            'export_pdf': 'Exporteren naar PDF',
            'copied': 'Gekopieerd!',
            'pdf_exported': 'PDF geëxporteerd!',
            'export_pdf_dialog_title': 'Exporteren naar PDF',
            'export_pdf_error': 'Fout bij het exporteren naar PDF: {0}',
            'no_question': 'Geen vraag',
            'no_response': 'Geen antwoord',
            'saved': 'Opgeslagen',
            'close_button': 'Sluiten',
            
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
            'menu_ask': 'Vraag {model}',
            
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
            'multi_book_template_label': 'Promptsjabloon voor meerdere boeken:',
            'multi_book_placeholder_hint': 'Gebruik {books_metadata} voor boekinformatie, {query} voor gebruikersvraag',
            
            # Foutmeldingen
            'error': 'Fout: ',
            'network_error': 'Netwerkfout',
            'request_timeout': 'Verzoek is verlopen',
            'request_failed': 'Verzoek mislukt',
            'question_too_long': 'Vraag is te lang',
            'auth_token_required_title': 'API-sleutel vereist',
            'auth_token_required_message': 'Stel de API-sleutel in de Plugin Configuratie in.',
            'error_preparing_request': 'Fout bij voorbereiden van verzoek',
            'empty_suggestion': 'Lege suggestie',
            'process_suggestion_error': 'Fout bij verwerken van suggestie',
            'unknown_error': 'Onbekende fout',
            'unknown_model': 'Onbekend model: {model_name}',
            'suggestion_error': 'Suggestiefout',
            'random_question_success': 'Willekeurige vraag succesvol gegenereerd!',
            'book_title_check': 'Boektitel vereist',
            'avoid_repeat_question': 'Gebruik een andere vraag a.u.b.',
            'empty_answer': 'Leeg antwoord',
            'invalid_response': 'Ongeldig antwoord',
            'auth_error_401': 'Niet geautoriseerd',
            'auth_error_403': 'Toegang geweigerd',
            'rate_limit': 'Tarieflimiet overschreden',
            'invalid_json': 'Ongeldige JSON',
            'no_response': 'Geen antwoord',
            'template_error': 'Sjabloonfout',
            'no_model_configured': 'Geen AI-model geconfigureerd. Configureer een AI-model in de instellingen.',
            'random_question_error': 'Fout bij genereren van willekeurige vraag',
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
            'model_disable_ssl_verify': 'SSL-verificatie uitschakelen',
            
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
            'pdf_info_not_available': 'Informatie niet beschikbaar',
        }