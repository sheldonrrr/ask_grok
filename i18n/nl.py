#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dutch language translations for Ask Grok plugin.
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
    def translations(self) -> dict:
        return {
            # Plugin informatie
            'plugin_name': 'Ask Grok',
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
            'suggest_button': 'Willekeurige vraag',
            'copy_response': 'Antwoord kopiëren',
            'copy_question_response': 'V&&A kopiëren',
            'copied': 'Gekopieerd!',
            'saved': 'Opgeslagen',
            'close_button': 'Sluiten',
            
            # UI - Configuratievelden
            'token_label': 'API-sleutel:',
            'model_label': 'Model:',
            'language_label': 'Taal',
            'base_url_label': 'Basis-URL:',
            'base_url_placeholder': 'Standaard: {default_api_base_url}',
            'shortcut': 'Sneltoets',
            'shortcut_open_dialog': 'Open dialoog',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Model',
            'current_ai': 'Huidige AI:',
            'action': 'Actie',
            'reset_button': 'Reset',
            'prompt_template': 'Promptsjabloon',
            'ask_prompts': 'Vraagprompts',
            'random_questions_prompts': 'Willekeurige vraagprompts',
            'display': 'Weergave',
            
            # UI - Dialoogelementen
            'input_placeholder': 'Typ je vraag...',
            'response_placeholder': 'Antwoord komt eraan...',
            
            # UI - Menu-items
            'menu_title': 'Vraag',
            'menu_ask': 'Vraag {model}',
            
            # UI - Statusberichten
            'loading': 'Laden',
            'loading_text': 'Vraag stellen',
            'save_success': 'Instellingen opgeslagen',
            'sending': 'Verzenden...',
            'requesting': 'Aanvragen',
            'formatting': 'Aanvraag geslaagd, formatteren',
            
            # Metadatavelden
            'metadata_title': 'Titel',
            'metadata_authors': 'Auteur',
            'metadata_publisher': 'Uitgever',
            'metadata_pubyear': 'Publicatiedatum',
            'metadata_language': 'Taal',
            'metadata_series': 'Serie',
            'no_metadata': 'Geen metadata',
            'no_series': 'Geen serie',
            'unknown': 'Onbekend',
            
            # Foutmeldingen
            'error': 'Fout: ',
            'network_error': 'Verbindingsfout',
            'request_timeout': 'Aanvraag time-out',
            'request_failed': 'Aanvraag mislukt',
            'question_too_long': 'Vraag te lang',
            'auth_token_required_title': 'API-sleutel vereist',
            'auth_token_required_message': 'Stel de API-sleutel in bij de Plugin Configuratie',
            'error_preparing_request': 'Fout bij voorbereiden aanvraag',
            'empty_suggestion': 'Lege suggestie',
            'process_suggestion_error': 'Fout bij verwerken suggestie',
            'unknown_error': 'Onbekende fout',
            'unknown_model': 'Onbekend model: {model_name}',
            'suggestion_error': 'Suggestiefout',
            'random_question_success': 'Willekeurige vraag succesvol gegenereerd!',
            'book_title_check': 'Boektitel vereist',
            'avoid_repeat_question': 'Gebruik een andere vraag',
            'empty_answer': 'Leeg antwoord',
            'invalid_response': 'Ongeldig antwoord',
            'auth_error_401': 'Niet geautoriseerd',
            'auth_error_403': 'Toegang geweigerd',
            'rate_limit': 'Te veel aanvragen',
            'invalid_json': 'Ongeldige JSON',
            'no_response': 'Geen antwoord',
            'template_error': 'Sjabloonfout',
            'no_model_configured': 'Geen AI-model geconfigureerd. Configureer een AI-model in de instellingen.',
            'random_question_error': 'Fout bij genereren willekeurige vraag',
            'clear_history_failed': 'Geschiedenis wissen mislukt',
            'clear_history_not_supported': 'Geschiedenis wissen voor één boek wordt nog niet ondersteund',
            'missing_required_config': 'Ontbrekende vereiste configuratie: {key}. Controleer uw instellingen.',
            'api_key_too_short': 'API-sleutel is te kort. Controleer en voer de volledige sleutel in.',
            
            # API-responsverwerking
            'api_request_failed': 'API-aanvraag mislukt: {error}',
            'api_content_extraction_failed': 'Kon inhoud niet uit API-antwoord halen',
            'api_invalid_response': 'Geen geldig API-antwoord ontvangen',
            'api_unknown_error': 'Onbekende fout: {error}',
            
            # Streaming-responsverwerking
            'stream_response_code': 'Streaming-antwoord statuscode: {code}',
            'stream_continue_prompt': 'Ga verder met uw vorige antwoord zonder reeds verstrekte inhoud te herhalen.',
            'stream_continue_code_blocks': 'Uw vorige antwoord had onafgesloten codeblokken. Ga verder en voltooi deze codeblokken.',
            'stream_continue_parentheses': 'Uw vorige antwoord had onafgesloten haakjes. Ga verder en zorg ervoor dat alle haakjes correct worden afgesloten.',
            'stream_continue_interrupted': 'Uw vorige antwoord lijkt onderbroken te zijn. Ga verder en voltooi uw laatste gedachte of uitleg.',
            'stream_timeout_error': 'De streaming-overdracht heeft 60 seconden geen nieuwe inhoud ontvangen, mogelijk een verbindingsprobleem.',
            
            # API-foutmeldingen
            'api_version_model_error': 'API-versie of modelnaam fout: {message}\n\nWerk de API-basis-URL bij naar "{base_url}" en het model naar "{model}" of een ander beschikbaar model in de instellingen.',
            'api_format_error': 'API-aanvraagformatfout: {message}',
            'api_key_invalid': 'API-sleutel ongeldig of niet geautoriseerd: {message}\n\nControleer uw API-sleutel en zorg ervoor dat API-toegang is ingeschakeld.',
            'api_rate_limit': 'Aanvraaglimiet overschreden, probeer het later opnieuw\n\nU heeft mogelijk uw gratis gebruiksquotum overschreden. Dit kan te wijten zijn aan:\n1. Te veel aanvragen per minuut\n2. Te veel aanvragen per dag\n3. Te veel invoertokens per minuut',
            
            # Configuratiefouten
            'missing_config_key': 'Ontbrekende vereiste configuratiesleutel: {key}',
            'api_base_url_required': 'API-basis-URL is vereist',
            'model_name_required': 'Modelnaam is vereist',
            'api_key_empty': 'API-sleutel is leeg. Voer een geldige API-sleutel in.',
            
            # Over informatie
            'author_name': 'Sheldon',
            'user_manual': 'Gebruikershandleiding',
            'about_plugin': 'Waarom Ask Grok?',
            'learn_how_to_use': 'Hoe te gebruiken',
            'email': 'iMessage',
            
            # Modelspecifieke configuraties
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Aangepast',
            'model_enable_streaming': 'Streaming inschakelen',
            'model_disable_ssl_verify': 'SSL-verificatie uitschakelen',
            
            # Algemene systeemberichten
            'default_system_message': 'U bent een expert in boekanalyse. Uw taak is om gebruikers te helpen boeken beter te begrijpen door inzichtelijke vragen en analyses te bieden.',
        }
