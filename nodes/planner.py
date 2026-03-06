from core.state import TestCaseState
from core.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate

def run(state: TestCaseState) -> dict:
    """
    基于分析出的功能点，规划测试策略与范围 (等价类，边界值，异常注入分析等)。
    """
    llm = get_llm(temperature=0.2)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个高级测试架构师。基于下发的功能点，你需要提供一份结构化的测试策略与测试点指引。要求覆盖：等价类、边界值、可能的异常状态流转等。只返回测试策略文本，不生成具体用例。"),
        ("user", "需要测试的功能点列表:\n{features}")
    ])
    
    chain = prompt | llm
    features_text = "\n".join([f"- {feat}" for feat in state.get("parsed_features", [])])
    
    result = chain.invoke({"features": features_text})
    
    return {"test_scope": result.content}
