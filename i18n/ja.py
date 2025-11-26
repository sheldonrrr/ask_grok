#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Japanese language translations for Ask Grok plugin.
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
            'plugin_name': 'Ask Grok',
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
            'suggest_button': 'ランダム質問',
            'copy_response': '回答をコピー',
            'copy_question_response': '問答をコピー',
            'copied': 'コピー完了！',
            'saved': '保存しました',
            'close_button': '閉じる',
            
            # UI - 設定フィールド
            'token_label': 'APIキー:',
            'model_label': 'モデル:',
            'language_label': '言語',
            'base_url_label': 'ベースURL:',
            'base_url_placeholder': 'デフォルト: {default_api_base_url}',
            'shortcut': 'ショートカットキー',
            'shortcut_open_dialog': 'ダイアログを開く',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'モデル',
            'current_ai': '現在のAI:',
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
            
            # エラーメッセージ
            'error': 'エラー: ',
            'network_error': '接続エラー',
            'request_timeout': 'リクエストタイムアウト',
            'request_failed': 'リクエスト失敗',
            'question_too_long': '質問が長すぎます',
            'auth_token_required_title': 'APIキーが必要です',
            'auth_token_required_message': 'プラグイン設定でAPIキーを設定してください',
            'error_preparing_request': 'リクエストの準備に失敗しました',
            'empty_suggestion': '空の提案',
            'process_suggestion_error': '提案処理エラー',
            'unknown_error': '不明なエラー',
            'unknown_model': '不明なモデル: {model_name}',
            'suggestion_error': '提案エラー',
            'random_question_success': 'ランダム質問が正常に生成されました！',
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
            'random_question_error': 'ランダム質問の生成中にエラーが発生しました',
            'clear_history_failed': '履歴のクリアに失敗しました',
            'clear_history_not_supported': '単一の本の履歴クリアはまだサポートされていません',
            'missing_required_config': '必要な設定が不足しています: {key}。設定を確認してください。',
            'api_key_too_short': 'APIキーが短すぎます。確認して完全なキーを入力してください。',
            
            # APIレスポンス処理
            'api_request_failed': 'APIリクエスト失敗: {error}',
            'api_content_extraction_failed': 'APIレスポンスからコンテンツを抽出できません',
            'api_invalid_response': '有効なAPIレスポンスを取得できません',
            'api_unknown_error': '不明なエラー: {error}',
            
            # ストリーミングレスポンス処理
            'stream_response_code': 'ストリーミングレスポンスステータスコード: {code}',
            'stream_continue_prompt': '前回の回答を続けてください。すでに提供された内容を繰り返さないでください。',
            'stream_continue_code_blocks': '前回の回答には閉じられていないコードブロックがあります。続けてこれらのコードブロックを完成させてください。',
            'stream_continue_parentheses': '前回の回答には閉じられていない括弧があります。続けてすべての括弧が正しく閉じられていることを確認してください。',
            'stream_continue_interrupted': '前回の回答が中断されたようです。続けて最後の考えや説明を完成させてください。',
            'stream_timeout_error': 'ストリーミング送信が60秒間新しいコンテンツを受信していません。接続の問題の可能性があります。',
            
            # APIエラーメッセージ
            'api_version_model_error': 'APIバージョンまたはモデル名エラー: {message}\n\n設定でAPIベースURLを"{base_url}"に、モデルを"{model}"または他の利用可能なモデルに更新してください。',
            'api_format_error': 'APIリクエストフォーマットエラー: {message}',
            'api_key_invalid': 'APIキーが無効または認証されていません: {message}\n\nAPIキーを確認し、APIアクセスが有効になっていることを確認してください。',
            'api_rate_limit': 'リクエストレート制限を超えました。後で再試行してください\n\n無料使用量を超えた可能性があります。次の原因が考えられます：\n1. 1分あたりのリクエストが多すぎる\n2. 1日あたりのリクエストが多すぎる\n3. 1分あたりの入力トークンが多すぎる',
            
            # 設定エラー
            'missing_config_key': '必要な設定キーが不足しています: {key}',
            'api_base_url_required': 'APIベースURLが必要です',
            'model_name_required': 'モデル名が必要です',
            'api_key_empty': 'APIキーが空です。有効なAPIキーを入力してください。',
            
            # 情報について
            'author_name': 'Sheldon',
            'user_manual': 'ユーザーマニュアル',
            'about_plugin': 'Ask Grokの特徴',
            'learn_how_to_use': '使い方',
            'email': 'iMessage',
            
            # モデル固有の設定
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'カスタム',
            'model_enable_streaming': 'ストリーミングを有効にする',
            'model_disable_ssl_verify': 'SSL認証を無効にする',
            
            # 共通システムメッセージ
            'default_system_message': 'あなたは本の分析の専門家です。あなたの任務は、洞察力のある質問と分析を提供することで、ユーザーが本をより良く理解できるように支援することです。',
            # Deprecation notice
            'deprecation_notice_title': '重要なお知らせ：プラグイン名変更',
            'deprecation_notice_message': '''Ask Grok プラグインは「Ask AI」に名称変更されました。

両方のプラグインは、calibreのオンラインプラグインリストで同じ作者「Sheldon」によって見つけることができます。

重要な変更点：
• 新しいAsk AIプラグインは、OpenAI、Anthropic、OpenRouter、Ollama、Geminiなど、より主流のAIサービスをサポートしています
• このプラグインは1ヶ月後に非推奨とマークされます

継続的な更新とサポートのため、新しいAsk AIプラグインへの切り替えをお勧めします。''',
            'deprecation_dont_show_again': '今後表示しない',
            'deprecation_got_it': '了解しました',
            'new_version_button': '新バージョン',
        }
