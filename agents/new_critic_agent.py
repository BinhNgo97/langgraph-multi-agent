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
    AI #2 - Critic: Phản biện chuyên sâu
    Sử dụng GPT-4o (mạnh hơn để phân tích sâu)
    """
    problem = state["problem"]
    solution = state.get("proposer_solution", "")
    iteration = state.get("iteration", 0)
    
    # Load prompt template
    prompt_template = load_prompt("critic.txt")
    if not prompt_template:
        prompt_template = """Bạn là một AI phản biện chuyên nghiệp với tư duy phản biện sắc bén.

VẤN ĐỀ:
{problem}

GIẢI PHÁP ĐỀ XUẤT:
{solution}

Nhiệm vụ: Phân tích kỹ lưỡng và chỉ ra:

1. **ĐIỂM YẾU CHÍNH:**
   - Lỗ hổng logic
   - Giả định chưa được chứng minh
   - Thiếu sót trong phân tích

2. **RỦI RO TIỀM ẨN:**
   - Rủi ro khi triển khai
   - Tác động phụ không mong muốn
   - Chi phí ẩn

3. **TRƯỜNG HỢP NGOẠI LỆ:**
   - Các tình huống giải pháp không hiệu quả
   - Edge cases chưa được xem xét

4. **ĐỀ XUẤT CẢI THIỆN:**
   - Hướng cải thiện cụ thể
   - Các yếu tố cần bổ sung
"""
    
    # Sử dụng GPT-4o cho phân tích sâu
    llm = settings.get_llm("openai", "gpt-4o")
    
    prompt = prompt_template.format(problem=problem, solution=solution)
    
    response = llm.invoke(prompt)
    feedback = response.content
    
    return {
        **state,
        "critic_feedback": feedback,
        "messages": [f"[Critic - Vòng {iteration}] Đã phản biện giải pháp"]
    }
