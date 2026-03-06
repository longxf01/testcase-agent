import os
from langchain_openai import ChatOpenAI

def get_llm(temperature: float = 0.1) -> ChatOpenAI:
    """
    统一提供给各节点的 LLM 实例（目前配置为对接阿里云 DashScope 的千问模型）。
    需要在 .env 或环境变量中提供: 
    DASHSCOPE_API_KEY
    """
    # 优先读取 DASHSCOPE_API_KEY，如果没有则退化为 OPENAI_API_KEY
    api_key = os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY", "")
    
    # 千问通过通义千问兼容的 OpenAI endpoint 访问
    base_url = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    
    # 默认使用 qwen-max 或者根据环境变量来
    model_name = os.getenv("LLM_MODEL", "qwen-max")
    
    return ChatOpenAI(
        api_key=api_key,
        base_url=base_url,
        model=model_name,
        temperature=temperature
    )
