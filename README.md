# Ask Grok

[English](README.md) | [简体中文](README_zh.md)

A simple calibre plugin that allows users to ask questions about books using Grok.

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

Download the latest version in [releases page](https://github.com/sheldonrrr/ask_grok/releases).

Import the file to calibre custom plugins:

1. In calibre, select "Preferences" -> "Plugins" -> "Load Plugin from file"
2. Select the downloaded plugin file to install
3. After installation, restart calibre

## Get Grok API Key

  - Go to Grok backend configuration address: https://console.x.ai/
  - Create a team if you don't have one
  - Select and enter the page: API Keys
  - Click the button: Create API Keys
  - Enter API Key naming
  - Click the button: Save
  - After successful creation, you will get a Key value: `x-ai *****`
  - Copy this Key

## Configure API Key

  - Click the Ask Grok dropdown menu in the menu bar, select `Configure`
  - Enter the API Key into the `X.AI Authorization Token` input box
  - Click the `Save` button
  - A `Save successful` text prompt will appear

## Interface Usage

1. Select a book in the calibre library
2. Click the "Ask Grok" button in the toolbar
3. Enter your question in the popup dialog
4. Click "Send" to get Grok's answer
5. Click "Random Question" to request AI-generated questions

## Shortcuts
- [Global] Ask: Command + L

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

## Grok API Key Notes

- API call count depends on the account's permissions

## Privacy Handling

- The Grok API Key is saved as a Json file locally after input and is not transmitted to the server
- When sending requests to Grok, the plugin will use the book's Metadata information submitted to Grok
- The plugin's privacy handling will depend on Grok's own privacy policy. Since Private Chat is not yet supported: yes, Grok will use your submitted data for model training

# Troubleshooting

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
- When providing feedback, please do not provide your Grok API Key, please keep it confidential, once leaked, your Grok API Key may be abused.