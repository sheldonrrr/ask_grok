# Fish Shell Configuration for Ask Grok Development

## Overview

This document contains useful Fish shell aliases and functions for developing the Ask Grok Calibre plugin. These configurations can be shared across different machines.

---

## Configuration File Location

Fish configuration file: `~/.config/fish/config.fish`

---

## Quick Edit Commands

### Edit Fish Configuration
```fish
alias vimfish "vim ~/.config/fish/config.fish"
```

**Usage:** `vimfish`

**Description:** Quickly open Fish configuration file in vim for editing.

---

### Reload Fish Configuration
```fish
alias soufish "source ~/.config/fish/config.fish"
```

**Usage:** `soufish`

**Description:** Reload Fish configuration after making changes (short for "source fish").

---

## Calibre Plugin Development

### Quick Build and Install Plugin

```fish
function cali-dag
    echo "Building calibre plugin Ask Grok..."
    calibre-debug -s
    sleep 1 # waiting for close
    calibre-customize -b "$HOME/ask_grok"
    if test $status -eq 0
        echo "Build successfully, now open calibre..."
        calibre-debug -g
    else
        echo "Build failed, plz check details."
    end
end
```

**Usage:** `cali-dag`

**Description:** 
- Stops running Calibre instance
- Builds and installs the plugin from source
- Launches Calibre in debug mode if build succeeds

**Commands Breakdown:**
1. `calibre-debug -s` - Stop running Calibre
2. `calibre-customize -b "$HOME/ask_grok"` - Build plugin from source directory
3. `calibre-debug -g` - Launch Calibre in debug mode (GUI)

---

## Installation Instructions

### 1. Open Fish Configuration File

```bash
vim ~/.config/fish/config.fish
```

Or if you already have the alias:
```bash
vimfish
```

---

### 2. Add Configuration

Copy and paste the following into your `config.fish`:

```fish
# Fish 配置快捷命令
alias vimfish "vim ~/.config/fish/config.fish"
alias soufish "source ~/.config/fish/config.fish"

#>>>Speed build in calibre>>>
function cali-dag
    echo "Building calibre plugin Ask Grok..."
    calibre-debug -s
    sleep 1 # waiting for close
    calibre-customize -b "$HOME/ask_grok"
    if test $status -eq 0
        echo "Build successfully, now open calibre..."
        calibre-debug -g
    else
        echo "Build failed, plz check details."
    end
end
#<<<
```

---

### 3. Adjust Plugin Path (if needed)

**Default path:** `$HOME/ask_grok` (expands to `/home/username/ask_grok`)

**If your plugin is in a different location:**

Replace `"$HOME/ask_grok"` with your actual path:

```fish
# Example: Plugin in a different directory
calibre-customize -b "$HOME/projects/ask_grok"

# Example: Plugin in a custom location
calibre-customize -b "/path/to/your/ask_grok"
```

---

### 4. Reload Configuration

```bash
source ~/.config/fish/config.fish
```

Or use the alias after first reload:
```bash
soufish
```

---

## Path Variables Reference

### Using Environment Variables

Fish shell supports these path variables for privacy and portability:

| Variable | Description | Example |
|----------|-------------|---------|
| `$HOME` | User home directory | `/home/username` |
| `~` | Shorthand for home | `/home/username` |
| `$USER` | Current username | `username` |
| `$PWD` | Current directory | `/current/path` |

### Recommended Path Patterns

```fish
# ✅ Good - Uses $HOME variable (portable)
calibre-customize -b "$HOME/ask_grok"

# ✅ Good - Uses tilde expansion (portable)
calibre-customize -b ~/ask_grok

# ❌ Avoid - Hardcoded username (not portable)
calibre-customize -b /home/she/ask_grok

# ✅ Good - Relative to home with subdirectories
calibre-customize -b "$HOME/projects/calibre-plugins/ask_grok"
```

---

## Advanced Configuration (Optional)

### Auto-reload After Editing

This version automatically reloads configuration after editing:

```fish
function vimfish
    vim ~/.config/fish/config.fish
    and source ~/.config/fish/config.fish
    and echo "✅ Fish configuration reloaded"
end
```

---

### Enhanced Build Function with Logging

```fish
function cali-dag
    set plugin_path "$HOME/ask_grok"
    set log_file "$HOME/calibre_build.log"
    
    echo "🔄 Building calibre plugin Ask Grok..."
    echo "📁 Plugin path: $plugin_path"
    
    # Stop Calibre
    calibre-debug -s
    sleep 1
    
    # Build and install
    calibre-customize -b "$plugin_path" 2>&1 | tee "$log_file"
    
    if test $status -eq 0
        echo "✅ Build successful! Opening Calibre..."
        calibre-debug -g
    else
        echo "❌ Build failed! Check log: $log_file"
        return 1
    end
end
```

**Features:**
- Logs build output to file
- Uses variables for paths
- Better error messages
- Emoji indicators

---

### Quick Plugin Rebuild (Without Restarting Calibre)

