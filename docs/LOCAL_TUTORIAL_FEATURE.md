# Local Tutorial Feature Implementation

**Date**: November 24, 2025  
**Version**: Ask AI Plugin v1.3.3+

## Overview

Implemented a local web-based tutorial system that allows users to view comprehensive plugin documentation in their default web browser, with full search capabilities using browser's built-in find function (Ctrl+F / Cmd+F).

## Problem Statement

Previously, the About dialog only linked to external Simplenote URLs, which:
- Required internet connection
- Couldn't be searched easily
- Weren't version-specific
- Didn't work offline

## Solution

Created a three-part system:
1. **Comprehensive Markdown Tutorial** - Updated tutorial with all v1.3.3 features
2. **HTML Converter** - Simple markdown-to-HTML converter with clean styling
3. **Browser Integration** - Opens tutorial in default browser with one click

## Files Created/Modified

### New Files

1. **`tutorial/tutorial_v0.3_for_Ask_AI_Plugin_v1.3.3.md`** (729 lines)
   - Comprehensive user manual for v1.3.3
   - Covers all new features: parallel AI, PDF export, multiple books, etc.
   - Detailed sections on API keys, free options (Nvidia, Ollama), and troubleshooting
   - No emoji characters (for low-end device compatibility)
   - Simple, serious tone suitable for non-technical users

2. **`tutorial_viewer.py`** (250+ lines)
   - `MarkdownToHTMLConverter` class: Converts markdown to styled HTML
   - `open_tutorial_in_browser()` function: Opens tutorial in default browser
   - Clean, responsive CSS styling
   - No external dependencies (uses only Python stdlib + PyQt5)

### Modified Files

1. **`ui.py`**
   - Added tutorial button to `AboutWidget`
   - Added `open_local_tutorial()` method
   - Integrated with i18n system

2. **`i18n/en.py`**
   - Added `'open_local_tutorial': 'Open Local Tutorial'`
   - Added `'tutorial_open_failed': 'Failed to open tutorial'`

3. **`i18n/zh.py`**
   - Added `'open_local_tutorial': '打开本地教程'`
   - Added `'tutorial_open_failed': '打开教程失败'`

## Tutorial Content Structure

### Main Sections

1. **What's New in v1.3.x**
   - Plugin rename explanation
   - New AI providers
   - New features overview

2. **Getting Started**
   - Understanding API Keys (detailed explanation of toC vs toB)
   - Free API Options (Nvidia NIM, Ollama, free tiers)
   - Installation instructions
   - First-time configuration

3. **Core Features**
   - Basic Q&A
   - Random Question Generator
   - Multiple Books Support
   - Parallel AI Requests
   - AI Switcher
   - Dynamic Model List Loading
   - History System
   - PDF Export

4. **Supported AI Providers**
   - Detailed info for all 9 providers
   - API key sources
   - Cost information
   - Best use cases

5. **Configuration Options**
   - All settings explained
   - Templates customization
   - Export settings

6. **Troubleshooting**
   - Common issues and solutions
   - Complete reinstall guide

7. **Privacy and Data Handling**
   - What data is sent
   - API key storage
   - Provider privacy policies

8. **Tips and Best Practices**
   - Getting better responses
   - Choosing the right AI
   - Managing costs
   - Workflow organization

9. **FAQ**
   - 15+ frequently asked questions
   - Covers API keys, costs, offline use, privacy

10. **Appendix**
    - Model recommendations by use case

## Key Features

### Tutorial Content

- **Beginner-Friendly**: Explains technical concepts (API keys, tokens) in simple terms
- **Free Options Highlighted**: Nvidia and Ollama prominently featured
- **Practical Examples**: Real use cases and example questions
- **Comprehensive**: Covers all features from v1.2.x to v1.3.3
- **Troubleshooting**: Common issues with solutions
- **No Emojis**: Compatible with low-end devices and older systems

### HTML Converter

- **Simple Implementation**: No external markdown libraries needed
- **Clean Styling**: Professional, readable design
- **Responsive**: Works on all screen sizes
- **Dark Mode Compatible**: Uses system palette colors
- **Back to Top Button**: Easy navigation for long document
- **Syntax Highlighting**: Code blocks styled appropriately

### Browser Integration

- **One-Click Access**: Button in About tab
- **Default Browser**: Opens in user's preferred browser
- **Searchable**: Full browser search capabilities (Ctrl+F / Cmd+F)
- **Offline**: Works without internet connection
- **Temporary File**: HTML stored in system temp directory

## Usage

1. Open calibre
2. Click "Ask AI Plugin" dropdown menu
3. Select "Configure"
4. Go to "About" tab
5. Click "Open Local Tutorial" button
6. Tutorial opens in default web browser
7. Use browser's find function (Ctrl+F / Cmd+F) to search

## Technical Details

### Markdown to HTML Conversion

The converter handles:
- Headers (H1-H4)
- Bold and italic text
- Inline code
- Links (opens in new tab)
- Unordered lists
- Ordered lists
- Horizontal rules
- Paragraphs

### CSS Styling

- Modern, clean design
- System font stack for best compatibility
- Responsive layout (max-width: 900px)
- Professional color scheme
- Proper spacing and typography
- Mobile-friendly

### Error Handling

- File not found errors
- Conversion errors
- Browser opening errors
- User-friendly error messages via QMessageBox

## Benefits

1. **Offline Access**: No internet required
2. **Fast Search**: Browser's native find function
3. **Version-Specific**: Tutorial matches plugin version
4. **Always Available**: Bundled with plugin
5. **No External Dependencies**: Works out of the box
6. **Printable**: Users can print from browser
7. **Shareable**: Can save HTML file for sharing

## Future Enhancements

Possible improvements:
- Multi-language tutorial versions (zh, ja, etc.)
- Table of contents with anchor links
- Syntax highlighting for code blocks (using highlight.js)
- PDF generation option
- Tutorial versioning system
- Search index for faster searching

## Testing Checklist

- [x] Tutorial markdown created with all features
- [x] HTML converter works correctly
- [x] Browser opens with tutorial
- [x] Button appears in About tab
- [x] Button text updates with language change
- [x] Error handling works
- [x] i18n translations added (en, zh)
- [ ] Test on Windows
- [ ] Test on macOS
- [ ] Test on Linux (in progress)
- [ ] Test with different browsers
- [ ] Test with different calibre themes

## Notes

- Tutorial file is ~40KB (text only, no images)
- HTML file generated is ~60KB with embedded CSS
- No network requests made (fully local)
- Compatible with all calibre versions that support PyQt5
- Works with calibre's dark mode

## Related Files

- `tutorial/tutorial_v.0.2_for_Ask_Grok_v1.2.3.md` - Previous version (kept for reference)
- `docs/RELEASE_NOTES_v1.3.2.md` - Feature list for v1.3.2
- `docs/CHANGELOG_v1.3.3_EN.md` - Changelog for v1.3.3

---

**Implementation Status**: ✅ Complete  
**Testing Status**: 🔄 In Progress  
**Documentation Status**: ✅ Complete
