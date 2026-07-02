#!/usr/bin/env bash
#
# dev.sh - Command-line development tool for the "Ask AI Plugin" calibre plugin.
#
# This wraps calibre's CLI (calibre-customize / calibre / calibredb) so the
# whole dev loop (build -> run -> smoke test) can be driven from the terminal,
# including on headless machines via xvfb-run.
#
# Usage:
#   ./dev.sh build            Rebuild + (re)install the plugin into calibre
#   ./dev.sh run              Launch the calibre GUI with the dev library
#   ./dev.sh run-headless     Launch the calibre GUI under xvfb (no display needed)
#   ./dev.sh smoke            Headless, isolated smoke test: build + load + check
#   ./dev.sh compile          Fast syntax check (py_compile) of all plugin sources
#   ./dev.sh library          Create the dev library + a sample book if missing
#   ./dev.sh logs             Print the plugin's log directory contents
#   ./dev.sh help             Show this help
#
# Environment variables:
#   CALIBRE_LIBRARY   Path to the dev calibre library (default: ~/calibre-library)
#   DISPLAY           If set, 'run' uses it; otherwise falls back to xvfb-run.

set -euo pipefail

PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CALIBRE_LIBRARY="${CALIBRE_LIBRARY:-$HOME/calibre-library}"
SAMPLE_TITLE="The Adventures of Sherlock Holmes"
SAMPLE_AUTHOR="Arthur Conan Doyle"

log()  { printf '\033[1;34m[dev]\033[0m %s\n' "$*"; }
err()  { printf '\033[1;31m[dev:error]\033[0m %s\n' "$*" >&2; }

require() {
    if ! command -v "$1" >/dev/null 2>&1; then
        err "required command '$1' not found. Is calibre installed and on PATH?"
        exit 127
    fi
}

cmd_build() {
    require calibre-customize
    log "Building + installing plugin from $PLUGIN_DIR"
    calibre-customize -b "$PLUGIN_DIR"
}

cmd_compile() {
    log "Compiling all plugin Python sources (syntax check)"
    # Only check the plugin's own top-level sources, skip vendored libs.
    python3 - "$PLUGIN_DIR" <<'PY'
import sys, os, py_compile, glob
root = sys.argv[1]
failed = False
for path in sorted(glob.glob(os.path.join(root, "*.py"))):
    try:
        py_compile.compile(path, doraise=True)
    except py_compile.PyCompileError as e:
        failed = True
        print(f"FAIL {path}: {e}")
for sub in ("models", "aiprovider"):
    for path in sorted(glob.glob(os.path.join(root, sub, "*.py"))):
        try:
            py_compile.compile(path, doraise=True)
        except py_compile.PyCompileError as e:
            failed = True
            print(f"FAIL {path}: {e}")
if failed:
    sys.exit(1)
print("OK: all top-level plugin sources compile")
PY
}

cmd_library() {
    require calibredb
    if [ -f "$CALIBRE_LIBRARY/metadata.db" ]; then
        log "Dev library already exists at $CALIBRE_LIBRARY"
    else
        log "Creating dev library at $CALIBRE_LIBRARY with a sample book"
        mkdir -p "$CALIBRE_LIBRARY"
        local tmp
        tmp="$(mktemp -d)"
        cat > "$tmp/sample.html" <<HTML
<html><head><title>${SAMPLE_TITLE}</title></head>
<body><h1>${SAMPLE_TITLE}</h1><p>By ${SAMPLE_AUTHOR}</p>
<p>To Sherlock Holmes she is always the woman.</p></body></html>
HTML
        ebook-convert "$tmp/sample.html" "$tmp/sample.epub" \
            --authors="$SAMPLE_AUTHOR" --title="$SAMPLE_TITLE" >/dev/null 2>&1
        calibredb add "$tmp/sample.epub" --with-library "$CALIBRE_LIBRARY" >/dev/null
        rm -rf "$tmp"
    fi
    calibredb list --with-library "$CALIBRE_LIBRARY"
}

cmd_run() {
    require calibre
    cmd_library >/dev/null || true
    if [ -n "${DISPLAY:-}" ]; then
        log "Launching calibre GUI on DISPLAY=$DISPLAY (library: $CALIBRE_LIBRARY)"
        exec calibre --with-library "$CALIBRE_LIBRARY"
    else
        log "No DISPLAY set; launching under xvfb-run"
        cmd_run_headless
    fi
}

cmd_run_headless() {
    require calibre
    require xvfb-run
    cmd_library >/dev/null || true
    log "Launching calibre GUI headless via xvfb-run (library: $CALIBRE_LIBRARY)"
    exec xvfb-run -a calibre --with-library "$CALIBRE_LIBRARY"
}

cmd_smoke() {
    require calibre
    require calibre-customize
    require xvfb-run
    require timeout
    local cfg lib rc=0
    cfg="$(mktemp -d)"
    lib="$(mktemp -d)"
    log "Smoke test in isolated config dir: $cfg"

    CALIBRE_CONFIG_DIRECTORY="$cfg" calibre-customize -b "$PLUGIN_DIR" >/dev/null
    # Seed the plugin config so the fresh-config migration path in config.py
    # (which references an unbound 'logger' on main) does not crash on first load.
    mkdir -p "$cfg/plugins"
    printf '{\n  "use_interface_language": false\n}\n' > "$cfg/plugins/ask_ai_plugin.json"

    local logf="$cfg/smoke.log"
    log "Launching calibre headless (up to 40s) to verify plugin loads"
    CALIBRE_CONFIG_DIRECTORY="$cfg" timeout 40 xvfb-run -a \
        calibre --with-library "$lib" > "$logf" 2>&1 &
    local pid=$!
    sleep 22
    kill "$pid" 2>/dev/null || true
    pkill -P "$pid" 2>/dev/null || true
    sleep 2

    if grep -q "ask_ai_plugin" "$logf" && grep -qi "traceback" "$logf"; then
        err "Plugin raised an error during load:"
        grep -A20 -i "traceback" "$logf" >&2 || true
        rc=1
    fi

    if CALIBRE_CONFIG_DIRECTORY="$cfg" calibre-customize --list-plugins 2>/dev/null \
        | grep -qi "ask ai"; then
        log "Plugin is registered."
    else
        err "Plugin is NOT registered."
        rc=1
    fi

    rm -rf "$cfg" "$lib"
    if [ "$rc" -eq 0 ]; then
        log "SMOKE PASS: plugin builds and loads cleanly."
    else
        err "SMOKE FAIL."
    fi
    return "$rc"
}

cmd_logs() {
    local dir="$HOME/.config/calibre/plugins/ask_ai_plugin_logs"
    if [ -d "$dir" ]; then
        log "Plugin logs in $dir:"
        ls -la "$dir"
    else
        log "No plugin log directory found at $dir yet."
    fi
}

cmd_help() {
    sed -n '3,21p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

main() {
    local sub="${1:-help}"
    shift || true
    case "$sub" in
        build)         cmd_build "$@" ;;
        compile)       cmd_compile "$@" ;;
        library)       cmd_library "$@" ;;
        run)           cmd_run "$@" ;;
        run-headless)  cmd_run_headless "$@" ;;
        smoke)         cmd_smoke "$@" ;;
        logs)          cmd_logs "$@" ;;
        help|-h|--help) cmd_help ;;
        *) err "unknown command: $sub"; echo; cmd_help; exit 2 ;;
    esac
}

main "$@"
