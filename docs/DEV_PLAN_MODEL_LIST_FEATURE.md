# 开发计划：模型列表动态加载功能

**创建日期：** 2025.10.21 Night  
**功能名称：** Dynamic Model List Loading  
**优先级：** High  
**预计工时：** 4-6小时

---

## 📋 需求概述

### 当前问题
- 用户需要手动输入模型名称，容易出错
- 不同AI提供商的模型名称格式不同，用户体验差
- 无法知道哪些模型可用
- 模型名称可能随时更新，插件无法及时同步

### 目标
实现从AI提供商API动态获取可用模型列表，让用户通过下拉选择而非手动输入。

### 核心功能
1. **动态加载模型列表** - 点击"加载模型"按钮从API获取
2. **下拉选择模型** - 从获取的列表中选择
3. **自定义模型名称** - 支持手动输入（向后兼容）
4. **配置迁移** - 保留现有用户的模型配置

---

## 🎯 功能需求详细分析

### 1. UI变更需求

#### 1.1 模型选择区域布局
```
Model: [下拉选择框]  [加载模型按钮]
☐ 使用自定义的模型名称
[文本输入框 - 仅当勾选时显示]
```

#### 1.2 交互逻辑
- **初始状态**: 下拉框为空，"加载模型"按钮可点击
- **点击"加载模型"**: 验证API Key → 调用API → 填充下拉框
- **勾选"使用自定义"**: 下拉框禁用，显示文本输入框
- **向后兼容**: 模型不在列表中时自动切换到自定义模式

### 2. API功能需求

#### 2.1 各提供商API端点

| Provider | Endpoint | Auth Method | 支持状态 |
|----------|----------|-------------|---------|
| OpenAI | `GET /v1/models` | Bearer Token | ✅ |
| Anthropic | `GET /v1/models` | x-api-key | ✅ |
| Nvidia | `GET /v1/models` | Bearer Token | ✅ |
| Grok | `GET /v1/models` | Bearer Token | ✅ |
| DeepSeek | `GET /v1/models` | Bearer Token | ✅ |
| Gemini | `GET /v1beta/models?key={key}` | URL参数 | ✅ |
| Custom | `GET /v1/models` | Bearer Token | ✅ |

#### 2.2 新增方法签名

**在 `api.py` 中：**
```python
def fetch_available_models(self, model_name: str, config: Dict) -> Tuple[bool, Union[List[str], str]]
```

**在各模型类中：**
```python
def fetch_available_models(self) -> List[str]
```

### 3. 配置结构变更

**新增字段：**
```json
{
  "models": {
    "openai": {
      "use_custom_model_name": false,  // 新增
      "model": "gpt-4o-mini"
    }
  }
}
```

---

## 🏗️ 实现步骤

### Phase 1: 基础架构（1.5小时）

**文件：** `models/base.py`
- [ ] 在 `BaseAIModel` 中添加抽象方法 `fetch_available_models()`
- [ ] 添加异常类型 `ModelListNotSupportedError`

**文件：** `api.py`
- [ ] 实现 `APIClient.fetch_available_models()` 方法
- [ ] 添加参数验证和错误处理
- [ ] 添加日志记录

### Phase 2: 各模型实现（2小时）

**OpenAI兼容模型** (`openai.py`, `grok.py`, `deepseek.py`, `nvidia.py`, `custom.py`)
- [ ] 实现 `fetch_available_models()` 方法
- [ ] 使用 `GET /v1/models` 端点
- [ ] Bearer Token认证
- [ ] 解析响应并返回模型ID列表

**Anthropic模型** (`anthropic.py`)
- [ ] 实现 `fetch_available_models()` 方法
- [ ] 使用 `GET /v1/models` 端点
- [ ] x-api-key认证 + anthropic-version头
- [ ] 解析响应并返回模型ID列表

**Gemini模型** (`gemini.py`)
- [ ] 实现 `fetch_available_models()` 方法
- [ ] 使用 `GET /v1beta/models?key={key}` 端点
- [ ] URL参数认证
- [ ] 处理 "models/" 前缀

