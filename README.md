# 🤖 LangGraph Multi-Agent System

Hệ thống AI đa tác tử sử dụng LangGraph để giải quyết vấn đề phức tạp thông qua phản biện và tranh luận.

## 📋 Mô tả

Hệ thống này sử dụng kiến trúc graph-based với nhiều AI agents:
- **Solver**: Đưa ra giải pháp ban đầu
- **Critic**: Phản biện và tìm điểm yếu
- **Alternative**: Đưa ra phương án thay thế
- **Judge**: Đánh giá và chọn giải pháp tối ưu

## 🏗️ Kiến trúc

```
        ┌── Critic ──┐
        │             ↓
Solver ─┤           Judge ─→ End
        │             ↑
        └── Alternative ─┘
```

## 📁 Cấu trúc thư mục

```
lg_graph/
├─ .venv/                     # Virtual environment
├─ main.py                    # Entry point
├─ graph/
│   ├─ __init__.py
│   ├─ state.py               # Graph state definition
│   └─ builder.py             # Graph builder
├─ agents/
│   ├─ __init__.py
│   ├─ gpt_agent.py           # Solver agent
│   ├─ critic_agent.py        # Critic agent
│   └─ final_agent.py         # Alternative & Judge agents
├─ config/
│   ├─ __init__.py
│   └─ settings.py            # Configuration
├─ prompts/
│   ├─ gpt.txt                # Solver prompt
│   ├─ critic.txt             # Critic prompt
│   └─ final.txt              # Judge prompt
├─ requirements.txt
└─ README.md
```

## 🚀 Cài đặt

### 1. Tạo virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình API key

Tạo file `.env` từ `.env.example`:

```bash
copy .env.example .env
```

Chỉnh sửa `.env` và thêm OpenAI API key:

```
OPENAI_API_KEY=sk-your-api-key-here
MODEL_NAME=gpt-4
TEMPERATURE=0.7
```

## 💻 Sử dụng

### Chạy với ví dụ mặc định:

```bash
python main.py
```

### Chạy với vấn đề cụ thể:

```bash
python main.py "Làm thế nào để cải thiện hiệu suất của ứng dụng web?"
```

### Hoặc nhập trực tiếp khi chương trình chạy:

```bash
python main.py
> Nhập vấn đề của bạn...
```

## 🔄 Quy trình hoạt động

1. **Input**: Người dùng đưa ra vấn đề
2. **Solver**: AI phân tích và đưa ra giải pháp ban đầu
3. **Critic**: AI phản biện, tìm điểm yếu
4. **Alternative**: Đưa ra phương án thay thế dựa trên phản biện
5. **Loop**: Lặp lại bước 2-4 (tối đa 5 vòng)
6. **Judge**: Đánh giá và chọn giải pháp tối ưu
7. **Output**: Kết quả cuối cùng

## ⚙️ Tùy chỉnh

### Thay đổi số vòng lặp tối đa

Chỉnh sửa [config/settings.py](config/settings.py):

```python
self.max_iterations = 5  # Thay đổi số này
```

### Tùy chỉnh prompt

Chỉnh sửa các file trong thư mục `prompts/`:
- `gpt.txt`: Prompt cho Solver
- `critic.txt`: Prompt cho Critic
- `final.txt`: Prompt cho Judge

### Sử dụng model khác

Chỉnh sửa `.env`:

```
MODEL_NAME=gpt-3.5-turbo
# hoặc
MODEL_NAME=gpt-4-turbo
```

## 📊 Ví dụ Output

```
🤖 HỆ THỐNG AI ĐA TÁC TỬ - LANGGRAPH
======================================================================
❓ VẤN ĐỀ: Làm thế nào để tăng năng suất team?

📍 [SOLVER - Vòng 0]
Giải pháp: Áp dụng phương pháp Agile...

📍 [CRITIC - Vòng 0]
Phản biện: Giải pháp này có thể gặp vấn đề với...

📍 [ALTERNATIVE - Vòng 0]
Phương án thay thế: Thay vì Agile thuần túy...

📍 [JUDGE]
🎯 Quyết định: Kết hợp cả hai phương pháp...
```

## 🛠️ Troubleshooting

### Lỗi API key

```
⚠️  OPENAI_API_KEY chưa được cấu hình!
```
→ Kiểm tra file `.env` và đảm bảo API key đúng

### Lỗi import module

```
ModuleNotFoundError: No module named 'langgraph'
```
→ Chạy: `pip install -r requirements.txt`

## 📝 License

MIT License

## 👥 Tác giả

Hệ thống AI Multi-Agent với LangGraph

---

💡 **Tips**: Hãy thử với các vấn đề phức tạp để thấy sức mạnh của hệ thống phản biện!
