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

```bash
# 1. 更新教程文档版本号
# tutorial/tutorial_v0.3_for_Ask_AI_Plugin_v1.3.3.md Line 2
# Latest updated: November 25, 2025, Ask AI Plugin vX.Y.Z

# 2. 更新 VERSION_UPDATE_GUIDE.md
# 在"版本号历史记录"中添加新版本记录
```

---

## ✅ 完成检查

- [ ] version.py 已更新
- [ ] __init__.py Line 22 已更新（🔴 最重要）
- [ ] __init__.py Line 84 已更新
- [ ] setup.py Line 15 已更新
- [ ] 版本号验证通过
- [ ] 插件构建成功
- [ ] calibre 加载正常
- [ ] 界面显示正确版本号
- [ ] 文档已更新

---

## 📝 版本号规则

- **MAJOR**（主版本号）：不兼容的 API 修改
- **MINOR**（次版本号）：向下兼容的功能性新增
- **PATCH**（修订号）：向下兼容的问题修正

---

## ⚠️ 常见错误

### ❌ 只更新了 version.py
**后果：** 用户不会收到更新通知

### ❌ 忘记更新 __init__.py Line 22
**后果：** calibre 不会推送更新给用户

### ❌ 忘记更新 __init__.py Line 84
**后果：** 插件管理器显示旧版本号

### ❌ 忘记更新 setup.py Line 15
**后果：** setuptools 安装时显示旧版本号

---

## 🔗 相关文档

- 详细指南：`docs/VERSION_UPDATE_GUIDE.md`
- 变更日志：`CHANGELOG_VENDOR_NAMESPACE.md`
