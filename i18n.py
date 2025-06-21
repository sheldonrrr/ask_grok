#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QLabel, QTextFormat
from PyQt5.QtCore import Qt

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

# 建议提示词模板
SUGGESTION_TEMPLATES = {
    # 丹麦语
    'da': """Du er en ekspert i boganmeldelser. For bogen "{title}" af {author}, generér ÉT indsigtfuldt spørgsmål, der hjælper læserne med at forstå bogen bedre.

Regler:
1. Returner KUN spørgsmålet, uden introduktion eller forklaring
2. Fokuser på bogens indhold, ikke kun titlen
3. Gør spørgsmålet praktisk og tankevækkende
4. Hold det kort (15-25 ord)
5. Vær kreativ og generer et andet spørsmål hver gang, selv for samme bog""",

    # 德语
    'de': """Sie sind ein Experte für Buchrezensionen. Für das Buch "{title}" von {author} generieren Sie EINE aufschlussreiche Frage, die den Lesern hilft, das Buch besser zu verstehen.

Regeln:
1. Geben Sie NUR die Frage zurück, ohne Einleitung oder Erklärung
2. Konzentrieren Sie sich auf den Inhalt des Buches, nicht nur auf den Titel
3. Machen Sie die Frage praktisch und nachdenklich
4. Halten Sie sie kurz (15-25 Wörter)
5. Seien Sie kreativ und generieren Sie jedes Mal eine andere Frage, auch für dasselbe Buch""",

    # 英语
    'en': """You are an expert book reviewer. For the book "{title}" by {author}, generate ONE insightful question that helps readers better understand the book's core ideas, practical applications, or unique perspectives. 

Rules:
1. Return ONLY the question, without any introduction or explanation
2. Focus on the book's substance, not just its title
3. Make the question practical and thought-provoking
4. Keep it concise (15-25 words)
5. Be creative and generate a different question each time, even for the same book""",

    # 西班牙语
    'es': """Eres un experto en reseñas de libros. Para el libro "{title}" de {author} genera UNA pregunta perspicaz que ayude a los lectores a entender mejor el libro.

Reglas:
1. Devuelve SOLO la pregunta, sin introducción ni explicación
2. Concéntrate en el contenido del libro, no solo en el título
3. Haz que la pregunta sea práctica y reflexiva
4. Mantenla breve (15-25 palabras)
5. Sé creativo y genera una pregunta diferente cada vez, incluso para el mismo libro""",

    # 芬兰语
    'fi': """Olet kirja-arvostelun asiantuntija. Kirjalle "{title}" kirjailijana {author}, luo YKSI oivaltava kysymys, joka auttaa lukijoita ymmärtämään kirjaa paremmin.

Säännöt:
1. Palauta VAIN kysymys, ilman johdantoa tai selitystä
2. Keskity kirjan sisältöön, älä pelkästään otsikkoon
3. Tee kysymyksestä käytännöllinen ja ajatuksia herättävä
4. Pidä se lyhyenä (15-25 sanaa)
5. Ole luova ja luo eri kysymys joka kerta, myös samalle kirjalle""",

    # 法语
    'fr': """Vous êtes un expert en critiques de livres. Pour le livre "{title}" de {author}, générez UNE question pertinente qui aide les lecteurs à mieux comprendre le livre.

Règles:
1. Retournez UNIQUEMENT la question, sans introduction ni explication
2. Concentrez-vous sur le contenu du livre, pas seulement sur le titre
3. Faites en sorte que la question soit pratique et réflexive
4. Gardez-la concise (15-25 mots)
5. Soyez créatif et générez une question différente à chaque fois, même pour le même livre""",

    # 日语
    'ja': """あなたは本のレビューの専門家です。{author}著の本「{title}」について、読者が本の核心的な考え、実用的な応用、または独自の視点をよりよく理解するのに役立つような、1つの洞察に富んだ質問を生成してください。

ルール：
1. 質問のみを返し、導入や説明は不要です
2. 本の内容に焦点を当て、タイトルだけに焦点を当てないでください
3. 質問を実用的で考えさせられるようにしてください
4. 15〜25文字以内に保ちます
5. 創造的に、同じ本でも毎回異なる質問を生成してください""",

    # 荷兰语
    'nl': """U bent een expert in boekrecensies. Voor het boek "{title}" van {author} genereert u ÉÉN inzichtelijke vraag die lezers helpt om het boek beter te begrijpen.

Regels:
1. Retourneer ALLEEN de vraag, zonder inleiding of uitleg
2. Concentreer u op de inhoud van het boek, niet alleen op de titel
3. Maak de vraag praktisch en nadenkend
4. Houd het kort (15-25 woorden)
5. Wees creatief en genereer elke keer een andere vraag, zelfs voor hetzelfde boek""",

    # 挪威语
    'no': """Du er en ekspert i bokanmeldelser. For boken "{title}" av {author}, generer ÉT innsiktsfullt spørsmål som hjelper lesere med å forstå boken bedre.

Regler:
1. Returner KUN spørsmålet, uten introduksjon eller forklaring
2. Fokuser på bokens innhold, ikke bare tittelen
3. Gjør spørsmålet praktisk og tankevekkende
4. Hold det kort (15-25 ord)
5. Vær kreativ og generer et annet spørsmål hver gang, selv for samme bok""",

    # 葡萄牙语
    'pt': """Você é um especialista em resenhas de livros. Para o livro "{title}" de {author}, gere UMA pergunta perspicaz que ajude os leitores a entender melhor o livro.

Regras:
1. Retorne APENAS a pergunta, sem introdução ou explicação
2. Concentre-se no conteúdo do livro, não apenas no título
3. Faça a pergunta prática e reflexiva
4. Mantenha-a breve (15-25 palavras)
5. Seja criativo e gere uma pergunta diferente cada vez, mesmo para o mesmo livro""",

    # 俄语
    'ru': """Вы эксперт в области рецензий на книги. Для книги "{title}" автора {author} сгенерируйте ОДИН проницательный вопрос, который поможет читателям лучше понять книгу.

Правила:
1. Верните ТОЛЬКО вопрос, без введения или объяснения
2. Сосредоточьтесь на содержании книги, а не только на названии
3. Сделайте вопрос практичным и провокационным
4. Сдерживайте его кратким (15-25 слов)
5. Будьте креативны и генерируйте разные вопросы каждый раз, даже для одной и той же книги""",

    # 瑞典语
    'sv': """Du är en expert på bokrecensioner. För boken "{title}" av {author}, generera EN insiktsfull fråga som hjälper läsarna att förstå boken bättre.

Regler:
1. Returnera ENDAST frågan, utan introduktion eller förklaring
2. Fokusera på bokens innehåll, inte bara titeln
3. Gör frågan praktisk och tankeväckande
4. Håll den kort (15-25 ord)
5. Var kreativ och generera en annan fråga varje gång, även för samma bok""",

    # 简体中文
    'zh': """你是一位专业的图书点评人。请为《{title}》（作者：{author}）生成一个有见地的问题，帮助读者更好地理解这本书的核心思想、实用价值或独特观点。

规则：
1. 只返回问题本身，不要加任何介绍或解释
2. 关注书籍的实质内容，而不是仅仅分析标题
3. 问题要实用且发人深省
4. 保持简洁（15-25字）
5. 保持创意，即使是同一本书，每次也要生成不同的问题""",

    # 繁体中文
    'zht': """你是一位專業的圖書點評人。請為《{title}》（作者：{author}）生成一個有見地的問題，幫助讀者更好地理解這本書的核心思想、實用價值或獨特觀點。

規則：
1. 只返回問題本身，不要加任何介紹或解釋
2. 關注書籍的實質內容，而不是僅僅分析標題
3. 問題要實用且發人深省
4. 保持簡潔（15-25字）
5. 保持創意，即使是同一本書，每次也要生成不同的問題""",

    # 粤语
    'yue': """你係一位專業嘅圖書點評人。請為《{title}》（作者：{author}）生成一個有見地嘅問題，幫助讀者更好噉理解呢本書嘅核心思想、實用價值或獨特觀點。

規則：
1. 淨係返回問題本身，唔好加任何介紹或解釋
2. 關注書籍嘅實質內容，而唔係淨係分析標題
3. 問題要實用同發人深省
4. 保持簡潔（15-25字）
5. 保持創意，即使係同一本書，每次都要生成唔同嘅問題""",
}

