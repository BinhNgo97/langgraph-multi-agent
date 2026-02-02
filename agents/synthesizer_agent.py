from graph.state import GraphState
from config.settings import settings
import re


def synthesizer_node(state: GraphState) -> GraphState:
    """
    AI #4 - Synthesizer/Judge: Tổng hợp và đánh giá
    Sử dụng GPT-4o (model mạnh nhất)
    """
    problem = state["problem"]
    proposer = state.get("proposer_solution", "")
    critic = state.get("critic_feedback", "")
    challenger = state.get("challenger_counterexample", "")
    iteration = state.get("iteration", 0)
    
    prompt = f"""Bạn là một AI tổng hợp chuyên nghiệp, có khả năng đánh giá toàn diện.

VẤN ĐỀ:
{problem}

GIẢI PHÁP ĐỀ XUẤT:
{proposer}

PHẢN BIỆN:
{critic}

PHẢN VÍ DỤ & EDGE CASES:
{challenger}

Nhiệm vụ: Tổng hợp và đưa ra đánh giá toàn diện

1. **ĐÁNH GIÁ CHẤT LƯỢNG GIẢI PHÁP:**
   - Điểm chất lượng: [X/10]
   - Lý do cho điểm số

2. **KEY POINTS CHO NGƯỜI DÙNG:**

   **ƯU ĐIỂM (PROS):**
   - [Ưu điểm 1]
   - [Ưu điểm 2]
   - [Ưu điểm 3]

   **NHƯỢC ĐIỂM (CONS):**
   - [Nhược điểm 1]
   - [Nhược điểm 2]
   - [Nhược điểm 3]

   **RỦI RO (RISKS):**
   - [Rủi ro 1]
   - [Rủi ro 2]
   - [Rủi ro 3]

   **GIẢ ĐỊNH (ASSUMPTIONS):**
   - [Giả định 1]
   - [Giả định 2]
   - [Giả định 3]

3. **KHUYẾN NGHỊ:**
   - Nên làm gì tiếp theo
   - Cần chuẩn bị gì
   - Cách giảm thiểu rủi ro

4. **KẾT LUẬN:**
   [Có nên áp dụng giải pháp này không? Tại sao?]
"""
    
    # Sử dụng model được cấu hình cho agent này
    llm = settings.get_agent_llm("synthesizer")
    
    response = llm.invoke(prompt)
    synthesis = response.content
    
    # Extract điểm chất lượng
    quality_score = 7.0  # Default
    score_match = re.search(r'Điểm chất lượng:\s*\[?(\d+(?:\.\d+)?)/10\]?', synthesis)
    if score_match:
        quality_score = float(score_match.group(1))
    
    # Extract key points
    key_points = {
        "pros": extract_list(synthesis, "ƯU ĐIỂM"),
        "cons": extract_list(synthesis, "NHƯỢC ĐIỂM"),
        "risks": extract_list(synthesis, "RỦI RO"),
        "assumptions": extract_list(synthesis, "GIẢ ĐỊNH")
    }
    
    # Quyết định có nên tiếp tục vòng lặp không
    should_continue = quality_score < 8.0 and iteration < settings.max_iterations - 1
    
    return {
        **state,
        "synthesizer_result": synthesis,
        "quality_score": quality_score,
        "should_continue": should_continue,
        "key_points": key_points,
        "messages": [f"[Synthesizer - Vòng {iteration}] Điểm: {quality_score}/10"]
    }


def extract_list(text: str, section: str) -> list:
    """Extract bullet points from a section"""
    items = []
    # Tìm section
    pattern = rf'\*\*{section}.*?\*\*[:\s]*(.*?)(?=\*\*|\n\n|$)'
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    
    if match:
        content = match.group(1)
        # Extract các dòng bắt đầu bằng - hoặc số
        lines = re.findall(r'[-•]\s*(.+)', content)
        items = [line.strip() for line in lines if line.strip()]
    
    return items[:5]  # Giới hạn 5 items
