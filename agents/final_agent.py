from graph.state import GraphState
from config.settings import settings
from pathlib import Path


def load_prompt(filename: str) -> str:
    """Load prompt from file"""
    prompt_path = settings.prompts_dir / filename
    if prompt_path.exists():
        return prompt_path.read_text(encoding='utf-8')
    return ""


def alternative_node(state: GraphState) -> GraphState:
    """
    Agent Alternative: Đưa ra phương án thay thế dựa trên phản biện
    """
    problem = state["problem"]
    solver_solution = state.get("solver_solution", "")
    critic_feedback = state.get("critic_feedback", "")
    iteration = state.get("iteration", 0)
    
    # Load prompt template (using final.txt for now)
    prompt_template = """Bạn là một AI sáng tạo, nhiệm vụ là đưa ra phương án thay thế.

Vấn đề gốc: {problem}

Giải pháp hiện tại: {solver_solution}

Phản biện: {critic_feedback}

Dựa trên phản biện, hãy đưa ra một phương án thay thế hoàn toàn khác, giải quyết các điểm yếu đã chỉ ra.
Phương án của bạn nên:
- Khác biệt so với giải pháp ban đầu
- Giải quyết các vấn đề trong phản biện
- Có tính khả thi
- Có ưu điểm rõ ràng
"""
    
    # Get LLM
    llm = settings.get_llm()
    
    # Tạo prompt
    prompt = prompt_template.format(
        problem=problem,
        solver_solution=solver_solution,
        critic_feedback=critic_feedback
    )
    
    response = llm.invoke(prompt)
    alternative = response.content
    
    # Update state
    new_iteration = iteration + 1
    return {
        **state,
        "alternative_solution": alternative,
        "iteration": new_iteration,
        "messages": [f"[Alternative - Iteration {iteration}] Đã đưa ra phương án thay thế"]
    }


def judge_node(state: GraphState) -> GraphState:
    """
    Agent Judge: Đánh giá và quyết định giải pháp cuối cùng
    """
    problem = state["problem"]
    solver_solution = state.get("solver_solution", "")
    alternative_solution = state.get("alternative_solution", "")
    critic_feedback = state.get("critic_feedback", "")
    
    # Load prompt template
    prompt_template = load_prompt("final.txt")
    if not prompt_template:
        prompt_template = """Bạn là một AI đánh giá khách quan, nhiệm vụ là chọn giải pháp tối ưu nhất.

Vấn đề gốc: {problem}

Giải pháp A (Solver): {solver_solution}

Giải pháp B (Alternative): {alternative_solution}

Phản biện: {critic_feedback}

Hãy phân tích và đưa ra quyết định cuối cùng:
1. So sánh ưu nhược điểm của cả hai giải pháp
2. Chọn giải pháp tối ưu (hoặc kết hợp)
3. Giải thích lý do chọn
4. Đưa ra khuyến nghị thực hiện

Quyết định cuối cùng:
"""
    
    # Get LLM
    llm = settings.get_llm()
    
    # Tạo prompt
    prompt = prompt_template.format(
        problem=problem,
        solver_solution=solver_solution,
        alternative_solution=alternative_solution,
        critic_feedback=critic_feedback
    )
    
    response = llm.invoke(prompt)
    decision = response.content
    
    # Update state
    return {
        **state,
        "final_decision": decision,
        "final_reasoning": "Đã phân tích và chọn giải pháp tối ưu dựa trên các tiêu chí đánh giá",
        "messages": [f"[Judge] Đã đưa ra quyết định cuối cùng"]
    }
