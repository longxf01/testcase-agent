import os

def load_requirement_doc(file_path: str) -> str:
    """
    从本地 Markdown、txt 或通过 API 解析在线文档 (Confluence等)。
    用于在正式工程里替代硬编码的字符串需求。
    """
    if not os.path.exists(file_path):
        return ""
        
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
