#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Portuguese language translations for Ask Grok plugin.
"""

from ..models.base import BaseTranslation, TranslationRegistry, AIProvider


@TranslationRegistry.register
class PortugueseTranslation(BaseTranslation):
    """Portuguese language translation."""
    
    @property
    def code(self) -> str:
        return "pt"
    
    @property
    def name(self) -> str:
        return "Português"
    
    @property
    def default_template(self) -> str:
        return 'Sobre o livro "{title}": Autor: {author}, Editora: {publisher}, Ano de publicação: {pubyear}, livro em language: {language}, Série: {series}, Minha pergunta é: {query}'
    
    @property
    def suggestion_template(self) -> str:
        return """Você é um especialista em resenhas de livros. Para o livro "{title}" de {author}, publicação idioma é {language}, gere UMA pergunta perspicaz que ajude os leitores a entender melhor o livro. Regras: 1. Retorne APENAS a pergunta, sem introdução ou explicação 2. Concentre-se no conteúdo do livro, não apenas no título 3. Faça a pergunta prática e reflexiva 4. Mantenha-a breve (30-200 palavras) 5. Seja criativo e gere uma pergunta diferente cada vez, mesmo para o mesmo livro"""
    
    @property
    def translations(self) -> dict:
        return {
            # Informações do plugin
            'plugin_name': 'Ask Grok',
            'plugin_desc': 'Faça perguntas sobre um livro usando IA',
            
            # UI - Abas e seções
            'config_title': 'Configuração',
            'general_tab': 'Geral',
            'ai_models': 'IA',
            'shortcuts': 'Atalhos',
            'about': 'Sobre',
            'metadata': 'Metadados',
            
            # UI - Botões e ações
            'ok_button': 'OK',
            'save_button': 'Salvar',
            'send_button': 'Enviar',
            'suggest_button': 'Pergunta Aleatória',
            'copy_response': 'Copiar Resposta',
            'copy_question_response': 'Copiar P&&R',
            'copied': 'Copiado!',
            
            # UI - Campos de configuração
            'token_label': 'Chave API:',
            'model_label': 'Modelo:',
            'language_label': 'Idioma',
            'base_url_label': 'URL Base:',
            'base_url_placeholder': 'Padrão: {default_api_base_url}',
            'shortcut': 'Tecla de Atalho',
            'shortcut_open_dialog': 'Abrir Diálogo',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Modelo',
            'current_ai': 'IA Atual:',
            'action': 'Ação',
            'reset_button': 'Redefinir',
            'prompt_template': 'Modelo de Prompt',
            'ask_prompts': 'Prompts de Perguntas',
            'random_questions_prompts': 'Prompts de Perguntas Aleatórias',
            'display': 'Exibir',
            
            # UI - Elementos de diálogo
            'input_placeholder': 'Digite sua pergunta...',
            'response_placeholder': 'Resposta em breve...',
            
            # UI - Itens de menu
            'menu_title': 'Perguntar',
            'menu_ask': 'Perguntar ao {model}',
            
            # UI - Mensagens de status
            'loading': 'Carregando',
            'loading_text': 'Perguntando',
            'save_success': 'Configurações salvas',
            'sending': 'Enviando...',
            'requesting': 'Solicitando',
            'formatting': 'Solicitação bem-sucedida, formatando',
            
            # Campos de metadados
            'metadata_title': 'Título',
            'metadata_authors': 'Autor',
            'metadata_publisher': 'Editora',
            'metadata_pubyear': 'Data de Publicação',
            'metadata_language': 'Idioma',
            'metadata_series': 'Série',
            'no_metadata': 'Sem metadados',
            'no_series': 'Sem série',
            'unknown': 'Desconhecido',
            
            # Mensagens de erro
            'error': 'Erro: ',
            'network_error': 'Erro de conexão',
            'request_timeout': 'Tempo limite da solicitação',
            'request_failed': 'Falha na solicitação',
            'question_too_long': 'Pergunta muito longa',
            'auth_token_required_title': 'Chave API Necessária',
            'auth_token_required_message': 'Por favor, defina a chave API nas configurações',
            'error_preparing_request': 'Erro ao preparar solicitação',
            'empty_suggestion': 'Sugestão vazia',
            'process_suggestion_error': 'Erro ao processar sugestão',
            'unknown_error': 'Erro desconhecido',
            'unknown_model': 'Modelo desconhecido: {model_name}',
            'suggestion_error': 'Erro de sugestão',
            'book_title_check': 'Título do livro necessário',
            'avoid_repeat_question': 'Por favor, use uma pergunta diferente',
            'empty_answer': 'Resposta vazia',
            'invalid_response': 'Resposta inválida',
            'auth_error_401': 'Não autorizado',
            'auth_error_403': 'Acesso negado',
            'rate_limit': 'Muitas solicitações',
            'invalid_json': 'JSON inválido',
            'no_response': 'Sem resposta',
            'template_error': 'Erro de modelo',
            'no_model_configured': 'Nenhum modelo de IA configurado. Por favor, configure um modelo de IA nas configurações.',
            'random_question_error': 'Erro ao gerar pergunta aleatória',
            'clear_history_failed': 'Falha ao limpar histórico',
            'clear_history_not_supported': 'Limpar histórico para um único livro ainda não é suportado',
            
            # Informações sobre
            'author_name': 'Sheldon',
            'user_manual': 'Manual do Usuário',
            'about_plugin': 'Por que Ask Grok?',
            'learn_how_to_use': 'Como Usar',
            'email': 'iMessage',
            
            # Configurações específicas do modelo
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Personalizado',
        }
