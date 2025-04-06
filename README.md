# Ask Grok

[English](README.md) | [简体中文](README_zh.md)

A simple Calibre plugin that allows users to ask questions about books using Grok.

## Preview

<img src="https://github.com/sheldonrrr/ask_grok/blob/main/ask.gif" width="300">
<img src="https://github.com/sheldonrrr/ask_grok/blob/main/config.gif" width="300">

## Features

- Ask questions about books directly in Calibre
- Automatically includes the current book's metadata, no need to copy-paste or manually enter
- Single input-output dialog interface
- Configurable API key
- Configurable prompt template
- Previewable interface shortcuts
- Previewable plugin version information

## Installation

### Method 1: Install via GitHub zip plugin file

1. Download[Ask_Grok-v1.0.0.zip](https://github.com/sheldonrrr/ask_grok/releases/tag/v1.0.0)

Import the file to Calibre custom plugins:

1. In Calibre, select "Preferences" -> "Plugins" -> "Load plugin from file"
2. Select the downloaded plugin file to install
3. After installation, restart Calibre

### Method 2: Install via Calibre official plugin market

This method requires the plugin to be added to the Calibre plugin index before it can be searched. If searchable, I will update the index entry date here.

1. Open Calibre's `Preferences`
2. Open `Plugins`
3. Open `Get new plugins`
4. Enter `Ask Grok` in the `Filter by name`
5. Select the plugin to install
6. Restart Calibre

## Get Grok API Key

  - Go to Grok backend configuration address: https://console.x.ai/
  - Create a team if you don't have one
  - Select and enter the page: API Keys
  - Click the button: Create API Keys
  - Enter API Key naming, suggested: calibre_Ask_Grok
  - Click the button: Save
  - After successful creation, you will get a Key value: `Bearer x-ai *****`, or `x-ai *****`
  - Copy this Key

## Configure API Key

  - Click the Ask Grok dropdown menu in the menu bar, select `Configure`
  - Enter the API Key into the `X.AI Authorization Token` input box
  - Click the `Save` button
  - A `Save successful` text prompt will appear

## Interface Usage

1. Select a book in the Calibre library
2. Click the "Ask Grok" button in the toolbar
3. Enter your question in the popup dialog
4. Click "Send" to get Grok's answer
5. Click "Suggestion?" to request AI-generated questions

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

- Calibre 7.25 or higher
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

- When sending requests to Grok, the plugin will use the book's Metadata information, including: title, author, publisher, but will not include Tags, Comments, etc. that may contain user-defined information
- The Grok API Key is saved as a Json file locally after input and is not transmitted to the server
- Uses Python's requests module, does not go through third-party servers
- The plugin's privacy handling will depend on Grok's own privacy policy. Since Private Chat is not yet supported: yes, Grok will use your submitted data for model training
- The plugin supports getting the API Key from local environment variables, set `XAI_AUTH_TOKEN` in your local environment variables

> **Grok Official Statement**: Private Chat is private and won't appear in user's history or be used to train models. Grok may securely retain it for up to 30 days for safety purposes.
