# Release Notes - Ask AI Plugin v1.3.2

**Release Date:** November 17, 2025

---
## TL;DR updates summary

Optimized: 
- Multi-AI Provider
- Dynamic Model List Loading
- AI Switcher in Response Panel
- PDF Export Features
- Multiple Books Support
- Parallel AI Requests
UI/UX Improvements:
- Responsive Font Sizing
- Compact Layout
- Loading States
- Button Styling

## 🎉 Major Updates

### 🤖 Multi-AI Provider Support

**New AI Providers:**
- **OpenAI** - GPT-4o, GPT-4o-mini support
- **Anthropic Claude** - Claude 3.5 Sonnet and other models
- **Nvidia AI** - Free tier with llama-3.3-70b-instruct (40 RPM limit)

**Total Supported Providers:** 10 AI providers
- OpenAI, Anthropic, Google Gemini, Grok, DeepSeek, Nvidia AI, OpenRouter, Ollama, Custom API

---

### 🔄 Dynamic Model List Loading

**Feature:** Load available models directly from AI provider APIs

**Benefits:**
- ✅ No manual model name input required
- ✅ Always up-to-date model list
- ✅ One-click model loading via "Load Model List" button
- ✅ Backward compatible with custom model names

**Supported Providers:**
- OpenAI, Anthropic, Gemini, Grok, DeepSeek, Nvidia, OpenRouter, Custom API

---

### 🔄 AI Switcher in Response Panel

**Feature:** Switch between different AI providers without reopening the dialog

**Key Improvements:**
- ✅ Real-time AI switching in the response panel
- ✅ Remembers last selected AI per panel
- ✅ Seamless integration with history system
- ✅ Each response tagged with AI provider info

---

### 📝 Plugin Rename: Ask Grok → Ask AI Plugin

**Reason:** Plugin now supports 10+ AI providers, not just Grok

**Changes:**
- ✅ Display name: "Ask AI Plugin"
- ✅ Icon updated: `ask_ai_plugin.png`
- ✅ All UI text updated across 15 languages
- ⚠️ Internal paths preserved for backward compatibility

**Note:** User settings and history are fully preserved

---

### 📄 PDF Export Features

**New Capabilities:**

1. **Export Current Q&A**
   - Export active question and answer to PDF
   - Includes book metadata and AI provider info

2. **Export All History**
   - Export complete conversation history for current book(s)
   - Organized by timestamp
   - Includes all AI responses

**PDF Features:**
- ✅ Professional formatting with metadata
- ✅ Markdown rendering (bold, italic, code blocks, lists)
- ✅ Automatic page breaks
- ✅ AI provider and timestamp information

---

### 📚 Multiple Books Support

**Feature:** Ask questions about multiple books simultaneously

**Usage:**
1. Select multiple books in calibre library
2. Click "Ask AI Plugin"
3. Ask questions about the book collection

**Benefits:**
- ✅ Compare themes across books
- ✅ Analyze series or collections
- ✅ Cross-reference multiple sources
- ✅ Separate template for multi-book queries

---

### 🔀 Parallel AI Requests

**Feature:** Query multiple AI providers simultaneously

**Configuration:**
- Support 1-4 AI panels in parallel
- Smart layout: 1 (single), 2 (horizontal), 3 (1+2), 4 (2x2 grid)
- Dynamic window width adjustment

**Key Features:**
- ✅ Exclusive AI selection per panel
- ✅ Independent response handlers
- ✅ Compare AI responses side-by-side
- ✅ Each panel has its own AI switcher

---

### 🌍 Internationalization Improvements

**Enhanced i18n System:**
- ✅ Centralized translation management
- ✅ Consistent error messages across all languages
- ✅ Dynamic language switching without restart
- ✅ Better fallback handling

**Supported Languages:** 15
- Danish, German, English, Spanish, Finnish, French, Japanese, Dutch, Norwegian, Portuguese, Russian, Swedish, Simplified Chinese, Traditional Chinese, Cantonese

