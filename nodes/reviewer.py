from core.state import TestCaseState
from core.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class ReviewResult(BaseModel):
    feedback: str = Field(description="详细的评审建议。如果存在用例遗漏、步骤不清晰或边界未覆盖，以 '修改' 或 '补充' 开头指出问题所在。如果全部完美符合预期且涵盖了所有场景，请仅回复 '通过'。")

def run(state: TestCaseState) -> dict:
    """
    扮演挑剔的专家，审查生成的用例草稿是否满足所有的边界和异常预期，并给出改写建议。
    """
    llm = get_llm(temperature=0.1)
    structured_llm = llm.with_structured_output(ReviewResult)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一名严苛的 QA 测试把关专家。请评审下面的草稿测试用例是否完全覆盖了原始的业务需求，尤其要关注遗漏的异常边界和特殊流转。如果没有问题，回复'通过'。否则，给出'补充...'或者'修改...'开头的修改指令。"),
        ("user", "原始需求:\n{requirement}\n\n目前生成的测试用例草稿:\n{draft_cases}")
    ])
    
    chain = prompt | structured_llm
    
    # 转化用例格式方便 LLM 阅览
    draft_snapshot = ""
    for idx, c in enumerate(state.get("draft_test_cases", [])):
        draft_snapshot += f"{idx+1}. [{c['module']} - {c['priority']}] {c['case_name']}\n"
    
    result = chain.invoke({
        "requirement": state.get("original_requirement", ""),
        "draft_cases": draft_snapshot
    })
    
    print(f"[Reviewer Agent] 评审意见：{result.feedback}")
    
    return {"feedback": result.feedback}
