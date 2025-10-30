#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Japanese language translations for Ask AI Plugin.
"""

from ..models.base import BaseTranslation, TranslationRegistry, AIProvider


@TranslationRegistry.register
class JapaneseTranslation(BaseTranslation):
    """Japanese language translation."""
    
    @property
    def code(self) -> str:
        return "ja"
    
    @property
    def name(self) -> str:
        return "日本語"
    
    @property
    def default_template(self) -> str:
        return '本について "{title}": 著者: {author}, 出版社: {publisher}, 出版年: {pubyear}, 言語: {language}, シリーズ: {series}, 質問: {query}'
    
    @property
    def suggestion_template(self) -> str:
        return """あなたは本のレビューの専門家です。{author}著の本「{title}」公開言語は「{language}」について、読者が本の核心的な考え、実用的な応用、または独自の視点をよりよく理解するのに役立つような、1つの洞察に富んだ質問を生成してください。ルール： 1. 質問のみを返し、導入や説明は不要です 2. 本の内容に焦点を当て、タイトルだけに焦点を当てないでください 3. 質問を実用的で考えさせられるようにしてください 4. 30〜200文字以内に保ちます 5. 創造的に、同じ本でも毎回異なる質問を生成してください"""
    
    @property
    def translations(self) -> dict:
        return {
            # プラグイン情報
            'plugin_name': 'Ask AI Plugin',
            'plugin_desc': 'AIを使用して本について質問する',
            
            # UI - タブとセクション
            'config_title': '設定',
            'general_tab': '一般',
            'ai_models': 'AI',
            'shortcuts': 'ショートカット',
            'about': '情報',
            'metadata': 'メタデータ',
            
            # UI - ボタンとアクション
            'ok_button': 'OK',
            'save_button': '保存',
            'send_button': '送信',
            'stop_button': '停止',
            'suggest_button': 'ランダム質問',
            'copy_response': '回答をコピー',
            'copy_question_response': '問答をコピー',
            'export_pdf': 'PDFをエクスポート',
            'copied': 'コピー完了！',
            'pdf_exported': 'PDFをエクスポートしました！',
            'export_pdf_dialog_title': 'PDFにエクスポート',
            'export_pdf_error': 'PDFのエクスポートに失敗しました: {0}',
            'no_question': '質問なし',
            'no_response': '回答なし',
            'saved': '保存しました',
            'close_button': '閉じる',
            
            # UI - 設定フィールド
            'token_label': 'APIキー:',
            'api_key_label': 'APIキー:',
            'model_label': 'モデル:',
            'language_label': '言語:',
            'language_label_old': '言語',
            'base_url_label': 'ベースURL:',
            'base_url_placeholder': 'デフォルト: {default_api_base_url}',
            'shortcut': 'ショートカットキー',
            'shortcut_open_dialog': 'ダイアログを開く',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'モデル',
            'action': 'アクション',
            'reset_button': 'リセット',
            'prompt_template': 'プロンプトテンプレート',
            'ask_prompts': '質問プロンプト',
            'random_questions_prompts': 'ランダム質問プロンプト',
            'display': '表示',
            
            # UI - ダイアログ要素
            'input_placeholder': '質問を入力してください...',
            'response_placeholder': '回答はすぐに表示されます...',
            
            # UI - メニューアイテム
            'menu_title': '質問',
            'menu_ask': '{model}に質問',
            
            # UI - ステータスメッセージ
            'loading': '読み込み中',
            'loading_text': '質問中',
            'save_success': '設定を保存しました',
            'sending': '送信中...',
            'requesting': 'リクエスト中',
            'formatting': 'リクエスト成功、フォーマット中',
            
            # UI - モデルリスト機能
            'load_models': 'モデルを読み込む',
            'use_custom_model': 'カスタムモデル名を使用',
            'custom_model_placeholder': 'カスタムモデル名を入力',
            'model_placeholder': 'まずモデルを読み込んでください',
            'models_loaded': '{count}個のモデルを正常に読み込みました',
            'load_models_failed': 'モデルの読み込みに失敗しました: {error}',
            'model_list_not_supported': 'このプロバイダーはモデルの自動取得をサポートしていません',
            'api_key_required': 'まずAPIキーを入力してください',
            'invalid_params': '無効なパラメーター',
            'warning': '警告',
            'success': '成功',
            'error': 'エラー',
            
            # メタデータフィールド
            'metadata_title': 'タイトル',
            'metadata_authors': '著者',
            'metadata_publisher': '出版社',
            'metadata_pubyear': '出版日',
            'metadata_language': '言語',
            'metadata_series': 'シリーズ',
            'no_metadata': 'メタデータなし',
            'no_series': 'シリーズなし',
            'unknown': '不明',
            
            # 複数冊の本の機能
            'books_unit': '冊',
            'new_conversation': '新しい会話',
            'single_book': '単一の本',
            'multi_book': '複数冊の本',
            'deleted': '削除されました',
            'history': '履歴',
            'multi_book_template_label': '複数冊の本のプロンプトテンプレート:',
            'multi_book_placeholder_hint': '本の情報には {books_metadata}、ユーザーの質問には {query} を使用',
            
            # エラーメッセージ
            'error': 'エラー: ',
            'network_error': 'ネットワークエラー',
            'request_timeout': 'リクエストがタイムアウトしました',
            'request_failed': 'リクエストに失敗しました',
            'question_too_long': '質問が長すぎます',
            'auth_token_required_title': 'APIキーが必要です',
            'auth_token_required_message': 'APIキーをプラグイン設定で設定してください。',
            'error_preparing_request': 'リクエストの準備中にエラーが発生しました',
            'empty_suggestion': '空の提案',
            'process_suggestion_error': '提案の処理中にエラーが発生しました',
            'unknown_error': '不明なエラー',
            'unknown_model': '不明なモデル: {model_name}',
            'suggestion_error': '提案エラー',
            'random_question_success': 'ランダムな質問が正常に生成されました！',
            'book_title_check': '本のタイトルが必要です',
            'avoid_repeat_question': '別の質問を使用してください',
            'empty_answer': '空の回答',
            'invalid_response': '無効な応答',
            'auth_error_401': '認証されていません',
            'auth_error_403': 'アクセスが拒否されました',
            'rate_limit': 'レート制限を超過しました',
            'invalid_json': '無効なJSON',
            'no_response': '応答なし',
            'template_error': 'テンプレートエラー',
            'no_model_configured': 'AIモデルが設定されていません。設定でAIモデルを設定してください。',
            'random_question_error': 'ランダムな質問の生成中にエラーが発生しました',
            'clear_history_failed': '履歴のクリアに失敗しました',
            'clear_history_not_supported': '単一の本の履歴クリアはまだサポートされていません',
            'missing_required_config': '必要な設定が不足しています: {key}。設定を確認してください。',
            'api_key_too_short': 'APIキーが短すぎます。確認して完全なキーを入力してください。',
            
            # API応答処理
            'api_request_failed': 'APIリクエストに失敗しました: {error}',
            'api_content_extraction_failed': 'API応答からコンテンツを抽出できませんでした',
            'api_invalid_response': '有効なAPI応答を取得できませんでした',
            'api_unknown_error': '不明なエラー: {error}',
            
            # ストリーミング応答処理
            'stream_response_code': 'ストリーミング応答ステータスコード: {code}',
            'stream_continue_prompt': 'すでに提供されたコンテンツを繰り返さずに、前の応答を続けてください。',
            'stream_continue_code_blocks': '前の応答には閉じられていないコードブロックがありました。続けてこれらのコードブロックを完成させてください。',
            'stream_continue_parentheses': '前の応答には閉じられていない括弧がありました。続けて、すべての括弧が適切に閉じられていることを確認してください。',
            'stream_continue_interrupted': '前の応答が中断されたようです。続けて、最後の考えや説明を完了させてください。',
            'stream_timeout_error': 'ストリーミング送信が60秒間新しいコンテンツを受信していません。接続の問題の可能性があります。',
            
            # APIエラーメッセージ
            'api_version_model_error': 'APIバージョンまたはモデル名のエラー: {message}\n\n設定でAPIベースURLを「{base_url}」に、モデルを「{model}」または利用可能な別のモデルに更新してください。',
            'api_format_error': 'APIリクエスト形式のエラー: {message}',
            'api_key_invalid': 'APIキーが無効または認証されていません: {message}\n\nAPIキーを確認し、APIアクセスが有効になっていることを確認してください。',
            'api_rate_limit': 'リクエストレート制限を超過しました。後で再試行してください\n\n無料使用量を超えた可能性があります。次の原因が考えられます：\n1. 1分あたりのリクエストが多すぎる\n2. 1日あたりのリクエストが多すぎる\n3. 1分あたりの入力トークンが多すぎる',
            
            # 設定エラー
            'missing_config_key': '必要な設定キーが不足しています: {key}',
            'api_base_url_required': 'APIベースURLが必要です',
            'model_name_required': 'モデル名が必要です',
            'api_key_empty': 'APIキーが空です。有効なAPIキーを入力してください。',
            
            # モデルリスト取得
            'fetching_models_from': '{url}からモデルを取得中',
            'successfully_fetched_models': '{count}個の{provider}モデルを正常に取得しました',
            'failed_to_fetch_models': 'モデルの取得に失敗しました：{error}',
            
            # 情報について
            'author_name': 'Sheldon',
            'user_manual': 'ユーザーマニュアル',
            'about_plugin': 'Ask AI Pluginの特徴',
            'learn_how_to_use': '使い方',
            'email': 'iMessage',
            
            # モデル固有の設定
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'カスタム',
            'model_enable_streaming': 'ストリーミングを有効にする',
            'model_disable_ssl_verify': 'SSL検証を無効にする',
            
            # AIスイッチャー
            'current_ai': '現在のAI',
            'no_configured_models': 'AIが設定されていません - 設定で設定してください',
            
            # プロバイダー固有の情報
            'nvidia_free_info': '💡 新規ユーザーは6か月間無料でAPIアクセスを利用できます - クレジットカードは不要です',
            
            # 一般的なシステムメッセージ
            'default_system_message': 'あなたは本の分析の専門家です。あなたの仕事は、洞察に満ちた質問と分析を提供することで、ユーザーが本をよりよく理解できるようにすることです。',
            
            # リクエストタイムアウト設定
            'request_timeout_label': 'リクエストタイムアウト:',
            'seconds': '秒',
            'request_timeout_error': 'リクエストがタイムアウトしました。現在のタイムアウト: {timeout}秒',
            
            # 並列AI設定
            'parallel_ai_count_label': '並列AIの数:',
            'parallel_ai_count_tooltip': '同時にクエリを実行するAIモデルの数（1-2が利用可能、3-4は近日公開）',
            'parallel_ai_notice': '注意: これは質問の送信にのみ影響します。ランダムな質問は常に単一のAIを使用します。',
            'suggest_maximize': 'ヒント: 3つのAIでより見やすくするためにウィンドウを最大化してください',
            'ai_panel_label': 'AI {index}:',
            'no_ai_available': 'このパネルで利用可能なAIはありません',
            'add_more_ai_providers': '設定でAIプロバイダーを追加してください',
            'select_ai': '-- AIを選択 --',
            'coming_soon': '近日公開',
            'advanced_feature_tooltip': 'この機能は開発中です。更新情報にご期待ください！',
            
            # PDFエクスポートセクションのタイトル
            'pdf_book_metadata': '書籍のメタデータ',
            'pdf_question': '質問',
            'pdf_answer': '回答',
            'pdf_ai_model_info': 'AIモデル情報',
            'pdf_generated_by': '生成元',
            'pdf_provider': 'プロバイダー',
            'pdf_model': 'モデル',
            'pdf_api_base_url': 'APIベースURL',
            'pdf_panel': 'パネル',
            'pdf_plugin': 'プラグイン',
            'pdf_github': 'GitHub',
            'pdf_software': 'ソフトウェア',
            'pdf_generated_time': '生成時刻',
            'pdf_info_not_available': '情報なし',
        }