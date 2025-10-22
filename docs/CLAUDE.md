# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Ask Grok is a Calibre plugin that allows users to ask questions about books using various AI models including Grok (x.AI), Google Gemini, and DeepSeek. The plugin integrates directly into the Calibre interface, providing a seamless experience for users to interact with AI about their books.

## Architecture

The project follows a modular architecture with clear separation of concerns:

1. **Main Plugin Entry Point** (`__init__.py`) - Handles plugin registration with Calibre
2. **UI Components** (`ui.py`) - Implements the graphical interface and user interactions
3. **API Layer** (`api.py`) - Manages communication with different AI providers
4. **Model Abstraction** (`models/`) - Provides a unified interface for different AI models
5. **Configuration** (`config.py`) - Handles user preferences and settings
6. **Internationalization** (`i18n/`) - Supports multiple languages
7. **Utilities** (`utils.py`, `response_handler.py`, `random_question.py`) - Helper functions and specialized components

## Key Design Patterns

1. **Factory Pattern** - `AIModelFactory` creates instances of different AI models based on configuration
2. **Abstract Base Class** - `BaseAIModel` defines the interface that all AI model implementations must follow
3. **Strategy Pattern** - Different AI models can be selected and used interchangeably
4. **Observer Pattern** - Signal-based communication between UI components

## AI Model Architecture

The system supports multiple AI providers through a unified interface:

- **Grok** (x.AI) - Default model with streaming support
- **Google Gemini** - Google's AI model with streaming support
- **DeepSeek** - DeepSeek's AI model
- **Custom** - Allows connecting to any OpenAI-compatible API

Each model implementation:
- Inherits from `BaseAIModel`
- Implements provider-specific authentication and request formatting
- Handles streaming responses and error recovery
- Provides model-specific configuration defaults

## Common Development Tasks

### Adding a New AI Model

1. Create a new model class in `models/` inheriting from `BaseAIModel`
2. Implement required methods: `_validate_config`, `get_token`, `prepare_headers`, `prepare_request_data`, `ask`
3. Register the model in `models/__init__.py` with `AIModelFactory.register_model()`
4. Add default configuration in `config.py`
5. Update UI components to display the new model

### Modifying AI Request/Response Handling

- Core logic is in each model's `ask()` method
- Streaming responses are handled in `ask()` with callback mechanisms
- Error handling and retry logic is implemented per model
- Response parsing is model-specific due to different API formats

### UI Customization

- Main dialog is in `AskDialog` class in `ui.py`
- Configuration UI is in `ConfigDialog` class in `config.py`
- Internationalization strings are in `i18n/` directory
- Response formatting uses Markdown with custom styling

### Configuration Management

- Uses Calibre's `JSONConfig` for persistent storage
- Model configurations are stored separately for each provider
- Template system allows customizable prompts
- Language settings affect both UI and AI prompts

## Build and Development Commands

```bash
# The plugin is developed and distributed as a Calibre plugin
# No separate build process is required - zip the directory contents

# For testing, install the plugin in Calibre:
# 1. In Calibre, go to Preferences -> Plugins -> Load plugin from file
# 2. Select the plugin ZIP file
# 3. Restart Calibre
```

## Testing

The plugin is tested through manual integration testing within Calibre:

1. Install plugin in Calibre
2. Configure API keys for desired AI providers
3. Test functionality with various books
4. Verify error handling and edge cases

## Dependencies

External dependencies are bundled in the `lib/` directory:
- requests - HTTP library for API calls
- bleach - HTML sanitization
- markdown2 - Markdown to HTML conversion
- charset_normalizer, certifi, idna, urllib3 - requests dependencies

Calibre built-in dependencies:
- PyQt5 - GUI framework
- Standard Python library modules

## Internationalization

The plugin supports multiple languages through the `i18n/` directory. Each language has its own Python file that provides translations for UI strings and model-specific prompts. New languages can be added by creating a new translation file and registering it in the translation registry.