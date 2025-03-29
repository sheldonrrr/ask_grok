#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

# 默认提示词模板
DEFAULT_TEMPLATES = {
    # 丹麦语
    'da': 'Om bogen "{title}": Forfatter: {author}, Forlag: {publisher}, Udgivelsesdato: {pubdate}, Sprog: {language}, Serie: {series}, Mit spørgsmål er: {query}',
    
    # 德语
    'de': 'Über das Buch "{title}": Autor: {author}, Verlag: {publisher}, Erscheinungsdatum: {pubdate}, Sprache: {language}, Serie: {series}, Meine Frage ist: {query}',
    
    # 英语
    'en': 'About the book "{title}": Author: {author}, Publisher: {publisher}, Publication Date: {pubdate}, Language: {language}, Series: {series}, My question is: {query}',
    
    # 西班牙语
    'es': 'Sobre el libro "{title}": Autor: {author}, Editorial: {publisher}, Fecha de publicación: {pubdate}, Idioma: {language}, Serie: {series}, Mi pregunta es: {query}',
    
    # 芬兰语
    'fi': 'Kirjasta "{title}": Kirjailija: {author}, Kustantaja: {publisher}, Julkaisupäivä: {pubdate}, Kieli: {language}, Sarja: {series}, Kysymykseni on: {query}',
    
    # 法语
    'fr': 'À propos du livre "{title}": Auteur: {author}, Éditeur: {publisher}, Date de publication: {pubdate}, Langue: {language}, Série: {series}, Ma question est: {query}',
    
    # 日语
    'ja': '『{title}』について：著者：{author}、出版社：{publisher}、出版日：{pubdate}、言語：{language}、シリーズ：{series}、質問：{query}',
    
    # 荷兰语
    'nl': 'Over het boek "{title}": Auteur: {author}, Uitgever: {publisher}, Publicatiedatum: {pubdate}, Taal: {language}, Serie: {series}, Mijn vraag is: {query}',
    
    # 挪威语
    'no': 'Om boken "{title}": Forfatter: {author}, Forlag: {publisher}, Utgivelsesdato: {pubdate}, Språk: {language}, Serie: {series}, Mitt spørsmål er: {query}',
    
    # 葡萄牙语
    'pt': 'Sobre o livro "{title}": Autor: {author}, Editora: {publisher}, Data de publicação: {pubdate}, Idioma: {language}, Série: {series}, Minha pergunta é: {query}',
    
    # 俄语
    'ru': 'О книге "{title}": Автор: {author}, Издательство: {publisher}, Дата публикации: {pubdate}, Язык: {language}, Серия: {series}, Мой вопрос: {query}',
    
    # 瑞典语
    'sv': 'Om boken "{title}": Författare: {author}, Förlag: {publisher}, Utgivningsdatum: {pubdate}, Språk: {language}, Serie: {series}, Min fråga är: {query}',
    
    # 简体中文
    'zh': '关于《{title}》这本书的信息：作者：{author}，出版社：{publisher}，出版日期：{pubdate}，语言：{language}，系列：{series}，我的问题是：{query}',
    
    # 繁体中文
    'zht': '關於《{title}》這本書的資訊：作者：{author}，出版社：{publisher}，出版日期：{pubdate}，語言：{language}，系列：{series}，我的問題是：{query}',
    
    # 粤语
    'yue': '關於《{title}》呢本書嘅資料：作者：{author}，出版社：{publisher}，出版日期：{pubdate}，語言：{language}，系列：{series}，我想問嘅係：{query}',
}

