# Ask Grok - Project Structure

## Overview

Ask Grok is a Calibre plugin that enables users to ask questions about books using various AI models (Grok, Google Gemini, DeepSeek, and custom models). This document provides a comprehensive overview of the project structure.

---

## Directory Tree

```
ask_grok/
├── .git/                           # Git version control
├── .github/                        # GitHub workflows and configurations
│   └── workflows/                  # CI/CD workflows
├── docs/                           # 📁 Documentation folder
│   ├── CRITICAL_RULES.md          # ⚠️ Red lines for AI code editing
│   └── PROJECT_STRUCTURE.md       # 📄 This file - project overview
│
├── i18n/                          # 🌍 Internationalization
│   ├── __init__.py                # i18n module initialization
│   ├── base.py                    # Base translation utilities
│   ├── en.py                      # English translations
│   ├── zh.py                      # Simplified Chinese
│   ├── zht.py                     # Traditional Chinese
│   ├── yue.py                     # Cantonese
│   ├── ja.py                      # Japanese
│   ├── de.py                      # German
│   ├── fr.py                      # French
│   ├── es.py                      # Spanish
│   ├── pt.py                      # Portuguese
│   ├── ru.py                      # Russian
│   ├── da.py                      # Danish
│   ├── fi.py                      # Finnish
│   ├── nl.py                      # Dutch
│   ├── no.py                      # Norwegian
│   └── sv.py                      # Swedish
│
├── images/                        # 🎨 Plugin icons and images
│   └── ask_grok.png               # Main plugin icon
│
├── lib/                           # 📚 Third-party dependencies
│   ├── requests/                  # HTTP library for API calls
│   ├── bleach/                    # HTML sanitization
│   ├── markdown2/                 # Markdown rendering
│   └── [other dependencies]       # Additional bundled libraries
│
├── models/                        # 🤖 AI Model implementations
│   ├── __init__.py                # Models module initialization
│   ├── base.py                    # Base AI model class and factory
│   ├── grok.py                    # Grok (x.AI) implementation
│   ├── gemini.py                  # Google Gemini implementation
│   ├── deepseek.py                # DeepSeek implementation
│   └── custom.py                  # Custom model implementation
│
├── __init__.py                    # 🔴 CRITICAL: Plugin entry point
├── api.py                         # API client for AI services
├── config.py                      # Configuration dialog and preferences
├── history_manager.py             # Query history management
├── random_question.py             # Random question generation
├── response_handler.py            # AI response processing and rendering
├── shortcuts_widget.py            # Keyboard shortcuts configuration
├── ui.py                          # Main UI dialog and interface
├── utils.py                       # Utility functions
├── version.py                     # Version information
│
├── plugin-import-name-ask_grok.txt  # 🔴 CRITICAL: Plugin import name
├── requirements.txt               # Python dependencies list
├── setup.py                       # Plugin setup script
├── .gitignore                     # Git ignore rules
├── LICENSE                        # GPL v3 license
├── README.md                      # User documentation
└── ask_grok_gif_preview.gif       # Preview animation
```

---

## Core Components

### 1. Plugin Entry Point (`__init__.py`)

**Purpose:** Calibre plugin registration and initialization

**Key Components:**
- `AskGrokPlugin` class - Main plugin class inheriting from `InterfaceActionBase`
- Version information and metadata
- Lib directory path setup for bundled dependencies
- Logging system configuration
- Icon loading utilities

**Critical Sections:**
- Lines 81-98: Plugin class definition (DO NOT MODIFY without care)
- Lines 14-21: Lib directory setup (required for dependencies)
- Lines 23-30: Version constants (keep synchronized)

**Dependencies:**
- `calibre.customize.InterfaceActionBase`
- `calibre.utils.config.config_dir`

---

### 2. User Interface (`ui.py`)

**Purpose:** Main plugin UI and user interactions

**Key Components:**
- `AskGrokPluginUI` class - Main interface action
- `AskGrokDialog` - Main dialog for asking questions
- Event handlers for user interactions
- Markdown rendering for AI responses
- History display and management
- Random question generation UI