### Phase 3: UI实现（1.5小时）

**文件：** `config.py` - `ModelConfigWidget` 类

- [ ] 修改 `setup_ui()` 方法
  - [ ] 将模型输入框改为下拉框
  - [ ] 添加"加载模型"按钮
  - [ ] 添加"使用自定义模型名称"复选框
  - [ ] 添加自定义模型输入框（初始隐藏）

- [ ] 实现 `on_load_models_clicked()` 方法
  - [ ] 验证API Key
  - [ ] 调用 `api.fetch_available_models()`
  - [ ] 填充下拉框
  - [ ] 显示成功/错误消息

- [ ] 实现 `on_custom_model_toggled()` 方法
  - [ ] 切换控件可见性
  - [ ] 复制当前选中的模型名称

- [ ] 修改 `get_config()` 方法
  - [ ] 保存 `use_custom_model_name` 字段
  - [ ] 根据模式保存模型名称

- [ ] 修改 `load_model_config()` 方法
  - [ ] 加载 `use_custom_model_name` 字段
  - [ ] 向后兼容处理

### Phase 4: 国际化（0.5小时）

**文件：** `i18n.py` 或翻译文件

- [ ] 添加英文翻译（前期只先保证英文语言的实现，之后我会从英文中孵化出来其他语言的支持。）

**新增键：**
- `load_models`, `loading`, `use_custom_model`
- `custom_model_placeholder`, `model_placeholder`
- `models_loaded`, `load_models_failed`
- `model_list_not_supported`, `api_key_required`

### Phase 5: 测试（1小时）

- [ ] 单元测试：API方法
- [ ] 单元测试：UI交互
- [ ] 集成测试：端到端流程
- [ ] 手动测试：所有7个提供商
- [ ] 向后兼容测试
- [ ] 错误处理测试

---

## 🧪 测试清单

### 功能测试
- [ ] OpenAI: 加载模型列表
- [ ] Anthropic: 加载模型列表
- [ ] Nvidia: 加载模型列表
- [ ] Gemini: 加载模型列表（验证前缀处理）
- [ ] Grok: 加载模型列表
- [ ] DeepSeek: 加载模型列表
- [ ] Custom: 加载模型列表

### UI测试
- [ ] 下拉框正确填充
- [ ] "加载模型"按钮状态切换
- [ ] 自定义模式切换
- [ ] 配置保存和加载

### 兼容性测试
- [ ] 旧配置正确加载
- [ ] 模型不在列表时自动切换到自定义
- [ ] 新旧配置格式兼容

### 错误处理测试
- [ ] API Key未填写
- [ ] API请求失败
- [ ] 网络超时
- [ ] 无效API Key

---

## 📦 交付物

1. **代码文件**
   - `models/base.py` - 抽象方法定义
   - `models/*.py` - 各模型实现
   - `api.py` - 统一接口
   - `config.py` - UI实现
   - `i18n.py` - 翻译

2. **文档**
   - 本开发计划
   - API文档更新
   - 用户手册更新

3. **测试**
   - 单元测试代码
   - 测试报告

---

## 🚀 发布计划

1. **开发完成** → 内部测试
2. **测试通过** → 创建PR
3. **代码审查** → 合并到主分支
4. **版本号** → 1.3.0 → 1.4.0
5. **发布说明** → 更新CHANGELOG

---

## 📌 注意事项

1. **CORS问题**: Nvidia在浏览器中有CORS限制，但Calibre插件使用Python requests不受影响
2. **API限流**: 注意各提供商的API调用限制
3. **超时处理**: 设置合理的超时时间（10秒）
4. **错误提示**: 提供清晰的错误消息
5. **日志记录**: 记录所有API调用和错误
6. **向后兼容**: 确保旧配置仍然可用

---

**开发开始时间：** 待定  
**预计完成时间：** 开始后4-6小时  
**负责人：** Sheldon
