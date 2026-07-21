# 版本号更新快速检查清单

> Agent 精简版见：`.cursor/rules/version-update.mdc`

## 🚀 更新版本号到 X.Y.Z

### 第一步：更新版本号（5 个位置）

```bash
# 1️⃣ version.py Line 11
VERSION = (X, Y, Z)

# 2️⃣ __init__.py Line 22 🔴 最重要！
VERSION = (X, Y, Z) # 版本号推送触发

# 3️⃣ __init__.py Line 87
version = (X, Y, Z)

# 4️⃣ setup.py Line 15
version='X.Y.Z'

# 5️⃣ ui.py - 自动计算（无需手动更新）
# VERSION_DISPLAY 从 version.py 自动导入
```

当前版本示例（v1.5.0）：

```bash
# version.py
VERSION = (1, 5, 0)

# __init__.py — VERSION（推送触发）
VERSION = (1, 5, 0) # 版本号推送触发

# __init__.py — AskAIPlugin.version
version = (1, 5, 0)

# setup.py
version='1.5.0',
```

---

### 第二步：验证版本号

```bash
cd /Users/sheldon/ask_grok

# 检查所有版本号
grep -n "VERSION = (" version.py __init__.py
grep -n "version.*= (" __init__.py
grep -n "version=" setup.py

# 应该看到：
# version.py: VERSION = (1, 5, 0)
# __init__.py: VERSION = (1, 5, 0) # 版本号推送触发
# __init__.py:     version             = (1, 5, 0)
# setup.py:    version='1.5.0',
```

---

### 第三步：构建并测试

```bash
# 本地安装/更新插件（需要 calibre 命令可用）
calibre-customize -b .

# 应该看到：
# Plugin updated: Ask AI Plugin (1, 4, 5)

# 启动 calibre 测试
calibre-debug -g

# 检查：
# 1. 插件能否正常加载
# 2. 打开插件菜单 → About
# 3. 确认版本号显示为 v1.5.0
```

---

### 第四步：打包发布 zip

```bash
# 输出到 dist/ 目录（每次打包都会覆盖当前版本 zip）
chmod +x scripts/package.sh
./scripts/package.sh

# 会生成：
# dist/Ask_AI_Plugin_v1.5.0.zip
```

说明：
- 产物文件名规范：`Ask_AI_Plugin_vX.Y.Z.zip`（无空格；见 `docs/README.md`）
- `dist/` 目录保留在仓库中，zip 产物已被 `.gitignore` 忽略
- 打包脚本会排除 `.git/`、`.cursor/`、`.github/`、`aiprovider/`、`docs/`、`scripts/`、`tests/`、`bin/`、`backend/`、`__pycache__/` 等
- `aiprovider/`、`docs/` 仅保留在 GitHub 仓库中，不随插件 zip 分发

---

### 第五步：更新文档

#### 5.1 创建 CHANGELOG 文档（必须）

**🔴 重要：每次版本更新都必须创建新的 CHANGELOG 文档**

1. **创建新的 CHANGELOG 文件**
   ```bash
   # 在 docs/ 目录下创建新文件
   # 文件名格式：CHANGELOG_VX.Y.Z_EN.md
   # 例如：docs/CHANGELOG_V1.4.7_EN.md
   ```

2. **CHANGELOG 文档结构（包含两种格式）**
   
   文档分为两部分，使用相同内容但不同格式：
   
   **第一部分：calibre 官方论坛格式（BBCode）**
   ```
   # Ask AI Plugin - Version X.Y.Z Release Notes
   
   [b]New Features (vX.Y.Z)[/b]
   [list]
   [*][b]功能标题[/b] - 功能描述（简洁，不要过于技术化）
   [/list]
   
   [b]Bug Fixes (vX.Y.Z)[/b]
   [list]
   [*][b]修复标题[/b] - 修复描述
   [/list]
   
   [b]Improvements (vX.Y.Z)[/b]
   [list]
   [*][b]改进标题[/b] - 改进描述
   [/list]
   ```
   
   **第二部分：GitHub Release 格式（Markdown）**
   ```markdown
   ---
   
   ## GitHub Release Notes (vX.Y.Z)
   
   ### New Features
   - **功能标题** - 功能描述
   
   ### Bug Fixes
   - **修复标题** - 修复描述
   
   ### Improvements
   - **改进标题** - 改进描述
   ```

3. **内容编写原则**
   - ✅ 简洁明了，面向用户而非开发者
   - ✅ 突出用户可感知的变化
   - ❌ 避免过于技术化的细节
   - ❌ 不要提及内部代码重构（除非影响用户体验）

