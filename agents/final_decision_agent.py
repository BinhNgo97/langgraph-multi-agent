from graph.state import GraphState
from config.settings import settings


def final_decision_node(state: GraphState) -> GraphState:
    """
    Final Decision: Tổng kết cuối cùng với key points
    """
    problem = state["problem"]
    synthesizer = state.get("synthesizer_result", "")
    quality_score = state.get("quality_score", 0)
    key_points = state.get("key_points", {})
    iterations = state.get("iteration", 0)
    
    # Format key points
    pros = "\n".join([f"✅ {p}" for p in key_points.get("pros", [])])
    cons = "\n".join([f"❌ {c}" for c in key_points.get("cons", [])])
    risks = "\n".join([f"⚠️ {r}" for r in key_points.get("risks", [])])
    assumptions = "\n".join([f"📌 {a}" for a in key_points.get("assumptions", [])])
    
    final_output = f"""
# 🎯 KẾT QUẢ CUỐI CÙNG

**Điểm chất lượng:** {quality_score}/10
**Số vòng tranh luận:** {iterations + 1}

---

## 📊 KEY POINTS ĐỂ ĐÁNH GIÁ

### ✅ ƯU ĐIỂM (PROS)
{pros or "- Chưa xác định"}

### ❌ NHƯỢC ĐIỂM (CONS)
{cons or "- Chưa xác định"}

### ⚠️ RỦI RO (RISKS)
{risks or "- Chưa xác định"}

### 📌 GIẢ ĐỊNH (ASSUMPTIONS)
{assumptions or "- Chưa xác định"}

---

## 📝 PHÂN TÍCH CHI TIẾT

{synthesizer}

---

## 💡 KHUYẾN NGHỊ HÀNH ĐỘNG

Dựa trên phân tích trên, người dùng nên:
1. Đánh giá kỹ các ưu nhược điểm
2. Cân nhắc các rủi ro đã nêu
3. Kiểm chứng các giả định
4. Quyết định dựa trên mục tiêu và ngữ cảnh cụ thể của mình
"""
    
    return {
        **state,
        "final_decision": final_output,
        "final_reasoning": f"Đã tổng hợp qua {iterations + 1} vòng tranh luận với điểm {quality_score}/10",
        "messages": ["[Final Decision] Đã hoàn thành phân tích"]
    }
