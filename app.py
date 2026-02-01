"""
Streamlit UI cho LangGraph Multi-Agent System
"""

import streamlit as st
from graph.builder import build_graph
from config.settings import settings
import os

# Page config
st.set_page_config(
    page_title="LangGraph Multi-Agent System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .agent-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .solver-box {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .critic-box {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
    }
    .alternative-box {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .judge-box {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Cấu hình")
    
    # API Key
    api_key = st.text_input(
        "OpenAI API Key",
        value=settings.openai_api_key or "",
        type="password",
        help="Nhập OpenAI API key của bạn"
    )
    
    if api_key:
        settings.openai_api_key = api_key
        os.environ["OPENAI_API_KEY"] = api_key
    
    st.divider()
    
    # Model settings
    model_name = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        index=0,
        help="Chọn model OpenAI"
    )
    settings.model_name = model_name
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Độ sáng tạo của AI (0=chính xác, 1=sáng tạo)"
    )
    settings.temperature = temperature
    
    max_iterations = st.slider(
        "Số vòng lặp tối đa",
        min_value=1,
        max_value=10,
        value=5,
        help="Số lần tối đa các agents tranh luận"
    )
    settings.max_iterations = max_iterations
    
    st.divider()
    
    # Info
    st.markdown("### 📊 Thông tin")
    st.info(f"""
    **Model:** {model_name}  
    **Temperature:** {temperature}  
    **Max iterations:** {max_iterations}
    """)
    
    # Reset button
    if st.button("🔄 Reset Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []

# Main header
st.markdown('<div class="main-header">🤖 HỆ THỐNG AI ĐA TÁC TỬ</div>', unsafe_allow_html=True)
st.markdown("### Tìm giải pháp tối ưu thông qua phản biện và tranh luận")
st.divider()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Nhập vấn đề cần giải quyết..."):
    # Check API key
    if not settings.openai_api_key:
        st.error("⚠️ Vui lòng nhập OpenAI API Key ở sidebar!")
        st.stop()
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process with LangGraph
    with st.chat_message("assistant"):
        with st.spinner("🤔 Đang phân tích vấn đề..."):
            try:
                # Build graph
                app = build_graph()
                
                # Initial state
                initial_state = {
                    "problem": prompt,
                    "solver_solution": "",
                    "alternative_solution": "",
                    "critic_feedback": "",
                    "final_decision": "",
                    "final_reasoning": "",
                    "iteration": 0,
                    "messages": []
                }
                
                # Create containers for each agent
                solver_container = st.container()
                critic_container = st.container()
                alternative_container = st.container()
                judge_container = st.container()
                
                # Run graph
                result = None
                current_iteration = 0
                
                for output in app.stream(initial_state):
                    for node_name, node_output in output.items():
                        iteration = node_output.get("iteration", 0)
                        
                        if node_name == "solver":
                            with solver_container:
                                st.markdown(f'<div class="agent-box solver-box">', unsafe_allow_html=True)
                                st.markdown(f"**🔵 Solver** - Vòng {iteration}")
                                st.markdown(node_output.get("solver_solution", ""))
                                st.markdown('</div>', unsafe_allow_html=True)
                        
                        elif node_name == "critic":
                            with critic_container:
                                st.markdown(f'<div class="agent-box critic-box">', unsafe_allow_html=True)
                                st.markdown(f"**🟠 Critic** - Vòng {iteration}")
                                st.markdown(node_output.get("critic_feedback", ""))
                                st.markdown('</div>', unsafe_allow_html=True)
                        
                        elif node_name == "alternative":
                            with alternative_container:
                                st.markdown(f'<div class="agent-box alternative-box">', unsafe_allow_html=True)
                                st.markdown(f"**🟣 Alternative** - Vòng {iteration}")
                                st.markdown(node_output.get("alternative_solution", ""))
                                st.markdown('</div>', unsafe_allow_html=True)
                            current_iteration = iteration
                        
                        elif node_name == "judge":
                            with judge_container:
                                st.markdown(f'<div class="agent-box judge-box">', unsafe_allow_html=True)
                                st.markdown("**🟢 Judge - Quyết định cuối cùng**")
                                st.markdown(node_output.get("final_decision", ""))
                                st.markdown('</div>', unsafe_allow_html=True)
                            result = node_output
                
                # Summary
                if result:
                    st.divider()
                    st.success(f"✅ Hoàn thành sau {current_iteration} vòng lặp")
                    
                    # Save to history
                    st.session_state.history.append({
                        "problem": prompt,
                        "result": result.get("final_decision", ""),
                        "iterations": current_iteration
                    })
                    
                    # Add assistant message
                    response = f"""
**🎯 Kết quả cuối cùng:**

{result.get("final_decision", "")}

---
*Đã phân tích qua {current_iteration} vòng tranh luận*
"""
                    st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"❌ Lỗi: {str(e)}")
                import traceback
                with st.expander("Chi tiết lỗi"):
                    st.code(traceback.format_exc())

# Show history in expander
if st.session_state.history:
    with st.expander(f"📚 Lịch sử ({len(st.session_state.history)} câu hỏi)"):
        for i, item in enumerate(reversed(st.session_state.history)):
            st.markdown(f"**{i+1}. {item['problem']}**")
            st.markdown(f"*Số vòng lặp: {item['iterations']}*")
            st.divider()
