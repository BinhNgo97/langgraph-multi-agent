from graph.state import GraphState
from config.settings import settings


def input_normalizer_node(state: GraphState) -> GraphState:
    """
    Input Normalizer: Làm rõ vấn đề, chuẩn hóa ngữ cảnh
    """
    raw_problem = state["raw_problem"]
    
    # Sử dụng model được cấu hình cho agent này
    llm = settings.get_agent_llm("input_normalizer")
    
    prompt = f"""Bạn là một chuyên gia phân tích vấn đề. Nhiệm vụ của bạn là làm rõ và chuẩn hóa vấn đề từ người dùng.

Vấn đề gốc từ người dùng:
{raw_problem}

Hãy thực hiện:
1. Phân tích và làm rõ vấn đề chính
2. Xác định các yếu tố quan trọng
3. Bổ sung ngữ cảnh cần thiết
4. Liệt kê các ràng buộc (constraints) tiềm ẩn
5. Định nghĩa tiêu chí thành công

Kết quả trả về theo format:

**VẤN ĐỀ CHÍNH:**
[Mô tả rõ ràng vấn đề]

**YẾU TỐ QUAN TRỌNG:**
- [Yếu tố 1]
- [Yếu tố 2]
...

**RÀNG BUỘC & GIỚI HẠN:**
- [Ràng buộc 1]
- [Ràng buộc 2]
...

**TIÊU CHÍ THÀNH CÔNG:**
- [Tiêu chí 1]
- [Tiêu chí 2]
...
"""
    
    response = llm.invoke(prompt)
    normalized = response.content
    
    return {
        **state,
        "problem": normalized,
        "context": normalized,
        "messages": ["[Input Normalizer] Đã phân tích và làm rõ vấn đề"]
    }
