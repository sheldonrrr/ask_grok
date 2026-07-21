# /pack — Build the local release zip

Run the project packaging script and confirm the artifact path.

## Steps

1. From the repo root, run:

```bash
bash scripts/package.sh
```

2. Confirm output exists:

```text
dist/Ask_AI_Plugin_vX.Y.Z.zip
```

(`X.Y.Z` comes from `version.py` / `VERSION_STRING`.)

3. Optionally list the zip briefly to verify runtime files are present and GitHub-only trees are absent:
   - Should include: plugin Python, `i18n/`, `images/`, `lib/ask_ai_plugin_vendor/`, `tutorial/tutorial_v1.0.md`
   - Must **not** include: `docs/`, `aiprovider/`, `scripts/`, `tests/`, `bin/`, `.git/`, `.cursor/`

4. Reply with the full path to the zip and the version string.

## Packaging expectations

`scripts/package.sh` must keep excluding OS junk from Linux/macOS (and Windows), including at least:

- `.DS_Store`, `._*`, `__MACOSX/`, `.Spotlight-V100`, `.Trashes`, `.fseventsd`, `.TemporaryItems`
- `*~`, `*.swp`, `*.swo`
- `Thumbs.db`, `Desktop.ini`, `$RECYCLE.BIN/`
- `__pycache__/`, `*.py[cod]`, `.pytest_cache/`, `.mypy_cache/`

If those excludes are missing from `scripts/package.sh`, add them before packaging, then run the script.

## Do not

- Commit the zip
- Upload/release unless the user also asks
- Change the plugin version (use `/version-up` for that)