**Features:**
- Single input-output dialog interface
- Markdown rendering with syntax highlighting
- Copy answer/question functionality
- Recent query history display
- Language selection
- Model selection dropdown
- Keyboard shortcuts (Ctrl+L to open, Ctrl+Enter to send)

**Dependencies:**
- PyQt5 (QtWidgets, QtCore, Qt)
- `calibre.gui2.actions.InterfaceAction`
- `config.py` for settings
- `api.py` for API calls
- `response_handler.py` for rendering
- `i18n` for translations

---

### 3. Configuration (`config.py`)

**Purpose:** Plugin settings and configuration dialog

**Key Components:**
- `ConfigDialog` - Configuration UI
- `prefs` - JSONConfig object for persistent storage
- Model configurations (Grok, Gemini, DeepSeek, Custom)
- API key management
- Prompt template customization
- Language preferences

**Configuration Storage:**
- Path: `~/.config/calibre/plugins/ask_grok.json`
- Format: JSON

**Stored Settings:**
- `selected_model` - Currently active AI model
- `models` - Dictionary of model configurations
  - `api_key` - API key for each model
  - `prompt_template` - Custom prompt template
  - `model_name` - Specific model version
  - `base_url` - API endpoint (for custom models)
- `language` - Selected UI language
- `max_history` - Maximum history entries to display

**Dependencies:**
- PyQt5 widgets
- `calibre.utils.config.JSONConfig`
- `models.base` for model factory
- `i18n` for translations

---

### 4. AI Models (`models/`)

**Purpose:** AI service integrations and model implementations

#### Base Model (`models/base.py`)
- `BaseAIModel` - Abstract base class for all AI models
- `AIProvider` - Enum of supported providers
- `ModelConfig` - Configuration dataclass
- `AIModelFactory` - Factory for creating model instances
- `DEFAULT_MODELS` - Default configurations for each provider

#### Grok Model (`models/grok.py`)
- `GrokModel` - x.AI Grok implementation
- Endpoint: `https://api.x.ai/v1/chat/completions`
- Default model: `grok-beta`
- Streaming support

#### Gemini Model (`models/gemini.py`)
- `GeminiModel` - Google Gemini implementation
- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`
- Default model: `gemini-1.5-flash-latest`
- Streaming support

#### DeepSeek Model (`models/deepseek.py`)
- `DeepseekModel` - DeepSeek implementation
- Endpoint: `https://api.deepseek.com/chat/completions`
- Default model: `deepseek-chat`
- Streaming support

#### Custom Model (`models/custom.py`)
- `CustomModel` - Generic OpenAI-compatible API implementation
- Configurable base URL and model name
- Supports any OpenAI-compatible API (e.g., Nvidia, local models)

**Common Interface:**
```python
class BaseAIModel:
    def send_message(self, prompt: str, callback: callable) -> None
    def stop_stream(self) -> None
    def get_model_name(self) -> str
    def get_provider_name(self) -> str
```

---

### 5. API Client (`api.py`)

**Purpose:** HTTP communication with AI services

**Key Components:**
- `APIClient` - Main API client class
- Request handling with retry logic
- Streaming response processing
- Error handling and logging
- API key validation

**Features:**
- Automatic retry on failure
- Streaming support for real-time responses
- Request/response logging (with API key masking)
- Timeout handling
- Error message translation

**Dependencies:**
- `requests` library
- `models.base` for model factory
- `utils` for API key masking

---

### 6. Response Handler (`response_handler.py`)

**Purpose:** Process and render AI responses

**Key Components:**
- Markdown to HTML conversion
- HTML sanitization for security
- Syntax highlighting for code blocks
- Link handling
- Text formatting

**Features:**
- Safe HTML rendering with `bleach`
- Markdown rendering with `markdown2`
- Code syntax highlighting
- Clickable links
- Preserves formatting from AI responses

**Dependencies:**
- `markdown2` - Markdown parsing
- `bleach` - HTML sanitization
- PyQt5 for rendering

---

### 7. Internationalization (`i18n/`)

**Purpose:** Multi-language support

**Structure:**
- Each language file contains:
  - UI translations
  - Default prompt templates
  - Random question templates
  - Error messages

