import os
def load_config():
    '''读取模型并检查需要的变量'''
    config = {
        'LLM_API_KEY': os.getenv('LLM_API_KEY', '').strip(),
        'LLM_API_URL': os.getenv('LLM_API_URL', '').strip(),
        'LLM_MODEL_NAME': os.getenv('LLM_MODEL_NAME','').strip()
    }
    for name,value in config.items():
        if not value:
            raise ValueError(f'缺少环境变量：{name}')
    return config