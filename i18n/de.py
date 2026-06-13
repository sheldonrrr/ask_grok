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
        return 'Kontext: Sie unterstützen einen Benutzer von calibre (http://calibre-ebook.com), einer leistungsstarken E-Book-Verwaltungsanwendung, über das "Ask AI Plugin". Dieses Plugin ermöglicht es Benutzern, Fragen zu Büchern in ihrer calibre-Bibliothek zu stellen. Hinweis: Dieses Plugin kann nur Fragen zum Inhalt, zu Themen oder verwandten Themen des ausgewählten Buches beantworten - es kann Buchmetadaten nicht direkt ändern oder calibre-Operationen ausführen. Buchinformationen: Titel: "{title}", Autor: {author}, Verlag: {publisher}, Erscheinungsjahr: {pubyear}, Sprache: {language}, Reihe: {series}. Benutzerfrage: {query}. Bitte geben Sie eine hilfreiche Antwort basierend auf den Buchinformationen und Ihrem Wissen.'
    
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
            'shortcuts_note': "Sie können diese Tastenkombinationen in calibre anpassen: Einstellungen -> Tastenkombinationen (Suche nach 'Ask AI').\nDiese Seite zeigt die Standard-/Beispiel-Tastenkombinationen. Wenn Sie sie in den Tastenkombinationen geändert haben, haben die calibre-Einstellungen Vorrang.",
            'prompts_tab': 'Prompts',
            'about': 'Über',
            'metadata': 'Metadaten',
            
            # Abschnittsuntertitel
            'language_settings': 'Sprache',
            'language_subtitle': 'Wählen Sie Ihre bevorzugte Oberflächensprache',
            'ai_providers_subtitle': 'KI-Anbieter konfigurieren und Standard-KI auswählen',
            'prompts_subtitle': 'Anpassen, wie Fragen an die KI gesendet werden',
            'export_settings_subtitle': 'Standardordner für PDF-Export festlegen',
            'reset_all_data_subtitle': 'Warnung: Dies löscht dauerhaft alle Ihre Einstellungen und Daten',
            
            # Prompts-Tab
            'language_preference_title': 'Sprachpräferenz',
            'language_preference_subtitle': 'Steuern Sie, ob KI-Antworten mit Ihrer Oberflächensprache übereinstimmen sollen',
            'prompt_templates_title': 'Prompt-Vorlagen',
            'prompt_templates_subtitle': 'Passen Sie an, wie Buchinformationen mit dynamischen Feldern wie {title}, {author}, {query} an die KI gesendet werden',
            'ask_prompts': 'Frage-Prompts',
            'random_questions_prompts': 'Zufällige Fragen-Prompts',
            'multi_book_prompts_label': 'Mehrere Bücher-Prompts',
            'multi_book_placeholder_hint': 'Verwenden Sie {books_metadata} für Buchinformationen, {query} für Benutzerfrage',
            'dynamic_fields_title': 'Dynamische Felder-Referenz',
            'dynamic_fields_subtitle': 'Verfügbare Felder und Beispielwerte aus "Frankenstein" von Mary Shelley',
            'dynamic_fields_examples': '<b>{title}</b> → Frankenstein<br><b>{author}</b> → Mary Shelley<br><b>{publisher}</b> → Lackington, Hughes, Harding, Mavor & Jones<br><b>{pubyear}</b> → 1818<br><b>{language}</b> → English<br><b>{series}</b> → (keine)<br><b>{query}</b> → Ihr Fragetext',
            'reset_prompts': 'Prompts auf Standard zurücksetzen',
            'reset_prompts_confirm': 'Möchten Sie wirklich alle Prompt-Vorlagen auf ihre Standardwerte zurücksetzen? Diese Aktion kann nicht rückgängig gemacht werden.',
            'unsaved_changes_title': 'Nicht gespeicherte Änderungen',
            'unsaved_changes_message': 'Sie haben nicht gespeicherte Änderungen im Prompts-Tab. Möchten Sie diese speichern?',
            'use_interface_language': 'KI immer bitten, in der aktuellen Plugin-Oberflächensprache zu antworten',
            'language_instruction_label': 'Zu Prompts hinzugefügte Sprachanweisung:',
            'language_instruction_text': 'Bitte antworten Sie auf {language_name}.',
            
            # Persona-Einstellungen
            'persona_title': 'Persona',
            'persona_subtitle': 'Definieren Sie Ihren Forschungshintergrund und Ihre Ziele, um der KI zu helfen, relevantere Antworten zu geben',
            'use_persona': 'Persona verwenden',
            'persona_label': 'Persona',
            'persona_placeholder': 'Als Forscher möchte ich durch Buchdaten recherchieren.',
            'persona_hint': 'Je mehr die KI über Ihr Ziel und Ihren Hintergrund weiß, desto besser die Recherche oder Generierung.',
            
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
            
            # Export-Einstellungen
            'export_settings': 'Export-Einstellungen',
            'enable_default_export_folder': 'In Standardordner exportieren',
            'no_folder_selected': 'Kein Ordner ausgewählt',
            'browse': 'Durchsuchen...',
            'select_export_folder': 'Export-Ordner auswählen',
            
            # Schaltflächentext und Menüelemente
            'copy_response_btn': 'Antwort kopieren',
            'copy_qa_btn': 'F&A kopieren',
            'export_current_btn': 'F&A als PDF exportieren',
            'export_history_btn': 'Verlauf als PDF exportieren',
            'copy_mode_response': 'Antwort',
            'copy_mode_qa': 'F&A',
            'copy_format_plain': 'Klartext',
            'copy_format_markdown': 'Markdown',
            'export_mode_current': 'Aktuelles F&A',
            'export_mode_history': 'Verlauf',
            
            # PDF-Export bezogen
            'model_provider': 'Anbieter',
            'model_name': 'Modell',
            'model_api_url': 'API-Basis-URL',
            'pdf_model_info': 'KI-Modell-Informationen',
            'pdf_software': 'Software',
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
            'yes': 'Ja',
            'no': 'Nein',
            'no_book_selected_title': 'Kein Buch Ausgewählt',
            'no_book_selected_message': 'Bitte wählen Sie zuerst ein Buch aus, bevor Sie Fragen stellen.',
            'set_default_ai_title': 'Standard-KI Festlegen',
            'set_default_ai_message': 'Sie haben zu "{0}" gewechselt. Möchten Sie diese als Standard-KI für zukünftige Anfragen festlegen?',
            'set_default_ai_success': 'Standard-KI wurde auf "{0}" festgelegt.',
            'default_ai_mismatch_title': 'Standard-KI Geändert',
            'default_ai_mismatch_message': 'Die Standard-KI in der Konfiguration wurde auf "{default_ai}" geändert,\naber der aktuelle Dialog verwendet "{current_ai}".\n\nMöchten Sie zur neuen Standard-KI wechseln?',
            'copied': 'Kopiert!',
            'pdf_exported': 'PDF exportiert!',
            'export_pdf_dialog_title': 'In PDF exportieren',
            'export_pdf_error': 'Fehler beim Exportieren der PDF: {0}',
            'no_question': 'Keine Frage',
            'no_response': 'Keine Antwort',
            'saved': 'Gespeichert',
            'close_button': 'Schließen',
            'open_local_tutorial': 'Lokales Tutorial öffnen',
            'tutorial_open_failed': 'Tutorial konnte nicht geöffnet werden',
            'tutorial': 'Tutorial',

            'model_display_name_perplexity': 'Perplexity',
            
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
            'menu_ask': 'Frage',
            
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
            'error_opening_dialog': 'Fehler beim Öffnen des Dialogs:',
            'skipped_books_warning': '{count} Buch/Bücher wurden aufgrund von Dateizugriffsfehlern übersprungen.\nDies kann durch ungültige Zeichen in Dateipfaden oder durch von anderen Programmen gesperrte Dateien verursacht werden.',
            'failed_to_read_all_books': 'Metadaten für alle ausgewählten Bücher konnten nicht gelesen werden.\nDies kann durch ungültige Zeichen in Dateipfaden oder durch von anderen Programmen gesperrte Dateien verursacht werden.',
            'error_starting_request': 'Fehler beim Starten der Anfrage',
            'default_ai_mismatch_title': 'Standard-KI geändert',
            'default_ai_mismatch_message': 'Die Standard-KI in der Konfiguration wurde auf "{default_ai}" geändert,\naber die aktuelle Konversation verwendet "{current_ai}".\n\nMöchten Sie zur neuen Standard-KI wechseln?',
            
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
            'empty_question_placeholder': '(Keine Frage)',
            'history_ai_unavailable': 'Diese KI wurde aus der Konfiguration entfernt',
            'clear_current_book_history': 'Verlauf des aktuellen Buches löschen',
            'confirm_clear_book_history': 'Möchten Sie wirklich den gesamten Verlauf für folgende Bücher löschen?\n{book_titles}',
            'confirm': 'Bestätigen',
            'history_cleared': '{deleted_count} Verlaufseinträge gelöscht.',
            'multi_book_template_label': 'Prompt-Vorlage für mehrere Bücher:',
            'multi_book_placeholder_hint': 'Verwenden Sie {books_metadata} für Buchinformationen, {query} für die Benutzerfrage',
            
            # Fehlermeldungen
            'network_error': 'Verbindungsfehler',
            'request_timeout': 'Anfrage-Timeout',
            'request_failed': 'Anfrage fehlgeschlagen',
            'request_stopped': 'Anfrage gestoppt',
            'question_too_long': 'Frage zu lang',
            'question_too_long_detail': (
                'Prompt ist zu lang ({current} Zeichen, Limit {limit}, um {over} zu lang). '
                'Sie haben {book_count} Buch/Bücher ausgewählt.'
            ),
            'question_too_long_detail_library': (
                'Prompt ist zu lang ({current} Zeichen, Limit {limit}, um {over} zu lang). '
                'Ihr Bibliotheksindex enthält {book_count} Buch/Bücher.'
            ),
            'question_too_long_hint_ai_search': (
                'Für bibliotheksweite Suchen verwenden Sie AI Search (fragen ohne Bücher '
                'auszuwählen oder über das AI-Search-Menü), statt viele Bücher auszuwählen.'
            ),
            'question_too_long_hint_library_search': (
                'Ihr Bibliotheksindex überschreitet das aktuelle Prompt-Limit. Aktivieren Sie '
                '„Benutzerdefiniertes Prompt-Längenlimit“ unter Plugin-Konfiguration → General '
                '(Vorschlag: 524288 Zeichen), oder stellen Sie eine spezifischere Frage.'
            ),
            'question_too_long_reduce_books': (
                'Für einen tieferen Vergleich weniger Bücher versuchen Sie, etwa {count} '
                'Buch/Bücher abzuwählen.'
            ),
            'question_too_long_hint_default': (
                'Aktuelles Standardlimit: {limit} Zeichen ({mode}). '
                'Standard für ein Buch: 128.000; für mehrere Bücher: 256.000. '
                'Fortgeschrittene können ein benutzerdefiniertes Limit unter '
                'Plugin-Konfiguration → General aktivieren.'
            ),
            'question_too_long_hint_custom': (
                'Sie haben ein benutzerdefiniertes Prompt-Limit aktiviert. Bei Timeouts senken '
                'Sie das Limit unter Plugin-Konfiguration → General, wählen weniger Bücher '
                'aus oder stellen eine spezifischere Frage.'
            ),
            'large_selection_dialog_title': 'Viele Bücher ausgewählt',
            'large_selection_dialog_message': (
                'Sie haben {count} Bücher ausgewählt. Für bibliotheksweite Fragen eignet sich '
                'AI Search besser und durchsucht Ihre gesamte Bibliothek mit kompakten Metadaten.\n\n'
                'Zu AI Search wechseln oder mit den ausgewählten Büchern im Kompaktformat fortfahren?'
            ),
            'large_selection_use_ai_search': 'AI Search verwenden',
            'large_selection_continue': 'Mit Auswahl fortfahren',
            'multi_book_truncation_note': (
                'Hinweis: Aufgrund des Prompt-Limits sind nur die ersten {included} von {total} '
                'ausgewählten Büchern enthalten. Verwenden Sie AI Search für die gesamte '
                'Bibliothek oder erhöhen Sie das benutzerdefinierte Limit unter '
                'Plugin-Konfiguration → General.'
            ),
            'library_metadata_truncation_note': (
                'Hinweis: Aufgrund des Prompt-Limits sind nur die ersten {included} von {total} '
                'indizierten Büchern enthalten. Ergebnisse können bei sehr großen Bibliotheken '
                'unvollständig sein, sofern Sie das benutzerdefinierte Limit unter '
                'Plugin-Konfiguration → General nicht erhöhen.'
            ),
            'auth_token_required_title': 'API-Schlüssel erforderlich',
            'auth_token_required_message': 'Bitte API-Schlüssel in der Plugin-Konfiguration festlegen.',
            'open_configuration': 'Konfiguration öffnen',
            'cancel': 'Abbrechen',
            'yes_button': 'Ja',
            'no_button': 'Nein',
            'cancel_button': 'Abbrechen',
            "invalid_default_ai_title": "Ungültige Standard-KI",
            "invalid_default_ai_message": "Die Standard-KI \"{default_ai}\" ist nicht richtig konfiguriert.\n\nMöchten Sie stattdessen zu \"{first_ai}\" wechseln?",
            "switch_to_ai": "Wechseln zu {ai}",
            "keep_current": "Aktuell Beibehalten",
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
            'template_error': 'Vorlagenfehler',
            'no_model_configured': 'Kein KI-Modell konfiguriert. Bitte konfigurieren Sie ein KI-Modell in den Einstellungen.',
            'no_ai_configured_title': 'Keine KI konfiguriert',
            'no_ai_configured_message': 'Willkommen! Um Fragen zu Ihren Büchern zu stellen, müssen Sie zuerst einen KI-Anbieter konfigurieren.\n\nGute Nachricht: Dieses Plugin bietet jetzt einen KOSTENLOSEN Zugang (Nvidia AI Free), den Sie sofort ohne Konfiguration nutzen können!\n\nWeitere empfohlene Optionen:\n• Nvidia AI - 6 Monate KOSTENLOSER API-Zugang mit nur Ihrer Telefonnummer (keine Kreditkarte erforderlich)\n• Ollama - KI-Modelle lokal auf Ihrem Computer ausführen (völlig kostenlos und privat)\n\nMöchten Sie jetzt die Plugin-Konfiguration öffnen, um einen KI-Anbieter einzurichten?',
            'open_settings': 'Plugin-Konfiguration',
            'ask_anyway': 'Trotzdem fragen',
            'later': 'Später',
            'reset_all_data': 'Alle Daten zurücksetzen',
            'reset_all_data_warning': 'Dies löscht alle API-Schlüssel, Prompt-Vorlagen und lokale Verlaufseinträge. Ihre Spracheinstellung wird beibehalten. Bitte vorsichtig vorgehen.',
            'reset_all_data_confirm_title': 'Zurücksetzen bestätigen',
            'reset_all_data_confirm_message': 'Sind Sie sicher, dass Sie das Plugin auf den Ausgangszustand zurücksetzen möchten?\n\nDies löscht dauerhaft:\n• Alle API-Schlüssel\n• Alle benutzerdefinierten Prompt-Vorlagen\n• Alle Gesprächsverläufe\n• Alle Plugin-Einstellungen (Spracheinstellung wird beibehalten)\n\nDiese Aktion kann nicht rückgängig gemacht werden!',
            'reset_all_data_success': 'Alle Plugin-Daten wurden erfolgreich zurückgesetzt. Bitte starten Sie calibre neu, damit die Änderungen wirksam werden.',
            'reset_all_data_failed': 'Fehler beim Zurücksetzen der Plugin-Daten: {error}',
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
            
            # AI Switcher
            'no_configured_models': 'Keine KI konfiguriert - Bitte in den Einstellungen konfigurieren',
            
            # Provider specific info
            'nvidia_free_info': '💡 Neue Benutzer erhalten 6 Monate kostenlosen API-Zugang - Keine Kreditkarte erforderlich',
            
            # Common system messages
            'default_system_message': 'Sie sind ein Experte für Buchanalysen. Ihre Aufgabe ist es, Benutzern zu helfen, Bücher besser zu verstehen, indem Sie aufschlussreiche Fragen und Analysen bereitstellen.',

            # Request timeout settings
            'request_timeout_label': 'Anfrage-Timeout:',
            'seconds': 'Sekunden',
            'request_timeout_error': 'Anfrage-Timeout. Aktuelles Timeout: {timeout} Sekunden',
            'enable_custom_prompt_limit_label': 'Benutzerdefiniertes Prompt-Längenlimit',
            'enable_custom_prompt_limit_tooltip': (
                'Standardlimits sind 128.000 Zeichen (ein Buch) und 256.000 (mehrere Bücher). '
                'Die meisten Benutzer müssen dies nicht ändern. Für bibliotheksweite Suchen '
                'verwenden Sie AI Search. Aktivieren Sie ein benutzerdefiniertes Limit nur, wenn '
                'Ihr Modell einen deutlich größeren Kontext unterstützt und Anfragen weiterhin '
                'am Limit scheitern.'
            ),
            'max_prompt_length_label': 'Max. Prompt-Länge:',
            'max_prompt_length_unit': 'Zeichen',
            'max_prompt_length_tooltip': (
                'Gilt, wenn das benutzerdefinierte Limit aktiviert ist. Standardvorschlag: '
                '524288 Zeichen. Grobe Regel: 1 Token ≈ 3–4 Zeichen. Bei Ollama auch num_ctx '
                'auf der Modellseite setzen.'
            ),
            
            # Parallel AI settings
            'parallel_ai_count_label': 'Anzahl paralleler KIs:',
            'parallel_ai_count_tooltip': 'Anzahl der gleichzeitig abzufragenden KI-Modelle (1-2 verfügbar, 3-4 in Kürze)',
            'parallel_ai_notice': 'Hinweis: Dies betrifft nur das Senden von Fragen. Zufällige Fragen verwenden immer eine einzelne KI.',
            'suggest_maximize': 'Tipp: Maximieren Sie das Fenster für eine bessere Ansicht mit 3 KIs',
            'ai_panel_label': 'KI {index}:',
            'no_ai_available': 'Keine KI für dieses Panel verfügbar',
            'add_more_ai_providers': 'Bitte fügen Sie weitere KI-Anbieter in den Einstellungen hinzu',
            'select_ai': '-- KI auswählen --',
            'select_model': '-- Modell wechseln --',
            'request_model_list': 'Bitte Modellliste anfordern',
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
            'pdf_generated_time': 'Erstellungszeit',
            'discard_changes': 'Änderungen Verwerfen',
            'empty_response': 'Leere Antwort von API erhalten',
            'empty_response_after_filter': 'Antwort ist nach dem Filtern von Think-Tags leer',
            'error_401': 'API-Schlüssel-Authentifizierung fehlgeschlagen. Bitte prüfen: API-Schlüssel ist korrekt, Konto hat ausreichendes Guthaben, API-Schlüssel ist nicht abgelaufen.',
            'error_403': 'Zugriff verweigert. Bitte prüfen: API-Schlüssel hat ausreichende Berechtigungen, keine regionalen Zugriffsbeschränkungen.',
            'error_404': 'API-Endpunkt nicht gefunden. Bitte prüfen Sie, ob die API-Basis-URL-Konfiguration korrekt ist.',
            'error_429': 'Zu viele Anfragen, Ratenlimit erreicht. Bitte versuchen Sie es später erneut.',
            'error_5xx': 'Serverfehler. Bitte versuchen Sie es später erneut oder prüfen Sie den Status des Dienstanbieters.',
            'error_network': 'Netzwerkverbindung fehlgeschlagen. Bitte prüfen Sie Netzwerkverbindung, Proxy-Einstellungen oder Firewall-Konfiguration.',
            'error_unknown': 'Unbekannter Fehler.',
            'gemini_geo_restriction': 'Gemini API ist in Ihrer Region nicht verfügbar. Bitte versuchen Sie:\n1. VPN verwenden, um von einer unterstützten Region aus zu verbinden\n2. Andere KI-Anbieter verwenden (OpenAI, Anthropic, DeepSeek usw.)\n3. Google AI Studio für Regionsverfügbarkeit prüfen',
            'load_models_list': 'Modellliste Laden',
            'loading_models_text': 'Modelle werden geladen',
            'model_test_success': 'Modelltest erfolgreich!',
            'models_loaded_with_selection': '{count} Modelle erfolgreich geladen.\nAusgewähltes Modell: {model}',
            'ollama_model_not_available': 'Modell "{model}" ist nicht verfügbar. Bitte prüfen:\n1. Ist das Modell gestartet? Ausführen: ollama run {model}\n2. Ist der Modellname korrekt?\n3. Ist das Modell heruntergeladen? Ausführen: ollama pull {model}',
            'ollama_service_not_running': 'Ollama-Dienst läuft nicht. Bitte starten Sie zuerst den Ollama-Dienst.',
            'ollama_service_timeout': 'Ollama-Dienst-Verbindungszeitüberschreitung. Bitte prüfen Sie, ob der Dienst ordnungsgemäß läuft.',
            'reset_ai_confirm_message': '{ai_name} wird auf den Standardzustand zurückgesetzt.\n\nDies wird löschen:\n• API-Schlüssel\n• Benutzerdefinierter Modellname\n• Andere konfigurierte Parameter\n\nFortfahren?',
            'reset_ai_confirm_title': 'Zurücksetzen Bestätigen',
            'reset_current_ai': 'Aktuelle KI auf Standard Zurücksetzen',
            'reset_tooltip': 'Aktuelle KI auf Standardwerte zurücksetzen',
            'save_and_close': 'Speichern und Schließen',
            'skip': 'Überspringen',
            'technical_details': 'Technische Details',
            'test_current_model': 'Aktuelles Modell Testen',
            'test_model_button': 'Modell Testen',
            'test_model_prompt': 'Modelle erfolgreich geladen! Möchten Sie das ausgewählte Modell "{model}" testen?',
            'unsaved_changes_message': 'Sie haben ungespeicherte Änderungen. Was möchten Sie tun?',
            'unsaved_changes_title': 'Ungespeicherte Änderungen',


            'pdf_info_not_available': 'Informationen nicht verfügbar',
            
            # Field descriptions
            'api_key_desc': 'Ihr API-Schlüssel für die Authentifizierung. Halten Sie ihn sicher und teilen Sie ihn nicht.',
            'base_url_desc': 'Die API-Endpunkt-URL. Verwenden Sie die Standardeinstellung, es sei denn, Sie haben einen benutzerdefinierten Endpunkt.',
            'model_desc': 'Wählen Sie ein Modell aus der Liste oder verwenden Sie einen benutzerdefinierten Modellnamen.',
            'streaming_desc': 'Aktivieren Sie Echtzeit-Antwort-Streaming für schnelleres Feedback.',
            'advanced_section': 'Erweitert',
            
            # Provider-specific notices
            'perplexity_model_notice': 'Hinweis: Perplexity bietet keine öffentliche Modelllisten-API, daher sind die Modelle fest codiert.',
            'ollama_no_api_key_notice': 'Hinweis: Ollama ist ein lokales Modell und benötigt keinen API-Schlüssel.',
            'nvidia_free_credits_notice': 'Hinweis: Neue Benutzer erhalten kostenlose API-Credits - keine Kreditkarte erforderlich.',
            
            # Nvidia Free Fehlermeldungen
            'free_tier_rate_limit': 'Ratenlimit für kostenlosen Zugang überschritten. Bitte versuchen Sie es später erneut oder konfigurieren Sie Ihren eigenen Nvidia API-Schlüssel.',
            'free_tier_unavailable': 'Kostenloser Zugang ist vorübergehend nicht verfügbar. Bitte versuchen Sie es später erneut oder konfigurieren Sie Ihren eigenen Nvidia API-Schlüssel.',
            'free_tier_server_error': 'Serverfehler beim kostenlosen Zugang. Bitte versuchen Sie es später erneut.',
            'free_tier_error': 'Fehler beim kostenlosen Zugang',
            
            # Nvidia Free Anbieterinformationen
            'free': 'Kostenlos',
            'nvidia_free_provider_name': 'Nvidia AI (Kostenlos)',
            'nvidia_free_display_name': 'Nvidia AI (Kostenlos)',
            'nvidia_free_api_key_info': 'Wird vom Server abgerufen',
            'nvidia_free_desc': 'Dieser Dienst wird vom Entwickler gepflegt und bleibt kostenlos, kann aber weniger stabil sein. Für einen stabileren Dienst konfigurieren Sie bitte Ihren eigenen Nvidia API-Schlüssel.',
            
            # Nvidia Free Erstnutzungserinnerung
            'nvidia_free_first_use_title': 'Willkommen beim Ask AI Plugin',
            'nvidia_free_first_use_message': 'Sie können jetzt ohne Konfiguration Fragen stellen! Der Entwickler stellt Ihnen einen kostenlosen Zugang zur Verfügung, der jedoch möglicherweise nicht sehr stabil ist. Viel Spaß!\n\nSie können in den Einstellungen Ihre eigenen KI-Anbieter konfigurieren, um eine bessere Stabilität zu erzielen.',
            
            # Model buttons
            'refresh_model_list': 'Aktualisieren',
            'testing_text': 'Testen',
            'refresh_success': 'Modellliste erfolgreich aktualisiert.',
            'refresh_failed': 'Aktualisierung der Modellliste fehlgeschlagen.',
            'test_failed': 'Modelltest fehlgeschlagen.',
            
            # Tooltip
            'manage_ai_disabled_tooltip': 'Bitte fügen Sie zuerst einen KI-Anbieter hinzu.',

            # AI Search Version 1.4.2
            'library_tab': 'Suche',
            'library_search': 'KI-Suche',
            'library_info': 'KI-Suche ist immer aktiviert. Wenn Sie keine Bücher auswählen, können Sie Ihre gesamte Bibliothek mit natürlicher Sprache durchsuchen.',
            'library_enable': 'KI-Suche aktivieren',
            'library_enable_tooltip': 'Wenn aktiviert, können Sie Ihre Bibliothek mithilfe von KI durchsuchen, wenn keine Bücher ausgewählt sind',
            'library_update': 'Bibliotheksdaten aktualisieren',
            'library_update_tooltip': 'Buchtitel und Autoren aus Ihrer Bibliothek extrahieren',
            'library_updating': 'Aktualisierung...',
            'library_status': 'Status: {count} Bücher, letzte Aktualisierung: {time}',
            'library_status_empty': 'Status: Keine Daten. Klicken Sie auf "Bibliotheksdaten aktualisieren", um zu beginnen.',
            'library_status_error': 'Status: Fehler beim Laden der Daten',
            'library_update_success': 'Erfolgreich {count} Bücher aktualisiert',
            'library_update_failed': 'Bibliotheksdaten konnten nicht aktualisiert werden',
            'library_no_gui': 'GUI nicht verfügbar',
            'library_init_title': 'KI-Suche initialisieren',
            'library_init_message': 'Die KI-Suche benötigt Bibliotheks-Metadaten, um zu funktionieren. Möchten Sie diese jetzt initialisieren?\n\nDadurch werden Buchtitel und Autoren aus Ihrer Bibliothek extrahiert.',
            'library_init_required': 'Die KI-Suche kann ohne Bibliotheksdaten nicht aktiviert werden. Bitte klicken Sie auf "Bibliotheksdaten aktualisieren", wenn Sie bereit sind, diese Funktion zu nutzen.',
            'ai_search_welcome_title': 'Willkommen zur KI-Suche',
            'ai_search_welcome_message': 'KI-Suche ist aktiviert!\n\nAuslösemethoden:\n• Tastenkürzel (in den Einstellungen anpassbar)\n• Extras-Menü → KI-Suche\n• Ask-Dialog öffnen ohne Bücher auszuwählen\n\nSie können Ihre gesamte Bibliothek mit natürlicher Sprache durchsuchen. Zum Beispiel:\n• "Hast du Bücher über Python?"\n• "Zeig mir Bücher von Isaac Asimov"\n• "Finde Bücher über maschinelles Lernen"\n\nDie KI durchsucht Ihre Bibliothek und empfiehlt relevante Bücher. Klicken Sie auf Buchtitel, um sie direkt zu öffnen.',
            'ai_search_not_enough_books_title': 'Nicht genügend Bücher',
            'ai_search_not_enough_books_message': 'Die KI-Suche erfordert mindestens {min_books} Bücher in Ihrer Bibliothek.\n\nIhre aktuelle Bibliothek enthält nur {book_count} Buch/Bücher.\n\nBitte fügen Sie mehr Bücher hinzu, um die KI-Suche zu nutzen.',
            'ai_search_mode_info': 'Suche in der gesamten Bibliothek',
            'ai_search_feature_title': 'AI Search',
            'ai_search_feature_subtitle': 'Durchsuchen Sie Ihre gesamte Bibliothek in natürlicher Sprache',
            'ai_search_feature_description': (
                'AI Search hilft Ihnen, Bücher in Ihrer gesamten Calibre-Bibliothek zu entdecken.\n\n'
                '• Auslösen: Ask ohne Bücherauswahl öffnen, Extras → AI Search oder Tastenkürzel\n'
                '• Funktionsweise: Das Plugin sendet kompakte Metadaten (Buch-ID, Titel, Autor) '
                'für alle indizierten Bücher\n'
                '• Große Auswahl: Bei mehr als 50 Büchern schlägt Ask AI Search vor, statt jedes '
                'Buch im ausführlichen Format einzubetten\n'
                '• Daten aktuell halten: Nach Hinzufügen oder Entfernen von Büchern '
                '„Bibliotheksdaten aktualisieren“ klicken\n\n'
                'Beispielfragen: „Finde Bücher über Python“, „Zeig mir Bücher von Isaac Asimov“.'
            ),
            'ai_search_usage_hint': (
                'Tipp: AI Search eignet sich am besten für bibliotheksweite Suche. Für einen '
                'tiefen Vergleich weniger Bücher wählen Sie bis zu 30 Bücher aus.'
            ),
            'ai_search_data_title': 'Bibliotheksindex',
            'ai_search_data_subtitle': (
                'Aktualisieren Sie die kompakte Buchliste für die KI, wenn Sie Bücher '
                'hinzufügen oder entfernen'
            ),
            'library_prompt_template': 'Sie haben Zugriff auf die Buchbibliothek des Benutzers. Hier sind alle Bücher: {metadata} Benutzeranfrage: {query} Bitte finden Sie passende Bücher in der aktuellen Bibliothek und geben Sie sie in diesem Format zurück (**WICHTIG**: Verwenden Sie das HTML-Link-Format, damit Benutzer auf Buchtitel klicken können, um sie direkt zu öffnen): - <a href="calibre://book/BOOK_ID">Buchtitel</a> - Autorenname Beispiel: - <a href="calibre://book/123">Python lernen</a> - Mark Lutz - <a href="calibre://book/456">Machine Learning in Aktion</a> - Peter Harrington Hinweis: Einige Autoren können als "unknown" aufgeführt sein. Dies sind normale Daten, bitte geben Sie alle passenden Ergebnisse normal zurück. Nur Bücher zurückgeben, die der Anfrage entsprechen. Maximal 5 Ergebnisse.',
            'ai_search_privacy_title': 'Datenschutzhinweis',
            'ai_search_privacy_alert': 'Die KI-Suche verwendet Buch-Metadaten (Titel und Autoren) aus Ihrer Bibliothek. Diese Informationen werden an den von Ihnen konfigurierten KI-Anbieter gesendet, um Ihre Suchanfragen zu verarbeiten.',
            'ai_search_updated_info': '{count} Bücher vor {time_ago} aktualisiert',
            'ai_search_books_info': '{count} Bücher indiziert',
            'days_ago': '{n} Tagen',
            'hours_ago': '{n} Stunden',
            'minutes_ago': '{n} Minuten',
            'just_now': 'gerade eben',
            
            # Statistics tab (v1.4.2)
            'stat_tab': 'Statistik',
            'stat_overview': 'Übersicht',
            'stat_overview_subtitle': 'Statistik der AI-Anfragen',
            'stat_days_unit': 'Tage',
            'stat_days_label': 'Gestartet',
            'stat_start_at': 'Start am {date}',
            'stat_replies_unit': 'Mal',
            'stat_replies_label': 'AI fragen',
            'stat_books_unit': 'Bücher',
            'stat_books_label': 'Bibliothek',
            'stat_no_books': 'Im Suche-Tab aktualisieren',
            'stat_trends': 'Trends',
            'stat_curious_index': 'AI-Anfragen Verteilung diese Woche',
            'stat_daily_avg': 'Tagesdurchschnitt {n} Mal',
            'stat_sample_data': 'Beispieldaten angezeigt. Wechselt zu echten Daten nach 20+ Anfragen',
            'stat_heatmap': 'Heatmap',
            'stat_heatmap_subtitle': 'AI-Anfragen Verteilung diesen Monat',
            'stat_no_data_week': 'Keine Daten diese Woche',
            'stat_no_data_month': 'Keine Daten diesen Monat',
            'stat_data_not_enough': 'Nicht genügend Daten',
            
            # Statistik Benutzertitel (basierend auf Anfragezahl)
            'stat_title_curious': 'Blätterer',
            'stat_title_explorer': 'Bücherjäger',
            'stat_title_seeker': 'Leseratte',
            'stat_title_enthusiast': 'Bibliophiler',
            'stat_title_pursuer': 'Bücherwurm',
            
            # Statistik Bibliotheksbewertung (basierend auf Sammlungsgröße, historische Bibliotheken)
            'stat_books_impressive': 'Privates Studierzimmer',
            'stat_books_collection': 'Gelehrtenstube',
            'stat_books_variety': 'Stiftsbibliothek',
            'stat_books_awesome': 'Bayerische Staatsbibliothek',
            'stat_books_unbelievable': 'Bibliothek von Alexandria',
            
            # Links (v1.4.2)
            'online_tutorial': 'Online-Tutorial',
        }
