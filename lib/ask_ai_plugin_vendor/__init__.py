"""
Ask AI Plugin Vendor Libraries

This package contains vendored third-party libraries to avoid conflicts with other calibre plugins.
All external dependencies are isolated in this namespace.

Vendored libraries:
- requests (2.32.3) - HTTP library for API calls
- bleach (6.2.0) - HTML sanitization
- markdown2 (2.5.3) - Markdown to HTML conversion
- urllib3 (2.3.0) - HTTP client (requests dependency)
- certifi (2025.01.31) - SSL certificates (requests dependency)
- charset_normalizer (3.4.1) - Character encoding detection (requests dependency)
- idna (3.10) - Internationalized domain names (requests dependency)
"""

__version__ = '1.0.0'

# 设置导入钩子，让 vendor 库内部的相对导入能够正常工作
import sys
import os

# 获取当前包的路径
_vendor_dir = os.path.dirname(os.path.abspath(__file__))

# 临时添加到 sys.path，仅在导入 vendor 库时使用
if _vendor_dir not in sys.path:
    sys.path.insert(0, _vendor_dir)

# 导入所有 vendor 库，确保它们被加载到正确的命名空间
from . import requests
from . import urllib3
from . import certifi
from . import charset_normalizer
from . import idna
from . import bleach
from . import markdown2

# 移除临时路径（可选，但为了完全隔离，我们保留它）
# sys.path.remove(_vendor_dir)

__all__ = ['requests', 'urllib3', 'certifi', 'charset_normalizer', 'idna', 'bleach', 'markdown2']
