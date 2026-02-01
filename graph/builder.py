from langgraph.graph import StateGraph, END
from graph.state import GraphState
from agents.gpt_agent import solver_node
from agents.critic_agent import critic_node
from agents.final_agent import alternative_node, judge_node


def should_continue(state: GraphState) -> str:
    """
    Quyết định xem có tiếp tục vòng lặp không
    """
    iteration = state.get("iteration", 0)
    
    # Nếu có final_decision rồi thì kết thúc
    if state.get("final_decision"):
        return "end"
    
    # Giới hạn số lần lặp
    if iteration >= 5:
        return "judge"
    
    # Tiếp tục vòng phản biện
    return "continue"


def build_graph():
    """
    Xây dựng LangGraph workflow
    
    Flow:
    1. Solver: Đưa ra giải pháp ban đầu
    2. Critic: Phản biện giải pháp
    3. Alternative: Đưa ra phương án thay thế
    4. Judge: Đánh giá và chọn giải pháp tối ưu
    """
    
    # Khởi tạo graph
    workflow = StateGraph(GraphState)
    
    # Thêm các nodes (agents)
    workflow.add_node("solver", solver_node)
    workflow.add_node("critic", critic_node)
    workflow.add_node("alternative", alternative_node)
    workflow.add_node("judge", judge_node)
    
    # Định nghĩa edges (luồng chạy)
    workflow.set_entry_point("solver")
    
    # Solver -> Critic
    workflow.add_edge("solver", "critic")
    
    # Critic -> Alternative
    workflow.add_edge("critic", "alternative")
    
    # Alternative -> Judge (hoặc tiếp tục)
    workflow.add_conditional_edges(
        "alternative",
        should_continue,
        {
            "continue": "critic",  # Quay lại vòng phản biện
            "judge": "judge",       # Đi đến judge để kết thúc
            "end": END
        }
    )
    
    # Judge -> END
    workflow.add_edge("judge", END)
    
    # Compile graph
    app = workflow.compile()
    
    return app
