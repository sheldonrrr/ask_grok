# Ask Grok

[English](README.md) | [简体中文](README_zh.md)

A simple Calibre plugin that allows users to ask questions about books using Grok.

## Features

- Direct integration with Calibre to query Grok about selected books
- Automatic inclusion of book metadata, no manual copying required
- Single input/output dialogue interface
- Configurable API key
- Customizable prompt templates
- Keyboard shortcuts with preview
- Plugin version information with preview

## Installation

### Method 1: Via Calibre Plugin Market

1. Open Calibre's `Preferences`
2. Navigate to `Plugins`
3. Click `Get new plugins`
4. Search for `Ask Grok` in the filter
5. Select and install the plugin
6. Restart Calibre

### Method 2: Manual Installation via GitHub

1. Download the [Ask Grok zip file]()

To import the file as a custom plugin in Calibre:

1. In Calibre, go to "Preferences" -> "Plugins" -> "Load plugin from file"
2. Select the downloaded plugin file
3. Restart Calibre after installation

## Getting Grok API Key

  - Visit the Grok configuration page: https://console.x.ai/
  - Create a team if you don't have one
  - Navigate to: API Keys
  - Click: Create API Keys
  - Enter a name for your API Key (suggested: calibre_Ask_Grok)
  - Click: Save
  - You'll receive a key in the format: `Bearer x-ai *****` or `x-ai *****`
  - Copy this key

## Configuring API Key

  - Click the Ask Grok dropdown menu and select `Configure`
  - Paste your API Key into the `X.AI Authorization Token` field
  - Click `Save`
  - You'll see a "Save successful" message

## Usage

1. Select a book in your Calibre library
2. Click the "Ask Grok" button in the toolbar
3. Enter your question in the dialog box
4. Click "Send" to get Grok's answer
5. Click "Suggest?" to have AI generate a question

## Keyboard Shortcuts
- [Global] Ask: Command + L

## Requirements

- Calibre 7.25 or higher
- External Python modules: Requests

### Built-in Python Modules Used
- PyQt5 (Qt GUI framework)
  - QtWidgets: QDialog, QVBoxLayout, QHBoxLayout, QLabel, etc.
  - QtCore: Qt, QTimer
  - Qt: QKeySequence, QAction, QMenu
- Standard Library
  - os: File and path operations
  - sys: System-specific parameters
  - json: JSON data handling
  - logging: Debug and error logging
  - datetime: Time operations
  - threading: Thread management

## Grok API Key Notes

- API call limits depend on your account permissions

## Privacy

- When sending requests to Grok, the plugin includes book metadata (title, author, publisher) but excludes user-specific data like Tags and Comments
- Grok API Keys are stored locally in a JSON file and are not transmitted to any server
- Uses Python's requests module directly, no third-party servers involved
- Privacy handling follows Grok's privacy policy. Note: Until Private Chat is supported, Grok may use submitted data for model training
- API Key can be set via local environment variable `XAI_AUTH_TOKEN`

> **Official Grok Statement**: Private Chat is private and won't appear in user's history or be used to train models. Grok may securely retain it for up to 30 days for safety purposes.