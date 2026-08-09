#!/usr/bin/env bash
# Package Ask AI Plugin into dist/ for calibre / MobileRead distribution.
#
# Output (canonical, no spaces — safer on Windows / shells):
#   dist/Ask_AI_Plugin_vX.Y.Z.zip
#
# This public GitHub repo contains more than the plugin runtime.
# Keep zip excludes in sync with the "Packaging notes" section in .gitignore.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$ROOT/dist"
VERSION="$(python3 -c "import sys; sys.path.insert(0, '$ROOT'); from version import VERSION_STRING; print(VERSION_STRING)")"
VERSIONED_ZIP="Ask_AI_Plugin_v${VERSION}.zip"

mkdir -p "$DIST"
cd "$ROOT"

echo "Packaging Ask AI Plugin v${VERSION}..."

# Remove current + legacy artifact names
rm -f \
  "$DIST/$VERSIONED_ZIP" \
  "$DIST/Ask_AI_Plugin_v"*.zip \
  "$DIST/Ask AI Plugin.zip" \
  "$DIST/Ask AI Plugin-"*.zip

# zip -x patterns are matched against archive member names (paths relative to ROOT).
# Broad "*.git*" keeps .git / .gitignore / .gitattributes out of the ship zip.
zip -r "$DIST/$VERSIONED_ZIP" . \
  -x "*.git*" \
  \
  -x ".env" \
  -x ".env.*" \
  \
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
  -x ".windsurf/*" \
  -x ".windsurf/**" \
  -x ".idea/*" \
  -x ".idea/**" \
  -x ".vscode/*" \
  -x ".vscode/**" \
  -x ".github/*" \
  -x ".github/**" \
  -x ".obsidian/*" \
  -x ".obsidian/**" \
  -x ".sync/*" \
  -x ".sync/**" \
  \
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
  -x "release/*" \
  -x "release/**" \
  -x "backend/*" \
  -x "backend/**" \
  -x "lib/bin/*" \
  -x "lib/bin/**" \
  \
  -x "tutorial/about.md" \
  -x "ask_ai_plugin_gif_preview.gif" \
  -x "setup.py" \
  -x "requirements.txt" \
  -x "AGENTS.md" \
  -x "*.code-workspace" \
  -x "*.zip" \
  \
  -x "**/.pytest_cache/*" \
  -x "**/.pytest_cache/**" \
  -x "**/.mypy_cache/*" \
  -x "**/.mypy_cache/**" \
  -x "**/__pycache__/*" \
  -x "**/__pycache__/**" \
  -x "__pycache__/*" \
  -x "__pycache__/**" \
  -x "node_modules/*" \
  -x "node_modules/**" \
  -x "**/*.py[cod]" \
  \
  -x "**/.DS_Store" \
  -x ".DS_Store" \
  -x "**/._*" \
  -x "__MACOSX/*" \
  -x "__MACOSX/**" \
  -x "**/.Spotlight-V100/*" \
  -x "**/.Spotlight-V100/**" \
  -x "**/.Trashes/*" \
  -x "**/.Trashes/**" \
  -x "**/.fseventsd/*" \
  -x "**/.fseventsd/**" \
  -x "**/.TemporaryItems/*" \
  -x "**/.TemporaryItems/**" \
  -x "**/.AppleDouble/*" \
  -x "**/.AppleDouble/**" \
  -x "**/.LSOverride" \
  -x "**/*.icloud" \
  -x "**/*~" \
  -x "**/*.swp" \
  -x "**/*.swo" \
  -x "**/Thumbs.db" \
  -x "**/ehthumbs.db" \
  -x "**/Desktop.ini" \
  -x "**/\$RECYCLE.BIN/*" \
  -x "**/\$RECYCLE.BIN/**" \
  > /dev/null

# `.env.*` above also matches `.env.example`; re-add the safe template for users.
if [ -f "$ROOT/.env.example" ]; then
  zip -qj "$DIST/$VERSIONED_ZIP" "$ROOT/.env.example"
fi

echo "Created:"
echo "  $DIST/$VERSIONED_ZIP"
