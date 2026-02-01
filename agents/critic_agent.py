from graph.state import GraphState
from config.settings import settings
from pathlib import Path


def load_prompt(filename: str) -> str:
    """Load prompt from file"""
    prompt_path = settings.prompts_dir / filename
    if prompt_path.exists():
        return prompt_path.read_text(encoding='utf-8')
    return ""


def critic_node(state: GraphState) -> GraphState:
    """
    Agent Critic: Phản biện giải pháp hiện tại
    """
    problem = state["problem"]
    solution = state.get("solver_solution", "")
    alternative = state.get("alternative_solution", "")
    iteration = state.get("iteration", 0)
    
    # Load prompt template
    prompt_template = load_prompt("critic.txt")
    if not prompt_template:
        prompt_template = """Bạn là một AI phản biện chuyên nghiệp, nhiệm vụ là tìm ra các lỗ hổng, điểm yếu trong giải pháp.

Vấn đề gốc: {problem}

Giải pháp hiện tại: {solution}

Hãy phân tích chỉ trích giải pháp này:
- Những điểm yếu, thiếu sót
- Rủi ro tiềm ẩn
- Các trường hợp ngoại lệ chưa xét đến
- Đề xuất hướng cải thiện

Hãy phản biện mang tính xây dựng, giúp cải thiện giải pháp.
"""
    
    # Get LLM
    llm = settings.get_llm()
    
    # Tạo prompt
    prompt = prompt_template.format(problem=problem, solution=solution)
    
    if alternative:
        prompt += f"\n\nPhương án thay thế: {alternative}"
        prompt += "\n\nHãy so sánh cả hai phương án và chỉ ra ưu nhược điểm."
    
    response = llm.invoke(prompt)
    feedback = response.content
    
    # Update state
    return {
        **state,
        "critic_feedback": feedback,
        "messages": [f"[Critic - Iteration {iteration}] Đã phản biện giải pháp"]
    }
