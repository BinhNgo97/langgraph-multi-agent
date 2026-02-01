# 🚀 Hướng dẫn chạy UI Streamlit

## Bước 1: Cài đặt Streamlit

```powershell
pip install streamlit
```

## Bước 2: Chạy ứng dụng

```powershell
streamlit run app.py
```

## Bước 3: Mở trình duyệt

Ứng dụng sẽ tự động mở tại:
- **Local URL:** http://localhost:8501
- **Network URL:** http://192.168.x.x:8501

## 🎨 Tính năng UI

### Sidebar (Bên trái)
- ✅ Nhập OpenAI API Key
- ✅ Chọn model (gpt-4o-mini, gpt-4o, gpt-3.5-turbo...)
- ✅ Điều chỉnh Temperature (độ sáng tạo)
- ✅ Cài đặt số vòng lặp tối đa
- ✅ Nút Reset chat

### Main Chat
- ✅ Giao diện chat thân thiện
- ✅ Hiển thị từng bước agent:
  - 🔵 **Solver** - Đưa ra giải pháp
  - 🟠 **Critic** - Phản biện
  - 🟣 **Alternative** - Phương án thay thế
  - 🟢 **Judge** - Quyết định cuối cùng
- ✅ Hiển thị số vòng lặp
- ✅ Lưu lịch sử hội thoại

## 📝 Cách sử dụng

1. Nhập API key vào sidebar (hoặc để mặc định từ .env)
2. Chọn model và cấu hình
3. Gõ câu hỏi vào ô chat
4. Nhấn Enter và chờ kết quả
5. Xem các agent tranh luận từng bước
6. Nhận kết quả cuối cùng

## 🎯 Ví dụ

```
Câu hỏi: Làm sao để tăng doanh số bán hàng online?

→ Solver đưa giải pháp
→ Critic phản biện
→ Alternative đề xuất cách khác
→ Judge chọn phương án tối ưu
```

## 🛑 Dừng ứng dụng

Nhấn `Ctrl + C` trong terminal

## 💡 Tips

- **Auto-reload:** Khi sửa code, Streamlit tự động reload
- **Clear cache:** Nhấn `C` trong terminal hoặc nút "Clear cache" trên UI
- **Mobile friendly:** Responsive, xem được trên điện thoại
- **Share:** Nhấn "Deploy" trên UI để share online (Streamlit Cloud)

---

Chúc sử dụng vui vẻ! 🎉
