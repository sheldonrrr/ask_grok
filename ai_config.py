import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from i18n import get_translation
from config import get_prefs
from PyQt5.QtWidgets import (QFrame, QLabel, QLineEdit)
from PyQt5.QtCore import Qt

def create_config_section(parent, i18n, layout, config_type):
    """创建AI配置区域的通用函数"""
    # 获取配置前缀
    prefix = f"{config_type}_" if config_type != 'xai' else ''
    display_name = 'X.AI' if config_type == 'xai' else 'Gemini'
    
    # 分割线
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Sunken)
    layout.addWidget(line)
    
    # 标题
    title = QLabel(f"{display_name} 配置")
    title.setStyleSheet("font-weight: bold; margin-top: 10px;")
    layout.addWidget(title)
    
    if config_type == 'xai':
        # X.AI 特有配置
        token_label = QLabel(i18n['token_label'])
        layout.addWidget(token_label)
        
        token_edit = QLineEdit(parent)
        token_edit.setText(get_prefs().get('auth_token', ''))
        token_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(token_edit)
        
        # API Base URL
        url_label = QLabel(i18n['base_url_label'])
        layout.addWidget(url_label)
        
        url_edit = QLineEdit(parent)
        url_edit.setText(get_prefs().get('api_base_url', 'https://api.x.ai/v1'))
        layout.addWidget(url_edit)
        
        # 模型
        model_label = QLabel(i18n['model_label'])
        layout.addWidget(model_label)
        
        model_edit = QLineEdit(parent)
        model_edit.setText(get_prefs().get('model', 'grok-3-latest'))
        layout.addWidget(model_edit)
        
        # 保存到父对象
        parent.auth_token_edit = token_edit
        parent.api_base_url_edit = url_edit
        parent.model_edit = model_edit
        
    else:  # Gemini 配置
        # API 密钥
        key_label = QLabel("Gemini API 密钥:")
        layout.addWidget(key_label)
        
        key_edit = QLineEdit(parent)
        key_edit.setText(get_prefs().get('gemini_auth_token', ''))
        key_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(key_edit)
        
        # 模型
        model_label = QLabel("模型:")
        layout.addWidget(model_label)
        
        model_edit = QLineEdit(parent)
        model_edit.setText(get_prefs().get('gemini_model', 'gemini-2.0-flash'))
        layout.addWidget(model_edit)
        
        # 保存到父对象
        parent.gemini_auth_token_edit = key_edit
        parent.gemini_model_edit = model_edit

def ai_config(parent):
    """
    创建AI配置界面
    
    Args:
        parent: 父窗口对象
    """
    # 创建布局
    layout = QVBoxLayout()
    
    # 添加X.AI配置
    create_config_section(parent, parent.i18n, layout, 'xai')
    
    # 添加Gemini配置
    create_config_section(parent, parent.i18n, layout, 'gemini')
    
    # 将布局添加到父布局
    parent.layout().addLayout(layout)
    
    # 初始显示/隐藏配置
    def update_visibility():
        is_xai = parent.ai_combo.currentData() == 'xai'
        for widget in [parent.xai_token_edit, parent.xai_base_url_edit, parent.xai_model_edit]:
            widget.setVisible(is_xai)
        for widget in [parent.gemini_token_edit, parent.gemini_base_url_edit, parent.gemini_model_edit]:
            widget.setVisible(not is_xai)
    
    # 连接信号
    parent.ai_combo.currentIndexChanged.connect(update_visibility)
    update_visibility()  # 初始更新