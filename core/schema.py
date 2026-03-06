from pydantic import BaseModel, Field
from typing import List

class TestCase(BaseModel):
    module: str = Field(description="核心功能模块")
    case_name: str = Field(description="测试用例名称与测试目的")
    priority: str = Field(description="优先级：P0, P1, P2, P3")
    preconditions: str = Field(description="前置条件，无则写无")
    steps: str = Field(description="测试执行步骤，使用序号 1,2,3... 格式化描述")
    expected_result: str = Field(description="预期明确的测试结果")

class TestCaseList(BaseModel):
    cases: List[TestCase] = Field(description="测试用例列表")