**Supported Languages:** 16 languages (see directory tree above)

**Key Functions:**
- `get_translation(lang_code)` - Get UI translations
- `get_default_template(lang_code)` - Get default prompt template
- `get_suggestion_template(lang_code)` - Get random question template
- `get_all_languages()` - List all supported languages

**Translation Structure:**
```python
TRANSLATIONS = {
    'ask_question': 'Translated text',
    'send': 'Translated text',
    # ... more translations
}

DEFAULT_TEMPLATE = """
Default prompt template in target language
"""

SUGGESTION_TEMPLATE = """
Random question generation prompt in target language
"""
```

---

### 8. History Manager (`history_manager.py`)

**Purpose:** Manage query history per book

**Key Components:**
- `HistoryManager` - History storage and retrieval
- Per-book history tracking
- Automatic cleanup of old entries
- JSON-based persistence

**Storage:**
- Path: `~/.config/calibre/plugins/ask_grok_latest_history.json`
- Format: JSON with book ID as key

**Features:**
- Stores last N queries per book (configurable)
- Includes timestamp, question, and answer
- Automatic pruning of old entries
- Thread-safe operations

---

### 9. Utilities (`utils.py`)

**Purpose:** Common utility functions

**Key Functions:**
- `mask_api_key(api_key)` - Mask API keys in logs
- `mask_api_key_in_text(text)` - Mask API keys in text
- `safe_log_config(config)` - Safely log configuration with masked keys

**Purpose:** Prevent API key leakage in logs and error messages

---

### 10. Version Management (`version.py`)

**Purpose:** Centralized version information

**Key Components:**
- `VERSION` - Version tuple
- `VERSION_DISPLAY` - Human-readable version string
- Build and release metadata

---

## Data Flow

### 1. Plugin Loading
```
Calibre starts
    ↓
Reads plugin-import-name-ask_grok.txt
    ↓
Imports calibre_plugins.ask_grok
    ↓
Loads AskGrokPlugin class from __init__.py
    ↓
Calls load_actual_plugin()
    ↓
Imports and instantiates AskGrokPluginUI from ui.py
    ↓
Plugin ready
```

### 2. User Query Flow
```
User selects book and clicks "Ask Grok"
    ↓
AskGrokDialog opens
    ↓
Loads book metadata (title, author, comments, etc.)
    ↓
Displays recent history for this book
    ↓
User enters question
    ↓
Builds prompt using template + metadata + question
    ↓
APIClient sends request to selected AI model
    ↓
Streams response back to UI
    ↓
ResponseHandler renders markdown to HTML
    ↓
Displays formatted answer
    ↓
Saves to history
```

### 3. Configuration Flow
```
User clicks "Configure"
    ↓
ConfigDialog opens
    ↓
Loads current settings from prefs
    ↓
User modifies settings (API key, model, template, etc.)
    ↓
User clicks "Save"
    ↓
Validates settings
    ↓
Saves to JSONConfig (~/.config/calibre/plugins/ask_grok.json)
    ↓
Updates active model instance
```

---

## Key Design Patterns

### 1. Factory Pattern
- `AIModelFactory` creates appropriate model instances based on provider
- Allows easy addition of new AI providers

### 2. Strategy Pattern
- Each AI model implements `BaseAIModel` interface
- UI code doesn't need to know which model is being used

### 3. Observer Pattern
- Streaming responses use callbacks to update UI in real-time
- Decouples API client from UI rendering

### 4. Singleton Pattern
- `prefs` configuration object is shared across modules
- Ensures consistent settings access

---

## Extension Points

### Adding a New AI Model

1. Create new file in `models/` (e.g., `models/newmodel.py`)
2. Implement `BaseAIModel` interface
3. Add provider to `AIProvider` enum in `models/base.py`
4. Add default config to `DEFAULT_MODELS` in `models/base.py`
5. Register in `AIModelFactory`
6. Add UI elements in `config.py` for API key and settings
7. Add translations in `i18n/` files

### Adding a New Language

