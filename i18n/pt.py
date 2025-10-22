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
            'saved': 'Salvo',
            'close_button': 'Fechar',
            
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
            
            # UI - Função de lista de modelos
            'load_models': 'Carregar modelos',
            'use_custom_model': 'Usar nome de modelo personalizado',
            'custom_model_placeholder': 'Digite o nome do modelo personalizado',
            'model_placeholder': 'Por favor, carregue os modelos primeiro',
            'models_loaded': '{count} modelos carregados com sucesso',
            'load_models_failed': 'Falha ao carregar modelos: {error}',
            'model_list_not_supported': 'Este provedor não suporta busca automática de lista de modelos',
            'api_key_required': 'Por favor, insira a chave API primeiro',
            'invalid_params': 'Parâmetros inválidos',
            'warning': 'Aviso',
            'success': 'Sucesso',
            
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
            'auth_token_required_message': 'Por favor, defina a chave API na Configuração do Plugin',
            'error_preparing_request': 'Erro ao preparar solicitação',
            'empty_suggestion': 'Sugestão vazia',
            'process_suggestion_error': 'Erro ao processar sugestão',
            'unknown_error': 'Erro desconhecido',
            'unknown_model': 'Modelo desconhecido: {model_name}',
            'suggestion_error': 'Erro de sugestão',
            'random_question_success': 'Pergunta aleatória gerada com sucesso!',
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
            'missing_required_config': 'Configuração necessária ausente: {key}. Verifique suas configurações.',
            'api_key_too_short': 'Chave API muito curta. Verifique e insira a chave completa.',
            
            # Processamento de resposta da API
            'api_request_failed': 'Falha na solicitação da API: {error}',
            'api_content_extraction_failed': 'Não foi possível extrair conteúdo da resposta da API',
            'api_invalid_response': 'Não recebeu uma resposta válida da API',
            'api_unknown_error': 'Erro desconhecido: {error}',
            
            # Processamento de resposta de streaming
            'stream_response_code': 'Código de status da resposta de streaming: {code}',
            'stream_continue_prompt': 'Continue com sua resposta anterior sem repetir o conteúdo já fornecido.',
            'stream_continue_code_blocks': 'Sua resposta anterior tinha blocos de código não fechados. Continue e complete esses blocos de código.',
            'stream_continue_parentheses': 'Sua resposta anterior tinha parênteses não fechados. Continue e certifique-se de que todos os parênteses sejam fechados corretamente.',
            'stream_continue_interrupted': 'Sua resposta anterior parece ter sido interrompida. Continue e complete seu último pensamento ou explicação.',
            'stream_timeout_error': 'A transmissão de streaming não recebeu novo conteúdo por 60 segundos, possivelmente um problema de conexão.',
            
            # Mensagens de erro da API
            'api_version_model_error': 'Erro de versão da API ou nome do modelo: {message}\n\nAtualize a URL base da API para "{base_url}" e o modelo para "{model}" ou outro modelo disponível nas configurações.',
            'api_format_error': 'Erro de formato da solicitação da API: {message}',
            'api_key_invalid': 'Chave API inválida ou não autorizada: {message}\n\nVerifique sua chave API e certifique-se de que o acesso à API esteja ativado.',
            'api_rate_limit': 'Limite de solicitações excedido, tente novamente mais tarde\n\nVocê pode ter excedido sua cota de uso gratuito. Isso pode ser devido a:\n1. Muitas solicitações por minuto\n2. Muitas solicitações por dia\n3. Muitos tokens de entrada por minuto',
            
            # Erros de configuração
            'missing_config_key': 'Chave de configuração necessária ausente: {key}',
            'api_base_url_required': 'URL base da API é necessária',
            'model_name_required': 'Nome do modelo é necessário',
            'api_key_empty': 'A chave API está vazia. Por favor, insira uma chave API válida.',
            
            # Busca de lista de modelos
            'fetching_models_from': 'Buscando modelos de {url}',
            'successfully_fetched_models': '{count} modelos {provider} buscados com sucesso',
            'failed_to_fetch_models': 'Falha ao buscar modelos: {error}',
            
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
            'model_enable_streaming': 'Ativar streaming',
            'model_disable_ssl_verify': 'Desativar verificação SSL',
            
            # Mensagens de sistema gerais
            'default_system_message': 'Você é um especialista em análise de livros. Sua tarefa é ajudar os usuários a entender melhor os livros fornecendo perguntas e análises perspicazes.',
        }
