#!/usr/bin/env bash
# Package Ask AI Plugin into dist/ for release.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$ROOT/dist"
VERSION="$(python3 -c "import sys; sys.path.insert(0, '$ROOT'); from version import VERSION_STRING; print(VERSION_STRING)")"
ZIP_NAME="Ask AI Plugin.zip"
VERSIONED_ZIP="Ask AI Plugin-${VERSION}.zip"

mkdir -p "$DIST"
cd "$ROOT"

echo "Packaging Ask AI Plugin v${VERSION}..."

rm -f "$DIST/$ZIP_NAME" "$DIST/$VERSIONED_ZIP"

zip -r "$DIST/$ZIP_NAME" . \
  -x "*.git*" \
  -x ".env" \
  -x ".env.*" \
  -x ".cursor/*" \
  -x ".cursor/**" \
  -x ".claude/*" \
  -x ".claude/**" \
  -x ".codex/*" \
  -x ".codex/**" \
  -x ".agent/*" \
  -x ".agent/**" \
  -x ".history/*" \
  -x ".history/**" \
  -x "dist/*" \
  -x "dist/**" \
  -x "scripts/*" \
  -x "scripts/**" \
  -x "tests/*" \
  -x "tests/**" \
  -x "bin/*" \
  -x "bin/**" \
  -x "aiprovider/*" \
  -x "aiprovider/**" \
  -x "docs/*" \
  -x "docs/**" \
  -x "backend/*" \
  -x "backend/**" \
  -x ".github/*" \
  -x ".github/**" \
  -x ".obsidian/*" \
  -x ".obsidian/**" \
  -x ".sync/*" \
  -x ".sync/**" \
  -x ".idea/*" \
  -x ".idea/**" \
  -x ".vscode/*" \
  -x ".vscode/**" \
  -x ".windsurf/*" \
  -x ".windsurf/**" \
  -x "lib/bin/*" \
  -x "lib/bin/**" \
  -x "**/*.dist-info/*" \
  -x "**/*.dist-info/**" \
  -x "**/.pytest_cache/*" \
  -x "**/.pytest_cache/**" \
  -x "**/.mypy_cache/*" \
  -x "**/.mypy_cache/**" \
  -x "**/__pycache__/*" \
  -x "__pycache__/*" \
  -x "__pycache__/**" \
  -x "node_modules/*" \
  -x "node_modules/**" \
  -x "ask_ai_plugin_gif_preview.gif" \
  -x "setup.py" \
  -x "requirements.txt" \
  -x "**/*.py[cod]" \
  -x "**/.DS_Store" \
  -x ".DS_Store" \
  -x "**/._*" \
  -x "**/Thumbs.db" \
  -x "**/Desktop.ini" \
  -x "*.zip" \
  -x "*.code-workspace" \
  > /dev/null

cp "$DIST/$ZIP_NAME" "$DIST/$VERSIONED_ZIP"

echo "Created:"
echo "  $DIST/$ZIP_NAME"
echo "  $DIST/$VERSIONED_ZIP"
