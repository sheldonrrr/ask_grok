#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Portuguese language translations for Ask AI Plugin.
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
    def multi_book_default_template(self) -> str:
        return """Aqui está informações sobre vários livros: {books_metadata} Pergunta do usuário: {query} Por favor, responda à pergunta com base nas informações dos livros acima."""
    
    @property
    def translations(self) -> dict:
        return {
            # Informações do plugin
            'plugin_name': 'Ask AI Plugin',
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
            'stop_button': 'Parar',
            'suggest_button': 'Pergunta Aleatória',
            'copy_response': 'Copiar Resposta',
            'copy_question_response': 'Copiar P&R',
            'export_pdf': 'Exportar PDF',
            'export_current_qa': 'Exportar P&R Atual',
            'export_history': 'Exportar Histórico',
            
            # Configurações de exportação
            'export_settings': 'Configurações de Exportação',
            'enable_default_export_folder': 'Exportar para pasta padrão',
            'no_folder_selected': 'Nenhuma pasta selecionada',
            'browse': 'Procurar...',
            'select_export_folder': 'Selecionar Pasta de Exportação',
            
            # Texto dos botões e itens de menu
            'copy_response_btn': 'Copiar Resposta',
            'copy_qa_btn': 'Copiar P&R',
            'export_current_btn': 'Exportar P&R como PDF',
            'export_history_btn': 'Exportar Histórico como PDF',
            'copy_mode_response': 'Resposta',
            'copy_mode_qa': 'P&R',
            'export_mode_current': 'P&R Atual',
            'export_mode_history': 'Histórico',
            
            # Relacionado à exportação de PDF
            'model_provider': 'Provedor',
            'model_name': 'Modelo',
            'model_api_url': 'URL Base da API',
            'pdf_model_info': 'Informações do Modelo de IA',
            'pdf_software': 'Software',
            
            'export_all_history_dialog_title': 'Exportar Todo o Histórico para PDF',
            'export_all_history_title': 'TODO O HISTÓRICO DE P&R',
            'export_history_insufficient': 'São necessários pelo menos 2 registros de histórico para exportar.',
            'history_record': 'Registro',
            'question_label': 'Pergunta',
            'answer_label': 'Resposta',
            'default_ai': 'IA Padrão',
            'export_time': 'Exportado em',
            'total_records': 'Total de Registros',
            'info': 'Informação',
            'yes': 'Sim',
            'no': 'Não',
            'no_book_selected_title': 'Nenhum Livro Selecionado',
            'no_book_selected_message': 'Por favor, selecione um livro antes de fazer perguntas.',
            'set_default_ai_title': 'Definir IA Padrão',
            'set_default_ai_message': 'Você mudou para "{0}". Deseja defini-la como IA padrão para consultas futuras?',
            'set_default_ai_success': 'IA padrão foi definida como "{0}".',
            'copied': 'Copiado!',
            'pdf_exported': 'PDF Exportado!',
            'export_pdf_dialog_title': 'Exportar para PDF',
            'export_pdf_error': 'Erro na Exportação de PDF: {0}',
            'no_question': 'Sem pergunta',
            'no_response': 'Sem resposta',
            'saved': 'Salvo',
            'close_button': 'Fechar',
            'open_local_tutorial': 'Abrir tutorial local',
            'tutorial_open_failed': 'Falha ao abrir o tutorial',
            'tutorial': 'Tutorial',
            
            # UI - Campos de configuração
            'token_label': 'Chave API:',
            'api_key_label': 'Chave API:',
            'model_label': 'Modelo:',
            'language_label': 'Idioma:',
            'language_label_old': 'Idioma',
            'base_url_label': 'URL Base:',
            'base_url_placeholder': 'Padrão: {default_api_base_url}',
            'shortcut': 'Atalho',
            'shortcut_open_dialog': 'Abrir Diálogo',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Modelo',
            'action': 'Ação',
            'reset_button': 'Redefinir',
            'prompt_template': 'Modelo de Prompt',
            'ask_prompts': 'Prompts de Pergunta',
            'random_questions_prompts': 'Prompts de Perguntas Aleatórias',
            'display': 'Visualização',
            
            # UI - Elementos do Diálogo
            'input_placeholder': 'Digite sua pergunta aqui...',
            'response_placeholder': 'Resposta em breve...',
            
            # UI - Itens de Menu
            'menu_title': 'Perguntar',
            'menu_ask': 'Perguntar ao {model}',
            
            # UI - Mensagens de Status
            'loading': 'Carregando...',
            'loading_text': 'Perguntando',
            'save_success': 'Configurações salvas',
            'sending': 'Enviando...',
            'requesting': 'Requisitando',
            'formatting': 'Requisição bem-sucedida, formatando',
            
            # UI - Função de Lista de Modelos
            'load_models': 'Carregar Modelos',
            'use_custom_model': 'Usar nome de modelo personalizado',
            'custom_model_placeholder': 'Digite o nome do modelo personalizado',
            'model_placeholder': 'Por favor, carregue os modelos primeiro',
            'models_loaded': '{count} modelos carregados com sucesso',
            'load_models_failed': 'Falha ao carregar modelos: {error}',
            'model_list_not_supported': 'Este provedor não suporta a busca automática de lista de modelos',
            'api_key_required': 'Por favor, insira a chave API primeiro',
            'invalid_params': 'Parâmetros inválidos',
            'warning': 'Aviso',
            'success': 'Sucesso',
            'error': 'Erro',
            
            # Campos de Metadados
            'metadata_title': 'Título',
            'metadata_authors': 'Autor',
            'metadata_publisher': 'Editora',
            'metadata_pubyear': 'Ano de Publicação',
            'metadata_language': 'Idioma',
            'metadata_series': 'Série',
            'no_metadata': 'Sem metadados',
            'no_series': 'Sem série',
            'unknown': 'Desconhecido',
            
            # Recurso Multi-livros
            'books_unit': ' livros',
            'new_conversation': 'Nova Conversa',
            'single_book': 'Livro Único',
            'multi_book': 'Multi-livros',
            'deleted': 'Excluído',
            'history': 'Histórico',
            'no_history': 'Sem registros de histórico',
            'empty_question_placeholder': '(Sem pergunta)',
            'history_ai_unavailable': 'Esta IA foi removida da configuração',
            'clear_current_book_history': 'Limpar Histórico do Livro Atual',
            'confirm_clear_book_history': 'Tem certeza de que deseja limpar todo o histórico de:\n{book_titles}?',
            'confirm': 'Confirmar',
            'history_cleared': '{deleted_count} registros de histórico limpos.',
            'multi_book_template_label': 'Modelo de Prompt Multi-Livro:',
            'multi_book_placeholder_hint': 'Use {books_metadata} para informações do livro, {query} para a pergunta do usuário',
            
            # Mensagens de Erro
            'network_error': 'Erro de rede',
            'request_timeout': 'Tempo limite da requisição excedido',
            'request_failed': 'Requisição falhou',
            'question_too_long': 'A pergunta é muito longa',
            'auth_token_required_title': 'Chave API Necessária',
            'auth_token_required_message': 'Por favor, defina uma chave API válida na Configuração do Plugin.',
            'open_configuration': 'Abrir Configuração',
            'cancel': 'Cancelar',
            "invalid_default_ai_title": "IA Padrão Inválida",
            "invalid_default_ai_message": "A IA padrão \"{default_ai}\" não está configurada corretamente.\n\nGostaria de mudar para \"{first_ai}\" em vez disso?",
            "switch_to_ai": "Mudar para {ai}",
            "keep_current": "Manter Atual",
            'error_preparing_request': 'Falha ao preparar solicitação',
            'empty_suggestion': 'Sugestão vazia',
            'process_suggestion_error': 'Erro ao processar sugestão',
            'unknown_error': 'Erro desconhecido',
            'unknown_model': 'Modelo desconhecido: {model_name}',
            'suggestion_error': 'Erro de sugestão',
            'random_question_success': 'Pergunta aleatória gerada com sucesso!',
            'book_title_check': 'Título do livro é necessário',
            'avoid_repeat_question': 'Por favor, use uma pergunta diferente',
            'empty_answer': 'Resposta vazia',
            'invalid_response': 'Resposta inválida',
            'auth_error_401': 'Não Autorizado',
            'auth_error_403': 'Acesso Negado',
            'rate_limit': 'Muitas solicitações',
            'invalid_json': 'JSON inválido',
            'template_error': 'Erro de modelo',
            'no_model_configured': 'Nenhum modelo de IA configurado. Por favor, configure um modelo de IA nas configurações.',
            'no_ai_configured_title': 'IA Não Configurada',
            'no_ai_configured_message': 'Bem-vindo! Para começar a fazer perguntas sobre seus livros, você precisa configurar um provedor de IA primeiro.\n\nRecomendado para iniciantes:\n• Nvidia AI - Obtenha 6 meses de acesso API GRATUITO apenas com seu número de telefone (sem cartão de crédito)\n• Ollama - Execute modelos de IA localmente em seu computador (totalmente gratuito e privado)\n\nDeseja abrir a configuração do plugin para configurar um provedor de IA agora?',
            'open_settings': 'Configuração do Plugin',
            'ask_anyway': 'Perguntar Mesmo Assim',
            'later': 'Mais Tarde',
            'reset_all_data': 'Redefinir Todos os Dados',
            'reset_all_data_warning': 'Isso excluirá todas as chaves de API, modelos de prompt e registros de histórico local. Sua preferência de idioma será preservada. Por favor, prossiga com cuidado.',
            'reset_all_data_confirm_title': 'Confirmar Redefinição',
            'reset_all_data_confirm_message': 'Tem certeza de que deseja redefinir o plugin para seu estado inicial?\n\nIsso excluirá permanentemente:\n• Todas as chaves de API\n• Todos os modelos de prompt personalizados\n• Todo o histórico de conversas\n• Todas as configurações do plugin (a preferência de idioma será preservada)\n\nEsta ação não pode ser desfeita!',
            'reset_all_data_success': 'Todos os dados do plugin foram redefinidos com sucesso. Por favor, reinicie o calibre para que as alterações tenham efeito.',
            'reset_all_data_failed': 'Falha ao redefinir dados do plugin: {error}',
            'random_question_error': 'Erro ao gerar pergunta aleatória',
            'clear_history_failed': 'Falha ao limpar histórico',
            'clear_history_not_supported': 'Limpar histórico para livro único ainda não é suportado',
            'missing_required_config': 'Configuração necessária ausente: {key}. Verifique suas configurações.',
            'api_key_too_short': 'A chave API é muito curta. Por favor, verifique e insira a chave completa.',

            # Tratamento de Resposta da API
            'api_request_failed': 'A requisição à API falhou: {error}',
            'api_content_extraction_failed': 'Não foi possível extrair conteúdo da resposta da API',
            'api_invalid_response': 'Não foi recebida uma resposta de API válida',
            'api_unknown_error': 'Erro desconhecido: {error}',
            
            # Tratamento de Resposta de Streaming
            'stream_response_code': 'Código de status da resposta de streaming: {code}',
            'stream_continue_prompt': 'Por favor, continue sua resposta anterior sem repetir o conteúdo já fornecido.',
            'stream_continue_code_blocks': 'Sua resposta anterior tinha blocos de código não fechados. Por favor, continue e complete esses blocos de código.',
            'stream_continue_parentheses': 'Sua resposta anterior tinha parênteses não fechados. Por favor, continue e garanta que todos os parênteses estejam fechados corretamente.',
            'stream_continue_interrupted': 'Sua resposta anterior parece ter sido interrompida. Por favor, continue terminando seu último pensamento ou explicação.',
            'stream_timeout_error': 'A transmissão de streaming não recebeu novo conteúdo por 60 segundos, possivelmente um problema de conexão.',
            
            # Mensagens de Erro da API
            'api_version_model_error': 'Erro de versão da API ou nome do modelo: {message}\n\nPor favor, atualize a URL base da API para "{base_url}" e o modelo para "{model}" ou outro modelo disponível nas configurações.',
            'api_format_error': 'Erro de formato de requisição da API: {message}',
            'api_key_invalid': 'Chave API inválida ou não autorizada: {message}\n\nPor favor, verifique sua chave API e certifique-se de que o acesso à API está ativado.',
            'api_rate_limit': 'Limite de taxa de requisição excedido, tente novamente mais tarde\n\nVocê pode ter excedido sua cota de uso gratuito. Isso pode ser devido a:\n1. Muitas requisições por minuto\n2. Muitas requisições por dia\n3. Muitos tokens de entrada por minuto',
            
            # Erros de Configuração
            'missing_config_key': 'Chave de configuração necessária ausente: {key}',
            'api_base_url_required': 'URL base da API é necessária',
            'model_name_required': 'Nome do modelo é necessário',
            'api_key_empty': 'A chave API está vazia. Por favor, insira uma chave API válida.',
            
            # Busca de Lista de Modelos
            'fetching_models_from': 'Buscando modelos de {url}',
            'successfully_fetched_models': '{count} modelos {provider} buscados com sucesso',
            'failed_to_fetch_models': 'Falha ao buscar modelos: {error}',
            
            # Informações Sobre
            'author_name': 'Sheldon',
            'user_manual': 'Manual do Usuário',
            'about_plugin': 'Por que Ask AI Plugin?',
            'learn_how_to_use': 'Como Usar',
            'email': 'iMessage',
            
            # Configurações Específicas do Modelo
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Personalizado',
            'model_enable_streaming': 'Ativar streaming',
            
            # Seletor de IA
            'current_ai': 'IA Atual',
            'no_configured_models': 'Nenhuma IA configurada - Por favor, configure nas configurações',
            
            # Informações Específicas do Provedor
            'nvidia_free_info': '💡 Novos usuários recebem 6 meses de acesso gratuito à API - Não é necessário cartão de crédito',
            
            # Mensagens de Sistema Gerais
            'default_system_message': 'Você é um especialista em análise de livros. Sua tarefa é ajudar os usuários a entender melhor os livros fornecendo perguntas e análises perspicazes.',

            # Configurações de Tempo Limite da Requisição
            'request_timeout_label': 'Tempo limite da Requisição:',
            'seconds': 'segundos',
            'request_timeout_error': 'Tempo limite da requisição excedido. Tempo limite atual: {timeout} segundos',
            
            # Configurações de IA Paralela
            'parallel_ai_count_label': 'Contagem de IAs Paralelas:',
            'parallel_ai_count_tooltip': 'Número de modelos de IA a serem consultados simultaneamente (1-2 disponíveis, 3-4 em breve)',
            'parallel_ai_notice': 'Nota: Isso afeta apenas o envio de perguntas. Perguntas aleatórias sempre usam uma única IA.',
            'suggest_maximize': 'Dica: Maximize a janela para melhor visualização com 3 IAs',
            'ai_panel_label': 'IA {index}:',
            'no_ai_available': 'Nenhuma IA disponível para este painel',
            'add_more_ai_providers': 'Por favor, adicione mais provedores de IA nas configurações',
            'select_ai': '-- Selecione IA --',
            'select_model': '-- Trocar Modelo --',
            'request_model_list': 'Por favor, solicite a lista de modelos',
            'coming_soon': 'Em Breve',
            'advanced_feature_tooltip': 'Este recurso está em desenvolvimento. Fique ligado para atualizações!',
            
            # Títulos de Seção de Exportação de PDF
            'pdf_book_metadata': 'METADADOS DO LIVRO',
            'pdf_question': 'PERGUNTA',
            'pdf_answer': 'RESPOSTA',
            'pdf_ai_model_info': 'INFORMAÇÕES DO MODELO DE IA',
            'pdf_generated_by': 'GERADO POR',
            'pdf_provider': 'Provedor',
            'pdf_model': 'Modelo',
            'pdf_api_base_url': 'URL Base da API',
            'pdf_panel': 'Painel',
            'pdf_plugin': 'Plugin',
            'pdf_github': 'GitHub',
            'pdf_software': 'Software',
            'pdf_generated_time': 'Hora de Geração',
            'default_ai_mismatch_title': 'IA Padrão Alterada',
            'default_ai_mismatch_message': 'A IA padrão na configuração foi alterada para "{default_ai}",\nmas o diálogo atual está usando "{current_ai}".\n\nDeseja mudar para a nova IA padrão?',
            'discard_changes': 'Descartar Alterações',
            'empty_response': 'Resposta vazia recebida da API',
            'empty_response_after_filter': 'A resposta está vazia após filtrar as tags think',
            'error_401': 'Falha na autenticação da chave API. Verifique: a chave API está correta, a conta tem saldo suficiente, a chave API não expirou.',
            'error_403': 'Acesso negado. Verifique: a chave API tem permissões suficientes, não há restrições de acesso regional.',
            'error_404': 'Endpoint da API não encontrado. Verifique se a configuração da URL base da API está correta.',
            'error_429': 'Muitas solicitações, limite de taxa atingido. Tente novamente mais tarde.',
            'error_5xx': 'Erro do servidor. Tente novamente mais tarde ou verifique o status do provedor de serviços.',
            'error_network': 'Falha na conexão de rede. Verifique a conexão de rede, configurações de proxy ou configuração do firewall.',
            'error_unknown': 'Erro desconhecido.',
            'gemini_geo_restriction': 'A API Gemini não está disponível na sua região. Tente:\n1. Use uma VPN para conectar de uma região suportada\n2. Use outros provedores de IA (OpenAI, Anthropic, DeepSeek, etc.)\n3. Verifique o Google AI Studio para disponibilidade regional',
            'load_models_list': 'Carregar Lista de Modelos',
            'loading_models_text': 'Carregando modelos',
            'model_test_success': 'Teste do modelo bem-sucedido! Configuração salva.',
            'models_loaded_with_selection': '{count} modelos carregados com sucesso.\nModelo selecionado: {model}',
            'ollama_model_not_available': 'O modelo "{model}" não está disponível. Verifique:\n1. O modelo está iniciado? Execute: ollama run {model}\n2. O nome do modelo está correto?\n3. O modelo está baixado? Execute: ollama pull {model}',
            'ollama_service_not_running': 'O serviço Ollama não está em execução. Inicie o serviço Ollama primeiro.',
            'ollama_service_timeout': 'Tempo limite de conexão do serviço Ollama. Verifique se o serviço está funcionando corretamente.',
            'reset_ai_confirm_message': 'Prestes a redefinir {ai_name} para o estado padrão.\n\nIsso limpará:\n• Chave API\n• Nome do modelo personalizado\n• Outros parâmetros configurados\n\nContinuar?',
            'reset_ai_confirm_title': 'Confirmar Redefinição',
            'reset_current_ai': 'Redefinir IA Atual para Padrão',
            'reset_tooltip': 'Redefinir IA atual para valores padrão',
            'save_and_close': 'Salvar e Fechar',
            'skip': 'Pular',
            'technical_details': 'Detalhes Técnicos',
            'test_current_model': 'Testar Modelo Atual',
            'test_model_button': 'Testar Modelo',
            'test_model_prompt': 'Modelos carregados com sucesso! Deseja testar o modelo selecionado "{model}"?',
            'unsaved_changes_message': 'Você tem alterações não salvas. O que deseja fazer?',
            'unsaved_changes_title': 'Alterações Não Salvas',


            'pdf_info_not_available': 'Informação não disponível',
        }