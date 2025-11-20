# Ask AI Plugin - Version 1.3.3 Release Notes

**Release Date**: November 20, 2025

## Bug Fixes & Improvements

### PDF Export Enhancements
- **Improved PDF Filename Format**: PDF exports now use more user-friendly filenames with proper capitalization and readable timestamps
  - Old format: `ask_ai_qa_openai_panel1_20251120_094700.pdf`
  - New format: `OpenAI_QA_BookTitle_2025-11-20_09-47.pdf`
  - Removed meaningless panel numbers
  - Added book title to filename (up to 30 characters)
  - Improved timestamp format for better readability

- **Real-time Export Folder Configuration**: Fixed issue where PDF exports would use outdated folder settings
  - Export operations now always read the latest configuration
  - Changes to default export folder are immediately effective
  - Added debug logging for export configuration tracking

- **Export Success Feedback**: Added visual tooltips for successful PDF exports
  - Consistent feedback across all export types (single Q&A, multi-AI, history)
  - Similar to the copy success notification

- **Enhanced PDF Layout**: Improved PDF export formatting with cleaner separators
  - Changed separator from wide lines to elegant 4-character zen-style lines (────)
  - Better visual hierarchy and readability

### Configuration Dialog Improvements
- **Default Export Folder Settings**: Added support for configuring a default PDF export folder
  - New checkbox to enable/disable default export folder
  - Browse button to select target folder
  - Auto-save when folder is selected
  - Settings persist across sessions

- **Language Switching Fix**: Fixed issue where export configuration labels didn't update when switching languages
  - All export-related UI elements now properly translate
  - Checkbox, folder label, and browse button text update immediately

### UI/UX Enhancements
- **Copy Button Improvements**: Enhanced copy functionality in the Ask dialog
  - Unified content formatting across copy and export operations
  - Consistent metadata inclusion

- **Parallel AI Display Fix**: Fixed issue where parallel AI responses weren't displayed side-by-side
  - Multiple AI responses now properly show in parallel panels
  - Improved layout for multi-AI comparisons

### Technical Improvements
- **Configuration Persistence**: Improved configuration loading and saving
  - Export settings now correctly load when reopening config dialog
  - Fixed checkbox and folder path initialization
  - Added comprehensive debug logging

- **Code Quality**: Enhanced error handling and logging throughout export operations
  - Better tracking of export configuration states
  - Improved debugging capabilities

---

## For Users
This update focuses on improving the PDF export experience and fixing configuration-related issues. The new filename format makes it easier to identify exported files, and the default folder feature streamlines your workflow.

## For Developers
Key changes include:
- Added `_get_ai_display_name()` helper method for proper AI name capitalization
- Implemented `prefs.refresh()` calls before reading export configuration
- Enhanced `load_initial_values()` to properly initialize export UI elements
- Added language change handlers for export configuration UI

---

**Upgrade Notes**: This is a recommended update for all users. No breaking changes.
