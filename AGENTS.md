# AGENTS.md

## Cursor Cloud specific instructions

### What this repo is
This is **"Ask AI Plugin"**, a GUI plugin for the [calibre](https://calibre-ebook.com/)
e-book manager. It is a single Python package (not a monorepo) whose runtime is
calibre's bundled Python + PyQt. Third-party runtime deps are **vendored** in
`lib/ask_ai_plugin_vendor/`, so `requirements.txt` is dev-reference only and is
not required for the plugin to run inside calibre.

### Environment (already provisioned; not part of the update script)
- **calibre** is installed as a system app (`/opt/calibre`, provides
  `calibre`, `calibre-customize`, `calibre-debug`, `calibredb`). It is a system
  dependency and persists in the VM snapshot, so it is intentionally NOT in the
  update script.
- **fish** shell (used by the `caldbg` dev tool) and **xvfb** are installed. GUI
  system libs for Qt are installed and a virtual display is available on
  `DISPLAY=:1`.

### Command-line dev tool: `caldbg` (fish)
The project ships a fish-based dev loop. Source it or run the bash wrappers:
- `source scripts/caldbg.fish` then use the functions, or run `bin/caldbg*`
  directly from any shell (they `exec fish -c ...`):
  - `bin/caldbg`      – install plugin from source (`calibre-customize -b .`) + launch GUI
  - `bin/caldbg-ag`   – shut down a running calibre first, then install + launch (use this to reload after code changes)
  - `bin/caldbg-p`    – package `dist/*.zip` via `scripts/package.sh`, install the zip, launch
  - `bin/caldbg-pag`  – same as `caldbg-p` but shuts down a running calibre first
- The GUI (`calibre-debug --gui`) needs a display; in this env prefix with the
  existing `DISPLAY=:1`, or wrap in `xvfb-run -a` for headless.

### Automated tests
Plain `unittest`, no calibre runtime needed (they import `utils` / `prompt_limits`
directly from the repo root):
- `python3 -m unittest discover -s tests -v`
- `tests/test_i18n_parity.py` checks every `i18n/*.py` has the same keys as `en.py`.
- `tests/test_prompt_limits.py` covers prompt-length / compact-metadata logic and
  includes a `TestDeepSeekIntegration` group that is **skipped** unless
  `DEEPSEEK_API_KEY` is set (copy `.env.example` to `.env` to run live API tests).

### Non-obvious gotchas
- **First-run migration bug in `config.get_prefs()`:** the fresh-config migration
  branch references a `logger` that is only bound inside an `except` above it, so
  on a brand-new calibre config the first plugin load raises `UnboundLocalError`
  and calibre exits. It **self-heals**: the crashing launch writes
  `use_interface_language` to `plugins/ask_ai_plugin.json` before failing, so the
  *second* launch loads fine. To avoid the crash outright, seed
  `<calibre-config>/plugins/ask_ai_plugin.json` with `{"use_interface_language": false}`.
- **`DeviceScanner requires the /sys filesystem` traceback** at startup is a
  harmless background device-detection thread error in the container; it does not
  affect the plugin.
- **`calibredb`/`calibre` on the same library:** running a `calibredb` command
  while the calibre GUI is open prints an "another calibre program is running"
  warning because the GUI holds the library lock. Close the GUI or use a separate
  `--with-library` path.
- The `calibre_plugins.*` namespace only exists inside a running calibre; you
  cannot `import calibre_plugins.ask_ai_plugin` from a plain `calibre-debug -c`
  one-liner.
- Fully exercising an AI answer needs a configured provider API key
  (OpenAI/Anthropic/Gemini/DeepSeek/etc.); the default "Nvidia Free" provider
  routes through an external proxy and requires network access.