# 语言包
TRANSLATIONS = {
    # 英语 (en)
    'en': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Ask questions about a book using Grok',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Configuration',
        'token_label': 'X.AI Authorization Token:',
        'token_help': 'Format: Bearer xai-xxx or just xai-xxx (from <a href="https://console.x.ai">console.x.ai</a>)',
        'model_label': 'Model:',
        'model_placeholder': 'Default: grok-3-latest',
        'template_label': 'Prompt Template:',
        'template_placeholder': 'Example template:\nAbout the book "{title}": Author: {author}, Publisher: {publisher}, Publication Date: {pubdate}, Language: {language}, Series: {series}, My question is: {query}',
        'language_label': 'Interface Language:',
        'send_button': 'Send',
        'suggest_button': 'Suggest?',
        'loading': 'Loading',
        'shortcut_enter': 'Ctrl + Enter',
        'shortcut_return': 'Command + Return',
        'error_prefix': 'Error: ',
        'about': 'About',
        'about_title': 'About',
        'base_url_label': 'API Base URL:',
        'base_url_placeholder': 'Default: https://api.x.ai/v1',
        'input_placeholder': 'Type your question here...',
        'response_placeholder': 'Response will appear here...',
        'metadata_title': 'Title',
        'metadata_authors': 'Author',
        'metadata_publisher': 'Publisher',
        'metadata_pubdate': 'Publication Date',
        'metadata_language': 'Language',
        'metadata_series': 'Series',
        'menu_title': 'Ask',
        'menu_ask_grok': 'Ask Grok',
        'ok_button': 'OK',
        'save_button': 'Save',
        'save_success': 'Settings saved',
        'loading_text': 'Asking',
        'shortcuts_tab': 'Shortcuts',
        'shortcut_open_dialog': 'Open Ask Dialog',
        'author_name': 'Sheldon',
        'shortcuts_title': 'Shortcuts',
        'loading':'Loading',
        'network_error': 'Network error, please check your connection',
        'request_timeout': 'Request took too long, automatically terminated',
        'request_failed': 'Request failed, please try again later',
        'sending': 'Sending...',
        'requesting': 'Requesting, please wait',
        'formatting': 'Request successful, formatting',
        'no_metadata': 'No metadata available',
        'metadata': 'Metadata',
        'no_series': 'No Series',
        'unknown': 'Unknown',
        'question_too_long':'Question is too long, cannot be answered',
        'auth_token_required_title': 'Auth Token Required',
        'auth_token_required_message': 'Please set your Auth Token in the configuration dialog.',
        'invalid_token_title': 'Invalid Token Format',
        'invalid_token_message': 'The token format is invalid. It should start with "xai-" or "Bearer xai-".',
        'token_too_short_message': 'Token is too short. Please check and enter the complete token.',
        'auth_token_none_message': 'No auth token, Ask Grok can not work.'
    },

    # 丹麦语 (da)
    'da': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Stil spørgsmål om en bog med Grok',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Indstillinger',
        'token_label': 'X.AI Autorisationstoken:',
        'token_help': 'Format: Bearer xai-xxx eller bare xai-xxx (fra <a href="https://console.x.ai">console.x.ai</a>)',
        'model_label': 'Model:',
        'model_placeholder': 'Standard: grok-3-latest',
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
        'metadata_title': 'Otsikko',
        'metadata_authors': 'Kirjailija',
        'metadata_publisher': 'Kustantaja',
        'metadata_pubdate': 'Julkaisupäivä',
        'metadata_language': 'Kieli',
        'metadata_series': 'Sarja',
        'input_placeholder': 'Skriv dit spørgsmål her...',
        'menu_title': 'Spørg',
        'menu_ask_grok': 'Spørg Grok',
        'ok_button': 'OK',
        'save_button': 'Gem',
        'save_success': 'Indstillinger gemt',
        'response_placeholder': 'Groks svar vil blive vist her',
        'loading_text': 'Spørger',
        'suggest_button': 'Forslag?',
        'shortcuts_tab': 'Genveje',
        'shortcut_open_dialog': 'Åbn spørgsmålsvindue',
        'author_name': 'Sheldon',
        'shortcuts_title': 'Genveje',
        'loading':'Indlæser',
        'network_error': 'Netværksfejl, tjek venligst din forbindelse',
        'request_timeout': 'Anmodningen tog for lang tid, afbrudt automatisk',
        'request_failed': 'Anmodningen fejlede, prøv igen senere',
        'sending': 'Sender...',
        'requesting': 'Anmoder, vent venligst',
        'formatting': 'Anmodning succesfuld, formatterer',
        'no_metadata': 'Ingen metadata tilgængelig',
        'metadata': 'Metadata',
        'no_series': 'Ingen serie',
        'unknown': 'Ukendt',
        'question_too_long':'Spørgsmål for langt, kan ikke svare',
        'auth_token_required_title': 'Godkendelsestoken påkrævet',
        'auth_token_required_message': 'Indstil venligst dit godkendelsestoken i konfigurationsdialogboksen [Ask Grok].',
        'invalid_token_title': 'Ugyldigt token-format',
        'invalid_token_message': 'Token-formatet er ugyldigt. Det skal starte med "xai-" eller "Bearer xai-".',
        'token_too_short_message': 'Tokenet er for kort. Kontroller og indtast hele tokenet.',
        'auth_token_none_message': 'Ingen godkendelsestoken, Ask Grok kan ikke virke.'
    },
    
    # 德语 (de)
    'de': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Fragen zu einem Buch mit Grok stellen',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Konfiguration',
        'token_label': 'X.AI Autorisierungstoken:',
        'token_help': 'Format: Bearer xai-xxx oder einfach xai-xxx (von <a href="https://console.x.ai">console.x.ai</a>)',
        'model_label': 'Modell:',
        'model_placeholder': 'Standard: grok-3-latest',
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
        'response_placeholder': 'Groks Antwort wird hier angezeigt',
        'loading_text': 'Frage',
        'suggest_button': 'Vorschlag?',
        'shortcuts_tab': 'Tastenkombinationen',
        'shortcut_open_dialog': 'Fragenfenster öffnen',
        'author_name': 'Sheldon',
        'shortcuts_title': 'Tastenkombinationen',
        'loading':'Laden',
        'network_error': 'Netzwerkfehler, bitte überprüfen Sie Ihre Verbindung',
        'request_timeout': 'Anfrage dauerte zu lange, automatisch abgebrochen',
        'request_failed': 'Anfrage fehlgeschlagen, bitte versuchen Sie es später erneut',
        'sending': 'Senden...',
        'requesting': 'Anfrage, bitte warten',
        'formatting': 'Anfrage erfolgreich, formate',
        'no_metadata': 'Keine Metadaten verfügbar',
        'metadata': 'Metadaten',
        'no_series': 'Keine Serie',
        'unknown': 'Unbekannt',
        'question_too_long':'Frage zu lang, kann nicht beantworten',
        'auth_token_required_title': 'Authentifizierungstoken erforderlich',
        'auth_token_required_message': 'Bitte legen Sie das Authentifizierungstoken in der Konfigurationsdialogbox [Ask Grok] fest.',
        'invalid_token_title': 'Ungültiges Token-Format',
        'invalid_token_message': 'Das Token-Format ist ungültig. Es sollte mit "xai-" oder "Bearer xai-" beginnen.',
        'token_too_short_message': 'Token ist zu kurz. Bitte prüfen und den ganzen Token eingeben.',
        'auth_token_none_message': 'Kein Authentifizierungstoken, Ask Grok kann nicht funktionieren.'
    },
    
    # 西班牙语 (es)
    'es': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Hacer preguntas sobre un libro usando Grok',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Configuración',
        'token_label': 'Token de autorización X.AI:',
        'token_help': 'Formato: Bearer xai-xxx o simplemente xai-xxx (de <a href="https://console.x.ai">console.x.ai</a>)',
        'model_label': 'Modelo:',
        'model_placeholder': 'Predeterminado: grok-3-latest',
        'template_label': 'Modelo de prompt:',
        'template_placeholder': 'Ejemplo de modelo:\nSobre el libro "{title}": Autor: {author}, Editorial: {publisher}, Fecha de publicación: {pubdate}, Idioma: {language}, Serie: {series}, Mi pregunta es: {query}',
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
        'response_placeholder': 'La respuesta de Grok aparecerá aquí',
        'loading_text': 'Preguntando',
        'suggest_button': 'Sugerir?',
        'shortcuts_tab': 'Atajos',
        'shortcut_open_dialog': 'Abrir diálogo de preguntas',
        'author_name': 'Sheldon',
        'shortcuts_title': 'Atajos',
        'loading':'Cargando',
        'network_error': 'Error de red, por favor verifique su conexión',
        'request_timeout': 'La solicitud tardó demasiado, se terminó automáticamente',
        'request_failed': 'La solicitud falló, por favor inténtelo de nuevo más tarde',
        'sending': 'Enviando...',
        'requesting': 'Solicitando, por favor espere',
        'formatting': 'Solicitud exitosa, formateando',
        'no_metadata': 'No hay metadatos disponibles',
        'metadata': 'Metadatos',
        'no_series': 'Sin serie',
        'unknown': 'Desconocido',
        'question_too_long':'La pregunta es demasiado larga, no se puede responder',
        'auth_token_required_title': 'Token de autenticación requerido',
        'auth_token_required_message': 'Por favor, establezca su token de autenticación en el cuadro de diálogo de configuración de [Ask Grok].',
        'invalid_token_title': 'Formato de token inválido',
        'invalid_token_message': 'El formato del token es inválido. Debe comenzar con "xai-" o "Bearer xai-".',
        'token_too_short_message': 'Token es demasiado corto. Por favor, verifique y entre el token completo.',
        'auth_token_none_message': 'No hay token de autenticación, Ask Grok no puede funcionar.'
    },
    
    # 芬兰语 (fi)
    'fi': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Kysy kirjasta Grokin avulla',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Asetukset',
        'token_label': 'X.AI Valtuutusavain:',
        'token_help': 'Muoto: Bearer xai-xxx tai pelkkä xai-xxx (käyttäen <a href="https://console.x.ai">console.x.ai</a>)',
        'model_label': 'Malli:',
        'model_placeholder': 'Oletus: grok-3-latest',
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
        'response_placeholder': 'Grokin vastaus näkyy tässä',
        'loading_text': 'Kysytään',
        'suggest_button': 'Ehdota?',
        'shortcuts_tab': 'Pikanäppäimet',
        'shortcut_open_dialog': 'Avaa kysymysikkuna',
        'author_name': 'Sheldon',
        'shortcuts_title': 'Pikanäppäimet',
        'loading':'Ladataan',
        'network_error': 'Verkkovirhe, tarkista yhteytesi',
        'request_timeout': 'Pyyntö kesti liian kauan, automaattisesti keskeytetty',
        'request_failed': 'Pyyntö epäonnistui, yritä uudelleen myöhemmin',
        'sending': 'Lähetetään...',
        'requesting': 'Pyyntö, odota hetki',
        'formatting': 'Pyyntö onnistui, muotoillaan',
        'no_metadata': 'Ei metatietoa saatavilla',
        'metadata': 'Metatieto',
        'no_series': 'Ei sarjaa',
        'unknown': 'Tuntematon',
        'question_too_long':'Kysymys on liian pitkä, ei voida vastata',
        'auth_token_required_title': 'Todennustunniste vaaditaan',
        'auth_token_required_message': 'Aseta todennustunniste [Ask Grok] -asetusikkunassa.',
        'invalid_token_title': 'Virheellinen tunnisteen muoto',
        'invalid_token_message': 'Tunnisteen muoto on virheellinen. Sen pitäisi alkaa "xai-" tai "Bearer xai-".',
        'token_too_short_message': 'Tunnisteen on liian lyhyt. Tarkista ja kirjoita koko tunnisteen.',
        'auth_token_none_message': 'Tunnistetta ei ole asetettu, Ask Grok ei toimi.'
    },
    
    # 法语 (fr)
    'fr': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Poser des questions sur un livre avec Grok',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Configuration',
        'token_label': 'Token d\'autorisation X.AI :',
        'token_help': 'Format : Bearer xai-xxx ou simplement xai-xxx (à partir de <a href="https://console.x.ai">console.x.ai</a>)',
        'model_label': 'Modèle :',
        'model_placeholder': 'Par défaut : grok-3-latest',
        'template_label': 'Modèle de prompt :',
        'template_placeholder': 'Exemple de modèle :\nÀ propos du livre "{title}" : Auteur : {author}, Éditeur : {publisher}, Date de publication : {pubdate}, Langue : {language}, Série : {series}, Ma question est : {query}',
        'language_label': 'Langue de l\'interface :',
        'send_button': 'Envoyer',
        'shortcut_enter': 'Ctrl + Entrée',
        'shortcut_return': 'Command + Return',
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
        'response_placeholder': 'La réponse de Grok apparaîtra ici',
        'loading_text': 'Demande en cours',
        'suggest_button': 'Suggérer?',
        'shortcuts_tab': 'Raccourcis',
        'shortcut_open_dialog': 'Ouvrir la fenêtre de questions',
        'author_name': 'Sheldon',
        'shortcuts_title': 'Raccourcis',
        'loading':'Chargement',
        'network_error': 'Erreur réseau, veuillez vérifier votre connexion',
        'request_timeout': 'La requête a pris trop de temps, terminée automatiquement',
        'request_failed': 'La requête a échoué, veuillez réessayer plus tard',
        'sending': 'Envoi...',
        'requesting': 'Requête, veuillez patienter',
        'formatting': 'Requête réussie, mise en forme',
        'no_metadata': 'Aucune métadonnée disponible',
        'metadata': 'Métadonnées',
        'no_series': 'Pas de série',
        'unknown': 'Inconnu',
        'question_too_long':'La question est trop longue, impossible de répondre',
        'auth_token_required_title': 'Jeton d\'authentification requis',
        'auth_token_required_message': 'Veuillez définir votre jeton d\'authentification dans la boîte de dialogue de configuration [Ask Grok].',
        'invalid_token_title': 'Format de jeton non valide',
        'invalid_token_message': 'Le format du jeton n\'est pas valide. Il doit commencer par "xai-" ou "Bearer xai-".',
        'token_too_short_message': 'Le jeton est trop court. Veuillez vérifier et entrer le jeton complet.',
        'auth_token_none_message': 'Aucun jeton d\'authentification, Ask Grok ne peut pas fonctionner.'
    },
    
    # 日语 (ja)
    'ja': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Grokを使って本について質問する',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': '設定',
        'token_label': 'X.AI Authorization Token:',
        'token_help': '形式: Bearer xai-xxx または xai-xxx (から <a href="https://console.x.ai">console.x.ai</a> を使用)',
        'model_label': 'Model:',
        'model_placeholder': 'Default: grok-3-latest',
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
        'response_placeholder': 'Grokの回答がここに表示されます',
        'loading_text': '質問中',
        'suggest_button': '提案?',
        'shortcuts_tab': 'ショートカット',
        'shortcut_open_dialog': '質問ウィンドウを開く',
        'author_name': 'シェルドン',
        'shortcuts_title': 'ショートカット',
        'loading':'読み込み中',
        'network_error': 'ネットワークエラー、接続を確認してください',
        'request_timeout': 'リクエストが時間超過、自動終了しました',
        'request_failed': 'リクエストが失敗しました、後で再度試してください',
        'sending': '送信中...',
        'requesting': 'リクエスト中、少々お待ちください',
        'formatting': 'リクエスト成功、フォーマット中',
        'no_metadata': 'メタデータはありません',
        'metadata': 'メタデータ',
        'no_series': 'シリーズなし',
        'unknown': '不明',
        'question_too_long':'問題が長すぎ、答えられない',
        'auth_token_required_title': '認証トークンが必要です',
        'auth_token_required_message': '認証トークンを設定してください。',
        'invalid_token_title': '無効なトークン形式',
        'invalid_token_message': 'トークンの形式が無効です。"xai-"または"Bearer xai-"で始まる必要があります。',
        'token_too_short_message': 'トークンが短すぎます。トークンを確認して完全なトークンを入力してください。',
        'auth_token_none_message': '認証トークンがありません、Ask Grokは動作しません。'
    },
    
    # 荷兰语 (nl)
    'nl': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Stel vragen over een boek met Grok',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Instellingen',
        'token_label': 'X.AI Autorisatietoken:',
        'token_help': 'Formaat: Bearer xai-xxx of gewoon xai-xxx (van <a href="https://console.x.ai">console.x.ai</a>)',
        'model_label': 'Model:',
        'model_placeholder': 'Standaard: grok-3-latest',
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
        'response_placeholder': 'Het antwoord van Grok verschijnt hier',
        'loading_text': 'Vragen',
        'suggest_button': 'Suggestie?',
        'shortcuts_tab': 'Sneltoetsen',
        'shortcut_open_dialog': 'Vraagdialoog openen',
        'author_name': 'Sheldon',
        'shortcuts_title': 'Sneltoetsen',
        'loading':'Laden',
        'network_error': 'Netwerkfout, controleer uw verbinding',
        'request_timeout': 'Verzoek duurde te lang, automatisch beëindigd',
        'request_failed': 'Verzoek mislukt, probeer het later opnieuw',
        'sending': 'Verzenden...',
        'requesting': 'Verzoek, even geduld',
        'formatting': 'Verzoek succesvol, formatteren',
        'no_metadata': 'Geen metadata beschikbaar',
        'metadata': 'Metagegevens',
        'no_series': 'Geen serie',
        'unknown': 'Onbekend',
        'question_too_long':'Vraag is te lang, kan niet worden beantwoord',
        'auth_token_required_title': 'Auth Token vereist',
        'auth_token_required_message': 'Stel uw Auth Token in via het configuratievenster van [Ask Grok].',
        'invalid_token_title': 'Ongeldig tokenformaat',
        'invalid_token_message': 'Het tokenformaat is ongeldig. Het moet beginnen met "xai-" of "Bearer xai-".',
        'token_too_short_message': 'Het token is te kort. Controleer en voer het volledige token in.',
        'auth_token_none_message': 'Auth Token is niet ingesteld, Ask Grok kan niet werken.'
    },
    
    # 挪威语 (no)
    'no': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Still spørsmål om en bok med Grok',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Innstillinger',
        'token_label': 'X.AI Autorisasjonstoken:',
        'token_help': 'Format: Bearer xai-xxx eller bare xai-xxx (fra <a href="https://console.x.ai">console.x.ai</a>)',
        'model_label': 'Modell:',
        'model_placeholder': 'Standard: grok-3-latest',
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
        'response_placeholder': 'Groks svar vil bli vist her',
        'loading_text': 'Spør',
        'suggest_button': 'Forslag?',
        'shortcuts_tab': 'Hurtigtaster',
        'shortcut_open_dialog': 'Åpne spørsmålsdialog',
        'author_name': 'Sheldon',
        'shortcuts_title': 'Hurtigtaster',
        'loading':'Laster',
        'network_error': 'Nettverksfeil, sjekk tilkoblingen din',
        'request_timeout': 'Forespørselen tok for lang tid, automatisk avbrutt',
        'request_failed': 'Forespørselen feilet, prøv igjen senere',
        'sending': 'Sender...',
        'requesting': 'Forespørsel, vent litt',
        'formatting': 'Forespørsel vellykket, formatterer',
        'no_metadata': 'Ingen metadata tilgjengelig',
        'metadata': 'Metadata',
        'no_series': 'Ingen serie',
        'unknown': 'Ukjent',
        'question_too_long':'Spørsmålet er for langt, kan ikke besvares',
        'auth_token_required_title': 'Autorisasjonstoken kreves',
        'auth_token_required_message': 'Angi aut.token i konfigurasjonsdialogboksen [Ask Grok].',
        'invalid_token_title': 'Ugyldig tokenformat',
        'invalid_token_message': 'Tokenformatet er ugyldig. Det skal starte med "xai-" eller "Bearer xai-".',
        'token_too_short_message': 'Tokenet er for kort. Vennligst sjekk og skriv inn hele tokenet.',
        'auth_token_none_message': 'Ingen autentiseringstoken, Ask Grok fungerar inte.'
    },
    
    # 葡萄牙语 (pt)
    'pt': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Fazer perguntas sobre um livro usando Grok',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Configuração',
        'token_label': 'Token de autorização X.AI:',
        'token_help': 'Formato: Bearer xai-xxx ou simplesmente xai-xxx (de <a href="https://console.x.ai">console.x.ai</a>)',
        'model_label': 'Modelo:',
        'model_placeholder': 'Padrão: grok-3-latest',
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
        'response_placeholder': 'A resposta do Grok aparecerá aqui',
        'loading_text': 'Perguntando',
        'suggest_button': 'Sugerir?',
        'shortcuts_tab': 'Atalhos',
        'shortcut_open_dialog': 'Abrir diálogo de perguntas',
        'author_name': 'Sheldon',
        'shortcuts_title': 'Atalhos',
        'loading':'Carregando',
        'network_error': 'Erro de rede, verifique sua conexão',
        'request_timeout': 'A solicitação demorou muito, terminada automaticamente',
        'request_failed': 'A solicitação falhou, tente novamente mais tarde',
        'sending': 'Enviando...',
        'requesting': 'Solicitação, aguarde',
        'formatting': 'Solicitação bem-sucedida, formatando',
        'no_metadata': 'Nenhuma metadado disponível',
        'metadata': 'Metadados',
        'no_series': 'Sem série',
        'unknown': 'Desconhecido',
        'question_too_long':'A pergunta é muito longa, não pode ser respondida',
        'auth_token_required_title': 'Token de Autenticação Necessário',
        'auth_token_required_message': 'Defina o seu Token de Autenticação na caixa de diálogo de configuração [Ask Grok].',
        'invalid_token_title': 'Formato de Token Inválido',
        'invalid_token_message': 'O formato do token é inválido. Deve começar com "xai-" ou "Bearer xai-".',
        'token_too_short_message': 'O token é muito curto. Verifique e insira o token completo.',
        'auth_token_none_message': 'Token de autenticação não definido, Ask Grok não pode funcionar.'
    },
    
    # 俄语 (ru)
    'ru': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Задавать вопросы о книге с помощью Grok',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Настройки',
        'token_label': 'Токен авторизации X.AI:',
        'token_help': 'Формат: Bearer xai-xxx или просто xai-xxx (из <a href="https://console.x.ai">console.x.ai</a>)',
        'model_label': 'Модель:',
        'model_placeholder': 'По умолчанию: grok-3-latest',
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
        'response_placeholder': 'Ответ Grok появится здесь',
        'loading_text': 'Спрашиваю',
        'suggest_button': 'Предложить?',
        'shortcuts_tab': 'Горячие клавиши',
        'shortcut_open_dialog': 'Открыть диалог вопросов',
        'author_name': 'Шелдон',
        'shortcuts_title': 'Горячие клавиши',
        'loading':'Загрузка',
        'network_error': 'Ошибка сети, проверьте подключение',
        'request_timeout': 'Запрос занял слишком много времени, автоматически прерван',
        'request_failed': 'Запрос не удался, попробуйте еще раз позже',
        'sending': 'Отправка...',
        'requesting': 'Запрос, пожалуйста, подождите',
        'formatting': 'Запрос успешен, форматирую',
        'no_metadata': 'Нет метаданных',
        'metadata': 'Метаданные',
        'no_series': 'Нет серии',
        'unknown': 'Неизвестно',
        'question_too_long':'Вопрос слишком длинный, не может быть обработан',
        'auth_token_required_title': 'Требуется токен аутентификации',
        'auth_token_required_message': 'Установите токен аутентификации в диалоговом окне конфигурации [Ask Grok].',
        'invalid_token_title': 'Неверный формат токена',
        'invalid_token_message': 'Неверный формат токена. Он должен начинаться с "xai-" или "Bearer xai-".',
        'token_too_short_message': 'Токен слишком короткий. Проверьте и введите полный токен.',
        'auth_token_none_message': 'Токен аутентификации не установлен, Ask Grok не может работать.'
    },
    
    # 瑞典语 (sv)
    'sv': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': 'Ställ frågor om en bok med Grok',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': 'Inställningar',
        'token_label': 'X.AI Auktoriseringstoken:',
        'token_help': 'Format: Bearer xai-xxx eller bara xai-xxx (från <a href="https://console.x.ai">console.x.ai</a>)',
        'model_label': 'Modell:',
        'model_placeholder': 'Standard: grok-3-latest',
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
        'response_placeholder': 'Groks svar kommer att visas här',
        'loading_text': 'Frågar',
        'suggest_button': 'Föreslå?',
        'shortcuts_tab': 'Genvägar',
        'shortcut_open_dialog': 'Öppna frågedialog',
        'author_name': 'Sheldon',
        'shortcuts_title': 'Genvägar',
        'loading':'Laddar',
        'network_error': 'Nätverksfel, kontrollera din anslutning',
        'request_timeout': 'Begäran tog för lång tid, avslutades automatiskt',
        'request_failed': 'Begäran misslyckades, försök igen senare',
        'sending': 'Skickar...',
        'requesting': 'Begäran, vänligen vänta',
        'formatting': 'Begäran lyckades, formaterar',
        'no_metadata': 'Ingen metadata tillgänglig',
        'metadata': 'Metadata',
        'no_series': 'Ingen serie',
        'unknown': 'Okänd',
        'question_too_long':'Frågan är för lång, kan inte besvaras',
        'auth_token_required_title': 'Tillgångstoken krävs',
        'auth_token_required_message': 'Vänligen ange din autentiseringstoken i konfigurationsdialogrutan [Ask Grok].',
        'invalid_token_title': 'Ogiltigt tokenformat',
        'invalid_token_message': 'Tokenformatet är ogiltigt. Det måste börja med "xai-" eller "Bearer xai-".',
        'token_too_short_message': 'Token är för kort. Kontrollera och ange den fullständiga tokenen.',
        'auth_token_none_message': 'Ingen autentiseringstoken, Ask Grok kan inte fungera.'
    },
    
    # 简体中文 (zh)
    'zh': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': '使用 Grok 询问关于书籍的问题',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': '配置',
        'token_label': 'X.AI 授权令牌:',
        'token_help': '格式：Bearer xai-xxx 或直接 xai-xxx (从 <a href="https://console.x.ai">console.x.ai</a> 获取)',
        'model_label': '模型:',
        'model_placeholder': '默认：grok-3-latest',
        'template_label': '提示词模板:',
        'template_placeholder': '示例模板：\n关于《{title}》这本书的信息：作者：{author}，出版社：{publisher}，出版日期：{pubdate}，语言：{language}，系列：{series}，我的问题是：{query}',
        'language_label': '界面语言:',
        'send_button': '发送',
        'suggest_button': '建议？',
        'loading': '加载中',
        'shortcut_enter': 'Ctrl + Enter',
        'shortcut_return': 'Command + Return',
        'error_prefix': '错误：',
        'about': '关于',
        'about_title': '关于',
        'base_url_label': 'API 基础 URL:',
        'base_url_placeholder': '默认：https://api.x.ai/v1',
        'input_placeholder': '在这里输入你的问题...',
        'response_placeholder': 'Grok 的回答将显示在这里',
        'metadata_title': '标题',
        'metadata_authors': '作者',
        'metadata_publisher': '出版社',
        'metadata_pubdate': '出版日期',
        'metadata_language': '语言',
        'metadata_series': '系列',
        'menu_title': '询问',
        'menu_ask_grok': '询问 Grok',
        'ok_button': '确定',
        'save_button': '保存',
        'save_success': '设置已保存',
        'loading_text': '正在询问',
        'shortcuts_tab': '快捷键',
        'shortcut_open_dialog': '打开询问窗口',
        'author_name': 'Sheldon',
        'shortcuts_title': '快捷键',
        'loading':'加载中',
        'network_error': '网络错误，请检查网络连接',
        'request_timeout': '请求时间过长，已自动终止',
        'request_failed': '请求失败，请稍后重试',
        'sending': '发送中...',
        'requesting': '请求中，请稍等',
        'formatting': '请求成功，正在格式化',
        'no_metadata': '没有元数据',
        'metadata': '元数据',
        'no_series': '暂无',
        'unknown': '未知',
        'question_too_long':'问题过长，无法回答',
        'auth_token_required_title': '需要有授权令牌',
        'auth_token_required_message': '请在 [Ask Grok] 的配置对话框中设置授权令牌。',
        'invalid_token_title': '令牌格式无效',
        'invalid_token_message': '令牌格式无效，应以 "xai-" 或 "Bearer xai-" 开头。',
        'token_too_short_message': '令牌过短。请检查并输入完整令牌。',
        'auth_token_none_message': '授权令牌未设置，Ask Grok 无法工作。'
    },
    
    # 繁体中文 (zht)
    'zht': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': '用Grok詢問關於一本書的問題',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': '設定',
        'token_label': 'X.AI Authorization Token:',
        'token_help': '格式：Bearer xai-xxx 或直接輸入 xai-xxx (從 <a href="https://console.x.ai">console.x.ai</a> 獲取)',
        'model_label': 'Model:',
        'model_placeholder': 'Default: grok-3-latest',
        'template_label': '提示詞範本:',
        'template_placeholder': '範本示例：\n關於《{title}》這本書的資訊：作者：{author}，出版社：{publisher}，出版日期：{pubdate}，語言：{language}，系列：{series}，我的問題是：{query}',
        'language_label': '界面語言:',
        'send_button': '發送',
        'suggest_button': '建議？',
        'loading': 'Loading',
        'shortcut_enter': 'Ctrl + Enter',
        'shortcut_return': 'Command + Return',
        'error_prefix': '錯誤：',
        'about': '關於',
        'about_title': '關於',
        'base_url_label': 'API Base URL:',
        'base_url_placeholder': 'Default: https://api.x.ai/v1',
        'input_placeholder': '在此輸入你的問題...',
        'response_placeholder': 'Grok 的答案將顯示在這裡',
        'metadata_title': '書名',
        'metadata_authors': '作者',
        'metadata_publisher': '出版社',
        'metadata_pubdate': '出版日期',
        'metadata_language': '語言',
        'metadata_series': '系列',
        'menu_title': '詢問',
        'menu_ask_grok': '詢問 Grok',
        'ok_button': '確定',
        'save_button': '儲存',
        'save_success': '設定已儲存',
        'loading_text': '詢問中',
        'shortcuts_tab': '快速鍵',
        'shortcut_open_dialog': '開啟詢問視窗',
        'author_name': 'Sheldon',
        'shortcuts_title': '快速鍵',
        'loading':'Loading',
        'network_error': '網路錯誤，請檢查網路連線',
        'request_timeout': '請求時間過長，已經自動終止',
        'request_failed': '請求失敗，請稍後重試',
        'sending': '發送中...',
        'requesting': '請求中，請稍等',
        'formatting': '請求成功，正在格式化',
        'no_metadata': '沒有元資料',
        'metadata': '元資料',
        'no_series': '暫無',
        'unknown': '未知',
        'question_too_long':'問題過長，無法回答',
        'auth_token_required_title': '需要身份驗證令牌',
        'auth_token_required_message': '請在 [Ask Grok] 的配置對話框中設置授權令牌。',
        'invalid_token_title': '令牌格式無效',
        'invalid_token_message': '令牌格式無效，應以 "xai-" 或 "Bearer xai-" 開頭。',
        'token_too_short_message': '令牌過短。請檢查並輸入完整令牌。',
        'auth_token_none_message': '授權令牌未設置，Ask Grok 無法工作。'
    },
    
    # 粤语 (yue)
    'yue': {
        'plugin_name': 'Ask Grok',
        'plugin_desc': '用Grok問一本書嘅嘢',
        'shortcut': 'Command+L' if sys.platform == 'darwin' else 'Ctrl+L',
        'config_title': '設定',
        'token_label': 'X.AI Authorization Token:',
        'token_help': '格式：Bearer xai-xxx 或直接輸入 xai-xxx (從 <a href="https://console.x.ai">console.x.ai</a> 獲取)',
        'model_label': 'Model:',
        'model_placeholder': 'Default: grok-3-latest',
        'template_label': '提示詞範本:',
        'template_placeholder': '範本示例：\n關於《{title}》呢本書嘅資料：作者：{author}，出版社：{publisher}，出版日期：{pubdate}，語言：{language}，系列：{series}，我想問嘅係：{query}',
        'language_label': '界面語言:',
        'send_button': '發送',
        'suggest_button': '建議？',
        'loading': 'Loading',
        'shortcut_enter': 'Ctrl + Enter',
        'shortcut_return': 'Command + Return',
        'error_prefix': '出錯啦：',
        'about': '關於',
        'about_title': '關於',
        'base_url_label': 'API Base URL:',
        'base_url_placeholder': 'Default: https://api.x.ai/v1',
        'input_placeholder': '喺呢度輸入你嘅問題...',
        'response_placeholder': 'Grok 嘅答案將顯示喺呢度',
        'metadata_title': '書名',
        'metadata_authors': '作者',
        'metadata_publisher': '出版社',
        'metadata_pubdate': '出版日期',
        'metadata_language': '語言',
        'metadata_series': '系列',
        'menu_title': '問嘢',
        'menu_ask_grok': '問 Grok',
        'ok_button': '確定',
        'save_button': '保存',
        'save_success': '設定已保存',
        'loading_text': '問緊',
        'shortcuts_tab': '快速鍵',
        'shortcut_open_dialog': '開詢問視窗',
        'author_name': 'Sheldon',
        'shortcuts_title': '快速鍵',
        'loading':'Loading',
        'network_error': '網絡出咗問題，請檢查網絡',
        'request_timeout': '請求時間過長，已經自動停咗',
        'request_failed': '請求失敗，請稍後重試',
        'sending': '發送中...',
        'requesting': '請求中，請稍等',
        'formatting': '請求成功，正在格式化',
        'no_metadata': '冇元資料',
        'metadata': '元資料',
        'no_series': '冇系列',
        'unknown': '未知',
        'question_too_long':'問題過長，無法回答',
        'auth_token_required_title': '需要身份驗證令牌',
        'auth_token_required_message': '請在 [Ask Grok] 的配置對話框中設置授權令牌。',
        'invalid_token_title': '令牌格式無效',
        'invalid_token_message': '令牌格式無效，應以 "xai-" 或 "Bearer xai-" 開頭。',
        'token_too_short_message': '令牌過短。請檢查並輸入完整令牌。',
        'auth_token_none_message': '授權令牌未設置，Ask Grok 無法工作。'
    }
}

def get_translation(lang_code):
    """获取指定语言的翻译"""
    try:
        return TRANSLATIONS.get(lang_code, TRANSLATIONS['en'])
    except KeyError:
        return TRANSLATIONS['en']

def get_default_template(lang_code):
    """获取指定语言的默认提示词模板"""
    return DEFAULT_TEMPLATES.get(lang_code, DEFAULT_TEMPLATES['en'])
