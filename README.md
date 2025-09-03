# Ask Grok

A simple calibre plugin that allows users to ask questions about books using various AI models including Grok, Google Gemini, and DeepSeek.

## Preview

<img src="https://github.com/sheldonrrr/ask_grok/blob/main/ask_grok_gif_preview.gif" width="400">

## Features

- Ask questions about books directly in calibre
- Automatically includes the current book's metadata, no need to copy-paste or manually enter
- Single input-output dialog interface
- Configurable API key
- Configurable prompt template
- Automatically display the most recent query history based on a book
- Supports copying answers, copying questions and answers

## Installation

### Install from calibre Plugin Index (Recommended)

Ask Grok is now available in the official calibre Plugin Index:

1. In calibre, select "Preferences" -> "Plugins" -> "Get new plugins"
2. Search for "Ask Grok" in the search box
3. Select the plugin and click "Install"
4. After installation, restart calibre

### Manual Installation

Alternatively, you can download the latest version from the [releases page](https://github.com/sheldonrrr/ask_grok/releases).

Import the file to calibre custom plugins:

1. In calibre, select "Preferences" -> "Plugins" -> "Load Plugin from file"
2. Select the downloaded plugin file to install
3. After installation, restart calibre

## Get API Keys

Grok(x.AI) https://console.x.ai/
Google Gemini https://aistudio.google.com/
DeepSeek https://platform.deepseek.com/

### Free API Key

Recently, Nvidia released a free API key for llama, Deepseek-r1, you can get free API key from [here](https://build.nvidia.com/).

Available models:
- meta/llama-4-maverick-17b-128e-instruct",
- meta/llama-4-scout-17b-16e-instruct
- meta/llama-3.3-70b-instruct
- deepseek-ai/deepseek-r1
- qwen/qwen2.5-coder-32b-instruct

Base URL:
`https://integrate.api.nvidia.com/v1`

API Key:
- After logging in and validating through your phone number, you can generate an API Key to use. Now the only limit is the rate limit, just limited to 40 RPM.(If you are using it for personal use, there is almost no limit.)

## Configure API Key

  - Click the Ask Grok dropdown menu in the menu bar, select `Configure`
  - Select the AI model you want to use (Grok, Google Gemini, or DeepSeek)
  - Enter the corresponding API Key into the API Key input box
  - Click the `Save` button
  - Done

## Interface Usage

1. Select a book in the calibre library
2. Click the "Ask Grok" button in the toolbar
3. Enter your question in the popup dialog
4. Click "Send" to get an answer from your configured AI model (Grok, Google Gemini, or DeepSeek)
5. Click "Random Question" to request AI-generated questions based on your selected language

## Language Support

- Danish (da)
- German (de)
- English (en)
- Spanish (es)
- Finnish (fi)
- French (fr)
- Japanese (ja)
- Dutch (nl)
- Norwegian (no)
- Portuguese (pt)
- Russian (ru)
- Swedish (sv)
- Simplified Chinese (zh)
- Traditional Chinese (zht)
- Cantonese (yue)

## Requirements

- calibre 7.25 or higher
- External Python modules:
  - requests
  - bleach
  - markdown2

### Built-in Python Modules Used

- PyQt5 (Qt GUI Framework)
  - QtWidgets: QDialog, QVBoxLayout, QHBoxLayout, QLabel, etc.
  - QtCore: Qt, QTimer
  - Qt: QKeySequence, QAction, QMenu
- Standard Library
  - os: File and path operations
  - sys: System-related parameters
  - json: JSON data processing
  - logging: Debug and error logs
  - datetime: Time operations
  - threading: Thread management

## Privacy Handling

- The AI providers' API Keys (Grok, Google Gemini, DeepSeek) are saved as a Json file locally after input and are not transmitted to any third-party servers
- When sending requests to AI providers, the plugin will use the book's Metadata information submitted to the selected AI provider
- The plugin's privacy handling will depend on each AI provider's own privacy policy.

## Troubleshooting

If you continue to experience `Request failed` or other issues, please delete the Ask Grok and related configuration files and then re-install the latest version of the plugin.

Delete Ask Grok and related configuration files:
- calibre Preference
- Miscellaneous
- Open calibre Configuration Folder(Button)
- Plugins(Open this folder)
- Delete all things with `ask_grok` as prefix
- Install Plugin's Latest Version
- Restart calibre

About Ask Grok Configuration Files:
- Ask Grok.zip/Ask Grok folder: Plugin folder, delete it to remove the plugin
- ask_grok.json: Plugin configuration file, delete it to remove the plugin's configuration information
- ask_grok.logs folder: Plugin log folder, delete it to remove the plugin's log information
- ask_grok_latest_history.json: Plugin recent query history file, delete it to remove the plugin's recent query history information

Note!
- When providing feedback, please do not provide your AI provider's API Key, please keep it confidential, once leaked, your AI provider's API Key may be abused.