#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
German language translations for Ask AI Plugin.
"""

from ..models.base import BaseTranslation, TranslationRegistry, AIProvider


@TranslationRegistry.register
class GermanTranslation(BaseTranslation):
    """German language translation."""
    
    @property
    def code(self) -> str:
        return "de"
    
    @property
    def name(self) -> str:
        return "Deutsch"
    
    @property
    def default_template(self) -> str:
        return 'Über das Buch "{title}": Autor: {author}, Verlag: {publisher}, Erscheinungsjahr: {pubyear}, Buch in language: {language}, Reihe: {series}, Meine Frage ist: {query}'
    
    @property
    def suggestion_template(self) -> str:
        return """Sie sind ein Buchexperte. Generieren Sie für das Buch \"{title}\" von {author}, Sprache: {language}, EINE aufschlussreiche Frage, die den Lesern hilft, die Kernideen des Buches, praktische Anwendungen oder einzigartige Perspektiven besser zu verstehen. Regeln: 1. Geben Sie NUR die Frage zurück, ohne Einleitung oder Erklärung 2. Konzentrieren Sie sich auf den Inhalt des Buches, nicht nur auf den Titel 3. Stellen Sie eine praktische und zum Nachdenken anregende Frage 4. Halten Sie es kurz (30-200 Wörter) 5. Seien Sie kreativ und generieren Sie jedes Mal eine andere Frage, auch für dasselbe Buch"""
    
    @property
    def multi_book_default_template(self) -> str:
        return """Hier sind Informationen über mehrere Bücher: {books_metadata} Benutzerfrage: {query} Bitte beantworten Sie die Frage basierend auf den obigen Buchinformationen."""
    
    @property
    def translations(self) -> dict:
        return {
            # Plugin-Informationen
            'plugin_name': 'Ask AI Plugin',
            'plugin_desc': 'Stellen Sie Fragen zu einem Buch mit KI',
            
            # UI - Tabs und Abschnitte
            'config_title': 'Konfiguration',
            'general_tab': 'Allgemein',
            'ai_models': 'KI',
            'shortcuts': 'Tastenkombinationen',
            'about': 'Über',
            'metadata': 'Metadaten',
            
            # UI - Schaltflächen und Aktionen
            'ok_button': 'OK',
            'save_button': 'Speichern',
            'send_button': 'Senden',
            'stop_button': 'Stoppen',
            'suggest_button': 'Zufällige Frage',
            'copy_response': 'Antwort kopieren',
            'copy_question_response': 'F&&A kopieren',
            'export_pdf': 'PDF exportieren',
            'export_current_qa': 'Aktuelles Q&A exportieren',
            'export_history': 'Verlauf exportieren',
            'export_all_history_dialog_title': 'Gesamten Verlauf als PDF exportieren',
            'export_all_history_title': 'GESAMTER Q&A-VERLAUF',
            'export_history_insufficient': 'Mindestens 2 Verlaufseinträge erforderlich zum Exportieren.',
            'history_record': 'Eintrag',
            'question_label': 'Frage',
            'answer_label': 'Antwort',
            'default_ai': 'Standard-KI',
            'export_time': 'Exportiert am',
            'total_records': 'Gesamteinträge',
            'info': 'Information',
            'copied': 'Kopiert!',
            'pdf_exported': 'PDF exportiert!',
            'export_pdf_dialog_title': 'In PDF exportieren',
            'export_pdf_error': 'Fehler beim Exportieren der PDF: {0}',
            'no_question': 'Keine Frage',
            'no_response': 'Keine Antwort',
            'saved': 'Gespeichert',
            'close_button': 'Schließen',
            
            # UI - Konfigurationsfelder
            'token_label': 'API-Schlüssel:',
            'api_key_label': 'API-Schlüssel:',
            'model_label': 'Modell:',
            'language_label': 'Sprache:',
            'language_label_old': 'Sprache',
            'base_url_label': 'Basis-URL:',
            'base_url_placeholder': 'Standard: {default_api_base_url}',
            'shortcut': 'Tastenkombination',
            'shortcut_open_dialog': 'Dialog öffnen',
            'shortcut_enter': 'Strg + Eingabe',
            'shortcut_return': 'Befehl + Rückkehr',
            'using_model': 'Modell',
            'current_ai': 'Aktuelle KI:',
            'action': 'Aktion',
            'reset_button': 'Zurücksetzen',
            'prompt_template': 'Prompt-Vorlage',
            'ask_prompts': 'Frage-Prompts',
            'random_questions_prompts': 'Zufällige Fragen-Prompts',
            'display': 'Anzeige',
            
            # UI - Dialogelemente
            'input_placeholder': 'Geben Sie Ihre Frage ein...',
            'response_placeholder': 'Antwort kommt bald...',
            
            # UI - Menüpunkte
            'menu_title': 'Fragen',
            'menu_ask': 'Frage {model}',
            
            # UI - Statusmeldungen
            'loading': 'Laden...',
            'loading_text': 'Frage stellen',
            'save_success': 'Einstellungen gespeichert',
            'sending': 'Senden...',
            'requesting': 'Anfrage läuft',
            'formatting': 'Anfrage erfolgreich, Formatierung läuft',
            
            # UI - Modellliste-Funktion
            'load_models': 'Modelle laden',
            'use_custom_model': 'Benutzerdefinierten Modellnamen verwenden',
            'custom_model_placeholder': 'Benutzerdefinierten Modellnamen eingeben',
            'model_placeholder': 'Bitte laden Sie zuerst Modelle',
            'models_loaded': '{count} Modelle erfolgreich geladen',
            'load_models_failed': 'Fehler beim Laden der Modelle: {error}',
            'model_list_not_supported': 'Dieser Anbieter unterstützt kein automatisches Abrufen der Modellliste',
            'api_key_required': 'Bitte geben Sie zuerst den API-Schlüssel ein',
            'invalid_params': 'Ungültige Parameter',
            'warning': 'Warnung',
            'success': 'Erfolg',
            'error': 'Fehler',
            
            # Metadatenfelder
            'metadata_title': 'Titel',
            'metadata_authors': 'Autor',
            'metadata_publisher': 'Verlag',
            'metadata_pubyear': 'Veröffentlichungsdatum',
            'metadata_language': 'Sprache',
            'metadata_series': 'Reihe',
            'no_metadata': 'Keine Metadaten',
            'no_series': 'Keine Reihe',
            'unknown': 'Unbekannt',

            # Multi-book feature
            'books_unit': ' Bücher',
            'new_conversation': 'Neue Unterhaltung',
            'single_book': 'Einzelnes Buch',
            'multi_book': 'Mehrere Bücher',
            'deleted': 'Gelöscht',
            'history': 'Verlauf',
            'no_history': 'Keine Verlaufseinträge',
            'clear_current_book_history': 'Verlauf des aktuellen Buches löschen',
            'confirm_clear_book_history': 'Möchten Sie wirklich den gesamten Verlauf für folgende Bücher löschen?\n{book_titles}',
            'confirm': 'Bestätigen',
            'history_cleared': '{deleted_count} Verlaufseinträge gelöscht.',
            'multi_book_template_label': 'Prompt-Vorlage für mehrere Bücher:',
            'multi_book_placeholder_hint': 'Verwenden Sie {books_metadata} für Buchinformationen, {query} für die Benutzerfrage',
            
            # Fehlermeldungen
            'error': 'Fehler: ',
            'network_error': 'Verbindungsfehler',
            'request_timeout': 'Anfrage-Timeout',
            'request_failed': 'Anfrage fehlgeschlagen',
            'question_too_long': 'Frage zu lang',
            'auth_token_required_title': 'API-Schlüssel erforderlich',
            'auth_token_required_message': 'Bitte API-Schlüssel in der Plugin-Konfiguration festlegen.',
            'error_preparing_request': 'Fehler bei der Anfragevorbereitung',
            'empty_suggestion': 'Leerer Vorschlag',
            'process_suggestion_error': 'Fehler bei der Vorschlagsverarbeitung',
            'unknown_error': 'Unbekannter Fehler',
            'unknown_model': 'Unbekanntes Modell: {model_name}',
            'suggestion_error': 'Vorschlagsfehler',
            'random_question_success': 'Zufällige Frage erfolgreich generiert!',
            'book_title_check': 'Buchtitel erforderlich',
            'avoid_repeat_question': 'Bitte verwenden Sie eine andere Frage',
            'empty_answer': 'Leere Antwort',
            'invalid_response': 'Ungültige Antwort',
            'auth_error_401': 'Nicht autorisiert',
            'auth_error_403': 'Zugriff verweigert',
            'rate_limit': 'Zu viele Anfragen',
            'invalid_json': 'Ungültiges JSON',
            'no_response': 'Keine Antwort',
            'template_error': 'Vorlagenfehler',
            'no_model_configured': 'Kein KI-Modell konfiguriert. Bitte konfigurieren Sie ein KI-Modell in den Einstellungen.',
            'random_question_error': 'Fehler beim Generieren einer zufälligen Frage',
            'clear_history_failed': 'Löschen des Verlaufs fehlgeschlagen',
            'clear_history_not_supported': 'Löschen des Verlaufs für ein einzelnes Buch wird noch nicht unterstützt',
            'missing_required_config': 'Fehlende erforderliche Konfiguration: {key}. Bitte überprüfen Sie Ihre Einstellungen.',
            'api_key_too_short': 'API-Schlüssel ist zu kurz. Bitte überprüfen Sie und geben Sie den vollständigen Schlüssel ein.',
            
            # API-Antwortverarbeitung
            'api_request_failed': 'API-Anfrage fehlgeschlagen: {error}',
            'api_content_extraction_failed': 'Inhalt konnte nicht aus der API-Antwort extrahiert werden',
            'api_invalid_response': 'Keine gültige API-Antwort erhalten',
            'api_unknown_error': 'Unbekannter Fehler: {error}',
            
            # Streaming-Antwortverarbeitung
            'stream_response_code': 'Streaming-Antwort-Statuscode: {code}',
            'stream_continue_prompt': 'Bitte setzen Sie Ihre vorherige Antwort fort, ohne bereits bereitgestellte Inhalte zu wiederholen.',
            'stream_continue_code_blocks': 'Ihre vorherige Antwort hatte ungeschlossene Code-Blöcke. Bitte fahren Sie fort und vervollständigen Sie diese Code-Blöcke.',
            'stream_continue_parentheses': 'Ihre vorherige Antwort hatte ungeschlossene Klammern. Bitte fahren Sie fort und stellen Sie sicher, dass alle Klammern ordnungsgemäß geschlossen sind.',
            'stream_continue_interrupted': 'Ihre vorherige Antwort scheint unterbrochen worden zu sein. Bitte fahren Sie fort und vervollständigen Sie Ihren letzten Gedanken oder Ihre Erklärung.',
            'stream_timeout_error': 'Die Streaming-Übertragung hat 60 Sekunden lang keine neuen Inhalte erhalten, möglicherweise ein Verbindungsproblem.',
            
            # API-Fehlermeldungen
            'api_version_model_error': 'API-Version oder Modellname-Fehler: {message}\n\nBitte aktualisieren Sie die API-Basis-URL auf "{base_url}" und das Modell auf "{model}" oder ein anderes verfügbares Modell in den Einstellungen.',
            'api_format_error': 'API-Anforderungsformatfehler: {message}',
            'api_key_invalid': 'API-Schlüssel ungültig oder nicht autorisiert: {message}\n\nBitte überprüfen Sie Ihren API-Schlüssel und stellen Sie sicher, dass der API-Zugriff aktiviert ist.',
            'api_rate_limit': 'Anfragelimit überschritten, bitte versuchen Sie es später erneut\n\nSie haben möglicherweise das kostenlose Nutzungskontingent überschritten. Dies könnte auf Folgendes zurückzuführen sein:\n1. Zu viele Anfragen pro Minute\n2. Zu viele Anfragen pro Tag\n3. Zu viele Eingabe-Tokens pro Minute',
            
            # Konfigurationsfehler
            'missing_config_key': 'Fehlender erforderlicher Konfigurationsschlüssel: {key}',
            'api_base_url_required': 'API-Basis-URL ist erforderlich',
            'model_name_required': 'Modellname ist erforderlich',
            'api_key_empty': 'API-Schlüssel ist leer. Bitte geben Sie einen gültigen API-Schlüssel ein.',
            
            # Modellliste abrufen
            'fetching_models_from': 'Modelle werden von {url} abgerufen',
            'successfully_fetched_models': '{count} {provider}-Modelle erfolgreich abgerufen',
            'failed_to_fetch_models': 'Fehler beim Abrufen der Modelle: {error}',
            
            # Über Informationen
            'author_name': 'Sheldon',
            'user_manual': 'Benutzerhandbuch',
            'about_plugin': 'Warum Ask AI Plugin?',
            'learn_how_to_use': 'Nutzungsanleitung',
            'email': 'iMessage',
            
            # Modellspezifische Konfigurationen
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Benutzerdefiniert',
            'model_enable_streaming': 'Streaming aktivieren',
            'model_disable_ssl_verify': 'SSL-Verifizierung deaktivieren',

            # AI Switcher
            'current_ai': 'Aktuelle KI',
            'no_configured_models': 'Keine KI konfiguriert - Bitte in den Einstellungen konfigurieren',
            
            # Provider specific info
            'nvidia_free_info': '💡 Neue Benutzer erhalten 6 Monate kostenlosen API-Zugang - Keine Kreditkarte erforderlich',
            
            # Common system messages
            'default_system_message': 'Sie sind ein Experte für Buchanalysen. Ihre Aufgabe ist es, Benutzern zu helfen, Bücher besser zu verstehen, indem Sie aufschlussreiche Fragen und Analysen bereitstellen.',

            # Request timeout settings
            'request_timeout_label': 'Anfrage-Timeout:',
            'seconds': 'Sekunden',
            'request_timeout_error': 'Anfrage-Timeout. Aktuelles Timeout: {timeout} Sekunden',
            
            # Parallel AI settings
            'parallel_ai_count_label': 'Anzahl paralleler KIs:',
            'parallel_ai_count_tooltip': 'Anzahl der gleichzeitig abzufragenden KI-Modelle (1-2 verfügbar, 3-4 in Kürze)',
            'parallel_ai_notice': 'Hinweis: Dies betrifft nur das Senden von Fragen. Zufällige Fragen verwenden immer eine einzelne KI.',
            'suggest_maximize': 'Tipp: Maximieren Sie das Fenster für eine bessere Ansicht mit 3 KIs',
            'ai_panel_label': 'KI {index}:',
            'no_ai_available': 'Keine KI für dieses Panel verfügbar',
            'add_more_ai_providers': 'Bitte fügen Sie weitere KI-Anbieter in den Einstellungen hinzu',
            'select_ai': '-- KI auswählen --',
            'coming_soon': 'Demnächst verfügbar',
            'advanced_feature_tooltip': 'Diese Funktion befindet sich in der Entwicklung. Bleiben Sie dran für Updates!',
            
            # PDF export section titles
            'pdf_book_metadata': 'BUCHMETADATEN',
            'pdf_question': 'FRAGE',
            'pdf_answer': 'ANTWORT',
            'pdf_ai_model_info': 'KI-MODELL-INFORMATIONEN',
            'pdf_generated_by': 'GENERIERET VON',
            'pdf_provider': 'Anbieter',
            'pdf_model': 'Modell',
            'pdf_api_base_url': 'API-Basis-URL',
            'pdf_panel': 'Panel',
            'pdf_plugin': 'Plugin',
            'pdf_github': 'GitHub',
            'pdf_software': 'Software',
            'pdf_generated_time': 'Generierte Zeit',
            'pdf_info_not_available': 'Informationen nicht verfügbar',
        }