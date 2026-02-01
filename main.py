"""
LangGraph Multi-Agent System
Hệ thống AI đa tác tử để giải quyết vấn đề phức tạp
"""

from graph.builder import build_graph
from graph.state import GraphState
from config.settings import settings
import sys


def print_header():
    """In header của ứng dụng"""
    print("=" * 70)
    print("🤖 HỆ THỐNG AI ĐA TÁC TỬ - LANGGRAPH")
    print("=" * 70)
    print("Mục tiêu: Tìm giải pháp tối ưu thông qua phản biện và tranh luận")
    print("=" * 70)
    print()


def print_step(step_name: str, content: str, iteration: int = 0):
    """In kết quả từng bước"""
    print(f"\n{'─' * 70}")
    print(f"📍 [{step_name.upper()}]" + (f" - Vòng {iteration}" if iteration > 0 else ""))
    print(f"{'─' * 70}")
    print(content)
    print()


def run_graph(problem: str):
    """
    Chạy LangGraph với vấn đề đầu vào
    """
    print_header()
    print(f"❓ VẤN ĐỀ CẦN GIẢI QUYẾT:")
    print(f"   {problem}")
    print()
    
    # Build graph
    print("🔄 Đang khởi tạo hệ thống AI đa tác tử...")
    app = build_graph()
    
    # Khởi tạo state
    initial_state = {
        "raw_problem": problem,
        "problem": "",
        "context": "",
        "proposer_solution": "",
        "critic_feedback": "",
        "challenger_counterexample": "",
        "synthesizer_result": "",
        "final_decision": "",
        "final_reasoning": "",
        "key_points": {},
        "iteration": 0,
        "quality_score": 0.0,
        "should_continue": True,
        "messages": []
    }
    
    # Chạy graph
    print("✅ Bắt đầu phân tích với 4 AI agents...\n")
    
    try:
        # Invoke graph và theo dõi từng bước
        result = None
        for output in app.stream(initial_state):
            for node_name, node_output in output.items():
                iteration = node_output.get("iteration", 0)
                
                if node_name == "input_normalizer":
                    print_step("Input Normalizer - Phân tích vấn đề", 
                              node_output.get("problem", "")[:500] + "...")
                
                elif node_name == "proposer":
                    print_step("AI #1: Proposer - Đề xuất giải pháp", 
                              node_output.get("proposer_solution", ""), 
                              iteration)
                
                elif node_name == "critic":
                    print_step("AI #2: Critic - Phản biện", 
                              node_output.get("critic_feedback", ""), 
                              iteration)
                
                elif node_name == "challenger":
                    print_step("AI #3: Challenger - Phản ví dụ", 
                              node_output.get("challenger_counterexample", ""), 
                              iteration)
                
                elif node_name == "synthesizer":
                    score = node_output.get("quality_score", 0)
                    print_step(f"AI #4: Synthesizer - Tổng hợp (Điểm: {score}/10)", 
                              node_output.get("synthesizer_result", "")[:500] + "...", 
                              iteration)
                
                elif node_name == "final_decision":
                    print_step("Final Decision - Kết luận cuối cùng", 
                              node_output.get("final_decision", ""))
                    result = node_output
        
        # In kết quả cuối cùng
        if result:
            print("\n" + "=" * 70)
            print("✅ Hoàn thành phân tích")
            print("=" * 70)
            print()
        
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """Entry point của ứng dụng"""
    
    # Kiểm tra API key
    if not settings.openai_api_key:
        print("⚠️  Cảnh báo: OPENAI_API_KEY chưa được cấu hình!")
        print("Vui lòng:")
        print("1. Tạo file .env từ .env.example")
        print("2. Thêm API key của bạn vào file .env")
        print()
        
        # Cho phép nhập tạm thời
        api_key = input("Hoặc nhập OpenAI API key tạm thời (Enter để bỏ qua): ").strip()
        if api_key:
            settings.openai_api_key = api_key
        else:
            print("❌ Không thể chạy mà không có API key!")
            return
    
    # Lấy vấn đề từ command line hoặc input
    if len(sys.argv) > 1:
        problem = " ".join(sys.argv[1:])
    else:
        print("Nhập vấn đề cần giải quyết (hoặc Enter để dùng ví dụ):")
        problem = input("> ").strip()
        
        if not problem:
            problem = "Làm thế nào để tăng năng suất làm việc cho team phát triển phần mềm?"
            print(f"📝 Sử dụng ví dụ: {problem}\n")
    
    # Chạy graph
    run_graph(problem)


if __name__ == "__main__":
    main()
