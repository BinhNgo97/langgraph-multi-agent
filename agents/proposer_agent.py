from graph.state import GraphState
from config.settings import settings
from pathlib import Path


def load_prompt(filename: str) -> str:
    """Load prompt from file"""
    prompt_path = settings.prompts_dir / filename
    if prompt_path.exists():
        return prompt_path.read_text(encoding='utf-8')
    return ""


def proposer_node(state: GraphState) -> GraphState:
    """
    AI #1 - Proposer: Đưa ra giải pháp ban đầu
    Sử dụng GPT-4o-mini
    """
    problem = state["problem"]
    context = state.get("context", "")
    iteration = state.get("iteration", 0)
    
    # Load prompt template
    prompt_template = load_prompt("proposer.txt")
    if not prompt_template:
        prompt_template = """Bạn là một AI chuyên gia giải quyết vấn đề sáng tạo.

{context}

Nhiệm vụ: Đưa ra giải pháp chi tiết, khả thi và sáng tạo nhất.

Giải pháp của bạn phải:
- Rõ ràng, cụ thể, có tính thực tế
- Có các bước thực hiện chi tiết
- Xem xét ưu nhược điểm
- Dự đoán kết quả
- Đề xuất cách đo lường thành công
"""
    
    # Sử dụng model được cấu hình cho agent này
    llm = settings.get_agent_llm("proposer")
    
    prompt = prompt_template.format(context=context)
    
    # Nếu là vòng lặp tiếp theo, thêm feedback
    if iteration > 0:
        critic = state.get("critic_feedback", "")
        challenger = state.get("challenger_counterexample", "")
        prompt += f"\n\n**PHẢN BIỆN TỪ VÒNG TRƯỚC:**\n{critic}"
        prompt += f"\n\n**PHẢN VÍ DỤ TỪ VÒNG TRƯỚC:**\n{challenger}"
        prompt += "\n\nHãy cải thiện giải pháp dựa trên các phản hồi trên."
    
    response = llm.invoke(prompt)
    solution = response.content
    
    return {
        **state,
        "proposer_solution": solution,
        "iteration": iteration,
        "messages": [f"[Proposer - Vòng {iteration}] Đã đưa ra giải pháp"]
    }
