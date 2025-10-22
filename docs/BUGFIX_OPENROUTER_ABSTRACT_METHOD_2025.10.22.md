# OpenRouter 抽象方法实现修复
**修复日期**: 2025-10-22  
**问题**: OpenRouter 无法实例化，提示抽象方法 `ask` 未实现

---

## 问题描述

在测试 OpenRouter 的 Load Models 功能时，出现以下错误：

```
Failed to load models: 未知錯誤: Can't instantiate abstract class OpenRouterModel with abstract method ask
```

---

## 根本原因

在 `models/openrouter.py` 的初始实现中，我计划让 OpenRouter 继承基类的 OpenAI 兼容实现，但忘记了基类中的 `ask()` 和 `prepare_request_data()` 是抽象方法（`@abstractmethod`），必须在子类中实现。

原始代码只有注释说明要继承基类实现：
```python
# OpenRouter 使用基类的默认实现（OpenAI 兼容格式）
# 继承以下方法：
# - prepare_request_data() - OpenAI 标准格式
# - ask() - OpenAI 标准实现（支持流式和非流式）
# - fetch_available_models() - GET /v1/models 端点
```

但实际上基类中这些方法是抽象的，必须实现。

---

## 修复内容

### 添加 `prepare_request_data()` 方法

```python
def prepare_request_data(self, prompt: str, **kwargs) -> Dict[str, Any]:
    """
    准备 OpenRouter API 请求数据
    
    OpenRouter 使用 OpenAI 兼容格式
    
    :param prompt: 提示文本
    :param kwargs: 其他参数，如 temperature、stream 等
    :return: 请求数据字典
    """
    translations = get_translation(self.config.get('language', 'en'))
    system_message = kwargs.get('system_message', translations.get('default_system_message', 'You are an expert in book analysis. Your task is to help users understand books better by providing insightful questions and analysis.'))
    
    data = {
        "model": self.config.get('model', self.DEFAULT_MODEL),
        "messages": [
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": kwargs.get('temperature', 0.7),
        "max_tokens": kwargs.get('max_tokens', 4096)
    }
    
    # 添加流式传输支持（只有明确指定 stream=True 才添加）
    if kwargs.get('stream', False):
        data['stream'] = True
        
    return data
```

### 添加 `ask()` 方法

完整的 `ask()` 方法实现，支持：
- ✅ 流式传输（SSE 格式）
- ✅ 非流式传输
- ✅ 错误处理
- ✅ 超时处理
- ✅ 日志记录

```python
def ask(self, prompt: str, **kwargs) -> str:
    """
    向 OpenRouter API 发送提示并获取响应
    
    :param prompt: 提示文本
    :param kwargs: 其他参数，如 temperature、stream、stream_callback 等
    :return: AI 模型的响应文本
    :raises Exception: 当请求失败时抛出异常
    """
    import json
    import requests
    import time
    
    # 检查是否使用流式传输 - 尊重显式传递的 stream 参数
    if 'stream' not in kwargs:
        kwargs['stream'] = self.config.get('enable_streaming', True)
    
    use_stream = kwargs['stream']
    stream_callback = kwargs.get('stream_callback', None)
    
    # 准备请求头和数据
    headers = self.prepare_headers()
    data = self.prepare_request_data(prompt, **kwargs)
    
    logger = logging.getLogger('calibre_plugins.ask_grok.models.openrouter')
    
    try:
        # 流式传输模式
        if use_stream and stream_callback:
            # ... 流式处理逻辑
        
        # 非流式模式
        else:
            api_url = f"{self.config['api_base_url']}/chat/completions"
            response = requests.post(
                api_url,
                headers=headers,
                json=data,
                timeout=kwargs.get('timeout', 60),
                verify=False
            )
            response.raise_for_status()
            
            result = response.json()
            if 'choices' in result and result['choices']:
                return result['choices'][0]['message']['content']
            else:
                translations = get_translation(self.config.get('language', 'en'))
                raise Exception(translations.get('invalid_response', 'Invalid API response format'))
                
    except requests.exceptions.RequestException as e:
        logger.error(f"OpenRouter API request error: {str(e)}")
        translations = get_translation(self.config.get('language', 'en'))
        raise Exception(translations.get('api_request_error', f'API request failed: {str(e)}'))
```

---

## 实现细节

### OpenAI 兼容性
OpenRouter 完全兼容 OpenAI API 格式：
- 端点：`/chat/completions`
- 请求格式：与 OpenAI 相同
- 响应格式：与 OpenAI 相同
- 流式格式：SSE（Server-Sent Events）

### 特殊请求头
OpenRouter 的 `prepare_headers()` 方法已经实现了可选的特殊请求头：
- `HTTP-Referer`: 用于在 OpenRouter 上进行排名
- `X-Title`: 应用名称标识

### 模型列表
`fetch_available_models()` 方法使用基类的默认实现：
- 端点：`GET /v1/models`
- 认证：Bearer Token
- 响应格式：OpenAI 兼容

---

## 修改文件

- `models/openrouter.py` - 添加 `prepare_request_data()` 和 `ask()` 方法（约 140 行代码）

---

## 验证步骤

1. **实例化测试**
   - OpenRouter 模型应该可以正常实例化
   - 不再出现 "Can't instantiate abstract class" 错误

2. **Load Models 功能**
   - 点击 "Load Models" 按钮
   - 应该能成功获取 OpenRouter 的模型列表
   - 模型名称应该包含前缀（如 `openai/gpt-4o`）

3. **Send 功能（非流式）**
   - 发送问题
   - 应该能收到完整的响应

4. **Send 功能（流式）**
   - 启用流式传输
   - 发送问题
   - 应该能看到逐字显示的响应

5. **Random Question 功能**
   - 点击 "Random Question" 按钮
   - 应该能生成随机问题

---

## 代码统计

| 修改 | 行数 |
|------|------|
| 添加 `prepare_request_data()` | 34 行 |
| 添加 `ask()` | 99 行 |
| **总计** | **133 行** |

---

## 相关问题

### 为什么不能真正"继承"基类实现？

Python 的抽象基类（ABC）要求所有标记为 `@abstractmethod` 的方法必须在子类中实现。即使基类有默认实现，子类也必须显式重写这些方法。

### 其他模型是否有同样的问题？

不会。其他模型（Grok, Gemini, DeepSeek, Custom, OpenAI, Anthropic, Nvidia, Ollama）都已经实现了所有必需的抽象方法。

---

## 相关文档

- `docs/DEV_PLAN_OPENROUTER_OLLAMA_2025.10.22.md` - 开发计划
- `docs/IMPLEMENTATION_COMPLETE_OPENROUTER_OLLAMA_2025.10.22.md` - 实施完成报告
- `docs/BUGFIX_CONFIG_UI_OPENROUTER_OLLAMA_2025.10.22.md` - 配置界面修复
- `models/openrouter.py` - OpenRouter 模型实现

---

**修复状态**: ✅ 已完成  
**测试状态**: ⏳ 待测试  
**文档版本**: 1.0  
**最后更新**: 2025-10-22
