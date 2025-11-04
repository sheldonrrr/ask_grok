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
        return 'À propos du livre "{title}": Auteur: {author}, Éditeur: {publisher}, Année de publication: {pubyear}, livre en language: {language}, Série: {series}, Ma question est: {query}'
    
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
            'plugin_name': 'Ask AI Plugin',
            'plugin_desc': 'Posez des questions sur un livre en utilisant l\'IA',
            
            # UI - Onglets et sections
            'config_title': 'Configuration',
            'general_tab': 'Général',
            'ai_models': 'IA',
            'shortcuts': 'Raccourcis',
            'about': 'À propos',
            'metadata': 'Métadonnées',
            
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
            'copied': 'Copié!',
            'pdf_exported': 'PDF Exporté!',
            'export_pdf_dialog_title': 'Exporter au format PDF',
            'export_pdf_error': 'Échec de l\'exportation PDF: {0}',
            'no_question': 'Pas de question',
            'no_response': 'Pas de réponse',
            'saved': 'Enregistré',
            'close_button': 'Fermer',
            
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
            'menu_ask': 'Demander à {model}',
            
            # UI - Messages d'état
            'loading': 'Chargement...',
            'loading_text': 'Demande en cours',
            'save_success': 'Paramètres enregistrés',
            'sending': 'Envoi en cours...',
            'requesting': 'Requête en cours',
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
            
            # Champs de métadonnées
            'metadata_title': 'Titre',
            'metadata_authors': 'Auteur',
            'metadata_publisher': 'Éditeur',
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
            'clear_current_book_history': 'Effacer l\'historique du livre actuel',
            'confirm_clear_book_history': 'Êtes-vous sûr de vouloir effacer tout l\'historique pour:\n{book_titles}?',
            'confirm': 'Confirmer',
            'history_cleared': '{deleted_count} enregistrements d\'historique effacés.',
            'multi_book_template_label': 'Modèle de Prompt Multi-Livres:',
            'multi_book_placeholder_hint': 'Utilisez {books_metadata} pour les informations du livre, {query} pour la question de l\'utilisateur',
            
            # Messages d'erreur
            'error': 'Erreur: ',
            'network_error': 'Erreur de connexion',
            'request_timeout': 'Délai de requête dépassé',
            'request_failed': 'Échec de la requête',
            'question_too_long': 'Question trop longue',
            'auth_token_required_title': 'Clé API Requise',
            'auth_token_required_message': 'Veuillez définir une clé API valide dans la Configuration du Plugin.',
            'open_configuration': 'Ouvrir la Configuration',
            'cancel': 'Annuler',
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
            'invalid_response': 'Réponse invalide',
            'auth_error_401': 'Non autorisé',
            'auth_error_403': 'Accès refusé',
            'rate_limit': 'Limite de taux de requêtes dépassée',
            'invalid_json': 'JSON invalide',
            'no_response': 'Pas de réponse',
            'template_error': 'Erreur de modèle',
            'no_model_configured': 'Aucun modèle d\'IA configuré. Veuillez configurer un modèle d\'IA dans les paramètres.',
            'no_ai_configured_title': 'Aucune IA configurée',
            'no_ai_configured_message': 'Bienvenue! Pour commencer à poser des questions sur vos livres, vous devez d\'abord configurer un fournisseur d\'IA.\n\nRecommandé pour les débutants:\n• Nvidia AI - Obtenez 6 mois d\'accès API GRATUIT avec juste votre numéro de téléphone (aucune carte de crédit requise)\n• Ollama - Exécutez des modèles d\'IA localement sur votre ordinateur (totalement gratuit et privé)\n\nSouhaitez-vous ouvrir la configuration du plugin pour configurer un fournisseur d\'IA maintenant?',
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

            # Informations à propos
            'author_name': 'Sheldon',
            'user_manual': 'Manuel d\'Utilisateur',
            'about_plugin': 'Pourquoi Ask AI Plugin?',
            'learn_how_to_use': 'Comment Utiliser',
            'email': 'iMessage',

            # Configurations spécifiques au modèle
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Personnalisé',
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

            # Paramètres d'IA parallèle
            'parallel_ai_count_label': 'Nombre d\'IA parallèles:',
            'parallel_ai_count_tooltip': 'Nombre de modèles d\'IA à interroger simultanément (1-2 disponibles, 3-4 à venir)',
            'parallel_ai_notice': 'Remarque: Cela n\'affecte que l\'envoi des questions. Les questions aléatoires utilisent toujours une seule IA.',
            'suggest_maximize': 'Conseil: Maximisez la fenêtre pour une meilleure visualisation avec 3 IAs',
            'ai_panel_label': 'IA {index}:',
            'no_ai_available': 'Aucune IA disponible pour ce panneau',
            'add_more_ai_providers': 'Veuillez ajouter plus de fournisseurs d\'IA dans les paramètres',
            'select_ai': '-- Sélectionner l\'IA --',
            'coming_soon': 'Bientôt disponible',
            'advanced_feature_tooltip': 'Cette fonctionnalité est en cours de développement. Restez à l\'écoute des mises à jour!',

            # Titres de section d'exportation PDF
            'pdf_book_metadata': 'MÉTADONNÉES DU LIVRE',
            'pdf_question': 'QUESTION',
            'pdf_answer': 'RÉPONSE',
            'pdf_ai_model_info': 'INFORMATIONS SUR LE MODÈLE D\'IA',
            'pdf_generated_by': 'GÉNÉRÉ PAR',
            'pdf_provider': 'Fournisseur',
            'pdf_model': 'Modèle',
            'pdf_api_base_url': 'URL de base de l\'API',
            'pdf_panel': 'Panneau',
            'pdf_plugin': 'Plugin',
            'pdf_github': 'GitHub',
            'pdf_software': 'Logiciel',
            'pdf_generated_time': 'Heure de génération',
            'pdf_info_not_available': 'Information non disponible',
        }