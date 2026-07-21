#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
French language translations for Ask AI Plugin.
"""

from ..models.base import BaseTranslation, TranslationRegistry, AIProvider


@TranslationRegistry.register
class FrenchTranslation(BaseTranslation):
    """French language translation."""
    
    @property
    def code(self) -> str:
        return "fr"
    
    @property
    def name(self) -> str:
        return "Français"
    
    @property
    def default_template(self) -> str:
        return 'Contexte : Vous assistez un utilisateur de calibre (http://calibre-ebook.com), une puissante application de gestion de livres électroniques, via le plugin "Ask AI Plugin". Ce plugin permet aux utilisateurs de poser des questions sur les livres de leur bibliothèque calibre. Remarque : Ce plugin ne peut répondre qu\'aux questions sur le contenu, les thèmes ou les sujets connexes du livre sélectionné - il ne peut pas modifier directement les métadonnées du livre ni effectuer des opérations calibre. Informations sur le livre : Titre : "{title}", Auteur : {author}, Éditeur : {publisher}, Année de publication : {pubyear}, Langue : {language}, Série : {series}. Question de l\'utilisateur : {query}. Veuillez fournir une réponse utile basée sur les informations du livre et vos connaissances.'
    
    @property
    def suggestion_template(self) -> str:
        return """Vous êtes un expert en critique littéraire. Pour le livre \"{title}\" de {author}, dont la langue de publication est {language}, générez UNE question perspicace qui aide les lecteurs à mieux comprendre les idées centrales du livre, ses applications pratiques ou ses perspectives uniques. Règles: 1. Retournez UNIQUEMENT la question, sans introduction ni explication 2. Concentrez-vous sur le contenu du livre, pas seulement sur son titre 3. Rendez la question pratique et stimulante 4. Soyez concis (30-200 mots) 5. Soyez créatif et générez une question différente à chaque fois, même pour le même livre"""
    
    @property
    def multi_book_default_template(self) -> str:
        return """Voici des informations sur plusieurs livres : {books_metadata} Question de l'utilisateur : {query} Veuillez répondre à la question en vous basant sur les informations ci-dessus sur les livres."""
    
    @property
    def translations(self) -> dict:
        return {
            # Informations sur le plugin
            'plugin_name': 'Plugin Ask AI',
            'plugin_desc': 'Posez des questions sur un livre en utilisant l\'IA',
            
            # UI - Onglets et sections
            'config_title': 'Configuration',
            'general_tab': 'Général',
            'ai_models': 'IA',
            'shortcuts': 'Raccourcis',
            'shortcuts_note': "Vous pouvez personnaliser ces raccourcis dans calibre : Préférences -> Raccourcis (recherchez 'Ask AI').\nCette page affiche les raccourcis par défaut/exemples. Si vous les avez modifiés dans Raccourcis, les paramètres de calibre sont prioritaires.",
            'prompts_tab': 'Prompts',
            'about': 'À propos',
            'metadata': 'Métadonnées',
            
            # Sous-titres de section
            'language_settings': 'Langue',
            'language_subtitle': 'Choisissez votre langue d\'interface préférée',
            'ai_providers_subtitle': 'Configurez les fournisseurs d\'IA et sélectionnez votre IA par défaut',
            'prompts_subtitle': 'Personnalisez la façon dont les questions sont envoyées à l\'IA',
            'export_settings_subtitle': 'Définissez le dossier par défaut pour l\'export de PDF',
            'reset_all_data_subtitle': 'Attention : Cela supprimera définitivement tous vos paramètres et données',
            
            # Onglet Prompts
            'language_preference_title': 'Préférence de Langue',
            'language_preference_subtitle': 'Contrôlez si les réponses de l\'IA doivent correspondre à la langue de votre interface',
            'prompt_templates_title': 'Modèles de Prompts',
            'prompt_templates_subtitle': 'Personnalisez la façon dont les informations du livre sont envoyées à l\'IA en utilisant des champs dynamiques comme {title}, {author}, {query}',
            'ask_prompts': 'Prompts de Questions',
            'random_questions_prompts': 'Prompts de Questions Aléatoires',
            'multi_book_prompts_label': 'Prompts Multi-Livres',
            'multi_book_placeholder_hint': 'Utilisez {books_metadata} pour les informations du livre, {query} pour la question de l\'utilisateur',
            'dynamic_fields_title': 'Référence des Champs Dynamiques',
            'dynamic_fields_subtitle': 'Champs disponibles et exemples de valeurs tirés de "Frankenstein" de Mary Shelley',
            'dynamic_fields_examples': '<b>{title}</b> → Frankenstein<br><b>{author}</b> → Mary Shelley<br><b>{publisher}</b> → Lackington, Hughes, Harding, Mavor & Jones<br><b>{pubyear}</b> → 1818<br><b>{language}</b> → English<br><b>{series}</b> → (aucune)<br><b>{query}</b> → Votre texte de question',
            'reset_prompts': 'Réinitialiser les Prompts par défaut',
            'reset_prompts_confirm': 'Êtes-vous sûr de vouloir réinitialiser tous les modèles de prompts à leurs valeurs par défaut ? Cette action ne peut pas être annulée.',
            'unsaved_changes_title': 'Modifications non enregistrées',
            'unsaved_changes_message': 'Vous avez des modifications non enregistrées dans l\'onglet Prompts. Voulez-vous les enregistrer ?',
            'use_interface_language': 'Toujours demander à l\'IA de répondre dans la langue actuelle de l\'interface du plugin',
            'language_instruction_label': 'Instruction de langue ajoutée aux prompts :',
            'language_instruction_text': 'Veuillez répondre en {language_name}.',
            
            # Paramètres de Persona
            'persona_title': 'Persona',
            'persona_subtitle': 'Définissez votre contexte de recherche et vos objectifs pour aider l\'IA à fournir des réponses plus pertinentes',
            'use_persona': 'Utiliser persona',
            'persona_label': 'Persona',
            'persona_placeholder': 'En tant que chercheur, je souhaite effectuer des recherches à travers les données de livres.',
            'persona_hint': 'Plus l\'IA en sait sur votre objectif et votre contexte, meilleure sera la recherche ou la génération.',
            
            # UI - Boutons et actions
            'ok_button': 'OK',
            'save_button': 'Enregistrer',
            'send_button': 'Envoyer',
            'stop_button': 'Arrêter',
            'suggest_button': 'Question Aléatoire',
            'copy_response': 'Copier la Réponse',
            'copy_question_response': 'Copier Q&&R',
            'export_pdf': 'Exporter PDF',
            'export_current_qa': 'Exporter Q&R Actuel',
            'export_history': 'Exporter l\'Historique',
            
            # Paramètres d'exportation
            'export_settings': 'Paramètres d\'Exportation',
            'enable_default_export_folder': 'Exporter vers le dossier par défaut',
            'no_folder_selected': 'Aucun dossier sélectionné',
            'browse': 'Parcourir...',
            'select_export_folder': 'Sélectionner le Dossier d\'Exportation',
            
            # Texte des boutons et éléments de menu
            'copy_response_btn': 'Copier la Réponse',
            'copy_qa_btn': 'Copier Q&R',
            'export_current_btn': 'Exporter Q&R en PDF',
            'export_history_btn': 'Exporter l\'Historique en PDF',
            'copy_mode_response': 'Réponse',
            'copy_mode_qa': 'Q&R',
            'copy_format_plain': 'Texte brut',
            'copy_format_markdown': 'Markdown',
            'export_mode_current': 'Q&R Actuel',
            'export_mode_history': 'Historique',
            
            # Lié à l'exportation PDF
            'model_provider': 'Fournisseur',
            'model_name': 'Modèle',
            'model_api_url': 'URL de Base API',
            'pdf_model_info': 'Informations sur le Modèle IA',
            'pdf_software': 'Logiciel',
            
            'export_all_history_dialog_title': 'Exporter Tout l\'Historique en PDF',
            'export_all_history_title': 'TOUT L\'HISTORIQUE Q&R',
            'export_history_insufficient': 'Au moins 2 enregistrements d\'historique requis pour exporter.',
            'history_record': 'Enregistrement',
            'question_label': 'Question',
            'answer_label': 'Réponse',
            'default_ai': 'IA par Défaut',
            'export_time': 'Exporté le',
            'total_records': 'Total des Enregistrements',
            'info': 'Information',
            'yes': 'Oui',
            'no': 'Non',
            'no_book_selected_title': 'Aucun Livre Sélectionné',
            'no_book_selected_message': 'Veuillez sélectionner un livre avant de poser des questions.',
            'set_default_ai_title': 'Définir l\'IA par Défaut',
            'set_default_ai_message': 'Vous avez basculé vers "{0}". Souhaitez-vous la définir comme IA par défaut pour les futures requêtes?',
            'set_default_ai_success': 'L\'IA par défaut a été définie sur "{0}".',
            'set_default_ai_after_add_message': '« {0} » a été ajouté avec succès. Souhaitez-vous la définir comme IA par défaut ?',
            'copied': 'Copié!',
            'pdf_exported': 'PDF Exporté!',
            'export_pdf_dialog_title': 'Exporter au format PDF',
            'export_pdf_error': 'Échec de l\'exportation PDF: {0}',
            'no_question': 'Pas de question',
            'no_response': 'Pas de réponse',
            'saved': 'Enregistré',
            'close_button': 'Fermer',
            'open_local_tutorial': 'Ouvrir le tutoriel local',
            'tutorial_open_failed': 'Échec de l\'ouverture du tutoriel',
            'tutorial': 'Tutoriel',

            'model_display_name_perplexity': 'Perplexity',
            
            # UI - Champs de configuration
            'token_label': 'Clé API:',
            'api_key_label': 'Clé API:',
            'model_label': 'Modèle:',
            'language_label': 'Langue:',
            'language_label_old': 'Langue',
            'base_url_label': 'URL de Base:',
            'base_url_placeholder': 'Par défaut: {default_api_base_url}',
            'shortcut': 'Touche de Raccourci',
            'shortcut_open_dialog': 'Ouvrir la Boîte de Dialogue',
            'shortcut_enter': 'Ctrl + Entrée',
            'shortcut_return': 'Command + Retour',
            'using_model': 'Modèle',
            'action': 'Action',
            'reset_button': 'Réinitialiser',
            'prompt_template': 'Modèle de Prompt',
            'ask_prompts': 'Prompts de Questions',
            'random_questions_prompts': 'Prompts de Questions Aléatoires',
            'display': 'Affichage',
            
            # UI - Éléments de dialogue
            'input_placeholder': 'Tapez votre question...',
            'response_placeholder': 'Réponse bientôt...',
            
            # UI - Éléments de menu
            'menu_title': 'Demander',
            'menu_ask': 'Demander',
            
            # UI - Messages d'état
            'loading': 'Chargement...',
            'loading_text': 'Demande en cours',
            'save_success': 'Paramètres enregistrés',
            'sending': 'Envoi en cours...',
            'requesting': 'Requête en cours',
            'request_stopped': 'Requête arrêtée',
            'formatting': 'Requête réussie, formatage en cours',
            
            # UI - Fonction de liste de modèles
            'load_models': 'Charger les modèles',
            'use_custom_model': 'Utiliser un nom de modèle personnalisé',
            'custom_model_placeholder': 'Entrez le nom du modèle personnalisé',
            'model_placeholder': 'Veuillez d\'abord charger les modèles',
            'models_loaded': '{count} modèles chargés avec succès',
            'load_models_failed': 'Échec du chargement des modèles : {error}',
            'model_list_not_supported': 'Ce fournisseur ne prend pas en charge la récupération automatique de la liste des modèles',
            'api_key_required': 'Veuillez d\'abord entrer la clé API',
            'invalid_params': 'Paramètres invalides',
            'warning': 'Avertissement',
            'success': 'Succès',
            'error': 'Erreur',
            'error_opening_dialog': "Erreur lors de l'ouverture du dialogue:",
            'skipped_books_warning': "{count} livre(s) ignoré(s) en raison d'erreurs d'accès aux fichiers.\nCela peut être causé par des caractères invalides dans les chemins de fichiers ou des fichiers verrouillés par un autre programme.",
            'failed_to_read_all_books': "Impossible de lire les métadonnées de tous les livres sélectionnés.\nCela peut être causé par des caractères invalides dans les chemins de fichiers ou des fichiers verrouillés par un autre programme.",
            'error_starting_request': "Erreur lors du démarrage de la requête",
            'default_ai_mismatch_title': "IA par défaut modifiée",
            'default_ai_mismatch_message': "L'IA par défaut dans la configuration a été changée en \"{default_ai}\",\nmais la conversation actuelle utilise \"{current_ai}\".\n\nVoulez-vous passer à la nouvelle IA par défaut ?",
            
            # Champs de métadonnées
            'metadata_title': 'Titre',
            'metadata_authors': 'Auteur',
            'metadata_publisher': 'Éditeur',
            'metadata_pubdate': 'Date de publication',
            'metadata_pubyear': 'Date de Publication',
            'metadata_language': 'Langue',
            'metadata_series': 'Série',
            'no_metadata': 'Pas de métadonnées',
            'no_series': 'Pas de série',
            'unknown': 'Inconnu',

            # Fonctionnalité multi-livres
            'books_unit': ' livres',
            'new_conversation': 'Nouvelle Conversation',
            'single_book': 'Livre Unique',
            'multi_book': 'Multi-Livres',
            'deleted': 'Supprimé',
            'history': 'Historique',
            'no_history': 'Aucun enregistrement d\'historique',
            'empty_question_placeholder': '(Aucune question)',
            'history_ai_unavailable': 'Cette IA a été supprimée de la configuration',
            'clear_current_book_history': 'Effacer l\'Historique du Livre Actuel',
            'confirm_clear_book_history': 'Êtes-vous sûr de vouloir effacer tout l\'historique pour:\n{book_titles}?',
            'confirm': 'Confirmer',
            'history_cleared': '{deleted_count} enregistrements d\'historique effacés.',
            'multi_book_template_label': 'Modèle de Prompt Multi-Livres:',
            'multi_book_placeholder_hint': 'Utilisez {books_metadata} pour les informations du livre, {query} pour la question de l\'utilisateur',
            
            # Messages d'erreur
            'network_error': 'Erreur de connexion',
            'request_timeout': 'Délai de requête dépassé',
            'request_failed': 'Échec de la requête',
            'question_too_long': 'Question trop longue',
            'question_too_long_detail': (
                'Le prompt est trop long ({current} caractères, limite {limit}, dépassement de {over}). '
                'Vous avez sélectionné {book_count} livre(s).'
            ),
            'question_too_long_detail_library': (
                'Le prompt est trop long ({current} caractères, limite {limit}, dépassement de {over}). '
                'Votre index de bibliothèque contient {book_count} livre(s).'
            ),
            'question_too_long_hint_ai_search': (
                'Pour les recherches à l\'échelle de la bibliothèque, utilisez AI Search (posez '
                'une question sans sélectionner de livres, ou via le menu AI Search) au lieu de '
                'sélectionner de nombreux livres.'
            ),
            'question_too_long_hint_library_search': (
                'Votre index de bibliothèque dépasse la limite de prompt actuelle. Activez '
                '« Limite de longueur de prompt personnalisée » dans Configuration du plugin → '
                'General (suggestion : 524288 caractères), ou posez une question plus précise.'
            ),
            'question_too_long_reduce_books': (
                'Pour comparer un plus petit ensemble en profondeur, essayez de désélectionner '
                'environ {count} livre(s).'
            ),
            'question_too_long_hint_default': (
                'Limite par défaut actuelle : {limit} caractères ({mode}). '
                'Par défaut pour un livre : 128 000 ; pour plusieurs livres : 256 000. '
                'Les utilisateurs avancés peuvent activer une limite personnalisée dans '
                'Configuration du plugin → General.'
            ),
            'question_too_long_hint_custom': (
                'Vous avez activé une limite de prompt personnalisée. En cas de timeout, '
                'diminuez la limite dans Configuration du plugin → General, réduisez la '
                'sélection ou posez une question plus précise.'
            ),
            'large_selection_dialog_title': 'Nombreux livres sélectionnés',
            'large_selection_dialog_message': (
                'Vous avez sélectionné {count} livres. Pour les questions à l\'échelle de la '
                'bibliothèque, AI Search est plus adapté et recherche toute votre bibliothèque '
                'avec des métadonnées compactes.\n\n'
                'Passer à AI Search, ou continuer avec les livres sélectionnés en format compact ?'
            ),
            'large_selection_use_ai_search': 'Utiliser AI Search',
            'large_selection_continue': 'Continuer avec la sélection',
            'multi_book_truncation_note': (
                'Note : en raison de la limite de prompt, seuls les {included} premiers livres '
                'sur {total} sélectionnés sont inclus. Utilisez AI Search pour interroger toute '
                'votre bibliothèque, ou augmentez la limite personnalisée dans '
                'Configuration du plugin → General.'
            ),
            'library_metadata_truncation_note': (
                'Note : en raison de la limite de prompt, seuls les {included} premiers livres '
                'sur {total} indexés sont inclus. Les résultats peuvent être incomplets pour '
                'les très grandes bibliothèques sauf si vous augmentez la limite personnalisée '
                'dans Configuration du plugin → General.'
            ),
            'auth_token_required_title': 'Clé API Requise',
            'auth_token_required_message': 'Veuillez définir une clé API valide dans la Configuration du Plugin.',
            'open_configuration': 'Ouvrir la Configuration',
            'cancel': 'Annuler',
            
            # AI Manager Dialog
            'ai_manager_title': 'Gérer les Fournisseurs d\'IA',
            'add_ai_title': 'Ajouter un Fournisseur d\'IA',
            'manage_ai_title': 'Gérer l\'IA Configurée',
            'configured_ai_list': 'IA Configurée',
            'available_ai_list': 'Disponible à Ajouter',
            'ai_config_panel': 'Configuration',
            'select_ai_to_configure': 'Sélectionnez une IA dans la liste pour configurer',
            'select_provider': 'Sélectionner le Fournisseur d\'IA',
            'select_provider_hint': 'Sélectionnez un fournisseur dans la liste',
            'select_ai_to_edit': 'Sélectionnez une IA dans la liste pour modifier',
            'set_as_default': 'Définir par Défaut',
            'save_ai_config': 'Enregistrer',
            'remove_ai_config': 'Supprimer',
            'delete_ai': 'Supprimer',
            'close_button': 'Fermer',
            'add_ai_button': 'Ajouter IA',
            'ai_manager_window_hint': '« Ajouter / Gérer » ouvre une fenêtre redimensionnable (maximisable). Double-cliquez une IA configurée pour l’éditer.',
            'edit_ai_button': 'Modifier IA',
            'manage_configured_ai_button': 'Gérer l\'IA Configurée',
            'manage_ai_button': 'Gérer IA',
            'no_configured_ai': 'Aucune IA configurée pour le moment',
            'no_configured_ai_hint': 'Aucune IA configurée. Le plugin ne peut pas fonctionner. Veuillez cliquer sur "Ajouter IA" pour ajouter un fournisseur d\'IA.',
            'default_ai_label': 'IA par Défaut:',
            'default_ai_tag': 'Par Défaut',
            'ai_not_configured_cannot_set_default': 'Cette IA n\'est pas encore configurée. Veuillez d\'abord enregistrer la configuration.',
            'ai_set_as_default_success': '{name} a été défini comme IA par défaut.',
            'ai_config_saved_success': 'Configuration de {name} enregistrée avec succès.',
            'confirm_remove_title': 'Confirmer la Suppression',
            'confirm_remove_ai': 'Êtes-vous sûr de vouloir supprimer {name}? Cela effacera la clé API et réinitialisera la configuration.',
            'confirm_delete_title': 'Confirmer la Suppression',
            'confirm_delete_ai': 'Êtes-vous sûr de vouloir supprimer {name}?',
            'api_key_required': 'La clé API est requise.',
            'success': 'Succès',
            'configuration': 'Configuration',
            'yes_button': 'Oui',
            'no_button': 'Non',
            'cancel_button': 'Annuler',
            "invalid_default_ai_title": "IA par Défaut Invalide",
            "invalid_default_ai_message": "L'IA par défaut \"{default_ai}\" n'est pas correctement configurée.\n\nVoulez-vous plutôt passer à \"{first_ai}\" ?",
            "switch_to_ai": "Passer à {ai}",
            "keep_current": "Garder Actuel",
            'error_preparing_request': 'Échec de la préparation de la requête',
            'empty_suggestion': 'Suggestion vide',
            'process_suggestion_error': 'Erreur de traitement de la suggestion',
            'unknown_error': 'Erreur inconnue',
            'unknown_model': 'Modèle inconnu: {model_name}',
            'suggestion_error': 'Erreur de suggestion',
            'random_question_success': 'Question aléatoire générée avec succès!',
            'book_title_check': 'Titre du livre requis',
            'avoid_repeat_question': 'Veuillez utiliser une question différente',
            'empty_answer': 'Réponse vide',
            'empty_response': "Réponse vide reçue de l'API",
            'empty_response_after_filter': 'La réponse est vide après filtrage des balises think',
            'invalid_response': 'Réponse invalide',
            'auth_error_401': 'Non autorisé',
            'auth_error_403': 'Accès refusé',
            'rate_limit': 'Limite de taux de requêtes dépassée',
            'invalid_json': 'JSON invalide',
            'template_error': 'Erreur de modèle',
            'no_model_configured': 'Aucun modèle d\'IA configuré. Veuillez configurer un modèle d\'IA dans les paramètres.',
            'no_ai_configured_title': 'Aucune IA configurée',
            'no_ai_configured_message': 'Bienvenue ! Pour commencer à poser des questions sur vos livres, vous devez d\'abord configurer un fournisseur d\'IA.\n\nBonne nouvelle : Ce plugin propose maintenant un niveau GRATUIT (Nvidia AI Free) que vous pouvez utiliser immédiatement sans aucune configuration !\n\nAutres options recommandées :\n• Nvidia AI - Obtenez 6 mois d\'accès API GRATUIT avec juste votre numéro de téléphone (aucune carte de crédit requise)\n• Ollama - Exécutez des modèles d\'IA localement sur votre ordinateur (complètement gratuit et privé)\n\nSouhaitez-vous ouvrir la configuration du plugin pour configurer un fournisseur d\'IA maintenant ?',
            'open_settings': 'Configuration du Plugin',
            'ask_anyway': 'Demander Quand Même',
            'later': 'Plus Tard',
            'reset_all_data': 'Réinitialiser Toutes les Données',
            'reset_all_data_warning': 'Cela supprimera toutes les clés API, les modèles de prompt et les enregistrements d\'historique locaux. Votre préférence linguistique sera préservée. Veuillez procéder avec prudence.',
            'reset_all_data_confirm_title': 'Confirmer la Réinitialisation',
            'reset_all_data_confirm_message': 'Êtes-vous sûr de vouloir réinitialiser le plugin à son état initial?\n\nCela supprimera définitivement:\n• Toutes les clés API\n• Tous les modèles de prompt personnalisés\n• Tout l\'historique des conversations\n• Tous les paramètres du plugin (la préférence linguistique sera préservée)\n\nCette action ne peut pas être annulée!',
            'reset_all_data_success': 'Toutes les données du plugin ont été réinitialisées avec succès. Veuillez redémarrer calibre pour que les modifications prennent effet.',
            'reset_all_data_failed': 'Échec de la réinitialisation des données du plugin: {error}',
            'random_question_error': 'Erreur lors de la génération d\'une question aléatoire',
            'clear_history_failed': 'Échec de l\'effacement de l\'historique',
            'clear_history_not_supported': 'L\'effacement de l\'historique pour un seul livre n\'est pas encore supporté',
            'missing_required_config': 'Configuration requise manquante: {key}. Veuillez vérifier vos paramètres.',
            'api_key_too_short': 'La clé API est trop courte. Veuillez vérifier et entrer la clé complète.',

            # Gestion des réponses API
            'api_request_failed': 'Échec de la requête API: {error}',
            'api_content_extraction_failed': 'Impossible d\'extraire le contenu de la réponse API',
            'api_invalid_response': 'Impossible d\'obtenir une réponse API valide',
            'api_unknown_error': 'Erreur inconnue: {error}',

            # Gestion des réponses en streaming
            'stream_response_code': 'Code d\'état de la réponse en streaming: {code}',
            'stream_continue_prompt': 'Veuillez continuer votre réponse précédente sans répéter le contenu déjà fourni.',
            'stream_continue_code_blocks': 'Votre réponse précédente contenait des blocs de code non fermés. Veuillez continuer et compléter ces blocs de code.',
            'stream_continue_parentheses': 'Votre réponse précédente contenait des parenthèses non fermées. Veuillez continuer et vous assurer que toutes les parenthèses sont correctement fermées.',
            'stream_continue_interrupted': 'Votre réponse précédente semble avoir été interrompue. Veuillez continuer en complétant votre dernière pensée ou explication.',
            'stream_timeout_error': 'La connexion de streaming n\'a pas reçu de nouveau contenu depuis 60 secondes, il s\'agit probablement d\'un problème de connexion.',

            # Messages d'erreur API
            'api_version_model_error': 'Erreur de version API ou de nom de modèle: {message}\n\nVeuillez mettre à jour l\'URL de base de l\'API vers "{base_url}" et le modèle vers "{model}" ou un autre modèle disponible dans les paramètres.',
            'api_format_error': 'Erreur de format de requête API: {message}',
            'api_key_invalid': 'Clé API invalide ou non autorisée: {message}\n\nVeuillez vérifier votre clé API et vous assurer que l\'accès à l\'API est activé.',
            'api_rate_limit': 'Limite de taux de requête dépassée, veuillez réessayer plus tard\n\nVous avez peut-être dépassé le quota d\'utilisation gratuit. Cela peut être dû à:\n1. Trop de requêtes par minute\n2. Trop de requêtes par jour\n3. Trop de jetons d\'entrée par minute',

            # Erreurs de configuration
            'missing_config_key': 'Clé de configuration requise manquante: {key}',
            'api_base_url_required': 'URL de base API requise',
            'model_name_required': 'Nom du modèle requis',
            'api_key_empty': 'La clé API est vide. Veuillez entrer une clé API valide.',

            # Récupération de la liste des modèles
            'fetching_models_from': 'Récupération des modèles depuis {url}',
            'successfully_fetched_models': '{count} modèles {provider} récupérés avec succès',
            'failed_to_fetch_models': 'Échec de la récupération des modèles : {error}',
            'error_401': "Échec de l'authentification de la clé API. Veuillez vérifier : la clé API est correcte, le compte a un solde suffisant, la clé API n'a pas expiré.",
            'error_403': "Accès refusé. Veuillez vérifier : la clé API a des permissions suffisantes, aucune restriction d'accès régional.",
            'error_404': "Point de terminaison API introuvable. Veuillez vérifier si la configuration de l'URL de base API est correcte.",

            # Informations à propos
            'author_name': 'Sheldon',
            'user_manual': 'Manuel d\'Utilisateur',
            'about_plugin': 'Pourquoi Ask AI Plugin?',
            'learn_how_to_use': 'Comment Utiliser',
            'email': 'iMessage',
            'about_title': 'À propos de Ask AI Plugin',
            'about_version_label': 'Version',
            'about_description': "Posez des questions sur vos livres calibre avec les services d'IA que vous choisissez.",
            'about_related_plugins': 'Plugins associés',
            'about_markdown_title': 'Markdown pour calibre',
            'about_markdown_desc': 'Exportez les livres en fichiers texte Markdown.',
            'about_tradsimp_title': 'Conversion du chinois pour calibre',
            'about_tradsimp_desc': 'Convertissez le chinois traditionnel et simplifié dans les ebooks.',
            'about_open_mobileread': 'Ouvrir MobileRead',
            'about_open_nowtiny': 'Ouvrir Nowtiny',
            'about_nowtiny_note': "Plus d'outils et l'état des plugins sont sur Nowtiny.",

            # Configurations spécifiques au modèle
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_kimi': 'Kimi (Moonshot)',
            'model_display_name_custom': 'Personnalisé',
            'model_display_name_ollama': 'Ollama(Local)',
            'model_display_name_lmstudio': 'LM Studio(Local)',
            'model_display_name_koboldcpp': 'KoboldCpp(Local)',
            'local_openai_compat_no_api_key_notice': 'Note: This local OpenAI-compatible service usually does not require an API key. Start the local server, then refresh the model list.',
            'lmstudio_no_api_key_notice': 'Note: LM Studio uses the OpenAI-compatible API locally and usually does not require an API key.',
            'koboldcpp_no_api_key_notice': 'Note: KoboldCpp uses the OpenAI-compatible API locally and usually does not require an API key.',
            'local_service_not_running': 'Cannot connect to the local AI service. Please confirm it is running and the Base URL is correct.',
            'model_enable_streaming': 'Activer le streaming',
            
            # AI Switcher
            'current_ai': 'IA Actuelle',
            'no_configured_models': 'Aucune IA configurée - Veuillez configurer dans les paramètres',

            # Info spécifique au fournisseur
            'nvidia_free_info': '💡 Les nouveaux utilisateurs bénéficient de 6 mois d\'accès API gratuit - Aucune carte de crédit requise',

            # Messages système communs
            'default_system_message': 'Vous êtes un expert en analyse de livres. Votre tâche est d\'aider les utilisateurs à mieux comprendre les livres en fournissant des questions et des analyses perspicaces.',

            # Paramètres de délai de requête
            'request_timeout_label': 'Délai d\'attente de la requête:',
            'seconds': 'secondes',
            'request_timeout_error': 'Délai d\'attente de la requête dépassé. Délai actuel: {timeout} secondes',
            'max_prompt_length_normalized_title': 'Limite de prompt ajustée',
            'max_prompt_length_normalized': (
                'La longueur du prompt a été normalisée à {value} caractères (des séparateurs tels que des virgules '
                'ou des espaces ont été supprimés).'
            ),
            'enable_custom_prompt_limit_label': 'Limite de longueur de prompt personnalisée',
            'enable_custom_prompt_limit_tooltip': (
                'Les limites par défaut sont de 128 000 caractères (un livre) et 256 000 '
                '(plusieurs livres). La plupart des utilisateurs n\'ont pas besoin de modifier '
                'cela. Pour les recherches à l\'échelle de la bibliothèque, utilisez AI Search. '
                'Activez une limite personnalisée uniquement si votre modèle supporte un contexte '
                'beaucoup plus large et que les requêtes atteignent encore la limite.'
            ),
            'max_prompt_length_label': 'Longueur max. du prompt :',
            'max_prompt_length_unit': 'caractères',
            'max_prompt_length_tooltip': (
                'S\'applique lorsque la limite personnalisée est activée. Suggestion par défaut : '
                '524288 caractères. Règle approximative : 1 token ≈ 3–4 caractères. Pour Ollama, '
                'configurez aussi num_ctx côté modèle.'
            ),

            # Paramètres d'IA parallèle
            'parallel_ai_count_label': 'Nombre d\'IA parallèles:',
            'parallel_ai_count_tooltip': 'Nombre de modèles d\'IA à interroger simultanément (1-2 disponibles, 3-4 à venir)',
            'parallel_ai_notice': 'Remarque: Cela n\'affecte que l\'envoi des questions. Les questions aléatoires utilisent toujours une seule IA.',
            'suggest_maximize': 'Conseil: Maximisez la fenêtre pour une meilleure visualisation avec 3 IAs',
            'ai_panel_label': 'IA {index}:',
            'no_ai_available': 'Aucune IA disponible pour ce panneau',
            'add_more_ai_providers': 'Veuillez ajouter plus de fournisseurs d\'IA dans les paramètres',
            'select_ai': '-- Sélectionner l\'IA --',
            'select_model': '-- Changer de Modèle --',
            'request_model_list': 'Veuillez demander la liste des modèles',
            'coming_soon': 'Bientôt disponible',
            'advanced_feature_tooltip': 'Cette fonctionnalité est en cours de développement. Restez à l\'écoute des mises à jour!',

            # Titres de section d'exportation PDF
            'pdf_book_metadata': 'MÉTADONNÉES DU LIVRE',
            'pdf_question': 'QUESTION',
            'pdf_answer': 'RÉPONSE',
            'pdf_ai_model_info': 'INFORMATIONS SUR LE MODÈLE IA',
            'pdf_generated_by': 'GÉNÉRÉ PAR',
            'pdf_provider': 'Fournisseur',
            'pdf_model': 'Modèle',
            'pdf_api_base_url': 'URL de base API',
            'pdf_panel': 'Panneau',
            'pdf_plugin': 'Plugin',
            'pdf_github': 'GitHub',
            'pdf_generated_time': 'Heure de génération',
            'error_429': 'Trop de requêtes, limite de débit atteinte. Veuillez réessayer plus tard.',
            'error_5xx': 'Erreur serveur. Veuillez réessayer plus tard ou vérifier l\'état du fournisseur de services.',
            'error_network': 'Échec de la connexion réseau. Veuillez vérifier la connexion réseau, les paramètres du proxy ou la configuration du pare-feu.',
            'error_unknown': 'Erreur inconnue.',
            'gemini_geo_restriction': 'L\'API Gemini n\'est pas disponible dans votre région. Veuillez essayer:\n1. Utiliser un VPN pour se connecter depuis une région prise en charge\n2. Utiliser d\'autres fournisseurs d\'IA (OpenAI, Anthropic, DeepSeek, etc.)\n3. Vérifier Google AI Studio pour la disponibilité régionale',
            'load_models_list': 'Charger la Liste des Modèles',
            'loading_models_text': 'Chargement des modèles',
            'model_test_success': 'Test du modèle réussi!',
            'models_loaded_with_selection': '{count} modèles chargés avec succès.\nModèle sélectionné: {model}',
            'ollama_model_not_available': 'Le modèle "{model}" n\'est pas disponible. Veuillez vérifier:\n1. Le modèle est-il démarré? Exécutez: ollama run {model}\n2. Le nom du modèle est-il correct?\n3. Le modèle est-il téléchargé? Exécutez: ollama pull {model}',
            'ollama_service_not_running': 'Le service Ollama n\'est pas en cours d\'exécution. Veuillez d\'abord démarrer le service Ollama.',
            'ollama_service_timeout': 'Délai de connexion du service Ollama. Veuillez vérifier si le service fonctionne correctement.',
            'reset_ai_confirm_message': 'Sur le point de réinitialiser {ai_name} à l\'état par défaut.\n\nCela effacera:\n• Clé API\n• Nom de modèle personnalisé\n• Autres paramètres configurés\n\nContinuer?',
            'reset_ai_confirm_title': 'Confirmer la Réinitialisation',
            'reset_current_ai': 'Réinitialiser l\'IA Actuelle par Défaut',
            'reset_tooltip': 'Réinitialiser l\'IA actuelle aux valeurs par défaut',
            'save_and_close': 'Enregistrer et Fermer',
            'discard_changes': 'Abandonner les modifications',
            'skip': 'Ignorer',
            'technical_details': 'Détails Techniques',
            'test_current_model': 'Tester le Modèle Actuel',
            'test_model_button': 'Tester le Modèle',
            'test_model_prompt': 'Modèles chargés avec succès! Voulez-vous tester le modèle sélectionné "{model}"?',
            'unsaved_changes_message': 'Vous avez des modifications non enregistrées. Que voulez-vous faire?',
            'unsaved_changes_title': 'Modifications Non Enregistrées',


            'pdf_info_not_available': 'Information non disponible',
            
            # Field descriptions
            'api_key_desc': 'Votre clé API pour l\'authentification. Gardez-la en sécurité et ne la partagez pas.',
            'base_url_desc': 'L\'URL du point de terminaison de l\'API. Utilisez la valeur par défaut sauf si vous avez un point de terminaison personnalisé.',
            'base_url_desc_kimi': 'Les clés internationales utilisent https://api.moonshot.ai/v1 ; les clés de la plateforme Chine utilisent https://api.moonshot.cn/v1. Ne les mélangez pas.',
            'kimi_region_label': 'Plateforme',
            'kimi_region_global': 'International',
            'kimi_region_china': 'Chine continentale',
            'kimi_base_url_readonly_tip': "L'URL de base est déterminée par la plateforme sélectionnée.",
            'model_desc': 'Sélectionnez un modèle dans la liste ou utilisez un nom de modèle personnalisé.',
            'streaming_desc': 'Activez la diffusion de réponses en temps réel pour un retour plus rapide.',
            'advanced_section': 'Avancé',
            
            # Provider-specific notices
            'perplexity_model_notice': 'Remarque: Perplexity ne fournit pas d\'API publique de liste de modèles, les modèles sont donc codés en dur.',
            'ollama_no_api_key_notice': 'Note: Ollama uses the OpenAI-compatible API locally and usually does not require an API key.',
            'nvidia_free_credits_notice': 'Remarque: Les nouveaux utilisateurs obtiennent des crédits API gratuits - aucune carte de crédit requise.',
            
            # Messages d'erreur Nvidia Free
            'free_tier_rate_limit': 'Limite de taux d\'accès gratuit dépassée. Veuillez réessayer plus tard ou configurer votre propre clé API Nvidia.',
            'free_tier_unavailable': 'L\'accès gratuit est temporairement indisponible. Veuillez réessayer plus tard ou configurer votre propre clé API Nvidia.',
            'free_tier_server_error': 'Erreur du serveur d\'accès gratuit. Veuillez réessayer plus tard.',
            'free_tier_error': 'Erreur d\'accès gratuit',
            
            # Informations sur le fournisseur Nvidia Free
            'free': 'Gratuit',
            'nvidia_free_provider_name': 'Nvidia AI (Gratuit)',
            'nvidia_free_display_name': 'Nvidia AI (Gratuit)',
            'nvidia_free_api_key_info': 'Sera obtenu depuis le serveur',
            'nvidia_free_desc': 'Ce service est maintenu par le développeur et reste gratuit, mais peut être moins stable. Pour un service plus stable, veuillez configurer votre propre clé API Nvidia.',
            
            # Rappel de première utilisation Nvidia Free
            'nvidia_free_first_use_title': 'Bienvenue dans le plugin Ask AI',
            'nvidia_free_first_use_message': 'Vous pouvez maintenant poser des questions sans aucune configuration ! Le développeur maintient un niveau gratuit pour vous, mais il peut ne pas être très stable. Profitez-en !\n\nVous pouvez configurer vos propres fournisseurs d\'IA dans les paramètres pour une meilleure stabilité.',
            
            # Model buttons
            'refresh_model_list': 'Actualiser',
            'testing_text': 'Test',
            'refresh_success': 'Liste de modèles actualisée avec succès.',
            'refresh_failed': 'Échec de l\'actualisation de la liste de modèles.',
            'test_failed': 'Test du modèle échoué.',
            
            # Tooltip
            'manage_ai_disabled_tooltip': 'Veuillez d\'abord ajouter un fournisseur d\'IA.',

            #AI Search v1.4.2
            'library_tab': 'Rechercher',
            'library_search': 'Recherche IA',
            'library_info': 'La recherche IA est toujours activée. Lorsque vous ne sélectionnez aucun livre, vous pouvez effectuer une recherche dans toute votre bibliothèque en langage naturel.',
            'library_enable': 'Activer la recherche IA',
            'library_enable_tooltip': 'Une fois activée, vous pouvez effectuer des recherches dans votre bibliothèque à l\'aide de l\'IA quand aucun livre n\'est sélectionné',
            'library_update': 'Mettre à jour les données',
            'library_update_tooltip': 'Extraire les titres et auteurs de votre bibliothèque',
            'library_updating': 'Mise à jour...',
            'library_status': 'Statut : {count} livres, dernière mise à jour : {time}',
            'library_status_empty': 'Statut : Aucune donnée. Cliquez sur "Mettre à jour les données" pour commencer.',
            'library_status_error': 'Statut : Erreur lors du chargement des données',
            'library_update_success': '{count} livres mis à jour avec succès',
            'library_update_failed': 'Échec de la mise à jour des données',
            'library_no_gui': 'Interface graphique non disponible',
            'library_init_title': 'Initialiser la recherche IA',
            'library_init_message': 'La recherche IA nécessite les métadonnées de la bibliothèque. Souhaitez-vous l\'initialiser maintenant ?\n\nCela extraira les titres et les auteurs de vos livres.',
            'library_init_required': 'La recherche IA ne peut pas être activée sans données. Veuillez cliquer sur "Mettre à jour les données" quand vous serez prêt.',
            'ai_search_welcome_title': 'Bienvenue dans la Recherche IA',
            'ai_search_welcome_message': 'La recherche IA est activée !\n\nComment déclencher :\n• Raccourci clavier (personnalisable dans les paramètres)\n• Menu Outils → Recherche IA\n• Ouvrir le dialogue Ask sans sélectionner de livres\n\nVous pouvez rechercher dans toute votre bibliothèque en langage naturel. Par exemple :\n• "Avez-vous des livres sur Python ?"\n• "Montrez-moi les livres d\'Isaac Asimov"\n• "Trouvez des livres sur l\'apprentissage automatique"\n\nL\'IA recherchera et recommandera des livres pertinents. Cliquez sur les titres pour les ouvrir directement.',
            'ai_search_not_enough_books_title': 'Pas assez de livres',
            'ai_search_not_enough_books_message': 'La recherche IA nécessite au moins {min_books} livres dans votre bibliothèque.\n\nVotre bibliothèque actuelle ne contient que {book_count} livre(s).\n\nVeuillez ajouter plus de livres pour utiliser la recherche IA.',
            'ai_search_mode_info': 'Recherche dans toute la bibliothèque',
            'ai_search_feature_title': 'AI Search',
            'ai_search_feature_subtitle': 'Recherchez toute votre bibliothèque en langage naturel',
            'ai_search_feature_description': (
                'AI Search vous aide à découvrir des livres dans toute votre bibliothèque Calibre.\n\n'
                '• Déclenchement : ouvrir Ask sans sélectionner de livres, Outils → AI Search, '
                'ou raccourci clavier\n'
                '• Fonctionnement : le plugin envoie des métadonnées compactes (ID, titre, auteur) '
                'pour tous les livres indexés\n'
                '• Grandes sélections : si vous sélectionnez plus de 50 livres, Ask suggère AI Search '
                'au lieu d\'intégrer chaque livre en format détaillé\n'
                '• Données à jour : cliquez sur « Mettre à jour les données » après avoir ajouté '
                'ou supprimé des livres\n\n'
                'Exemples : « Trouvez des livres sur Python », « Montrez-moi les livres d\'Isaac Asimov ».'
            ),
            'ai_search_usage_hint': (
                'Conseil : AI Search convient mieux à la découverte à l\'échelle de la bibliothèque. '
                'Pour comparer quelques livres en profondeur, sélectionnez jusqu\'à 30 livres.'
            ),
            'ai_search_data_title': 'Index de bibliothèque',
            'ai_search_data_subtitle': (
                'Actualisez la liste compacte de livres envoyée à l\'IA lorsque vous ajoutez '
                'ou supprimez des livres'
            ),
            'library_prompt_template': 'Vous avez accès à la bibliothèque de livres de l\'utilisateur. Voici tous les livres : {metadata} Requête de l\'utilisateur : {query} Veuillez trouver les livres correspondants dans la bibliothèque actuelle et les retourner dans ce format (**IMPORTANT** : Utilisez le format de lien HTML pour que les utilisateurs puissent cliquer sur les titres des livres pour les ouvrir directement) : - <a href="calibre://book/BOOK_ID">Titre du livre</a> - Nom de l\'auteur Exemple : - <a href="calibre://book/123">Apprendre Python</a> - Mark Lutz - <a href="calibre://book/456">Machine Learning en action</a> - Peter Harrington Remarque : Certains auteurs peuvent être listés comme "unknown". Ce sont des données normales, veuillez retourner tous les résultats correspondants normalement. Ne retournez que les livres correspondant à la requête. Maximum 5 résultats.',
            'ai_search_privacy_title': 'Avis de confidentialité',
            'ai_search_privacy_alert': 'La recherche IA utilise les métadonnées (titres et auteurs) de votre bibliothèque. Ces informations seront envoyées au fournisseur d\'IA configuré pour traiter vos requêtes.',
            'ai_search_updated_info': '{count} livres mis à jour il y a {time_ago}',
            'ai_search_books_info': '{count} livres indexés',
            'days_ago': '{n} jours',
            'hours_ago': '{n} heures',
            'minutes_ago': '{n} minutes',
            'just_now': 'à l\'instant',
            
            # Statistics tab (v1.4.2)
            'stat_tab': 'Statistiques',
            'stat_overview': 'Aperçu',
            'stat_overview_subtitle': 'Statistiques des requêtes AI',
            'stat_days_unit': 'jours',
            'stat_days_label': 'Démarré',
            'stat_start_at': 'Début le {date}',
            'stat_replies_unit': 'fois',
            'stat_replies_label': 'Demander AI',
            'stat_books_unit': 'livres',
            'stat_books_label': 'Bibliothèque',
            'stat_no_books': 'Mettre à jour dans l\'onglet Recherche',
            'stat_trends': 'Tendances',
            'stat_curious_index': 'Distribution des requêtes AI cette semaine',
            'stat_daily_avg': 'Moyenne quotidienne {n} fois',
            'stat_sample_data': 'Données d\'exemple affichées. Passera aux données réelles après 20+ requêtes',
            'stat_heatmap': 'Carte thermique',
            'stat_heatmap_subtitle': 'Distribution des requêtes AI ce mois',
            'stat_no_data_week': 'Pas de données cette semaine',
            'stat_no_data_month': 'Pas de données ce mois',
            'stat_data_not_enough': 'Données insuffisantes',
            
            # Titres utilisateur statistiques (basés sur le nombre de requêtes)
            'stat_title_curious': 'Feuilleteur',
            'stat_title_explorer': 'Chasseur de livres',
            'stat_title_seeker': 'Lecteur assidu',
            'stat_title_enthusiast': 'Bibliophile',
            'stat_title_pursuer': 'Rat de bibliothèque',
            
            # Évaluations de bibliothèque (basées sur la taille de collection, références historiques)
            'stat_books_impressive': 'Cabinet de lecture',
            'stat_books_collection': 'Bureau d\'érudit',
            'stat_books_variety': 'Bibliothèque Mazarine',
            'stat_books_awesome': 'Bibliothèque nationale de France',
            'stat_books_unbelievable': 'Bibliothèque d\'Alexandrie',
            
            # Links (v1.4.2)
            'online_tutorial': 'Tutoriel en ligne',
        }
