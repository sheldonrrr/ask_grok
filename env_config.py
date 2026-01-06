"""
Environment Configuration for Ask AI Plugin
管理测试和生产环境的配置
"""

class EnvironmentConfig:
    """
    环境配置类
    用于管理不同环境下的 API 端点和配置
    """
    
    # 当前环境: 'development' 或 'production'
    # 修改此值以切换环境
    CURRENT_ENV = 'production'
    
    # Nvidia Free 代理配置
    NVIDIA_FREE_CONFIG = {
        'development': {
            'proxy_url': 'http://localhost:8787',
            'description': 'Local development server',
        },
        'production': {
            'proxy_url': 'https://nvidia-proxy.boy-liushaopeng.workers.dev',
            'description': 'Cloudflare Worker production server',
        }
    }
    
    @classmethod
    def get_nvidia_free_proxy_url(cls) -> str:
        """
        获取当前环境的 Nvidia Free 代理 URL
        
        :return: 代理服务器 URL
        """
        return cls.NVIDIA_FREE_CONFIG[cls.CURRENT_ENV]['proxy_url']
    
    @classmethod
    def get_nvidia_free_description(cls) -> str:
        """
        获取当前环境的描述
        
        :return: 环境描述
        """
        return cls.NVIDIA_FREE_CONFIG[cls.CURRENT_ENV]['description']
    
    @classmethod
    def is_development(cls) -> bool:
        """
        检查是否为开发环境
        
        :return: True 如果是开发环境
        """
        return cls.CURRENT_ENV == 'development'
    
    @classmethod
    def is_production(cls) -> bool:
        """
        检查是否为生产环境
        
        :return: True 如果是生产环境
        """
        return cls.CURRENT_ENV == 'production'
    
    @classmethod
    def set_environment(cls, env: str):
        """
        设置当前环境
        
        :param env: 环境名称 ('development' 或 'production')
        :raises ValueError: 如果环境名称无效
        """
        if env not in ['development', 'production']:
            raise ValueError(f"Invalid environment: {env}. Must be 'development' or 'production'")
        cls.CURRENT_ENV = env