---

### 📜 History System Enhancements

**Improvements:**

1. **Multi-AI History Support**
   - Each response tagged with AI provider
   - Display AI name and model in history info bar
   - Filter and switch between different AI responses

2. **History Menu Polish**
   - Cleaner UI with book titles
   - Timestamp display
   - Quick access to related conversations
   - Clear current book history option

3. **Export History to PDF**
   - Export all conversations for current book(s)
   - Organized chronologically
   - Includes all metadata

---

### 🎨 UI/UX Improvements

**Interface Polish:**

1. **Responsive Font Sizing**
   - All text respects calibre system font settings
   - Relative font sizes (em units) throughout
   - Consistent scaling across all UI elements

2. **Compact Layout**
   - Optimized spacing using 8px grid system
   - Better use of screen real estate
   - Cleaner visual hierarchy

3. **Loading States**
   - Improved loading animations
   - Better feedback during AI requests
   - Consistent "Requesting..." messages

4. **Button Styling**
   - Standardized button styles via `ui_constants.py`
   - Consistent padding and sizing
   - Better visual feedback

---

### 🐛 Bug Fixes

**Stream Error Handling:**
- ✅ Fixed streaming response errors
- ✅ Better error recovery
- ✅ Improved connection timeout handling

**History & Export:**
- ✅ Fixed history loading issues
- ✅ Corrected PDF export formatting
- ✅ Resolved multi-book history conflicts

**DeepSeek Reasoner:**
- ✅ Fixed compatibility with DeepSeek R1 model
- ✅ Proper handling of reasoning tokens

---

### 🔧 Technical Improvements

**Code Organization:**

1. **UI Constants System**
   - Centralized design system in `ui_constants.py`
   - Consistent spacing, colors, fonts
   - Reusable button styles and animations

2. **Logging Optimization**
   - Reduced redundant DEBUG logs by ~70%
   - Retained critical ERROR and WARNING logs
   - Better log readability

3. **Error Message Formatting**
   - Unified error format: user-friendly + technical details
   - Internationalized error messages
   - Consistent across all AI providers

---

## 📊 Statistics

**Files Modified:** 50+
**New Features:** 8 major features
**Bug Fixes:** 10+
**Languages:** 15 supported
**AI Providers:** 10 supported
**Documentation:** 5+ new docs

---

## 🚀 Upgrade Instructions

### Automatic Update (Recommended)
- Plugin will auto-update if enabled in calibre settings

### Manual Update
1. Download latest version from calibre Plugin Index
2. Or: `Preferences → Plugins → Get new plugins`
3. Search "Ask AI Plugin"
4. Click "Install" or "Update"
5. Restart calibre

**Note:** All settings and history are preserved

---

## 🔗 Resources

- **GitHub:** https://github.com/sheldonrrr/ask_grok
- **User Manual:** http://simp.ly/publish/FwMSSr
- **About Plugin:** http://simp.ly/publish/xYW5Tr
- **Issue Report:** sheldonrrr@gmail.com

---

## 📝 Next Steps

### Planned for Future Versions

1. **Performance Optimization**
   - Further reduce plugin size
   - Optimize dependency loading

2. **Enhanced Features**
   - Conversation threading
   - Advanced search in history
   - Custom AI provider templates

3. **Integration**
   - Better calibre metadata integration
   - Plugin API for other plugins

---

## 🙏 Acknowledgments

Special thanks to all users who provided feedback and feature requests. Your input drives the continuous improvement of Ask AI Plugin.

---

## Version Information

- **Version:** 1.3.2
- **Release Date:** November 17, 2025
- **Minimum calibre Version:** 7.25.0+
- **Supported Platforms:** Windows, macOS, Linux

---

**Ask AI Plugin - Enhance Your Reading with AI!** 📚✨
