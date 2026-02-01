from langgraph.graph import StateGraph, END
from graph.state import GraphState
from agents.input_normalizer import input_normalizer_node
from agents.proposer_agent import proposer_node
from agents.new_critic_agent import critic_node
from agents.challenger_agent import challenger_node
from agents.synthesizer_agent import synthesizer_node
from agents.final_decision_agent import final_decision_node


def should_continue_loop(state: GraphState) -> str:
    """
    Quyết định có tiếp tục vòng lặp tranh luận không
    Dựa trên quality_score và số lần lặp
    """
    should_continue = state.get("should_continue", False)
    quality_score = state.get("quality_score", 0)
    iteration = state.get("iteration", 0)
    
    # Nếu chất lượng đủ tốt (>= 8.0) hoặc đã đủ số vòng
    if not should_continue or quality_score >= 8.0 or iteration >= 4:
        return "finalize"
    
    # Tiếp tục vòng lặp
    return "continue"


def build_graph():
    """
    Xây dựng LangGraph workflow mới
    
    Flow:
    1. Input Normalizer: Làm rõ vấn đề
    2. Proposer (GPT-4o-mini): Đưa ra giải pháp
    3. Critic (GPT-4o): Phản biện
    4. Challenger (Claude/GPT): Tìm phản ví dụ
    5. Synthesizer (GPT-4o): Tổng hợp và đánh giá
    6. Loop nếu chưa đủ tốt (quality_score < 8.0)
    7. Final Decision: Kết luận với key points
    """
    
    # Khởi tạo graph
    workflow = StateGraph(GraphState)
    
    # Thêm các nodes (agents)
    workflow.add_node("input_normalizer", input_normalizer_node)
    workflow.add_node("proposer", proposer_node)
    workflow.add_node("critic", critic_node)
    workflow.add_node("challenger", challenger_node)
    workflow.add_node("synthesizer", synthesizer_node)
    workflow.add_node("final_decision", final_decision_node)
    
    # Định nghĩa edges (luồng chạy)
    workflow.set_entry_point("input_normalizer")
    
    # Input Normalizer -> Proposer
    workflow.add_edge("input_normalizer", "proposer")
    
    # Proposer -> Critic
    workflow.add_edge("proposer", "critic")
    
    # Critic -> Challenger
    workflow.add_edge("critic", "challenger")
    
    # Challenger -> Synthesizer
    workflow.add_edge("challenger", "synthesizer")
    
    # Synthesizer -> Continue hoặc Finalize
    workflow.add_conditional_edges(
        "synthesizer",
        should_continue_loop,
        {
            "continue": "proposer",  # Quay lại proposer để cải thiện
            "finalize": "final_decision"
        }
    )
    
    # Final Decision -> END
    workflow.add_edge("final_decision", END)
    
    # Compile graph
    app = workflow.compile()
    
    return app