# 语言包
TRANSLATIONS = {
    # 丹麦语 (da)
    'da': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Stil spørgsmål om en bog med Grok',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Indstillinger',
        'token_label': 'X.AI Autorisationstoken:',
        'token_help': 'Format: Bearer xai-xxx eller bare xai-xxx',
        'model_label': 'Model:',
        'model_placeholder': 'Standard: grok-2-latest',
        'template_label': 'Promptskabelon:',
        'template_placeholder': 'Eksempel på skabelon:\nOm bogen "{title}": Forfatter: {author}, Forlag: {publisher}, Udgivelsesdato: {pubdate}, Sprog: {language}, Serie: {series}, Mit spørgsmål er: {query}',
        'language_label': 'Grænsefladesprog:',
        'send_button': 'Send',
        'shortcut_enter': 'Ctrl + Enter',
        'shortcut_return': 'Command + Return',
        'error_prefix': 'Fejl: ',
        'about': 'Om',
        'about_title': 'Om',
        'base_url_label': 'API Base-URL:',
        'base_url_placeholder': 'Standard: https://api.x.ai/v1',
        'metadata_title': 'Titel',
        'metadata_authors': 'Forfatter',
        'metadata_publisher': 'Forlag',
        'metadata_pubdate': 'Udgivelsesdato',
        'metadata_language': 'Sprog',
        'metadata_series': 'Serie',
        'input_placeholder': 'Skriv dit spørgsmål her...',
        'menu_title': 'Spørg',
        'menu_ask_grok': 'Spørg Grok',
        'ok_button': 'OK',
        'save_button': 'Gem',
        'save_success': 'Indstillinger gemt',
    },
    
    # 德语 (de)
    'de': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Fragen zu einem Buch mit Grok stellen',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Konfiguration',
        'token_label': 'X.AI Autorisierungstoken:',
        'token_help': 'Format: Bearer xai-xxx oder einfach xai-xxx',
        'model_label': 'Modell:',
        'model_placeholder': 'Standard: grok-2-latest',
        'template_label': 'Prompt-Vorlage:',
        'template_placeholder': 'Beispielvorlage:\nÜber das Buch "{title}": Autor: {author}, Verlag: {publisher}, Erscheinungsdatum: {pubdate}, Sprache: {language}, Serie: {series}, Meine Frage ist: {query}',
        'language_label': 'Oberflächensprache:',
        'send_button': 'Senden',
        'shortcut_enter': 'Strg + Eingabe',
        'shortcut_return': 'Command + Return',
        'error_prefix': 'Fehler: ',
        'about': 'Über',
        'about_title': 'Über',
        'base_url_label': 'API-Basis-URL:',
        'base_url_placeholder': 'Standard: https://api.x.ai/v1',
        'metadata_title': 'Titel',
        'metadata_authors': 'Autor',
        'metadata_publisher': 'Verlag',
        'metadata_pubdate': 'Erscheinungsdatum',
        'metadata_language': 'Sprache',
        'metadata_series': 'Serie',
        'input_placeholder': 'Geben Sie hier Ihre Frage ein...',
        'menu_title': 'Fragen',
        'menu_ask_grok': 'Grok fragen',
        'ok_button': 'OK',
        'save_button': 'Speichern',
        'save_success': 'Einstellungen gespeichert',
    },
    
    # 英语 (en)
    'en': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Ask questions about a book using Grok',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Configuration',
        'token_label': 'X.AI Authorization Token:',
        'token_help': 'Format: Bearer xai-xxx or just xai-xxx',
        'model_label': 'Model:',
        'model_placeholder': 'Default: grok-2-latest',
        'template_label': 'Prompt Template:',
        'template_placeholder': 'Example template:\nAbout the book "{title}": Author: {author}, Publisher: {publisher}, Publication Date: {pubdate}, Language: {language}, Series: {series}, My question is: {query}',
        'language_label': 'Interface Language:',
        'send_button': 'Send',
        'shortcut_enter': 'Ctrl + Enter',
        'shortcut_return': 'Command + Return',
        'error_prefix': 'Error: ',
        'about': 'About',
        'about_title': 'About',
        'base_url_label': 'API Base URL:',
        'base_url_placeholder': 'Default: https://api.x.ai/v1',
        'metadata_title': 'Title',
        'metadata_authors': 'Author',
        'metadata_publisher': 'Publisher',
        'metadata_pubdate': 'Publication Date',
        'metadata_language': 'Language',
        'metadata_series': 'Series',
        'input_placeholder': 'Enter your question here...',
        'menu_title': 'Ask',
        'menu_ask_grok': 'Ask Grok',
        'ok_button': 'OK',
        'save_button': 'Save',
        'save_success': 'Settings saved',
    },
    
    # 西班牙语 (es)
    'es': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Hacer preguntas sobre un libro usando Grok',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Configuración',
        'token_label': 'Token de autorización X.AI:',
        'token_help': 'Formato: Bearer xai-xxx o simplemente xai-xxx',
        'model_label': 'Modelo:',
        'model_placeholder': 'Predeterminado: grok-2-latest',
        'template_label': 'Plantilla de prompt:',
        'template_placeholder': 'Ejemplo de plantilla:\nSobre el libro "{title}": Autor: {author}, Editorial: {publisher}, Fecha de publicación: {pubdate}, Idioma: {language}, Serie: {series}, Mi pregunta es: {query}',
        'language_label': 'Idioma de la interfaz:',
        'send_button': 'Enviar',
        'shortcut_enter': 'Ctrl + Intro',
        'shortcut_return': 'Command + Return',
        'error_prefix': 'Error: ',
        'about': 'Acerca de',
        'about_title': 'Acerca de',
        'base_url_label': 'URL base de la API:',
        'base_url_placeholder': 'Predeterminado: https://api.x.ai/v1',
        'metadata_title': 'Título',
        'metadata_authors': 'Autor',
        'metadata_publisher': 'Editorial',
        'metadata_pubdate': 'Fecha de publicación',
        'metadata_language': 'Idioma',
        'metadata_series': 'Serie',
        'input_placeholder': 'Escriba su pregunta aquí...',
        'menu_title': 'Preguntar',
        'menu_ask_grok': 'Preguntar a Grok',
        'ok_button': 'OK',
        'save_button': 'Guardar',
        'save_success': 'Configuración guardada',
    },
    
    # 芬兰语 (fi)
    'fi': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Kysy kirjasta Grokin avulla',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Asetukset',
        'token_label': 'X.AI Valtuutusavain:',
        'token_help': 'Muoto: Bearer xai-xxx tai pelkkä xai-xxx',
        'model_label': 'Malli:',
        'model_placeholder': 'Oletus: grok-2-latest',
        'template_label': 'Kehotepohja:',
        'template_placeholder': 'Esimerkkipohja:\nKirjasta "{title}": Kirjailija: {author}, Kustantaja: {publisher}, Julkaisupäivä: {pubdate}, Kieli: {language}, Sarja: {series}, Kysymykseni on: {query}',
        'language_label': 'Käyttöliittymän kieli:',
        'send_button': 'Lähetä',
        'shortcut_enter': 'Ctrl + Enter',
        'shortcut_return': 'Command + Return',
        'error_prefix': 'Virhe: ',
        'about': 'Tietoja',
        'about_title': 'Tietoja',
        'base_url_label': 'API-perus-URL:',
        'base_url_placeholder': 'Oletus: https://api.x.ai/v1',
        'metadata_title': 'Otsikko',
        'metadata_authors': 'Kirjailija',
        'metadata_publisher': 'Kustantaja',
        'metadata_pubdate': 'Julkaisupäivä',
        'metadata_language': 'Kieli',
        'metadata_series': 'Sarja',
        'input_placeholder': 'Kirjoita kysymyksesi tähän...',
        'menu_title': 'Kysy',
        'menu_ask_grok': 'Kysy Grok',
        'ok_button': 'OK',
        'save_button': 'Tallenna',
        'save_success': 'Asetukset tallennettu',
    },
    
    # 法语 (fr)
    'fr': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Poser des questions sur un livre avec Grok',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Configuration',
        'token_label': 'Token d\'autorisation X.AI :',
        'token_help': 'Format : Bearer xai-xxx ou simplement xai-xxx',
        'model_label': 'Modèle :',
        'model_placeholder': 'Par défaut : grok-2-latest',
        'template_label': 'Modèle de prompt :',
        'template_placeholder': 'Exemple de modèle :\nÀ propos du livre "{title}" : Auteur : {author}, Éditeur : {publisher}, Date de publication : {pubdate}, Langue : {language}, Série : {series}, Ma question est : {query}',
        'language_label': 'Langue de l\'interface :',
        'send_button': 'Envoyer',
        'shortcut_enter': 'Ctrl + Entrée',
        'shortcut_return': 'Command + Retour',
        'error_prefix': 'Erreur : ',
        'about': 'À propos',
        'about_title': 'À propos',
        'base_url_label': 'URL de base de l\'API :',
        'base_url_placeholder': 'Par défaut : https://api.x.ai/v1',
        'metadata_title': 'Titre',
        'metadata_authors': 'Auteur',
        'metadata_publisher': 'Éditeur',
        'metadata_pubdate': 'Date de publication',
        'metadata_language': 'Langue',
        'metadata_series': 'Série',
        'input_placeholder': 'Saisissez votre question ici...',
        'menu_title': 'Demander',
        'menu_ask_grok': 'Poser une question à Grok',
        'ok_button': 'OK',
        'save_button': 'Enregistrer',
        'save_success': 'Paramètres enregistrés',
    },
    
    # 日语 (ja)
    'ja': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Grokを使って本について質問する',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': '設定',
        'token_label': 'X.AI Authorization Token:',
        'token_help': '形式: Bearer xai-xxx または xai-xxx',
        'model_label': 'Model:',
        'model_placeholder': 'Default: grok-2-latest',
        'template_label': 'プロンプトテンプレート:',
        'template_placeholder': 'テンプレート例:\n『{title}』について：著者：{author}、出版社：{publisher}、出版日：{pubdate}、言語：{language}、シリーズ：{series}、質問：{query}',
        'language_label': 'インターフェース言語:',
        'send_button': '送信',
        'shortcut_enter': 'Ctrl + Enter',
        'shortcut_return': 'Command + Return',
        'error_prefix': 'エラー：',
        'about': '概要',
        'about_title': '概要',
        'base_url_label': 'API Base URL:',
        'base_url_placeholder': 'Default: https://api.x.ai/v1',
        'metadata_title': 'タイトル',
        'metadata_authors': '著者',
        'metadata_publisher': '出版社',
        'metadata_pubdate': '出版日',
        'metadata_language': '言語',
        'metadata_series': 'シリーズ',
        'input_placeholder': 'ここに質問を入力してください...',
        'menu_title': '質問',
        'menu_ask_grok': 'Grok に質問する',
        'ok_button': 'OK',
        'save_button': '保存',
        'save_success': '設定を保存しました',
    },
    
    # 荷兰语 (nl)
    'nl': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Stel vragen over een boek met Grok',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Instellingen',
        'token_label': 'X.AI Autorisatietoken:',
        'token_help': 'Formaat: Bearer xai-xxx of gewoon xai-xxx',
        'model_label': 'Model:',
        'model_placeholder': 'Standaard: grok-2-latest',
        'template_label': 'Promptsjabloon:',
        'template_placeholder': 'Voorbeeldsjabloon:\nOver het boek "{title}": Auteur: {author}, Uitgever: {publisher}, Publicatiedatum: {pubdate}, Taal: {language}, Serie: {series}, Mijn vraag is: {query}',
        'language_label': 'Interfacetaal:',
        'send_button': 'Verzenden',
        'shortcut_enter': 'Ctrl + Enter',
        'shortcut_return': 'Command + Return',
        'error_prefix': 'Fout: ',
        'about': 'Over',
        'about_title': 'Over',
        'base_url_label': 'API Basis-URL:',
        'base_url_placeholder': 'Standaard: https://api.x.ai/v1',
        'metadata_title': 'Titel',
        'metadata_authors': 'Auteur',
        'metadata_publisher': 'Uitgever',
        'metadata_pubdate': 'Publicatiedatum',
        'metadata_language': 'Taal',
        'metadata_series': 'Serie',
        'input_placeholder': 'Voer hier uw vraag in...',
        'menu_title': 'Vraag',
        'menu_ask_grok': 'Vraag aan Grok',
        'ok_button': 'OK',
        'save_button': 'Opslaan',
        'save_success': 'Instellingen opgeslagen',
    },
    
    # 挪威语 (no)
    'no': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Still spørsmål om en bok med Grok',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Innstillinger',
        'token_label': 'X.AI Autorisasjonstoken:',
        'token_help': 'Format: Bearer xai-xxx eller bare xai-xxx',
        'model_label': 'Modell:',
        'model_placeholder': 'Standard: grok-2-latest',
        'template_label': 'Promptmal:',
        'template_placeholder': 'Eksempel på mal:\nOm boken "{title}": Forfatter: {author}, Forlag: {publisher}, Utgivelsesdato: {pubdate}, Språk: {language}, Serie: {series}, Mitt spørsmål er: {query}',
        'language_label': 'Grensesnittspråk:',
        'send_button': 'Send',
        'shortcut_enter': 'Ctrl + Enter',
        'shortcut_return': 'Command + Return',
        'error_prefix': 'Feil: ',
        'about': 'Om',
        'about_title': 'Om',
        'base_url_label': 'API Base-URL:',
        'base_url_placeholder': 'Standard: https://api.x.ai/v1',
        'metadata_title': 'Tittel',
        'metadata_authors': 'Forfatter',
        'metadata_publisher': 'Forlag',
        'metadata_pubdate': 'Utgivelsesdato',
        'metadata_language': 'Språk',
        'metadata_series': 'Serie',
        'input_placeholder': 'Skriv spørsmålet ditt her...',
        'menu_title': 'Spør',
        'menu_ask_grok': 'Spør Grok',
        'ok_button': 'OK',
        'save_button': 'Lagre',
        'save_success': 'Innstillinger lagret',
    },
    
    # 葡萄牙语 (pt)
    'pt': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Fazer perguntas sobre um livro usando Grok',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Configuração',
        'token_label': 'Token de autorização X.AI:',
        'token_help': 'Formato: Bearer xai-xxx ou simplesmente xai-xxx',
        'model_label': 'Modelo:',
        'model_placeholder': 'Padrão: grok-2-latest',
        'template_label': 'Modelo de prompt:',
        'template_placeholder': 'Exemplo de modelo:\nSobre o livro "{title}": Autor: {author}, Editora: {publisher}, Data de publicação: {pubdate}, Idioma: {language}, Série: {series}, Minha pergunta é: {query}',
        'language_label': 'Idioma da interface:',
        'send_button': 'Enviar',
        'shortcut_enter': 'Ctrl + Enter',
        'shortcut_return': 'Command + Return',
        'error_prefix': 'Erro: ',
        'about': 'Sobre',
        'about_title': 'Sobre',
        'base_url_label': 'URL base da API:',
        'base_url_placeholder': 'Padrão: https://api.x.ai/v1',
        'metadata_title': 'Título',
        'metadata_authors': 'Autor',
        'metadata_publisher': 'Editora',
        'metadata_pubdate': 'Data de publicação',
        'metadata_language': 'Idioma',
        'metadata_series': 'Série',
        'input_placeholder': 'Digite sua pergunta aqui...',
        'menu_title': 'Perguntar',
        'menu_ask_grok': 'Perguntar ao Grok',
        'ok_button': 'OK',
        'save_button': 'Salvar',
        'save_success': 'Configurações salvas',
    },
    
    # 俄语 (ru)
    'ru': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Задавать вопросы о книге с помощью Grok',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Настройки',
        'token_label': 'Токен авторизации X.AI:',
        'token_help': 'Формат: Bearer xai-xxx или просто xai-xxx',
        'model_label': 'Модель:',
        'model_placeholder': 'По умолчанию: grok-2-latest',
        'template_label': 'Шаблон запроса:',
        'template_placeholder': 'Пример шаблона:\nО книге "{title}": Автор: {author}, Издательство: {publisher}, Дата публикации: {pubdate}, Язык: {language}, Серия: {series}, Мой вопрос: {query}',
        'language_label': 'Язык интерфейса:',
        'send_button': 'Отправить',
        'shortcut_enter': 'Ctrl + Enter',
        'shortcut_return': 'Command + Return',
        'error_prefix': 'Ошибка: ',
        'about': 'О программе',
        'about_title': 'О программе',
        'base_url_label': 'Базовый URL API:',
        'base_url_placeholder': 'По умолчанию: https://api.x.ai/v1',
        'metadata_title': 'Название',
        'metadata_authors': 'Автор',
        'metadata_publisher': 'Издательство',
        'metadata_pubdate': 'Дата публикации',
        'metadata_language': 'Язык',
        'metadata_series': 'Серия',
        'input_placeholder': 'Введите ваш вопрос здесь...',
        'menu_title': 'Спросить',
        'menu_ask_grok': 'Спросить у Grok',
        'ok_button': 'OK',
        'save_button': 'Сохранить',
        'save_success': 'Настройки сохранены',
    },
    
    # 瑞典语 (sv)
    'sv': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Ställ frågor om en bok med Grok',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Inställningar',
        'token_label': 'X.AI Auktoriseringstoken:',
        'token_help': 'Format: Bearer xai-xxx eller bara xai-xxx',
        'model_label': 'Modell:',
        'model_placeholder': 'Standard: grok-2-latest',
        'template_label': 'Promptmall:',
        'template_placeholder': 'Exempel på mall:\nOm boken "{title}": Författare: {author}, Förlag: {publisher}, Utgivningsdatum: {pubdate}, Språk: {language}, Serie: {series}, Min fråga är: {query}',
        'language_label': 'Gränssnittsspråk:',
        'send_button': 'Skicka',
        'shortcut_enter': 'Ctrl + Enter',
        'shortcut_return': 'Command + Return',
        'error_prefix': 'Fel: ',
        'about': 'Om',
        'about_title': 'Om',
        'base_url_label': 'API Bas-URL:',
        'base_url_placeholder': 'Standard: https://api.x.ai/v1',
        'metadata_title': 'Titel',
        'metadata_authors': 'Författare',
        'metadata_publisher': 'Förlag',
        'metadata_pubdate': 'Utgivningsdatum',
        'metadata_language': 'Språk',
        'metadata_series': 'Serie',
        'input_placeholder': 'Skriv din fråga här...',
        'menu_title': 'Fråga',
        'menu_ask_grok': 'Fråga Grok',
        'ok_button': 'OK',
        'save_button': 'Spara',
        'save_success': 'Inställningar sparade',
    },
    
    # 简体中文 (zh)
    'zh': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': '使用 Grok 询问关于书籍的问题',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': '配置',
        'token_label': 'X.AI 授权令牌:',
        'token_help': '格式：Bearer xai-xxx 或直接 xai-xxx',
        'model_label': '模型:',
        'model_placeholder': '默认：grok-2-latest',
        'template_label': '提示词模板:',
        'template_placeholder': '示例模板：\n关于《{title}》这本书的信息：作者：{author}，出版社：{publisher}，出版日期：{pubdate}，语言：{language}，系列：{series}，我的问题是：{query}',
        'language_label': '界面语言:',
        'send_button': '发送',
        'shortcut_enter': 'Ctrl + Enter',
        'shortcut_return': 'Command + Return',
        'error_prefix': '错误：',
        'about': '关于',
        'about_title': '关于',
        'base_url_label': 'API 基础 URL:',
        'base_url_placeholder': '默认：https://api.x.ai/v1',
        'metadata_title': '标题',
        'metadata_authors': '作者',
        'metadata_publisher': '出版社',
        'metadata_pubdate': '出版日期',
        'metadata_language': '语言',
        'metadata_series': '系列',
        'input_placeholder': '在这里输入你的问题...',
        'menu_title': '询问',
        'menu_ask_grok': '询问 Grok',
        'ok_button': '确定',
        'save_button': '保存',
        'save_success': '设置已保存',
        'response_placeholder': 'Grok 的回答将显示在这里',
        'loading_text': '正在询问',
    },
    
    # 繁体中文 (zht)
    'zht': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': '用Grok詢問關於一本書的問題',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': '設定',
        'token_label': 'X.AI Authorization Token:',
        'token_help': '格式: Bearer xai-xxx 或直接輸入 xai-xxx',
        'model_label': 'Model:',
        'model_placeholder': 'Default: grok-2-latest',
        'template_label': '提示詞範本:',
        'template_placeholder': '範本示例：\n關於《{title}》這本書的資訊：作者：{author}，出版社：{publisher}，出版日期：{pubdate}，語言：{language}，系列：{series}，我的問題是：{query}',
        'language_label': '界面語言:',
        'send_button': '發送',
        'shortcut_enter': 'Ctrl + Enter',
        'shortcut_return': 'Command + Return',
        'error_prefix': '錯誤：',
        'about': '關於',
        'about_title': '關於',
        'base_url_label': 'API Base URL:',
        'base_url_placeholder': 'Default: https://api.x.ai/v1',
        'metadata_title': '書名',
        'metadata_authors': '作者',
        'metadata_publisher': '出版社',
        'metadata_pubdate': '出版日期',
        'metadata_language': '語言',
        'metadata_series': '系列',
        'input_placeholder': '在此輸入你的問題...',
        'menu_title': '詢問',
        'menu_ask_grok': '詢問 Grok',
        'ok_button': '確定',
        'save_button': '儲存',
        'save_success': '設定已儲存',
    },
    
    # 粤语 (yue)
    'yue': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': '用Grok問一本書嘅嘢',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': '設定',
        'token_label': 'X.AI Authorization Token:',
        'token_help': '格式: Bearer xai-xxx 或直接輸入 xai-xxx',
        'model_label': 'Model:',
        'model_placeholder': 'Default: grok-2-latest',
        'template_label': '提示詞模板:',
        'template_placeholder': '範例：\n關於《{title}》呢本書嘅資料：作者：{author}，出版社：{publisher}，出版日期：{pubdate}，語言：{language}，系列：{series}，我想問嘅係：{query}',
        'language_label': '界面語言:',
        'send_button': '發送',
        'shortcut_enter': 'Ctrl + Enter',
        'shortcut_return': 'Command + Return',
        'error_prefix': '出錯啦：',
        'about': '關於',
        'about_title': '關於',
        'base_url_label': 'API Base URL:',
        'base_url_placeholder': 'Default: https://api.x.ai/v1',
        'metadata_title': '書名',
        'metadata_authors': '作者',
        'metadata_publisher': '出版社',
        'metadata_pubdate': '出版日期',
        'metadata_language': '語言',
        'metadata_series': '系列',
        'input_placeholder': '喺呢度輸入你嘅問題...',
        'menu_title': '問嘢',
        'menu_ask_grok': '問 Grok',
        'ok_button': '確定',
        'save_button': '保存',
        'save_success': '設定已保存',
    }
}

def get_translation(lang_code):
    """获取指定语言的翻译"""
    return TRANSLATIONS.get(lang_code, TRANSLATIONS['en'])

def get_default_template(lang_code):
    """获取指定语言的默认提示词模板"""
    return DEFAULT_TEMPLATES.get(lang_code, DEFAULT_TEMPLATES['en'])
