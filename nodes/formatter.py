from core.state import TestCaseState

def run(state: TestCaseState) -> dict:
    """
    负责将最终的 JSON 内部状态格式化为人类可读的 Markdown 或者平台可导入的文件。
    """
    cases = state.get("draft_test_cases", [])
    
    markdown_output = "# 🤖 AI 测试用例汇总报告\n\n"
    markdown_output += f"> 根据 {state.get('iteration', 1)} 轮自我评审与修正生成。\n\n---\n"
    
    for i, case in enumerate(cases, 1):
        markdown_output += f"## {i}. {case.get('case_name')}\n"
        markdown_output += f"- **核心模块**: `{case.get('module')}`\n"
        markdown_output += f"- **优先级**: `{case.get('priority')}`\n"
        markdown_output += f"- **前置条件**: {case.get('preconditions')}\n"
        markdown_output += f"### 执行步骤\n{case.get('steps')}\n"
        markdown_output += f"### 预期结果\n{case.get('expected_result')}\n\n"
        markdown_output += "---\n\n"
        
    return {"final_output": markdown_output}
