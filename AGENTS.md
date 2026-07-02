# AGENTS.md

## Cursor Cloud specific instructions

### What this repo is
This is **"Ask AI Plugin"**, a GUI plugin for the [calibre](https://calibre-ebook.com/)
e-book manager. It is a single Python package (not a monorepo) whose runtime is
calibre's bundled Python + PyQt. Third-party deps are **vendored** in
`lib/ask_ai_plugin_vendor/`, so `requirements.txt` is dev-reference only and is
not required at runtime.

### Environment (already provisioned; not part of the update script)
- **calibre** is installed as a system app (`/opt/calibre`, provides
  `calibre`, `calibre-customize`, `calibre-debug`, `calibredb`). It is a system
  dependency and persists in the VM snapshot, so it is intentionally NOT in the
  update script.
- GUI system libs (`libegl1`, `libopengl0`, `libxcb-*`, etc.) are installed so
  calibre's Qt GUI can start; a virtual display is available on `DISPLAY=:1`, and
  `xvfb-run` works for headless runs.

### Command-line dev tool: `./dev.sh`
`dev.sh` wraps the calibre CLI so the whole loop runs from the terminal:
- `./dev.sh build` – rebuild + reinstall the plugin (`calibre-customize -b .`).
- `./dev.sh run` – launch the calibre GUI (uses `DISPLAY`, else `xvfb-run`).
- `./dev.sh run-headless` – launch the GUI under `xvfb-run` (no display needed).
- `./dev.sh smoke` – isolated headless build+load check; exits non-zero if the
  plugin fails to load. Good CI-style sanity check.
- `./dev.sh compile` – fast `py_compile` syntax check of plugin sources.
- `./dev.sh library` – create the dev library (`~/calibre-library`) + a sample book.
- `./dev.sh logs` – show the plugin's log directory.

### Non-obvious gotchas
- **First-run migration bug on `main`:** `config.get_prefs()` references an
  unbound local `logger` in the fresh-config migration branch (fixed on `dev`).
  On a brand-new calibre config the very first plugin load raises
  `UnboundLocalError` and calibre exits. It **self-heals**: the crashing launch
  writes `use_interface_language` to `plugins/ask_ai_plugin.json` before it
  fails, so the *second* launch loads fine. Alternatively, seed
  `<calibre-config>/plugins/ask_ai_plugin.json` with
  `{"use_interface_language": false}`. `./dev.sh smoke` seeds this automatically.
- **`DeviceScanner requires the /sys filesystem` traceback** at startup is a
  harmless background device-detection thread error in the container; it does
  **not** affect the plugin.
- **`calibredb`/`calibre` on the same library:** running a `calibredb` command
  while the calibre GUI is open prints a "another calibre program is running"
  warning because the GUI holds the library lock. Close the GUI or use a
  separate `--with-library` path.
- The `calibre_plugins.*` namespace only exists inside a running calibre; you
  cannot `import calibre_plugins.ask_ai_plugin` from a plain `calibre-debug -c`
  one-liner.
- Fully exercising an AI answer needs a configured provider API key
  (OpenAI/Anthropic/Gemini/etc.); the default "Nvidia Free" provider routes
  through an external proxy and requires network access.
