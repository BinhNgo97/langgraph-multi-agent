from graph.state import GraphState
from config.settings import settings


def challenger_node(state: GraphState) -> GraphState:
    """
    AI #3 - Challenger: Tìm phản ví dụ và edge cases
    Sử dụng Claude (góc nhìn khác biệt)
    """
    problem = state["problem"]
    solution = state.get("proposer_solution", "")
    critic = state.get("critic_feedback", "")
    iteration = state.get("iteration", 0)
    
    prompt = f"""Bạn là một AI tư duy phản biện với khả năng tìm ra các trường hợp ngoại lệ.

VẤN ĐỀ:
{problem}

GIẢI PHÁP ĐỀ XUẤT:
{solution}

PHẢN BIỆN:
{critic}

Nhiệm vụ của bạn: Tìm các PHẢN VÍ DỤ và EDGE CASES

1. **PHẢN VÍ DỤ CỤ THỂ:**
   - Các tình huống thực tế mà giải pháp này THẤT BẠI
   - Ví dụ minh họa cụ thể
   - Dữ liệu hoặc nghiên cứu ủng hộ (nếu có)

2. **EDGE CASES QUAN TRỌNG:**
   - Các trường hợp biên giới
   - Điều kiện đặc biệt chưa được xét đến
   - Các yếu tố môi trường ảnh hưởng

3. **NHỮNG GÌ CÓ THỂ SAI:**
   - Worst-case scenarios
   - Các giả định dễ vỡ
   - Dependencies nguy hiểm

4. **KIỂM CHỨNG CẦN THIẾT:**
   - Cần test/validate gì trước khi triển khai
   - Các chỉ số cảnh báo sớm
"""
    
    # Sử dụng model được cấu hình cho agent này (mặc định: Claude)
    try:
        llm = settings.get_agent_llm("challenger")
    except ValueError as e:
        # Nếu không có API key Claude, fallback sang GPT
        print(f"Warning: {e}. Falling back to GPT-4o-mini")
        llm = settings.get_llm("openai", "gpt-4o-mini")
    
    response = llm.invoke(prompt)
    counterexample = response.content
    
    return {
        **state,
        "challenger_counterexample": counterexample,
        "messages": [f"[Challenger - Vòng {iteration}] Đã tìm phản ví dụ và edge cases"]
    }