1. Create new file in `i18n/` (e.g., `i18n/xx.py`)
2. Copy structure from `i18n/en.py`
3. Translate all strings in `TRANSLATIONS` dict
4. Translate `DEFAULT_TEMPLATE` and `SUGGESTION_TEMPLATE`
5. Add language to `get_all_languages()` in `i18n/__init__.py`
6. Test with language selection in config dialog

### Adding a New Feature

1. Update UI in `ui.py` if needed
2. Add configuration options in `config.py` if needed
3. Add translations in all `i18n/*.py` files
4. Update `README.md` with feature documentation
5. Test on all platforms (Windows, macOS, Linux)
6. Update version number in `__init__.py` and `version.py`

---

## Dependencies

### Bundled in `lib/`
- **requests** - HTTP library for API calls
- **bleach** - HTML sanitization
- **markdown2** - Markdown rendering

### Calibre Built-in
- **PyQt5** - GUI framework
- **calibre.customize** - Plugin API
- **calibre.gui2** - Calibre GUI utilities
- **calibre.utils.config** - Configuration management

### Python Standard Library
- **os, sys** - System operations
- **json** - JSON parsing
- **logging** - Logging system
- **datetime** - Timestamp handling
- **threading** - Thread management
- **importlib** - Dynamic imports

---

## File Size Considerations

### Large Files
- `lib/` - ~199 items (bundled dependencies)
- `config.py` - 67KB (large configuration dialog)
- `ui.py` - 58KB (complex UI implementation)
- `response_handler.py` - 28KB (rendering logic)
- `gemini.py` - 25KB (Gemini-specific handling)
- `random_question.py` - 21KB (question generation)

### Small Files
- `plugin-import-name-ask_grok.txt` - 9 bytes (critical!)
- `version.py` - 744 bytes
- `setup.py` - 673 bytes

---

## Testing Strategy

### Manual Testing Checklist
- [ ] Plugin loads without errors
- [ ] Configuration dialog opens and saves
- [ ] Each AI model works with valid API key
- [ ] Streaming responses display correctly
- [ ] History saves and loads per book
- [ ] Random questions generate in all languages
- [ ] Markdown rendering works (code blocks, links, formatting)
- [ ] Keyboard shortcuts work (Ctrl+L, Ctrl+Enter)
- [ ] Copy answer/question functions work
- [ ] Plugin works on Windows, macOS, Linux
- [ ] Plugin works with Calibre 7.0.0+

### Automated Testing
- Currently no automated tests
- Future: Add unit tests for models, API client, utils
- Future: Add integration tests for UI workflows

---

## Logging and Debugging

### Log Locations
- **Plugin log:** `~/.config/calibre/plugins/ask_grok_logs/ask_grok_debug.log`
- **Calibre debug log:** Preferences → Advanced → Miscellaneous → View Calibre Debug Log

### Log Levels
- **DEBUG:** Detailed information for debugging
- **INFO:** General information about plugin operation
- **WARNING:** Warning messages for potential issues
- **ERROR:** Error messages for failures

### What Gets Logged
- Plugin initialization
- Configuration changes (with masked API keys)
- API requests and responses (with masked keys)
- Errors and exceptions
- User actions (button clicks, dialog opens)

---

## Security Considerations

### API Key Protection
- API keys are masked in all logs using `mask_api_key()`
- Keys stored locally in `~/.config/calibre/plugins/ask_grok.json`
- Keys never transmitted except to configured AI provider
- User warned not to share API keys in bug reports

### HTML Sanitization
- All AI responses sanitized with `bleach` before rendering
- Prevents XSS attacks from malicious AI responses
- Only safe HTML tags and attributes allowed

### Network Security
- All API calls use HTTPS
- No data sent to third parties except configured AI provider
- Book metadata sent to AI provider (user should be aware)

---

## Performance Considerations

### Streaming Responses
- Responses streamed in real-time for better UX
- Reduces perceived latency
- Allows user to see progress

### History Management
- Limited to N most recent queries per book
- Automatic cleanup prevents unbounded growth
- JSON file remains small and fast to load

### Dependency Loading
- Dependencies loaded from `lib/` only when needed
- Lazy loading where possible
- Minimal impact on Calibre startup time

---

## Future Enhancements

