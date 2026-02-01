from graph.state import GraphState
from config.settings import settings
from pathlib import Path


def load_prompt(filename: str) -> str:
    """Load prompt from file"""
    prompt_path = settings.prompts_dir / filename
    if prompt_path.exists():
        return prompt_path.read_text(encoding='utf-8')
    return ""


def solver_node(state: GraphState) -> GraphState:
    """
    Agent Solver: Đưa ra giải pháp ban đầu cho vấn đề
    """
    problem = state["problem"]
    iteration = state.get("iteration", 0)
    
    # Load prompt template
    prompt_template = load_prompt("gpt.txt")
    if not prompt_template:
        prompt_template = """Bạn là một AI giải quyết vấn đề chuyên nghiệp.

Vấn đề: {problem}

Hãy phân tích và đưa ra giải pháp chi tiết, khả thi nhất cho vấn đề trên.
Giải pháp của bạn nên:
- Rõ ràng, cụ thể
- Có tính khả thi cao
- Xem xét các ưu và nhược điểm
- Đưa ra các bước thực hiện
"""
    
    # Get LLM
    llm = settings.get_llm()
    
    # Tạo prompt
    prompt = prompt_template.format(problem=problem)
    
    # Lấy phản hồi
    if iteration > 0 and state.get("critic_feedback"):
        prompt += f"\n\nPhản biện từ vòng trước: {state['critic_feedback']}"
        prompt += f"\n\nHãy cải thiện giải pháp dựa trên phản biện này."
    
    response = llm.invoke(prompt)
    solution = response.content
    
    # Update state
    return {
        **state,
        "solver_solution": solution,
        "iteration": iteration,
        "messages": [f"[Solver - Iteration {iteration}] Đã đưa ra giải pháp"]
    }
