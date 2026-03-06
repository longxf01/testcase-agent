import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from core.graph import build_graph

app = FastAPI(
    title="TestCase Generation Agent based on LangGraph",
    description="A multi-agent workflow to auto-generate standardized test cases from requirements.",
    version="1.0.0"
)

# Initialize the workflow graph globally
workflow_graph = build_graph()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/generate")
async def generate_testcases(requirement: str):
    """
    Trigger the LangGraph workflow to generate test cases.
    """
    initial_state = {
        "original_requirement": requirement,
        "iteration": 0
    }
    
    # Execute the graph
    result = workflow_graph.invoke(initial_state)
    
    return {
        "final_output": result.get("final_output"),
        "iteration": result.get("iteration")
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
