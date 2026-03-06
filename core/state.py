from typing import TypedDict, List
from typing_extensions import NotRequired

class TestCaseState(TypedDict):
    original_requirement: str                # 原始需求输入
    parsed_features: NotRequired[List[str]]  # 提取出的核心业务流/功能点
    test_scope: NotRequired[str]             # 测试策略与范围描述（边界值、等价类等提示）
    draft_test_cases: NotRequired[List[dict]]# AI生成的草稿用例集
    feedback: NotRequired[str]               # Reviewer的评审反馈意见
    iteration: int                           # 当前循环/自我纠错的次数，防止死循环
    final_output: NotRequired[str]           # 最终格式化交付的测试用例文件或字符串
