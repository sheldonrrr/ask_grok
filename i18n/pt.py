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
        return 'Contexto: Você está auxiliando um usuário do calibre (http://calibre-ebook.com), um poderoso aplicativo de gerenciamento de e-books, através do plugin "Ask AI Plugin". Este plugin permite que os usuários façam perguntas sobre livros em sua biblioteca calibre. Nota: Este plugin só pode responder perguntas sobre o conteúdo, temas ou tópicos relacionados do livro selecionado - não pode modificar diretamente os metadados do livro nem executar operações do calibre. Informações do livro: Título: "{title}", Autor: {author}, Editora: {publisher}, Ano de Publicação: {pubyear}, Idioma: {language}, Série: {series}. Pergunta do usuário: {query}. Por favor, forneça uma resposta útil com base nas informações do livro e seu conhecimento.'

    @property
    def suggestion_template(self) -> str:
        return """Você é um revisor de livros especialista. Para o livro "{title}" de {author}, o idioma de publicação é {language}, gere UMA pergunta perspicaz que ajude os leitores a compreenderem melhor as ideias centrais do livro, aplicações práticas ou perspectivas únicas. Regras: 1. Retorne APENAS a pergunta, sem qualquer introdução ou explicação 2. Foque na substância do livro, não apenas no título 3. Faça a pergunta prática e que incite a reflexão 4. Mantenha-a concisa (30-200 palavras) 5. Seja criativo e gere uma pergunta diferente a cada vez, mesmo para o mesmo livro"""

    @property
    def multi_book_default_template(self) -> str:
        return """Aqui está a informação sobre vários livros: {books_metadata} Pergunta do usuário: {query} Por favor, responda à pergunta com base nas informações dos livros acima."""

    @property
    def translations(self) -> dict:
        return {
            # Plugin information
            'plugin_name': 'Plugin Perguntar à IA',
            'plugin_desc': 'Faça perguntas sobre um livro usando IA',

            # UI - Tabs and sections
            'config_title': 'Configuração',
            'general_tab': 'Geral',
            'ai_models': 'Provedores de IA',
            'shortcuts': 'Atalhos',
            'shortcuts_note': "Você pode personalizar estes atalhos no calibre: Preferências -> Atalhos (pesquise 'Ask AI').\nEsta página mostra os atalhos padrão/exemplo. Se você os alterou em Atalhos, as configurações do calibre têm precedência.",
            'prompts_tab': 'Prompts',
            'about': 'Sobre',
            'metadata': 'Metadados',

            # Section subtitles
            'language_settings': 'Idioma',
            'language_subtitle': 'Escolha seu idioma de interface preferido',
            'ai_providers_subtitle': 'Configure os provedores de IA e selecione sua IA padrão',
            'prompts_subtitle': 'Personalize como as perguntas são enviadas à IA',
            'export_settings_subtitle': 'Defina a pasta padrão para exportar PDFs',
            'reset_all_data_subtitle': 'Aviso: Isso excluirá permanentemente todas as suas configurações e dados',

            # Prompts tab
            'language_preference_title': 'Preferência de idioma',
            'language_preference_subtitle': 'Controla se as respostas da IA devem corresponder ao idioma da sua interface',
            'prompt_templates_title': 'Modelos de Prompt',
            'prompt_templates_subtitle': 'Personalize como as informações do livro são enviadas à IA usando campos dinâmicos como {title}, {author}, {query}',
            'ask_prompts': 'Prompts de Pergunta',
            'random_questions_prompts': 'Prompts de Perguntas Aleatórias',
            'multi_book_prompts_label': 'Prompts de Múltiplos Livros',
            'multi_book_placeholder_hint': 'Use {books_metadata} para informações do livro, {query} para a pergunta do usuário',
            'dynamic_fields_title': 'Referência de Campos Dinâmicos',
            'dynamic_fields_subtitle': 'Campos disponíveis e valores de exemplo de "Frankenstein" de Mary Shelley',
            'dynamic_fields_examples': '<b>{title}</b> → Frankenstein<br><b>{author}</b> → Mary Shelley<br><b>{publisher}</b> → Lackington, Hughes, Harding, Mavor & Jones<br><b>{pubyear}</b> → 1818<br><b>{language}</b> → Inglês<br><b>{series}</b> → (nenhum)<br><b>{query}</b> → Seu texto de pergunta',
            'reset_prompts': 'Redefinir Prompts para Padrão',
            'reset_prompts_confirm': 'Tem certeza de que deseja redefinir todos os modelos de prompt para seus valores padrão? Esta ação não pode ser desfeita.',
            'unsaved_changes_title': 'Alterações Não Salvas',
            'unsaved_changes_message': 'Você tem alterações não salvas na guia Prompts. Deseja salvá-las?',
            'use_interface_language': 'Sempre pedir à IA para responder no idioma atual da interface do plugin',
            'language_instruction_label': 'Instrução de idioma adicionada aos prompts:',
            'language_instruction_text': 'Por favor, responda em {language_name}.',

            # Persona settings
            'persona_title': 'Persona',
            'persona_subtitle': 'Defina seu histórico e objetivos de pesquisa para ajudar a IA a fornecer respostas mais relevantes',
            'use_persona': 'Usar persona',
            'persona_label': 'Persona',
            'persona_placeholder': 'Como pesquisador, quero pesquisar dados de livros.',
            'persona_hint': 'Quanto mais a IA souber sobre seu objetivo e histórico, melhor será a pesquisa ou geração.',

            # UI - Buttons and actions
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
            'export_all_history_dialog_title': 'Exportar Todo o Histórico para PDF',
            'export_all_history_title': 'TODO O HISTÓRICO DE P&R',
            'export_history_insufficient': 'Necessário pelo menos 2 registros de histórico para exportar.',
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
            'set_default_ai_message': 'Você mudou para "{0}". Deseja defini-lo como a IA padrão para futuras consultas?',
            'set_default_ai_success': 'A IA padrão foi definida como "{0}".',
            'default_ai_mismatch_title': 'IA Padrão Alterada',
            'default_ai_mismatch_message': 'A IA padrão na configuração foi alterada para "{default_ai}",\nmas o diálogo atual está usando "{current_ai}".\n\nDeseja mudar para a nova IA padrão?',
            'copied': 'Copiado!',
            'pdf_exported': 'PDF Exportado!',
            'export_pdf_dialog_title': 'Exportar para PDF',
            'export_pdf_error': 'Falha ao exportar PDF: {0}',
            'no_question': 'Nenhuma pergunta',
            'no_response': 'Nenhuma resposta',
            'saved': 'Salvo',
            'close_button': 'Fechar',
            'open_local_tutorial': 'Abrir Tutorial Local',
            'tutorial_open_failed': 'Falha ao abrir tutorial',
            'tutorial': 'Tutorial',

            'model_display_name_perplexity': 'Perplexity',

            # UI - Configuration fields
            'token_label': 'Chave API:',
            'api_key_label': 'Chave API:',
            'model_label': 'Modelo:',
            'language_label': 'Idioma:',
            'language_label_old': 'Idioma',
            'base_url_label': 'URL Base:',
            'base_url_placeholder': 'Padrão: {default_api_base_url}',
            'shortcut': 'Tecla de Atalho',
            'shortcut_open_dialog': 'Abrir Diálogo',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Modelo',
            'action': 'Ação',
            'reset_button': 'Redefinir para Padrão',
            'reset_current_ai': 'Redefinir IA Atual para Padrão',
            'reset_ai_confirm_title': 'Confirmar Redefinição',
            'reset_ai_confirm_message': 'Prestes a redefinir {ai_name} para o estado padrão.\n\nIsso limpará:\n• Chave API\n• Nome de modelo personalizado\n• Outros parâmetros configurados\n\nContinuar?',
            'reset_tooltip': 'Redefinir IA atual para valores padrão',
            'unsaved_changes_title': 'Alterações Não Salvas',
            'unsaved_changes_message': 'Você tem alterações não salvas. O que gostaria de fazer?',
            'save_and_close': 'Salvar e Fechar',
            'discard_changes': 'Descartar Alterações',
            'cancel': 'Cancelar',
            'yes_button': 'Sim',
            'no_button': 'Não',
            'cancel_button': 'Cancelar',
            'invalid_default_ai_title': 'IA Padrão Inválida',
            'invalid_default_ai_message': 'A IA padrão "{default_ai}" não está configurada corretamente.\n\nGostaria de mudar para "{first_ai}"?',
            'switch_to_ai': 'Mudar para {ai}',
            'keep_current': 'Manter Atual',
            'prompt_template': 'Modelo de Prompt',
            'ask_prompts': 'Prompts de Pergunta',
            'random_questions_prompts': 'Prompts de Perguntas Aleatórias',
            'display': 'Exibir',
            'export_settings': 'Configurações de Exportação',
            'enable_default_export_folder': 'Exportar para pasta padrão',
            'no_folder_selected': 'Nenhuma pasta selecionada',
            'browse': 'Procurar...',
            'select_export_folder': 'Selecionar Pasta de Exportação',

            # Button text and menu items
            'copy_response_btn': 'Copiar Resposta',
            'copy_qa_btn': 'Copiar P&R',
            'export_current_btn': 'Exportar P&R como PDF',
            'export_history_btn': 'Exportar Histórico como PDF',
            'copy_mode_response': 'Resposta',
            'copy_mode_qa': 'P&R',
            'copy_format_plain': 'Texto simples',
            'copy_format_markdown': 'Markdown',
            'export_mode_current': 'P&R Atual',
            'export_mode_history': 'Histórico',

            # PDF Export related
            'model_provider': 'Provedor',
            'model_name': 'Modelo',
            'model_api_url': 'URL Base da API',
            'pdf_model_info': 'Informações do Modelo de IA',
            'pdf_software': 'Software',

            # UI - Dialog elements
            'input_placeholder': 'Digite sua pergunta...',
            'response_placeholder': 'Resposta em breve...',  # Placeholder for all models

            # UI - Menu items
            'menu_title': 'Perguntar à IA',
            'menu_ask': 'Perguntar',

            # UI - Status information
            'loading': 'Carregando',
            'loading_text': 'Perguntando',
            'loading_models_text': 'Carregando modelos',
            'save_success': 'Configurações salvas',
            'sending': 'Enviando...',
            'requesting': 'Solicitando',
            'formatting': 'Solicitação bem-sucedida, formatando',

            # UI - Model list feature
            'load_models': 'Carregar Modelos',
            'load_models_list': 'Carregar Lista de Modelos',
            'test_current_model': 'Testar Modelo Atual',
            'use_custom_model': 'Usar nome de modelo personalizado',
            'custom_model_placeholder': 'Digite o nome do modelo personalizado',
            'model_placeholder': 'Por favor, carregue os modelos primeiro',
            'models_loaded': 'Carregados {count} modelos com sucesso',
            'models_loaded_with_selection': 'Carregados {count} modelos com sucesso.\nModelo selecionado: {model}',
            'load_models_failed': 'Falha ao carregar modelos: {error}',
            'model_list_not_supported': 'Este provedor não suporta a busca automática da lista de modelos',
            'api_key_required': 'Por favor, digite a Chave API primeiro',
            'invalid_params': 'Parâmetros inválidos',
            'warning': 'Aviso',
            'success': 'Sucesso',
            'error': 'Erro',
            'error_opening_dialog': 'Erro ao abrir diálogo:',
            'skipped_books_warning': '{count} livro(s) ignorado(s) devido a erros de acesso a arquivos.\nIsso pode ser causado por caracteres inválidos nos caminhos dos arquivos ou arquivos bloqueados por outro programa.',
            'failed_to_read_all_books': 'Falha ao ler metadados de todos os livros selecionados.\nIsso pode ser causado por caracteres inválidos nos caminhos dos arquivos ou arquivos bloqueados por outro programa.',
            'error_starting_request': 'Erro ao iniciar solicitação',
            'default_ai_mismatch_title': 'IA padrão alterada',
            'default_ai_mismatch_message': 'A IA padrão na configuração foi alterada para "{default_ai}",\nmas a conversa atual está usando "{current_ai}".\n\nDeseja mudar para a nova IA padrão?',

            # Metadata fields
            'metadata_title': 'Título',
            'metadata_authors': 'Autor',
            'metadata_publisher': 'Editora',
            'metadata_pubdate': 'Data de Publicação',
            'metadata_pubyear': 'Ano de Publicação',
            'metadata_language': 'Idioma',
            'metadata_series': 'Série',
            'no_metadata': 'Sem metadados',
            'no_series': 'Sem série',
            'unknown': 'Desconhecido',

            # Multi-book feature
            'books_unit': ' livros',
            'new_conversation': 'Nova Conversa',
            'single_book': 'Livro Único',
            'multi_book': 'Múltiplos Livros',
            'deleted': 'Excluído',
            'history': 'Histórico',
            'no_history': 'Nenhum registro de histórico',
            'empty_question_placeholder': '(Nenhuma pergunta)',
            'history_ai_unavailable': 'Esta IA foi removida da configuração',
            'clear_current_book_history': 'Limpar Histórico do Livro Atual',
            'confirm_clear_book_history': 'Tem certeza de que deseja limpar todo o histórico para:\n{book_titles}?',
            'confirm': 'Confirmar',
            'history_cleared': '{deleted_count} registros de histórico limpos.',
            'multi_book_template_label': 'Modelo de Prompt de Múltiplos Livros:',
            'multi_book_placeholder_hint': 'Use {books_metadata} para informações do livro, {query} para a pergunta do usuário',

            # Error messages (Note: 'error' is already defined above, these are other error types)
            'network_error': 'Erro de conexão',
            'request_timeout': 'Tempo limite da solicitação',
            'request_failed': 'Solicitação falhou',
            'request_stopped': 'Solicitação interrompida',
            'question_too_long': 'Pergunta muito longa',
            'question_too_long_detail': (
                'O prompt é muito longo ({current} caracteres, limite {limit}, excede em {over}). '
                'Você selecionou {book_count} livro(s).'
            ),
            'question_too_long_detail_library': (
                'O prompt é muito longo ({current} caracteres, limite {limit}, excede em {over}). '
                'O índice da sua biblioteca contém {book_count} livro(s).'
            ),
            'question_too_long_hint_ai_search': (
                'Para pesquisas em toda a biblioteca, use AI Search (pergunte sem selecionar livros '
                'ou use o menu AI Search) em vez de selecionar muitos livros.'
            ),
            'question_too_long_hint_library_search': (
                'O índice da biblioteca excede o limite de prompt atual. Ative Limite de comprimento '
                'de prompt personalizado em Configuração do plugin → General (sugestão: 524288 '
                'caracteres), ou faça uma pergunta mais específica.'
            ),
            'question_too_long_reduce_books': (
                'Para comparar um conjunto menor em profundidade, tente desmarcar cerca de {count} livro(s).'
            ),
            'question_too_long_hint_default': (
                'Limite padrão atual: {limit} caracteres ({mode}). '
                'Padrão para um livro: 128.000; para vários livros: 256.000. '
                'Usuários avançados podem ativar um limite personalizado em '
                'Configuração do plugin → General.'
            ),
            'question_too_long_hint_custom': (
                'Você ativou um limite de prompt personalizado. Se as solicitações expirarem, '
                'reduza o limite em Configuração do plugin → General, selecione menos livros '
                'ou faça uma pergunta mais específica.'
            ),
            'large_selection_dialog_title': 'Muitos livros selecionados',
            'large_selection_dialog_message': (
                'Você selecionou {count} livros. Para perguntas em toda a biblioteca, AI Search '
                'funciona melhor e pesquisa toda a biblioteca com metadados compactos.\n\n'
                'Mudar para AI Search ou continuar com os livros selecionados em formato compacto?'
            ),
            'large_selection_use_ai_search': 'Usar AI Search',
            'large_selection_continue': 'Continuar com a seleção',
            'multi_book_truncation_note': (
                'Nota: devido ao limite de prompt, apenas os primeiros {included} de {total} livros '
                'selecionados estão incluídos. Use AI Search para consultar toda a biblioteca ou '
                'aumente o limite personalizado em Configuração do plugin → General.'
            ),
            'library_metadata_truncation_note': (
                'Nota: devido ao limite de prompt, apenas os primeiros {included} de {total} livros '
                'indexados estão incluídos. Os resultados podem estar incompletos para bibliotecas '
                'muito grandes, a menos que aumente o limite personalizado em '
                'Configuração do plugin → General.'
            ),
            'auth_token_required_title': 'Serviço de IA Necessário',
            'auth_token_required_message': 'Por favor, configure um serviço de IA válido na Configuração do Plugin.',
            'open_configuration': 'Abrir Configuração',
            'error_preparing_request': 'Falha ao preparar a solicitação',
            'empty_suggestion': 'Sugestão vazia',
            'process_suggestion_error': 'Erro no processamento da sugestão',
            'unknown_error': 'Erro desconhecido',
            'unknown_model': 'Modelo desconhecido: {model_name}',
            'suggestion_error': 'Erro de sugestão',
            'random_question_success': 'Pergunta aleatória gerada com sucesso!',
            'book_title_check': 'Título do livro obrigatório',
            'avoid_repeat_question': 'Por favor, use uma pergunta diferente',
            'empty_answer': 'Resposta vazia',
            'invalid_json': 'JSON inválido',
            'invalid_response': 'Resposta inválida',
            'auth_error_401': 'Não autorizado',
            'auth_error_403': 'Acesso negado',
            'rate_limit': 'Muitas solicitações',
            'empty_response': 'Recebeu resposta vazia da API',
            'empty_response_after_filter': 'A resposta está vazia após filtrar as tags de pensamento',
            'no_response': 'Nenhuma resposta',
            'template_error': 'Erro de modelo',
            'no_model_configured': 'Nenhum modelo de IA configurado. Por favor, configure um modelo de IA nas configurações.',
            'no_ai_configured_title': 'Nenhuma IA Configurada',
            'no_ai_configured_message': 'Bem-vindo(a)! Para começar a fazer perguntas sobre seus livros, você precisa configurar um provedor de IA primeiro.\n\nBoas Notícias: Este plugin agora tem um nível GRATUITO (Nvidia AI Free) que você pode usar imediatamente sem qualquer configuração!\n\nOutras Opções Recomendadas:\n• Nvidia AI - Obtenha 6 meses de acesso GRATUITO à API apenas com seu número de telefone (não é necessário cartão de crédito)\n• Ollama - Execute modelos de IA localmente em seu computador (totalmente gratuito e privado)\n\nDeseja abrir a configuração do plugin para configurar um provedor de IA agora?',
            'open_settings': 'Configuração do Plugin',
            'ask_anyway': 'Perguntar Mesmo Assim',
            'later': 'Mais Tarde',
            'reset_all_data': 'Redefinir Todos os Dados',
            'reset_all_data_warning': 'Isso excluirá todas as Chaves API, modelos de prompt e registros de histórico local. Sua preferência de idioma será preservada. Prossiga com cautela.',
            'reset_all_data_confirm_title': 'Confirmar Redefinição',
            'reset_all_data_confirm_message': 'Tem certeza de que deseja redefinir o plugin para o estado inicial?\n\nIsso excluirá permanentemente:\n• Todas as Chaves API\n• Todos os modelos de prompt personalizados\n• Todo o histórico de conversas\n• Todas as configurações do plugin (a preferência de idioma será preservada)\n\nEsta ação não pode ser desfeita!',
            'reset_all_data_success': 'Todos os dados do plugin foram redefinidos com sucesso. Por favor, reinicie o calibre para que as alterações entrem em vigor.',
            'reset_all_data_failed': 'Falha ao redefinir os dados do plugin: {error}',
            'random_question_error': 'Erro ao gerar pergunta aleatória',
            'clear_history_failed': 'Falha ao limpar histórico',
            'clear_history_not_supported': 'Limpar histórico para um único livro ainda não é suportado',
            'missing_required_config': 'Configuração obrigatória ausente: {key}. Por favor, verifique suas configurações.',
            'api_key_too_short': 'A Chave API é muito curta. Por favor, verifique e digite a chave completa.',

            # API response handling
            'api_request_failed': 'A solicitação da API falhou: {error}',
            'api_content_extraction_failed': 'Não foi possível extrair conteúdo da resposta da API',
            'api_invalid_response': 'Não foi possível obter uma resposta de API válida',
            'api_unknown_error': 'Erro desconhecido: {error}',

            # Stream response handling
            'stream_response_code': 'Código de status da resposta do stream: {code}',
            'stream_continue_prompt': 'Por favor, continue sua resposta anterior sem repetir o conteúdo já fornecido.',
            'stream_continue_code_blocks': 'Sua resposta anterior tinha blocos de código não fechados. Por favor, continue e complete esses blocos de código.',
            'stream_continue_parentheses': 'Sua resposta anterior tinha parênteses não fechados. Por favor, continue e certifique-se de que todos os parênteses estejam corretamente fechados.',
            'stream_continue_interrupted': 'Sua resposta anterior parece ter sido interrompida. Por favor, continue completando seu último pensamento ou explicação.',
            'stream_timeout_error': 'A transmissão do stream não recebeu conteúdo novo por 60 segundos, possivelmente um problema de conexão.',

            # API error messages
            'api_version_model_error': 'Erro de versão da API ou nome do modelo: {message}\n\nPor favor, atualize a URL Base da API para "{base_url}" e o modelo para "{model}" ou outro modelo disponível nas configurações.',
            'api_format_error': 'Erro de formato da solicitação da API: {message}',
            'api_key_invalid': 'Chave API inválida ou não autorizada: {message}\n\nPor favor, verifique sua Chave API e certifique-se de que o acesso à API esteja habilitado.',
            'api_rate_limit': 'Limite de taxa de solicitação excedido, por favor, tente novamente mais tarde\n\nVocê pode ter excedido a cota de uso gratuito. Isso pode ser devido a:\n1. Muitas solicitações por minuto\n2. Muitas solicitações por dia\n3. Muitos tokens de entrada por minuto',

            # Configuration errors
            'missing_config_key': 'Chave de configuração obrigatória ausente: {key}',
            'api_base_url_required': 'URL Base da API é obrigatória',
            'model_name_required': 'Nome do modelo é obrigatório',

            # Model list fetching
            'fetching_models_from': 'Buscando modelos de {url}',
            'successfully_fetched_models': 'Buscou {count} modelos {provider} com sucesso',
            'failed_to_fetch_models': 'Falha ao carregar modelos: {error}',
            'api_key_empty': 'A Chave API está vazia. Por favor, digite uma Chave API válida.',

            # Error messages for model fetching
            'error_401': 'A autenticação da Chave API falhou. Por favor, verifique: a Chave API está correta, a conta tem saldo suficiente, a Chave API não expirou.',
            'error_403': 'Acesso negado. Por favor, verifique: a Chave API tem permissões suficientes, não há restrições de acesso regional.',
            'error_404': 'Ponto de extremidade da API não encontrado. Por favor, verifique se a configuração da URL Base da API está correta.',
            'error_429': 'Muitas solicitações, limite de taxa atingido. Por favor, tente novamente mais tarde.',
            'error_5xx': 'Erro do servidor. Por favor, tente novamente mais tarde ou verifique o status do provedor de serviço.',
            'error_network': 'A conexão de rede falhou. Por favor, verifique a conexão de rede, as configurações de proxy ou a configuração do firewall.',
            'error_unknown': 'Erro desconhecido.',
            'technical_details': 'Detalhes Técnicos',
            'ollama_service_not_running': 'O serviço Ollama não está em execução. Por favor, inicie o serviço Ollama primeiro.',
            'ollama_service_timeout': 'Tempo limite de conexão do serviço Ollama. Por favor, verifique se o serviço está em execução corretamente.',
            'ollama_model_not_available': 'O modelo "{model}" não está disponível. Por favor, verifique:\n1. O modelo está iniciado? Execute: ollama run {model}\n2. O nome do modelo está correto?\n3. O modelo está baixado? Execute: ollama pull {model}',
            'gemini_geo_restriction': 'A API Gemini não está disponível em sua região. Por favor, tente:\n1. Usar uma VPN para conectar de uma região suportada\n2. Usar outros provedores de IA (OpenAI, Anthropic, DeepSeek, etc.)\n3. Verificar o Google AI Studio para disponibilidade regional',
            'model_test_success': 'Teste de modelo bem-sucedido!',
            'test_model_prompt': 'Modelos carregados com sucesso! Deseja testar o modelo selecionado "{model}"?',
            'test_model_button': 'Testar Modelo',
            'skip': 'Pular',

            # About information
            'author_name': 'Sheldon',
            'user_manual': 'Manual do Usuário',
            'about_plugin': 'Sobre o Plugin Ask AI',
            'learn_how_to_use': 'Como Usar',
            'email': 'iMessage',

            # Model specific configurations
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_kimi': 'Kimi (Moonshot)',
            'model_display_name_custom': 'Personalizado',
            'model_enable_streaming': 'Ativar Streaming',

            # AI Switcher
            'current_ai': 'IA Atual',
            'no_configured_models': 'Nenhuma IA configurada - Por favor, configure nas configurações',

            # Provider specific info
            'nvidia_free_info': '💡 Novos usuários recebem 6 meses de acesso gratuito à API - Não é necessário cartão de crédito',

            # Common system messages
            'default_system_message': 'Você é um especialista em análise de livros. Sua tarefa é ajudar os usuários a entender melhor os livros, fornecendo perguntas e análises perspicazes.',

            # Request timeout settings
            'request_timeout_label': 'Tempo limite da Solicitação:',
            'seconds': 'segundos',
            'request_timeout_error': 'Tempo limite da solicitação. Tempo limite atual: {timeout} segundos',
            'max_prompt_length_normalized_title': 'Limite de prompt ajustado',
            'max_prompt_length_normalized': (
                'O comprimento do prompt foi normalizado para {value} caracteres (separadores como vírgulas '
                'ou espaços foram removidos).'
            ),
            'enable_custom_prompt_limit_label': 'Limite de comprimento de prompt personalizado',
            'enable_custom_prompt_limit_tooltip': (
                'Os limites padrão são 128.000 caracteres (um livro) e 256.000 (vários livros). '
                'A maioria dos usuários não precisa alterar isso. Para pesquisas em toda a '
                'biblioteca, use AI Search. Ative um limite personalizado apenas se o seu modelo '
                'suportar um contexto muito maior e as solicitações ainda atingirem o limite.'
            ),
            'max_prompt_length_label': 'Comprimento máx. do prompt:',
            'max_prompt_length_unit': 'caracteres',
            'max_prompt_length_tooltip': (
                'Aplica-se quando o limite personalizado está ativado. Sugestão padrão: 524288 '
                'caracteres. Regra aproximada: 1 token ≈ 3–4 caracteres. Para Ollama, configure '
                'também num_ctx no lado do modelo.'
            ),

            # Parallel AI settings
            'parallel_ai_count_label': 'Contagem de IA Paralela:',
            'parallel_ai_count_tooltip': 'Número de modelos de IA a serem consultados simultaneamente (1-2 disponíveis, 3-4 em breve)',
            'parallel_ai_notice': 'Nota: Isso afeta apenas o envio de perguntas. Perguntas aleatórias sempre usam uma única IA.',
            'suggest_maximize': 'Dica: Maximize a janela para melhor visualização com 3 IAs',
            'ai_panel_label': 'IA {index}:',
            'no_ai_available': 'Nenhuma IA disponível para este painel',
            'add_more_ai_providers': 'Por favor, adicione mais provedores de IA nas configurações',
            'select_ai': '-- Selecionar IA --',
            'select_model': '-- Selecionar Modelo --',
            'request_model_list': 'Por favor, solicite a lista de modelos',
            'coming_soon': 'Em Breve',
            'advanced_feature_tooltip': 'Este recurso está em desenvolvimento. Fique atento às atualizações!',

            # AI Manager Dialog
            'ai_manager_title': 'Gerenciar Provedores de IA',
            'add_ai_title': 'Adicionar Provedor de IA',
            'manage_ai_title': 'Gerenciar IA Configurada',
            'configured_ai_list': 'IA Configurada',
            'available_ai_list': 'Disponível para Adicionar',
            'ai_config_panel': 'Configuração',
            'select_ai_to_configure': 'Selecione uma IA da lista para configurar',
            'select_provider': 'Selecionar Provedor de IA',
            'select_provider_hint': 'Selecione um provedor da lista',
            'select_ai_to_edit': 'Selecione uma IA da lista para editar',
            'set_as_default': 'Definir como Padrão',
            'save_ai_config': 'Salvar',
            'remove_ai_config': 'Remover',
            'delete_ai': 'Excluir',
            'add_ai_button': 'Adicionar IA',
            'edit_ai_button': 'Editar IA',
            'manage_configured_ai_button': 'Gerenciar IA Configurada',
            'manage_ai_button': 'Gerenciar IA',
            'no_configured_ai': 'Nenhuma IA configurada ainda',
            'no_configured_ai_hint': 'Nenhuma IA configurada. O plugin não pode funcionar. Por favor, clique em "Adicionar IA" para adicionar um provedor de IA.',
            'default_ai_label': 'IA Padrão:',
            'default_ai_tag': 'Padrão',
            'ai_not_configured_cannot_set_default': 'Esta IA ainda não está configurada. Por favor, salve a configuração primeiro.',
            'ai_set_as_default_success': '{name} foi definida como a IA padrão.',
            'ai_config_saved_success': 'A configuração de {name} foi salva com sucesso.',
            'confirm_remove_title': 'Confirmar Remoção',
            'confirm_remove_ai': 'Tem certeza de que deseja remover {name}? Isso limpará a chave API e redefinirá a configuração.',
            'confirm_delete_title': 'Confirmar Exclusão',
            'confirm_delete_ai': 'Tem certeza de que deseja excluir {name}?',
            'api_key_required': 'A Chave API é obrigatória.',
            'configuration': 'Configuração',

            # Field descriptions
            'api_key_desc': 'Sua chave API para autenticação. Mantenha-a segura e não a compartilhe.',
            'base_url_desc': 'A URL do ponto de extremidade da API. Use o padrão, a menos que você tenha um ponto de extremidade personalizado.',
            'model_desc': 'Selecione um modelo da lista ou use um nome de modelo personalizado.',
            'streaming_desc': 'Ativar o streaming de resposta em tempo real para feedback mais rápido.',
            'advanced_section': 'Avançado',

            # Provider-specific notices
            'perplexity_model_notice': 'Nota: Perplexity não fornece uma API pública de lista de modelos, então os modelos são codificados.',
            'ollama_no_api_key_notice': 'Nota: Ollama é um modelo local que não requer uma chave API.',
            'nvidia_free_credits_notice': 'Nota: Novos usuários obtêm créditos de API gratuitos - Não é necessário cartão de crédito.',

            # Nvidia Free error messages
            'free_tier_rate_limit': 'Limite de taxa de nível gratuito excedido. Por favor, tente novamente mais tarde ou configure sua própria chave API da Nvidia.',
            'free_tier_unavailable': 'O nível gratuito está temporariamente indisponível. Por favor, tente novamente mais tarde ou configure sua própria chave API da Nvidia.',
            'free_tier_server_error': 'Erro no servidor de nível gratuito. Por favor, tente novamente mais tarde.',
            'free_tier_error': 'Erro de nível gratuito',

            # Nvidia Free provider info
            'free': 'Gratuito',
            'nvidia_free_provider_name': 'Nvidia AI (Gratuito)',
            'nvidia_free_display_name': 'Nvidia AI (Gratuito)',
            'nvidia_free_api_key_info': 'Será obtido do servidor',
            'nvidia_free_desc': 'Este serviço é mantido pelo desenvolvedor e mantido gratuito, mas pode ser menos estável. Para um serviço mais estável, por favor, configure sua própria chave API da Nvidia.',

            # Nvidia Free first use reminder
            'nvidia_free_first_use_title': 'Bem-vindo(a) ao Plugin Ask AI',
            'nvidia_free_first_use_message': 'Agora você pode perguntar sem nenhuma configuração! O desenvolvedor mantém um nível gratuito para você, mas pode não ser muito estável. Aproveite!\n\nVocê pode configurar seus próprios provedores de IA nas configurações para maior estabilidade.',

            # Model buttons
            'refresh_model_list': 'Atualizar',
            'test_current_model': 'Testar',
            'testing_text': 'Testando',
            'refresh_success': 'Lista de modelos atualizada com sucesso.',
            'refresh_failed': 'Falha ao atualizar a lista de modelos.',
            'test_failed': 'O teste do modelo falhou.',

            # Tooltip
            'manage_ai_disabled_tooltip': 'Por favor, adicione um provedor de IA primeiro.',

            # PDF export section titles
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
            'pdf_generated_time': 'Hora de geração',
            'pdf_info_not_available': 'Informação não disponível',
            
            # Library Chat feature (v1.4.2)
            'library_tab': 'Pesquisa',
            'library_search': 'Pesquisa IA',
            'library_info': 'A pesquisa IA está sempre ativada. Quando você não seleciona nenhum livro, pode pesquisar toda a sua biblioteca usando linguagem natural.',
            'library_enable': 'Ativar pesquisa IA',
            'library_enable_tooltip': 'Quando ativado, você pode pesquisar sua biblioteca usando IA quando nenhum livro está selecionado',
            'library_update': 'Atualizar dados da biblioteca',
            'library_update_tooltip': 'Extrair títulos e autores de livros da sua biblioteca',
            'library_updating': 'Atualizando...',
            'library_status': 'Status: {count} livros, última atualização: {time}',
            'library_status_empty': 'Status: Sem dados. Clique em "Atualizar dados da biblioteca" para começar.',
            'library_status_error': 'Status: Erro ao carregar dados',
            'library_update_success': '{count} livros atualizados com sucesso',
            'library_update_failed': 'Falha ao atualizar dados da biblioteca',
            'library_no_gui': 'GUI não disponível',
            'library_init_title': 'Inicializar pesquisa IA',
            'library_init_message': 'A pesquisa IA requer metadados da biblioteca para funcionar. Deseja inicializar agora?\n\nIsso extrairá títulos e autores de livros da sua biblioteca.',
            'library_init_required': 'A pesquisa IA não pode ser ativada sem dados da biblioteca. Por favor, clique em "Atualizar dados da biblioteca" quando estiver pronto para usar este recurso.',
            'ai_search_welcome_title': 'Bem-vindo à pesquisa IA',
            'ai_search_welcome_message': 'A pesquisa IA está ativada!\n\nComo ativar:\n• Atalho de teclado (personalizável nas configurações)\n• Menu Ferramentas → Pesquisa IA\n• Abrir diálogo Ask sem selecionar livros\n\nVocê pode pesquisar toda a sua biblioteca usando linguagem natural. Por exemplo:\n• "Você tem livros sobre Python?"\n• "Mostre-me livros de Isaac Asimov"\n• "Encontre livros sobre aprendizado de máquina"\n\nA IA pesquisará sua biblioteca e recomendará livros relevantes. Clique nos títulos para abri-los diretamente.',
            'ai_search_not_enough_books_title': 'Livros insuficientes',
            'ai_search_not_enough_books_message': 'A pesquisa IA requer pelo menos {min_books} livros na sua biblioteca.\n\nSua biblioteca atual tem apenas {book_count} livro(s).\n\nPor favor, adicione mais livros para usar a pesquisa IA.',
            'ai_search_mode_info': 'Pesquisando em toda a sua biblioteca',
            'ai_search_feature_title': 'AI Search',
            'ai_search_feature_subtitle': 'Pesquise toda a sua biblioteca em linguagem natural',
            'ai_search_feature_description': (
                'AI Search ajuda você a descobrir livros em toda a sua biblioteca Calibre.\n\n'
                '• Ativar: abrir Ask sem selecionar livros, Ferramentas → AI Search ou atalho de teclado\n'
                '• Como funciona: o plugin envia metadados compactos (ID, título, autor) de todos '
                'os livros indexados\n'
                '• Grandes seleções: se selecionar mais de 50 livros, Ask sugere AI Search em vez '
                'de incluir cada livro em formato detalhado\n'
                '• Manter dados atualizados: clique em "Atualizar dados da biblioteca" após '
                'adicionar ou remover livros\n\n'
                'Exemplos: "Encontre livros sobre Python", "Mostre-me livros de Isaac Asimov".'
            ),
            'ai_search_usage_hint': (
                'Dica: AI Search funciona melhor para descoberta em toda a biblioteca. Para comparar '
                'alguns livros em profundidade, selecione até 30 livros.'
            ),
            'ai_search_data_title': 'Índice da biblioteca',
            'ai_search_data_subtitle': (
                'Atualize a lista compacta de livros enviada à IA ao adicionar ou remover livros'
            ),
            'library_prompt_template': 'Você tem acesso à biblioteca de livros do usuário. Aqui estão todos os livros: {metadata} Consulta do usuário: {query} Por favor, encontre livros correspondentes na biblioteca atual e retorne-os neste formato (**IMPORTANTE**: Use o formato de link HTML para que os usuários possam clicar nos títulos dos livros para abri-los diretamente): - <a href="calibre://book/BOOK_ID">Título do livro</a> - Nome do autor Exemplo: - <a href="calibre://book/123">Aprendendo Python</a> - Mark Lutz - <a href="calibre://book/456">Machine Learning em ação</a> - Peter Harrington Nota: Alguns autores podem aparecer como "unknown". Estes são dados normais, por favor retorne todos os resultados correspondentes normalmente. Retorne apenas livros que correspondam à consulta. Máximo 5 resultados.',
            'ai_search_privacy_title': 'Aviso de Privacidade',
            'ai_search_privacy_alert': 'A Busca IA utiliza metadados dos livros (títulos e autores). Esta informação será enviada para o fornecedor de IA que configurou para processar as suas pesquisas.',
            'ai_search_updated_info': '{count} livros atualizados há {time_ago}',
            'ai_search_books_info': '{count} livros indexados',
            'days_ago': '{n} dias atrás',
            'hours_ago': '{n} horas atrás',
            'minutes_ago': '{n} minutos atrás',
            'just_now': 'agora mesmo',
            
            # Statistics tab (v1.4.2)
            'stat_tab': 'Estatísticas',
            'stat_overview': 'Visão geral',
            'stat_overview_subtitle': 'Estatísticas de consultas AI',
            'stat_days_unit': 'dias',
            'stat_days_label': 'Iniciado',
            'stat_start_at': 'Início em {date}',
            'stat_replies_unit': 'vezes',
            'stat_replies_label': 'Perguntar AI',
            'stat_books_unit': 'livros',
            'stat_books_label': 'Biblioteca',
            'stat_no_books': 'Atualizar na aba Pesquisa',
            'stat_trends': 'Tendências',
            'stat_curious_index': 'Distribuição de consultas AI esta semana',
            'stat_daily_avg': 'Média diária {n} vezes',
            'stat_sample_data': 'Dados de exemplo exibidos. Mudará para dados reais após 20+ solicitações',
            'stat_heatmap': 'Mapa de calor',
            'stat_heatmap_subtitle': 'Distribuição de consultas AI este mês',
            'stat_no_data_week': 'Sem dados esta semana',
            'stat_no_data_month': 'Sem dados este mês',
            'stat_data_not_enough': 'Dados insuficientes',
            
            # Títulos de usuário estatísticos (baseados no número de consultas)
            'stat_title_curious': 'Folheador',
            'stat_title_explorer': 'Caçador de livros',
            'stat_title_seeker': 'Leitor ávido',
            'stat_title_enthusiast': 'Bibliófilo',
            'stat_title_pursuer': 'Rato de biblioteca',
            
            # Avaliações de biblioteca (baseadas no tamanho da coleção, referências históricas)
            'stat_books_impressive': 'Gabinete de leitura',
            'stat_books_collection': 'Escritório do erudito',
            'stat_books_variety': 'Biblioteca Joanina',
            'stat_books_awesome': 'Biblioteca Nacional de Portugal',
            'stat_books_unbelievable': 'Biblioteca de Alexandria',
            
            # Links (v1.4.2)
            'online_tutorial': 'Tutorial online',
        }