### Potential Features
- [ ] Add more AI providers (Claude, OpenAI, etc.)
- [ ] Add conversation history (multi-turn chat)
- [ ] Add book content extraction for context
- [ ] Add batch processing (ask about multiple books)
- [ ] Add export functionality (save Q&A to file)
- [ ] Add search in history
- [ ] Add favorites/bookmarks for good answers
- [ ] Add prompt library (save and reuse prompts)
- [ ] Add automated testing
- [ ] Add telemetry (opt-in, privacy-respecting)

### Technical Improvements
- [ ] Refactor large files (config.py, ui.py) into smaller modules
- [ ] Add type hints throughout codebase
- [ ] Add docstrings to all functions and classes
- [ ] Add unit tests for core functionality
- [ ] Add integration tests for UI workflows
- [ ] Improve error handling and user feedback
- [ ] Add performance monitoring
- [ ] Optimize memory usage for large responses

---

## Contributing Guidelines

### Code Style
- Follow PEP 8 Python style guide
- Use 4 spaces for indentation
- Maximum line length: 100 characters (flexible)
- Use descriptive variable names
- Add comments for complex logic

### Commit Messages
- Use clear, descriptive commit messages
- Format: `[Component] Brief description`
- Example: `[UI] Add keyboard shortcut for random question`

### Pull Request Process
1. Fork the repository
2. Create a feature branch
3. Make changes and test thoroughly
4. Update documentation (README.md, this file)
5. Submit pull request with description
6. Wait for review and address feedback

### Testing Requirements
- Test on at least one platform (Windows/macOS/Linux)
- Test with at least one AI provider
- Verify plugin loads without errors
- Verify existing features still work

---

## Troubleshooting

### Plugin Won't Load
1. Check Calibre debug log for errors
2. Verify `plugin-import-name-ask_grok.txt` is intact
3. Verify `__init__.py` class definition is correct
4. Verify `lib/` directory exists and contains dependencies
5. Try reinstalling the plugin

### API Calls Fail
1. Check API key is correct
2. Check internet connection
3. Check AI provider status (may be down)
4. Check plugin log for detailed error messages
5. Try different AI provider

### UI Issues
1. Check PyQt5 is available in Calibre
2. Check for errors in Calibre debug log
3. Try resetting configuration (delete `ask_grok.json`)
4. Try reinstalling the plugin

### Configuration Won't Save
1. Check file permissions on config directory
2. Check disk space
3. Check for errors in plugin log
4. Try manually deleting `ask_grok.json` and reconfiguring

---

## Resources

### Documentation
- **Calibre Plugin Development:** https://manual.calibre-ebook.com/creating_plugins.html
- **PyQt5 Documentation:** https://www.riverbankcomputing.com/static/Docs/PyQt5/
- **Grok API:** https://docs.x.ai/
- **Gemini API:** https://ai.google.dev/docs
- **DeepSeek API:** https://platform.deepseek.com/docs

### Community
- **GitHub Repository:** https://github.com/sheldonrrr/ask_grok
- **Issue Tracker:** https://github.com/sheldonrrr/ask_grok/issues
- **Calibre Forum:** https://www.mobileread.com/forums/forumdisplay.php?f=166

### Contact
- **Author:** Sheldon
- **Email:** sheldonrrr@gmail.com

---

## License

This plugin is licensed under GPL v3. See `LICENSE` file for details.

---

## Changelog

See GitHub releases for detailed changelog: https://github.com/sheldonrrr/ask_grok/releases

---

## Notes for AI Assistants

When working on this project:

1. **Always read `CRITICAL_RULES.md` first** - It contains red lines you must not cross
2. **Understand the data flow** - Know how components interact
3. **Test thoroughly** - Plugin crashes are hard to debug for users
4. **Maintain consistency** - Follow existing patterns and style
5. **Update documentation** - Keep this file and README.md current
6. **Consider all platforms** - Windows, macOS, and Linux behave differently
7. **Respect user privacy** - Never log API keys or sensitive data
8. **Be conservative with changes** - Small, focused changes are safer
9. **Ask questions** - If unsure, ask the user for clarification

---

**Last Updated:** 2025-01-21
**Version:** 1.2.3
