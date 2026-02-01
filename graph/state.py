from typing import TypedDict, Annotated, List
from operator import add


class GraphState(TypedDict):
    """
    State cho LangGraph - bộ nhớ chia sẻ giữa các agents
    """
    # Input từ user
    problem: str
    
    # Các giải pháp từ các agent
    solver_solution: str
    alternative_solution: str
    
    # Phản biện
    critic_feedback: str
    
    # Kết quả cuối cùng
    final_decision: str
    final_reasoning: str
    
    # Metadata
    iteration: int
    messages: Annotated[List[str], add]  # Lịch sử các bước
