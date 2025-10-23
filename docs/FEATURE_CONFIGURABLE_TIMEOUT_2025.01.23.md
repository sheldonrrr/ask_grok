# Configurable Request Timeout Feature

**Date:** 2025-01-23  
**Feature:** User-configurable request timeout setting

## Overview

Implemented a global configurable timeout setting to address user feedback about GPU performance limitations. Previously, the plugin used hardcoded timeout values (30s for online models, 60s for local models). Now users can configure a single global timeout value that applies to all AI models.

## Changes Made

### 1. Configuration (`config.py`)

**Default Configuration:**
- Added `prefs.defaults['request_timeout'] = 60` (default 60 seconds)
- Added validation in `get_prefs()` to ensure `request_timeout` key exists

**UI Implementation:**
- Added timeout input field in the AI models section
- Positioned below the Reset button with a dashed separator line
- Input field accepts only numeric values (1-3600 seconds)
- Layout: Label + Input (max width 100px) + "seconds" unit label

**Configuration Management:**
- Updated `save_settings()` to save timeout value
- Updated `load_initial_values()` to include timeout in initial values
- Updated `check_for_changes()` to detect timeout changes

### 2. API Client (`api.py`)

**Initialization:**
- Modified `__init__()` to accept optional `timeout` parameter
- If `timeout` is `None`, automatically loads from config: `prefs.get('request_timeout', 60)`
- Passes timeout to session creation and stores in `self._timeout`

**Backward Compatibility:**
- Existing code that passes explicit timeout values continues to work
- New code without timeout parameter automatically uses configured value

### 3. Random Question Dialog (`random_question.py`)

**Timeout Timer:**
- Removed hardcoded logic for reasoning vs. normal models (90s vs. 30s)
- Now loads timeout from config: `prefs.get('request_timeout', 60)`
- Simplified timeout calculation: `timeout_ms = timeout_sec * 1000`

### 4. Internationalization (`i18n/en.py`)

**New Translations:**
```python
'request_timeout_label': 'Request Timeout:',
'seconds': 'seconds',
```

## UI Layout

```
┌─────────────────────────────────────┐
│ AI Models Section                   │
├─────────────────────────────────────┤
│ Current AI: [Dropdown]              │
│                                     │
│ [Model Configuration Widget]        │
│   - API Key                         │
│   - Base URL                        │
│   - Model Selection                 │
│   - Enable Streaming                │
│   [Reset Button]                    │
│                                     │
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │ ← Dashed separator
│                                     │
│ Request Timeout: [60] seconds       │ ← New setting
└─────────────────────────────────────┘
```

## Technical Details

### Timeout Value Range
- Minimum: 1 second
- Maximum: 3600 seconds (1 hour)
- Default: 60 seconds
- Validation: `QIntValidator(1, 3600)`

### Global Application
The timeout setting is global and applies to:
- All AI model API requests (streaming and non-streaming)
- Random question generation
- Model list fetching (uses fixed 15s timeout)

### Model-Specific Timeout Usage

All model implementations use `kwargs.get('timeout', default)` pattern:
- **Streaming requests:** `timeout=kwargs.get('timeout', 300)` (5 min fallback)
- **Non-streaming requests:** `timeout=kwargs.get('timeout', 60)` (1 min fallback)

The APIClient passes `self._timeout` to model methods via kwargs, which now comes from the user configuration.

## Benefits

1. **User Control:** Users with slow GPUs can increase timeout as needed
2. **Unified Configuration:** Single setting instead of multiple hardcoded values
3. **Backward Compatible:** Existing installations get default 60s timeout
4. **Flexible:** Supports both fast cloud APIs and slow local models

## Testing Recommendations

1. Test with default 60s timeout
2. Test with very low timeout (5s) to verify timeout behavior
3. Test with high timeout (300s) for slow local models
4. Verify timeout persists after plugin restart
5. Test with different AI providers (online and local)

## Future Enhancements

Potential improvements for future versions:
- Per-model timeout settings
- Separate timeouts for streaming vs. non-streaming
- Auto-detect optimal timeout based on response times
- Timeout presets (Fast/Normal/Slow)
