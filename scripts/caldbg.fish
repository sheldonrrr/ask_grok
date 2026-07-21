# ask_grok — Calibre 本地调试（fish）
# 用法（任选其一）：
#   source scripts/caldbg.fish
#   soufish                    # 若已在 ~/.config/fish/config.fish 中 source 本文件
#   ~/ask_grok/bin/caldbg-ag   # 任意 shell 可直接运行

if not type -q calibre-customize
    if test -d /Applications/calibre.app/Contents/MacOS
        fish_add_path /Applications/calibre.app/Contents/MacOS
    else if test -x /opt/calibre/calibre-customize
        fish_add_path /opt/calibre
    end
end

function __ask_grok_caldbg_anchor; end
set -l _caldbg_fish (functions --details __ask_grok_caldbg_anchor)
functions -e __ask_grok_caldbg_anchor
if test -f "$_caldbg_fish"
    set -gx ASK_GROK_ROOT (path dirname -- (path dirname -- (path resolve -- $_caldbg_fish)))
else
    set -gx ASK_GROK_ROOT (path resolve -- .)
end

set -l _plugin_name "Ask AI Plugin"

function __ask_grok_check_dir
    if test -z "$ASK_GROK_ROOT"
        echo "错误: ASK_GROK_ROOT 为空"
        return 1
    end
    if not test -f "$ASK_GROK_ROOT/__init__.py"
        echo "错误: 插件目录无效: $ASK_GROK_ROOT"
        return 1
    end
    echo "ask_grok 目录: $ASK_GROK_ROOT"
end

function __ask_grok_install_plugin
    __ask_grok_check_dir; or return 1
    calibre-customize -r "$_plugin_name" 2>/dev/null
    calibre-customize -b "$ASK_GROK_ROOT"; or return 1
    set -l list_output (calibre-customize -l 2>/dev/null)
    set -l lines (string match "*$_plugin_name*" -- $list_output)
    if test (count $lines) -eq 0
        echo "警告: calibre-customize -l 中未找到 $_plugin_name"
        return 1
    end
    echo $lines[1]
    echo "OK: 插件已安装 — 在 Toolbars & menus 搜索 Ask AI"
    return 0
end

function caldbg
    __ask_grok_install_plugin; or return 1
    calibre-debug --gui
end

function caldbg-ag
    calibre-debug -s
    __ask_grok_install_plugin; or return 1
    calibre-debug --gui
end

function caldbg-p
    __ask_grok_check_dir; or return 1
    cd "$ASK_GROK_ROOT"
    bash scripts/package.sh
    set -l version (python3 -c "import sys; sys.path.insert(0, '$ASK_GROK_ROOT'); from version import VERSION_STRING; print(VERSION_STRING)")
    set -l zip "$ASK_GROK_ROOT/dist/Ask_AI_Plugin_v$version.zip"
    if not test -f "$zip"
        echo "未找到 dist/Ask_AI_Plugin_v$version.zip"
        return 1
    end
    calibre-customize -r "$_plugin_name" 2>/dev/null
    calibre-customize -a "$zip"
    calibre-customize -l 2>/dev/null | string match "*$_plugin_name*"
    calibre-debug --gui
end

function caldbg-pag
    calibre-debug -s
    caldbg-p
end

echo "ask_grok — source scripts/caldbg.fish"
echo "  caldbg      源码安装 + 启动"
echo "  caldbg-ag   结束旧进程 + 源码安装 + 启动"
echo "  caldbg-p    打包 dist + 安装 zip + 启动"
echo "  caldbg-pag  同 caldbg-p，但先结束旧进程"