4. **CHANGELOG 版本管理**
   - 始终保留最新两个版本的 CHANGELOG 文档
   - 创建新版本后，手动删除倒数第三个旧版本
   - 例如：创建 V1.4.7 后，删除倒数第三个旧版本（通常保留最新两个版本文档）

5. **发布流程**
   - 第一部分（BBCode）：复制到 mobileread.com 论坛发布帖
   - 第二部分（Markdown）：复制到 GitHub Release 页面
   - 上传 `dist/Ask_AI_Plugin_vX.Y.Z.zip` 到 GitHub Release

#### 5.2 更新 Tutorial 文档（就地修改，不新增文件）

**固定文件：`tutorial/tutorial_v1.0.md`** — 之后发版都直接改这一份，方便 git diff。不要再 `cp` 出 `tutorial_v*.md`。

每次版本升级至少更新文件头：
```bash
# Latest updated: [当前日期], Ask AI Plugin v[当前版本]
# 示例：Latest updated: Jul 21, 2026, Ask AI Plugin v1.5.0
```

若有用户可见的功能变化，在同一文件内改对应章节（保持介绍简短）。加载路径保持 `tutorial/tutorial_v1.0.md`，一般无需改 `tutorial_viewer.py` / `ui.py`。

#### 5.3 其他文档更新

```bash
# 1. 更新本文档（VERSION_UPDATE_CHECKLIST.md）
# 如果示例中的版本号或日期需要更新，同步修改

# 2. 更新 RELEASE_UPDATE_GUIDE.md（如有新的发版流程变化）
```

---

## ✅ 完成检查

### 代码更新
- [ ] version.py 已更新
- [ ] __init__.py Line 22 已更新（🔴 最重要）
- [ ] __init__.py Line 87 已更新
- [ ] setup.py Line 15 已更新
- [ ] 版本号验证通过

### 测试验证
- [ ] 插件构建成功（`calibre-customize -b .` 或 `./scripts/package.sh`）
- [ ] calibre 加载正常
- [ ] 界面显示正确版本号

### 打包发布
- [ ] `./scripts/package.sh` 已执行
- [ ] `dist/Ask_AI_Plugin_vX.Y.Z.zip` 已生成

### 文档更新
- [ ] 🔴 CHANGELOG_VX.Y.Z_EN.md 已创建（必须）
- [ ] CHANGELOG 包含 BBCode 格式（用于论坛）
- [ ] CHANGELOG 包含 Markdown 格式（用于 GitHub）
- [ ] 删除倒数第三个旧版本 CHANGELOG（如果存在）
- [ ] `tutorial/tutorial_v1.0.md` 已就地更新（日期/插件版本；有功能变化则改对应章节）
- [ ] 未新增额外的 tutorial_v*.md 文件

---

## 📝 版本号规则

- **MAJOR**（主版本号）：不兼容的 API 修改
- **MINOR**（次版本号）：向下兼容的功能性新增
- **PATCH**（修订号）：向下兼容的问题修正

---

## ⚠️ 常见错误

### 代码更新错误

#### ❌ 只更新了 version.py
**后果：** 用户不会收到更新通知

#### ❌ 忘记更新 __init__.py Line 22
**后果：** calibre 不会推送更新给用户

#### ❌ 忘记更新 __init__.py Line 87
**后果：** 插件管理器显示旧版本号

#### ❌ 忘记更新 setup.py Line 15
**后果：** setuptools 安装时显示旧版本号

### 文档更新错误

#### ❌ 忘记创建 CHANGELOG 文档
**后果：** 无法在论坛和 GitHub 发布更新说明，用户不知道更新了什么

#### ❌ CHANGELOG 只有一种格式
**后果：** 缺少 BBCode 格式无法发布到论坛，缺少 Markdown 格式无法发布到 GitHub

#### ❌ CHANGELOG 内容过于技术化
**后果：** 普通用户看不懂更新内容，降低用户体验

#### ❌ 忘记删除旧版本 CHANGELOG
**后果：** 文档目录混乱，保留过多无用文档

#### ❌ 为教程再新建一份 tutorial_v*.md
**后果：** diff 分散、加载回退逻辑易过时；应只改 `tutorial/tutorial_v1.0.md`

#### ❌ 发版时忘记更新教程头的日期/插件版本
**后果：** 用户手册显示旧版本号

#### ❌ 忘记执行 `./scripts/package.sh`
**后果：** 发版时没有可上传的 zip 文件

---

## 相关文档

- 文档命名规范：`docs/README.md`
- 发版补充指南：`docs/RELEASE_UPDATE_GUIDE.md`
- 变更日志：`docs/CHANGELOG_VX.Y.Z_EN.md`（仅保留最近两个版本）
