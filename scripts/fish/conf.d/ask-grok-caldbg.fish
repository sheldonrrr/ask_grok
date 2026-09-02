# ask_grok — 自动加载 Calibre 本地调试命令（caldbg-ag 等）
# 安装：ln -sf ~/ask_grok/scripts/fish/conf.d/ask-grok-caldbg.fish ~/.config/fish/conf.d/

function __ask_grok_conf_anchor; end
set -l _ask_grok_conf (functions --details __ask_grok_conf_anchor)
functions -e __ask_grok_conf_anchor
# .../ask_grok/scripts/fish/conf.d/ask-grok-caldbg.fish → 上跳 4 层到仓库根
set -l _ask_grok_root (path dirname -- (path dirname -- (path dirname -- (path dirname -- (path resolve -- $_ask_grok_conf)))))

if set -q ASK_GROK_ROOT; and test -f "$ASK_GROK_ROOT/scripts/caldbg.fish"
    set _ask_grok_root $ASK_GROK_ROOT
end

if test -f "$_ask_grok_root/scripts/caldbg.fish"
    # 静默加载函数；需要看用法时执行 source scripts/caldbg.fish
    source "$_ask_grok_root/scripts/caldbg.fish" >/dev/null
    fish_add_path -m "$_ask_grok_root/bin"
end
