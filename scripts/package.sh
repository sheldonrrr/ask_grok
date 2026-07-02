#!/usr/bin/env bash
# Package Ask AI Plugin into dist/ for release.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$ROOT/dist"
VERSION="$(python3 -c "import sys; sys.path.insert(0, '$ROOT'); from version import VERSION_STRING; print(VERSION_STRING)")"
VERSIONED_ZIP="Ask_AI_Plugin_v${VERSION}.zip"

mkdir -p "$DIST"
cd "$ROOT"

echo "Packaging Ask AI Plugin v${VERSION}..."

rm -f "$DIST/Ask AI Plugin.zip" "$DIST/Ask AI Plugin-${VERSION}.zip" "$DIST/$VERSIONED_ZIP"

zip -r "$DIST/$VERSIONED_ZIP" . \
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

# Keep sample env template in release package (align with .gitignore: !.env.example)
if [ -f "$ROOT/.env.example" ]; then
  zip -qj "$DIST/$VERSIONED_ZIP" "$ROOT/.env.example"
fi

echo "Created:"
echo "  $DIST/$VERSIONED_ZIP"
