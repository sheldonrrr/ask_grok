# 版本号更新快速检查清单

## 🚀 更新版本号到 X.Y.Z

### 第一步：更新版本号（5 个位置）

```bash
# 1️⃣ version.py Line 11
VERSION = (X, Y, Z)

# 2️⃣ __init__.py Line 22 🔴 最重要！
VERSION = (X, Y, Z) # 版本号推送触发

# 3️⃣ __init__.py Line 84
version = (X, Y, Z)

# 4️⃣ setup.py Line 15
version='X.Y.Z'

# 5️⃣ ui.py - 自动计算（无需手动更新）
# VERSION_DISPLAY 从 version.py 自动导入
```

---

### 第二步：验证版本号

```bash
cd /home/she/ask_grok

# 检查所有版本号
grep -n "VERSION = (" version.py __init__.py
grep -n "version.*= (" __init__.py
grep -n "version=" setup.py

# 应该看到：
# version.py:11:VERSION = (X, Y, Z)
# __init__.py:22:VERSION = (X, Y, Z) # 版本号推送触发
# __init__.py:84:    version             = (X, Y, Z)
# setup.py:15:    version='X.Y.Z',
```

---

### 第三步：构建并测试

```bash
# 构建插件
calibre-customize -b .

# 应该看到：
# Plugin updated: Ask AI Plugin (X, Y, Z)

# 启动 calibre 测试
calibre-debug -g

# 检查：
# 1. 插件能否正常加载
# 2. 打开插件菜单 → About
# 3. 确认版本号显示为 vX.Y.Z
```

---

### 第四步：更新文档

#### 4.1 创建 CHANGELOG 文档（必须）

**🔴 重要：每次版本更新都必须创建新的 CHANGELOG 文档**

1. **创建新的 CHANGELOG 文件**
   ```bash
   # 在 docs/ 目录下创建新文件
   # 文件名格式：CHANGELOG_VX.Y.Z_EN.md
   # 例如：docs/CHANGELOG_V1.4.1_EN.md
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
   - 例如：创建 V1.4.1 后，删除 V1.3.9（保留 V1.4.1 和 V1.4.0）

5. **发布流程**
   - 第一部分（BBCode）：复制到 mobileread.com 论坛发布帖
   - 第二部分（Markdown）：复制到 GitHub Release 页面

#### 4.2 更新 Tutorial 文档（仅当内容有变化时）

**注意：只有当教程内容（除日期和版本号外）有实质性修改时才需要升级 tutorial 版本**

1. **判断是否需要升级 tutorial 版本**
   - ✅ 需要升级：新增功能说明、修改操作步骤、更新配置说明等
   - ❌ 不需要升级：仅更新日期和版本号

2. **如果只是更新日期和版本号**
   ```bash
   # 直接修改最新的 tutorial 文件
   # 例如：tutorial/tutorial_v0.8.md
   # 更新第 3 行：Latest updated: [当前日期], Ask AI Plugin v[当前版本]
   # 示例：Latest updated: Feb 05, 2026, Ask AI Plugin v1.4.3
   ```

3. **如果需要升级 tutorial 版本**
   ```bash
   # 步骤 1：创建新版本文件
   cp tutorial/tutorial_v0.7.md tutorial/tutorial_v0.8.md
   
   # 步骤 2：修改新文件
   # - 更新标题：# Ask AI Plugin User Manual v0.8
   # - 更新日期和版本：Latest updated: [当前日期], Ask AI Plugin v[当前版本]
   # - 添加或修改教程内容
   
   # 步骤 3：🔴 更新代码中的 tutorial 加载逻辑（2 个位置）
   # tutorial_viewer.py Line ~198-200
   # ui.py Line ~721-723
   # 将两处的回退逻辑更新为最新两个版本
   # 例如：tutorial_v0.8.md -> tutorial_v0.7.md（删除 v0.6 的回退）
   
   # 步骤 4：删除过旧的 tutorial 文件
   # 只保留最新两个版本
   # 例如：删除 tutorial_v0.6.md
   ```

4. **Tutorial 版本号规则**
   - Tutorial 版本号（如 v0.7）独立于插件版本号（如 v1.4.1）
   - Tutorial 版本号只在教程内容有实质性变化时才递增
   - 一个 tutorial 版本可以对应多个插件版本

#### 4.3 其他文档更新

```bash
# 1. 更新本文档（VERSION_UPDATE_CHECKLIST.md）
# 如果示例中的版本号或日期需要更新，同步修改

# 2. 更新 VERSION_UPDATE_GUIDE.md
# 在"版本号历史记录"中添加新版本记录
```

---

## ✅ 完成检查

### 代码更新
- [ ] version.py 已更新
- [ ] __init__.py Line 22 已更新（🔴 最重要）
- [ ] __init__.py Line 84 已更新
- [ ] setup.py Line 15 已更新
- [ ] 版本号验证通过

### 测试验证
- [ ] 插件构建成功
- [ ] calibre 加载正常
- [ ] 界面显示正确版本号

### 文档更新
- [ ] 🔴 CHANGELOG_VX.Y.Z_EN.md 已创建（必须）
- [ ] CHANGELOG 包含 BBCode 格式（用于论坛）
- [ ] CHANGELOG 包含 Markdown 格式（用于 GitHub）
- [ ] 删除倒数第三个旧版本 CHANGELOG（如果存在）
- [ ] Tutorial 日期和版本号已更新
- [ ] Tutorial 版本已升级（如果内容有变化）
- [ ] Tutorial 加载逻辑已更新（如果升级了版本）
- [ ] 删除倒数第三个旧版本 Tutorial（如果升级了版本）

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

#### ❌ 忘记更新 __init__.py Line 84
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

#### ❌ Tutorial 只更新了日期但升级了版本号
**后果：** 版本号膨胀，没有实质性内容变化却增加了版本号

#### ❌ Tutorial 内容有变化但忘记升级版本号
**后果：** 用户看到的教程版本号与实际内容不符

#### ❌ 升级 Tutorial 版本但忘记更新代码中的加载逻辑
**后果：** 插件仍然加载旧版本教程，用户看不到新内容

---

## 🔗 相关文档

- 详细指南：`docs/VERSION_UPDATE_GUIDE.md`
- 变更日志：`CHANGELOG_VENDOR_NAMESPACE.md`
