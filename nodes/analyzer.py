from core.state import TestCaseState
from core.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List

class ExtractedFeatures(BaseModel):
    features: List[str] = Field(description="提取的核心功能点、业务流、以及隐含的需求约束")

def run(state: TestCaseState) -> dict:
    """
    分析原始需求，拆解提取出需要进行测试的功能点列表。
    """
    llm = get_llm(temperature=0.1)
    structured_llm = llm.with_structured_output(ExtractedFeatures)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个资深的需求分析师产品经理。你的主要职责是从用户的原始需求描述或 PRD 中，提取出具体需要开发与测试的核心功能点清单。注意挖掘异常场景的暗示。"),
        ("user", "原始需求如下:\n{requirement}")
    ])
    
    chain = prompt | structured_llm
    result = chain.invoke({"requirement": state.get("original_requirement", "")})
    
    return {"parsed_features": result.features}
