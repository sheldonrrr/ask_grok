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
    def multi_book_default_template(self) -> str:
        return """複数の本に関する情報は次のとおりです：{books_metadata} ユーザーの質問：{query} 上記の本の情報に基づいて質問に答えてください。"""
    
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
            'export_current_qa': '現在のQ&Aをエクスポート',
            'export_history': '履歴をエクスポート',
            
            # エクスポート設定
            'export_settings': 'エクスポート設定',
            'enable_default_export_folder': 'デフォルトフォルダにエクスポート',
            'no_folder_selected': 'フォルダが選択されていません',
            'browse': '参照...',
            'select_export_folder': 'エクスポートフォルダを選択',
            
            # ボタンテキストとメニュー項目
            'copy_response_btn': '回答をコピー',
            'copy_qa_btn': 'Q&Aをコピー',
            'export_current_btn': 'Q&AをPDFにエクスポート',
            'export_history_btn': '履歴をPDFにエクスポート',
            'copy_mode_response': '回答',
            'copy_mode_qa': 'Q&A',
            'export_mode_current': '現在のQ&A',
            'export_mode_history': '履歴',
            
            # PDFエクスポート関連
            'model_provider': 'プロバイダ',
            'model_name': 'モデル',
            'model_api_url': 'APIベースURL',
            'pdf_model_info': 'AIモデル情報',
            'pdf_software': 'ソフトウェア',
            
            'export_all_history_dialog_title': 'すべての履歴をPDFにエクスポート',
            'export_all_history_title': 'すべての問答履歴',
            'export_history_insufficient': 'エクスポートには少なくとも2件の履歴記録が必要です。',
            'history_record': '記録',
            'question_label': '質問',
            'answer_label': '回答',
            'default_ai': 'デフォルトAI',
            'export_time': 'エクスポート日時',
            'total_records': '総記録数',
            'info': '情報',
            'yes': 'はい',
            'no': 'いいえ',
            'no_book_selected_title': '本が選択されていません',
            'no_book_selected_message': '質問する前に本を選択してください。',
            'set_default_ai_title': 'デフォルトAIを設定',
            'set_default_ai_message': '"{0}"に切り替えました。今後のクエリのデフォルトAIとして設定しますか？',
            'set_default_ai_success': 'デフォルトAIが"{0}"に設定されました。',
            'copied': 'コピーされました！',
            'pdf_exported': 'PDFをエクスポートしました！',
            'export_pdf_dialog_title': 'PDFにエクスポート',
            'export_pdf_error': 'PDFのエクスポートに失敗しました: {0}',
            'no_question': '質問なし',
            'saved': '保存しました',
            'close_button': '閉じる',
            'open_local_tutorial': 'ローカルチュートリアルを開く',
            'tutorial_open_failed': 'チュートリアルを開けませんでした',
            'tutorial': 'チュートリアル',
            
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
            'no_history': '履歴レコードなし',
            'empty_question_placeholder': '（質問なし）',
            'history_ai_unavailable': 'このAIは設定から削除されました',
            'clear_current_book_history': '現在の本の履歴をクリア',
            'confirm_clear_book_history': '以下の本のすべての履歴を消去してもよろしいですか？\n{book_titles}',
            'confirm': '確認',
            'history_cleared': '{deleted_count}件の履歴記録が消去されました。',
            'multi_book_template_label': '複数本プロンプトテンプレート:',
            'multi_book_placeholder_hint': '{books_metadata}を本の情報に、{query}をユーザーの質問に使用してください',
            
            # エラーメッセージ
            'network_error': 'ネットワークエラー',
            'request_timeout': 'リクエストがタイムアウトしました',
            'request_failed': 'リクエストに失敗しました',
            'question_too_long': '質問が長すぎます',
            'auth_token_required_title': 'APIキーが必要です',
            'auth_token_required_message': 'プラグイン設定で有効なAPIキーを設定してください。',
            'open_configuration': '設定を開く',
            'cancel': 'キャンセル',
            "invalid_default_ai_title": "無効なデフォルトAI",
            "invalid_default_ai_message": "デフォルトのAI「{default_ai}」が正しく設定されていません。\n\n代わりに「{first_ai}」に切り替えますか？",
            "switch_to_ai": "{ai} に切り替える",
            "keep_current": "現在のままにする",
            'error_preparing_request': 'リクエストの準備に失敗しました',
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
            'rate_limit': 'リクエストが多すぎます',
            'invalid_json': '無効なJSON',
            'no_response': '応答なし',
            'template_error': 'テンプレートエラー',
            'no_model_configured': 'AIモデルが設定されていません。設定でAIモデルを設定してください。',
            'no_ai_configured_title': 'AIが設定されていません',
            'no_ai_configured_message': 'ようこそ！本について質問を始めるには、まずAIプロバイダーを設定する必要があります。\n\n初心者におすすめ：\n• Nvidia AI - 電話番号だけで6ヶ月間の無料APIアクセスを取得（クレジットカード不要）\n• Ollama - コンピューターでローカルにAIモデルを実行（完全に無料でプライベート）\n\n今すぐプラグイン設定を開いてAIプロバイダーを設定しますか？',
            'open_settings': 'プラグイン設定',
            'ask_anyway': 'とにかく質問する',
            'later': '後で',
            'reset_all_data': 'すべてのデータをリセット',
            'reset_all_data_warning': 'これにより、すべてのAPIキー、プロンプトテンプレート、ローカル履歴レコードが削除されます。言語設定は保持されます。慎重に進めてください。',
            'reset_all_data_confirm_title': 'リセットの確認',
            'reset_all_data_confirm_message': 'プラグインを初期状態にリセットしてもよろしいですか？\n\nこれにより永久に削除されます：\n• すべてのAPIキー\n• すべてのカスタムプロンプトテンプレート\n• すべての会話履歴\n• すべてのプラグイン設定（言語設定は保持されます）\n\nこの操作は元に戻せません！',
            'reset_all_data_success': 'すべてのプラグインデータが正常にリセットされました。変更を有効にするためにcalibreを再起動してください。',
            'reset_all_data_failed': 'プラグインデータのリセットに失敗しました: {error}',
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
            'select_model': '-- モデルを切り替え --',
            'request_model_list': 'モデルリストをリクエストしてください',
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
            'default_ai_mismatch_title': 'デフォルトAIが変更されました',
            'default_ai_mismatch_message': '設定のデフォルトAIが"{default_ai}"に変更されましたが、\n現在のダイアログは"{current_ai}"を使用しています。\n\n新しいデフォルトAIに切り替えますか？',
            'discard_changes': '変更を破棄',
            'empty_response': 'APIから空のレスポンスを受信しました',
            'empty_response_after_filter': 'thinkタグのフィルタリング後、レスポンスが空です',
            'error_401': 'APIキー認証に失敗しました。確認してください：APIキーが正しい、アカウントに十分な残高がある、APIキーが期限切れでない。',
            'error_403': 'アクセスが拒否されました。確認してください：APIキーに十分な権限がある、地域アクセス制限がない。',
            'error_404': 'APIエンドポイントが見つかりません。APIベースURLの設定が正しいか確認してください。',
            'error_429': 'リクエストが多すぎます。レート制限に達しました。後でもう一度お試しください。',
            'error_5xx': 'サーバーエラー。後でもう一度お試しいただくか、サービスプロバイダーのステータスを確認してください。',
            'error_network': 'ネットワーク接続に失敗しました。ネットワーク接続、プロキシ設定、またはファイアウォール設定を確認してください。',
            'error_unknown': '不明なエラー。',
            'gemini_geo_restriction': 'Gemini APIはお住まいの地域では利用できません。お試しください：\n1. サポートされている地域からVPNを使用して接続する\n2. 他のAIプロバイダーを使用する（OpenAI、Anthropic、DeepSeekなど）\n3. Google AI Studioで地域の利用可能性を確認する',
            'load_models_list': 'モデルリストを読み込む',
            'loading_models_text': 'モデルを読み込んでいます',
            'model_test_success': 'モデルテストが成功しました！設定が保存されました。',
            'models_loaded_with_selection': '{count}個のモデルが正常に読み込まれました。\n選択されたモデル：{model}',
            'ollama_model_not_available': 'モデル"{model}"は利用できません。確認してください：\n1. モデルは起動していますか？実行：ollama run {model}\n2. モデル名は正しいですか？\n3. モデルはダウンロードされていますか？実行：ollama pull {model}',
            'ollama_service_not_running': 'Ollamaサービスが実行されていません。最初にOllamaサービスを起動してください。',
            'ollama_service_timeout': 'Ollamaサービス接続タイムアウト。サービスが正常に実行されているか確認してください。',
            'reset_ai_confirm_message': '{ai_name}をデフォルト状態にリセットしようとしています。\n\nこれにより以下がクリアされます：\n• APIキー\n• カスタムモデル名\n• その他の設定パラメータ\n\n続行しますか？',
            'reset_ai_confirm_title': 'リセットの確認',
            'reset_current_ai': '現在のAIをデフォルトにリセット',
            'reset_tooltip': '現在のAIをデフォルト値にリセット',
            'save_and_close': '保存して閉じる',
            'skip': 'スキップ',
            'technical_details': '技術的な詳細',
            'test_current_model': '現在のモデルをテスト',
            'test_model_button': 'モデルをテスト',
            'test_model_prompt': 'モデルが正常に読み込まれました！選択されたモデル"{model}"をテストしますか？',
            'unsaved_changes_message': '保存されていない変更があります。どうしますか？',
            'unsaved_changes_title': '未保存の変更',


            'pdf_info_not_available': '情報なし',
        }