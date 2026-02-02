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
    st.markdown("### 🤖 Model chung")
    model_name = st.selectbox(
        "Model mặc định",
        ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        index=0,
        help="Model mặc định cho tất cả agents"
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
    
    st.divider()
    
    # Agent-specific models
    st.markdown("### 🎯 Model cho từng Agent")
    
    with st.expander("⚙️ Tùy chỉnh model cho từng agent", expanded=False):
        st.markdown("*Để trống để dùng model mặc định*")
        
        # Available models
        openai_models = ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]
        claude_models = ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229"]
        all_models = [""] + openai_models + claude_models
        
        # Input Normalizer
        normalizer_model = st.selectbox(
            "🔍 Input Normalizer",
            all_models,
            index=0,
            help="Model phân tích vấn đề đầu vào"
        )
        if normalizer_model:
            settings.agent_models["input_normalizer"] = normalizer_model
        
        # Proposer
        proposer_model = st.selectbox(
            "🔵 Proposer (AI #1)",
            all_models,
            index=0,
            help="Model đề xuất giải pháp"
        )
        if proposer_model:
            settings.agent_models["proposer"] = proposer_model
        
        # Critic
        critic_model = st.selectbox(
            "🟠 Critic (AI #2)",
            all_models,
            index=all_models.index("gpt-4o") if "gpt-4o" in all_models else 0,
            help="Model phản biện (nên dùng model mạnh)"
        )
        if critic_model:
            settings.agent_models["critic"] = critic_model
        
        # Challenger
        challenger_model = st.selectbox(
            "🟣 Challenger (AI #3)",
            all_models,
            index=all_models.index("claude-3-5-sonnet-20241022") if settings.anthropic_api_key else 0,
            help="Model tìm phản ví dụ (khuyên dùng Claude)"
        )
        if challenger_model:
            settings.agent_models["challenger"] = challenger_model
        
        # Synthesizer
        synthesizer_model = st.selectbox(
            "🟢 Synthesizer (AI #4)",
            all_models,
            index=all_models.index("gpt-4o") if "gpt-4o" in all_models else 0,
            help="Model tổng hợp (nên dùng model mạnh)"
        )
        if synthesizer_model:
            settings.agent_models["synthesizer"] = synthesizer_model
        
        # Hiển thị cấu hình hiện tại
        st.markdown("---")
        st.markdown("**Cấu hình hiện tại:**")
        for agent, model in settings.agent_models.items():
            provider = "🟦 OpenAI" if "gpt" in model.lower() else "🟣 Anthropic"
            st.text(f"{agent}: {model} ({provider})")
    
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
    
    # Hiển thị models đang dùng
    st.info(f"""
    **Model mặc định:** {model_name}  
    **Temperature:** {temperature}  
    **Max iterations:** {max_iterations}
    
    **Agent Models:**
    - Normalizer: {settings.agent_models.get('input_normalizer', 'default')}
    - Proposer: {settings.agent_models.get('proposer', 'default')}
    - Critic: {settings.agent_models.get('critic', 'default')}
    - Challenger: {settings.agent_models.get('challenger', 'default')}
    - Synthesizer: {settings.agent_models.get('synthesizer', 'default')}
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
                    "raw_problem": prompt,
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
                
                # Create containers for each agent
                normalizer_container = st.container()
                proposer_container = st.container()
                critic_container = st.container()
                challenger_container = st.container()
                synthesizer_container = st.container()
                final_container = st.container()
                
                # Run graph
                result = None
                current_iteration = 0
                for node_output in app.stream(initial_state):
                    node_name = list(node_output.keys())[0]
                    node_output = node_output[node_name]
                    iteration = node_output.get("iteration", 0)
                    
                    if node_name == "input_normalizer":
                        with normalizer_container:
                            st.markdown(f'<div class="agent-box solver-box">', unsafe_allow_html=True)
                            model_used = settings.agent_models.get("input_normalizer", "default")
                            st.markdown(f"**🔍 Input Normalizer** ({model_used})")
                            st.markdown(node_output.get("problem", ""))
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    elif node_name == "proposer":
                        with proposer_container:
                            st.markdown(f'<div class="agent-box solver-box">', unsafe_allow_html=True)
                            model_used = settings.agent_models.get("proposer", "default")
                            st.markdown(f"**🔵 AI #1: Proposer** - Vòng {iteration} ({model_used})")
                            st.markdown(node_output.get("proposer_solution", ""))
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    elif node_name == "critic":
                        with critic_container:
                            st.markdown(f'<div class="agent-box critic-box">', unsafe_allow_html=True)
                            model_used = settings.agent_models.get("critic", "default")
                            st.markdown(f"**🟠 AI #2: Critic** - Vòng {iteration} ({model_used})")
                            st.markdown(node_output.get("critic_feedback", ""))
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    elif node_name == "challenger":
                        with challenger_container:
                            st.markdown(f'<div class="agent-box alternative-box">', unsafe_allow_html=True)
                            model_used = settings.agent_models.get("challenger", "default")
                            st.markdown(f"**🟣 AI #3: Challenger** - Vòng {iteration} ({model_used})")
                            st.markdown(node_output.get("challenger_counterexample", ""))
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    elif node_name == "synthesizer":
                        score = node_output.get("quality_score", 0)
                        with synthesizer_container:
                            st.markdown(f'<div class="agent-box judge-box">', unsafe_allow_html=True)
                            model_used = settings.agent_models.get("synthesizer", "default")
                            st.markdown(f"**🟢 AI #4: Synthesizer** - Vòng {iteration} ({model_used}) - Điểm: {score}/10")
                            st.markdown(node_output.get("synthesizer_result", ""))
                            st.markdown('</div>', unsafe_allow_html=True)
                        current_iteration = iteration
                    
                    elif node_name == "final_decision":
                        with final_container:
                            st.markdown(f'<div class="agent-box judge-box">', unsafe_allow_html=True)
                            st.markdown("**🎯 Final Decision - Kết luận cuối cùng**")
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
