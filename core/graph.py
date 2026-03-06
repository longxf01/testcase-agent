from langgraph.graph import StateGraph, END
from core.state import TestCaseState
from nodes import analyzer, planner, generator, reviewer, formatter

def build_graph():
    """
    组装多 Agent 测试用例生成流水线图
    """
    builder = StateGraph(TestCaseState)
    
    # 1. 注册工作流节点 (Nodes)
    builder.add_node("Analyzer", analyzer.run)      # 需求分析节点
    builder.add_node("Planner", planner.run)        # 测试策略规划节点
    builder.add_node("Generator", generator.run)    # 核心编写用例节点
    builder.add_node("Reviewer", reviewer.run)      # QA 校验纠错节点
    builder.add_node("Formatter", formatter.run)    # 导出组装节点
    
    # 2. 编排基础顺序控制边 (Edges)
    builder.set_entry_point("Analyzer")
    builder.add_edge("Analyzer", "Planner")
    builder.add_edge("Planner", "Generator")
    builder.add_edge("Generator", "Reviewer")
    
    # 3. 编排核心条件判断边：自我纠错机制 (Conditional Edges)
    def should_continue(state: TestCaseState) -> str:
        iteration = state.get("iteration", 0)
        feedback = state.get("feedback", "")
        
        # 防止无限循环的兜底
        if iteration >= 3:
            return "Formatter"
            
        # 根据评审意见判断是否重做
        if "修改" in feedback or "补充" in feedback:
            return "Generator"
            
        return "Formatter"
        
    builder.add_conditional_edges("Reviewer", should_continue)
    builder.add_edge("Formatter", END)
    
    return builder.compile()
