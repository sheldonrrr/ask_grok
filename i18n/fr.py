#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
French language translations for Ask Grok plugin.
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
    def translations(self) -> dict:
        return {
            # Informations sur le plugin
            'plugin_name': 'Ask Grok',
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
            'suggest_button': 'Question Aléatoire',
            'copy_response': 'Copier la Réponse',
            'copy_question_response': 'Copier Q&&R',
            'copied': 'Copié!',
            'saved': 'Enregistré',
            'close_button': 'Fermer',
            
            # UI - Champs de configuration
            'token_label': 'Clé API:',
            'model_label': 'Modèle:',
            'language_label': 'Langue',
            'base_url_label': 'URL de Base:',
            'base_url_placeholder': 'Par défaut: {default_api_base_url}',
            'shortcut': 'Touche de Raccourci',
            'shortcut_open_dialog': 'Ouvrir la Boîte de Dialogue',
            'shortcut_enter': 'Ctrl + Entrée',
            'shortcut_return': 'Command + Retour',
            'using_model': 'Modèle',
            'current_ai': 'IA Actuelle:',
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
            'loading': 'Chargement',
            'loading_text': 'Demande en cours',
            'save_success': 'Paramètres enregistrés',
            'sending': 'Envoi en cours...',
            'requesting': 'Requête en cours',
            'formatting': 'Requête réussie, formatage en cours',
            
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
            
            # Messages d'erreur
            'error': 'Erreur: ',
            'network_error': 'Erreur de connexion',
            'request_timeout': 'Délai de requête dépassé',
            'request_failed': 'Échec de la requête',
            'question_too_long': 'Question trop longue',
            'auth_token_required_title': 'Clé API Requise',
            'auth_token_required_message': 'Veuillez définir la clé API dans la Configuration du Plugin',
            'error_preparing_request': 'Échec de préparation de la requête',
            'empty_suggestion': 'Suggestion vide',
            'process_suggestion_error': 'Erreur de traitement de suggestion',
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
            'rate_limit': 'Trop de requêtes',
            'invalid_json': 'JSON invalide',
            'no_response': 'Pas de réponse',
            'template_error': 'Erreur de modèle',
            'no_model_configured': 'Aucun modèle d\'IA configuré. Veuillez configurer un modèle d\'IA dans les paramètres.',
            'random_question_error': 'Erreur lors de la génération d\'une question aléatoire',
            'clear_history_failed': 'Échec de l\'effacement de l\'historique',
            'clear_history_not_supported': 'L\'effacement de l\'historique pour un seul livre n\'est pas encore pris en charge',
            'missing_required_config': 'Configuration requise manquante: {key}. Veuillez vérifier vos paramètres.',
            'api_key_too_short': 'La clé API est trop courte. Veuillez vérifier et saisir la clé complète.',
            
            # Traitement des réponses API
            'api_request_failed': 'Échec de la requête API: {error}',
            'api_content_extraction_failed': 'Impossible d\'extraire le contenu de la réponse API',
            'api_invalid_response': 'Impossible d\'obtenir une réponse API valide',
            'api_unknown_error': 'Erreur inconnue: {error}',
            
            # Traitement des réponses en streaming
            'stream_response_code': 'Code d\'état de réponse en streaming: {code}',
            'stream_continue_prompt': 'Veuillez continuer votre réponse précédente sans répéter le contenu déjà fourni.',
            'stream_continue_code_blocks': 'Votre réponse précédente contenait des blocs de code non fermés. Veuillez continuer et compléter ces blocs de code.',
            'stream_continue_parentheses': 'Votre réponse précédente contenait des parenthèses non fermées. Veuillez continuer et vous assurer que toutes les parenthèses sont correctement fermées.',
            'stream_continue_interrupted': 'Votre réponse précédente semble avoir été interrompue. Veuillez continuer à compléter votre dernière pensée ou explication.',
            'stream_timeout_error': 'La transmission en streaming n\'a pas reçu de nouveau contenu pendant 60 secondes, peut-être un problème de connexion.',
            
            # Messages d\'erreur API
            'api_version_model_error': 'Erreur de version API ou de nom de modèle: {message}\n\nVeuillez mettre à jour l\'URL de base API à "{base_url}" et le modèle à "{model}" ou un autre modèle disponible dans les paramètres.',
            'api_format_error': 'Erreur de format de requête API: {message}',
            'api_key_invalid': 'Clé API invalide ou non autorisée: {message}\n\nVeuillez vérifier votre clé API et vous assurer que l\'accès API est activé.',
            'api_rate_limit': 'Limite de fréquence de requêtes dépassée, veuillez réessayer plus tard\n\nVous avez peut-être dépassé le quota d\'utilisation gratuite. Cela pourrait être dû à:\n1. Trop de requêtes par minute\n2. Trop de requêtes par jour\n3. Trop de jetons d\'entrée par minute',
            
            # Erreurs de configuration
            'missing_config_key': 'Clé de configuration requise manquante: {key}',
            'api_base_url_required': 'URL de base API requise',
            'model_name_required': 'Nom du modèle requis',
            'api_key_empty': 'La clé API est vide. Veuillez saisir une clé API valide.',
            
            # Informations sur À propos
            'author_name': 'Sheldon',
            'user_manual': 'Manuel d\'Utilisateur',
            'about_plugin': 'Pourquoi Ask Grok?',
            'learn_how_to_use': 'Comment Utiliser',
            'email': 'iMessage',
            
            # Configurations spécifiques au modèle
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Personnalisé',
            'model_enable_streaming': 'Activer le streaming',
            'model_disable_ssl_verify': 'Désactiver la vérification SSL',
            
            # Messages système communs
            'default_system_message': 'Vous êtes un expert en analyse de livres. Votre tâche est d\'aider les utilisateurs à mieux comprendre les livres en fournissant des questions et des analyses perspicaces.',
        }
