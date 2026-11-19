# ask_grok — Calibre 本地调试（fish）
# 用法（任选其一）：
#   source scripts/caldbg.fish
#   soufish                    # 若已在 ~/.config/fish/config.fish 中 source 本文件
#   ~/ask_grok/bin/caldbg-ag   # 任意 shell 可直接运行
# 新开 fish 自动加载：
#   ln -sf ~/ask_grok/scripts/fish/conf.d/ask-grok-caldbg.fish ~/.config/fish/conf.d/

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

function __ask_grok_calibre_still_running
    # macOS 上图形界面进程名是 calibre；calibre-debug --gui 则是 calibre-debug。
    pgrep -x calibre >/dev/null 2>&1
    or pgrep -x calibre-debug >/dev/null 2>&1
    or pgrep -f '/calibre.app/Contents/MacOS/calibre($| )' >/dev/null 2>&1
end

function __ask_grok_bump_build
    __ask_grok_check_dir; or return 1
    set -l old (python3 -c 'import pathlib,re,sys; t=pathlib.Path(sys.argv[1]).read_text(); m=re.search(r"^VERSION = \(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", t, re.M); print("(%s, %s, %s)" % m.groups())' "$ASK_GROK_ROOT/version.py")
    set -l new (sh "$ASK_GROK_ROOT/scripts/bump-build.sh"); or return 1
    set -l shown (string replace -a '.' ', ' -- $new)
    echo "本地测试号: $old -> ($shown)"
end

function __ask_grok_wait_calibre_quit
    # calibre-debug -s returns before the app process is gone.
    # A new GUI started while that process is still alive is the old one,
    # so its terminal log keeps the plugin version from before this bump.
    for _i in (seq 1 75)
        if not __ask_grok_calibre_still_running
            sleep 0.3
            if not __ask_grok_calibre_still_running
                return 0
            end
        end
        sleep 0.2
    end
    echo "错误: Calibre 没有退出，已取消启动，避免日志仍是旧版本"
    return 1
end

function caldbg
    # 本地测试：第三位测试号 +1，等旧进程退出，再安装并启动。
    # 重新读取本文件，避免已经打开的终端还在用旧函数。
    source "$ASK_GROK_ROOT/scripts/caldbg.fish" >/dev/null
    __ask_grok_caldbg_ag_impl
end

function caldbg-ag
    # Re-read this file when an already-open terminal still has an older function.
    # The impl name is separate so this reload does not call itself.
    source "$ASK_GROK_ROOT/scripts/caldbg.fish" >/dev/null
    __ask_grok_caldbg_ag_impl
end

function __ask_grok_caldbg_ag_impl
    # 先退出已在运行的 Calibre，再递增并安装，最后才启动。
    # 启动日志读的是已安装插件的版本，所以递增和安装都必须在启动之前。
    if __ask_grok_calibre_still_running
        calibre-debug -s
        __ask_grok_wait_calibre_quit; or return 1
    end
    __ask_grok_bump_build; or return 1
    __ask_grok_install_plugin; or return 1
    set -l version (python3 -c "import sys; sys.path.insert(0, '$ASK_GROK_ROOT'); from version import VERSION_STRING; print(VERSION_STRING)")
    echo "启动插件: v$version"
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
echo "  caldbg      测试号 +1，等旧进程退出，再安装并启动"
echo "  caldbg-ag   同 caldbg"
echo "  caldbg-p    打包 dist + 安装 zip + 启动"
echo "  caldbg-pag  同 caldbg-p，但先结束旧进程"
