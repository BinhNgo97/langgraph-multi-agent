from typing import TypedDict, Annotated, List, Dict
from operator import add


class GraphState(TypedDict):
    """
    State cho LangGraph - bộ nhớ chia sẻ giữa các agents
    """
    # Input từ user
    raw_problem: str  # Vấn đề gốc từ user
    problem: str  # Vấn đề đã được normalize
    context: str  # Ngữ cảnh và constraints
    
    # Các giải pháp từ các agent
    proposer_solution: str  # AI #1 - Giải pháp ban đầu
    critic_feedback: str  # AI #2 - Phản biện
    challenger_counterexample: str  # AI #3 - Phản ví dụ, edge cases
    synthesizer_result: str  # AI #4 - Tổng hợp
    
    # Kết quả cuối cùng
    final_decision: str
    final_reasoning: str
    key_points: Dict[str, List[str]]  # Pros, Cons, Risks, Assumptions
    
    # Metadata
    iteration: int
    quality_score: float  # Điểm đánh giá chất lượng (0-10)
    should_continue: bool
    messages: Annotated[List[str], add]  # Lịch sử các bước
