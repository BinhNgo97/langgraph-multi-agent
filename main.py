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
    print("🔄 Đang khởi tạo hệ thống...")
    app = build_graph()
    
    # Khởi tạo state
    initial_state = {
        "problem": problem,
        "solver_solution": "",
        "alternative_solution": "",
        "critic_feedback": "",
        "final_decision": "",
        "final_reasoning": "",
        "iteration": 0,
        "messages": []
    }
    
    # Chạy graph
    print("✅ Bắt đầu phân tích...\n")
    
    try:
        # Invoke graph và theo dõi từng bước
        result = None
        for output in app.stream(initial_state):
            for node_name, node_output in output.items():
                iteration = node_output.get("iteration", 0)
                
                if node_name == "solver":
                    print_step("Solver - Đưa ra giải pháp", 
                              node_output.get("solver_solution", ""), 
                              iteration)
                
                elif node_name == "critic":
                    print_step("Critic - Phản biện", 
                              node_output.get("critic_feedback", ""), 
                              iteration)
                
                elif node_name == "alternative":
                    print_step("Alternative - Phương án thay thế", 
                              node_output.get("alternative_solution", ""), 
                              iteration)
                
                elif node_name == "judge":
                    print_step("Judge - Quyết định cuối cùng", 
                              node_output.get("final_decision", ""))
                    result = node_output
        
        # In kết quả cuối cùng
        if result and result.get("final_decision"):
            print("\n" + "=" * 70)
            print("🎯 KẾT QUẢ CUỐI CÙNG")
            print("=" * 70)
            print(result["final_decision"])
            print("=" * 70)
            print(f"\n✅ Hoàn thành sau {result.get('iteration', 0)} vòng lặp")
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
