from core.state import TestCaseState
from core.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from core.schema import TestCaseList

def run(state: TestCaseState) -> dict:
    """
    根据给定的特征和策略生成符合统一规范(Pydantic Schema)的测试用例草稿。
    """
    llm = get_llm(temperature=0.1)
    
    # 使用 Pydantic 进行约束的 Structured Output
    structured_llm = llm.with_structured_output(TestCaseList)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一名资深测试开发工程师，你的任务是根据传入的测试策略要求和功能点清单，输出标准的、可落地的软件测试用例集。\n\n历史反馈（如果有，请务必针对性修改）: {feedback}"),
        ("user", "功能点:\n{features}\n\n测试范围与策略指引:\n{test_scope}\n\n请按标准 Schema 输出。")
    ])
    
    chain = prompt | structured_llm
    
    features_text = "\n".join([f"- {feat}" for feat in state.get("parsed_features", [])])
    
    # 注入上下文进行执行
    result = chain.invoke({
        "features": features_text,
        "test_scope": state.get("test_scope", ""),
        "feedback": state.get("feedback", "（这是首次生成，无历史错误反馈）")
    })
    
    # 转换 Pydantic 对象为 dict
    draft_cases = [case.model_dump() for case in result.cases]
    current_iter = state.get("iteration", 0)
    
    return {
        "draft_test_cases": draft_cases,
        "iteration": current_iter + 1
    }