```fish
function cali-rebuild
    echo "🔄 Rebuilding plugin only..."
    calibre-customize -b "$HOME/ask_grok"
    if test $status -eq 0
        echo "✅ Plugin rebuilt. Restart Calibre to see changes."
    else
        echo "❌ Build failed."
    end
end
```

**Usage:** `cali-rebuild`

**Description:** Rebuilds plugin without stopping/starting Calibre (useful for quick iterations).

---

## Workflow Examples

### Typical Development Workflow

```bash
# 1. Edit plugin code
vim ~/ask_grok/ui.py

# 2. Rebuild and test
cali-dag

# 3. Edit fish config if needed
vimfish

# 4. Reload fish config
soufish
```

---

### Quick Iteration Workflow

```bash
# Edit code
vim ~/ask_grok/config.py

# Quick rebuild (Calibre stays open)
cali-rebuild

# Manually restart Calibre to see changes
```

---

## Troubleshooting

### Command Not Found

**Problem:** `cali-dag: command not found`

**Solution:**
```bash
# Reload configuration
source ~/.config/fish/config.fish

# Or restart terminal
```

---

### Build Fails

**Problem:** `calibre-customize` fails

**Solution:**
1. Check plugin path is correct: `ls $HOME/ask_grok`
2. Check Calibre is installed: `which calibre-customize`
3. Check for syntax errors in plugin code
4. View detailed error in build log

---

### Calibre Won't Close

**Problem:** `calibre-debug -s` doesn't close Calibre

**Solution:**
```bash
# Force kill Calibre
killall calibre

# Then rebuild
cali-dag
```

---

## Platform-Specific Notes

### Linux
- Default config: `~/.config/fish/config.fish`
- Home directory: `/home/username`

### macOS
- Default config: `~/.config/fish/config.fish`
- Home directory: `/Users/username`

### Windows (WSL)
- Default config: `~/.config/fish/config.fish`
- Home directory: `/home/username`
- May need to adjust Calibre paths

---

## Additional Useful Aliases

### Navigate to Plugin Directory

```fish
alias cdgrok "cd $HOME/ask_grok"
```

**Usage:** `cdgrok`

---

### View Plugin Logs

```fish
alias groklog "tail -f ~/.config/calibre/plugins/ask_grok_logs/ask_grok_debug.log"
```

**Usage:** `groklog`

**Description:** Follow plugin debug log in real-time.

---

### Clean Plugin Build

```fish
function cali-clean
    echo "🧹 Cleaning plugin build artifacts..."
    rm -rf "$HOME/ask_grok/__pycache__"
    rm -rf "$HOME/ask_grok"/**/__pycache__
    rm -f "$HOME/ask_grok"/**/*.pyc
    echo "✅ Cleanup complete"
end
```

**Usage:** `cali-clean`

**Description:** Remove Python cache files before rebuilding.

---

## Complete Configuration Template

Here's a complete template you can copy to a new machine:

```fish
# ============================================
# Ask Grok Calibre Plugin Development Config
# ============================================

# --- Quick Edit Commands ---
alias vimfish "vim ~/.config/fish/config.fish"
alias soufish "source ~/.config/fish/config.fish"

# --- Plugin Development ---
alias cdgrok "cd $HOME/ask_grok"
alias groklog "tail -f ~/.config/calibre/plugins/ask_grok_logs/ask_grok_debug.log"

# Build and install plugin
function cali-dag
    echo "🔄 Building calibre plugin Ask Grok..."
    calibre-debug -s
    sleep 1 # waiting for close
    calibre-customize -b "$HOME/ask_grok"
    if test $status -eq 0
        echo "✅ Build successfully, now open calibre..."
        calibre-debug -g
    else
        echo "❌ Build failed, plz check details."
    end
end

# Rebuild without restarting Calibre
function cali-rebuild
    echo "🔄 Rebuilding plugin only..."
    calibre-customize -b "$HOME/ask_grok"
    if test $status -eq 0
        echo "✅ Plugin rebuilt. Restart Calibre to see changes."
    else
        echo "❌ Build failed."
    end
end

# Clean build artifacts
function cali-clean
    echo "🧹 Cleaning plugin build artifacts..."
    rm -rf "$HOME/ask_grok/__pycache__"
    rm -rf "$HOME/ask_grok"/**/__pycache__
    rm -f "$HOME/ask_grok"/**/*.pyc
    echo "✅ Cleanup complete"
end
```

---

## Notes

- **Privacy:** All paths use `$HOME` variable instead of hardcoded usernames
- **Portability:** Configuration works across different machines and users
- **Customization:** Adjust plugin path in the functions if your directory structure differs
- **Backup:** Keep this file in version control for easy setup on new machines

---

## See Also

- [CRITICAL_RULES.md](./CRITICAL_RULES.md) - Plugin development red lines
- [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) - Project architecture overview
- [Fish Shell Documentation](https://fishshell.com/docs/current/)
- [Calibre Plugin Development Guide](https://manual.calibre-ebook.com/creating_plugins.html)

---

**Last Updated:** 2025-10-21
