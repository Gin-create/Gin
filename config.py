# 服务器配置文件
SERVER_CONFIG = {
    'servers': [
        {'name': '本地服务器', 'url': 'http://127.0.0.1:5000'},
        {'name': '测试服务器1', 'url': 'http://192.168.1.100:5000'},
        {'name': '测试服务器2', 'url': 'http://192.168.1.101:5000'}
    ],
    'secret_key': 'your-secret-key-here',
    'debug': True
}

# AI模型配置
AI_CONFIG = {
    'api_key': 'sk-orxlsmelhexcosqumhchsiabeasxhwkmvcfzqqjakwhqoaqv',
    'model_name': 'Qwen/Qwen2.5-7B-Instruct',
    'api_url': 'https://api.siliconflow.cn/v1/',
    'ai_username': '伯小爵'  # AI用户名称，用于@功能识别
}