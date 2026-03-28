# ☁️ Hướng dẫn Deploy lên Streamlit Cloud (Miễn phí)

Deploy ứng dụng lên cloud, truy cập từ bất kỳ đâu với link public!

## 📋 Yêu cầu
- Tài khoản GitHub
- Tài khoản Streamlit Cloud (miễn phí)

---

## 🚀 Bước 1: Chuẩn bị code

### 1.1. Tạo file .gitignore
```gitignore
# Python
__pycache__/
*.py[cod]
.Python
.venv/
*.egg-info/

# Environment
.env

# IDE
.vscode/
.idea/

# OS
.DS_Store
```

### 1.2. Tạo file secrets mẫu
Tạo file `secrets.toml.example`:
```toml
# Copy file này thành .streamlit/secrets.toml khi chạy local
# Trên Streamlit Cloud, thêm vào Settings > Secrets

OPENAI_API_KEY = "your_openai_api_key_here"
ANTHROPIC_API_KEY = "your_anthropic_api_key_here"
MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = "0.7"
```

### 1.3. Update config/settings.py để đọc từ Streamlit secrets

Thêm vào đầu file `config/settings.py`:
```python
import streamlit as st

# Try to load from Streamlit secrets first (for cloud deployment)
try:
    openai_key = st.secrets.get("OPENAI_API_KEY", "")
    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
except Exception:
    pass  # Not running in Streamlit or secrets not configured
```

---

## 🔧 Bước 2: Push code lên GitHub

### 2.1. Khởi tạo Git repository
```powershell
cd f:\02_PhanMem\08_AiAgent\lg_graph

git init
git add .
git commit -m "Initial commit: LangGraph Multi-Agent System"
```

### 2.2. Tạo repository trên GitHub
1. Truy cập: https://github.com/new
2. Tên repository: `langgraph-multi-agent`
3. Public hoặc Private (đều được)
4. **KHÔNG** tick "Add README" (đã có rồi)
5. Click **Create repository**

### 2.3. Push code lên GitHub
```powershell
git remote add origin https://github.com/your-username/langgraph-multi-agent.git
git branch -M main
git push -u origin main
```

---

## ☁️ Bước 3: Deploy lên Streamlit Cloud

### 3.1. Đăng ký Streamlit Cloud
1. Truy cập: https://share.streamlit.io/
2. Click **Sign up with GitHub**
3. Authorize Streamlit

### 3.2. Deploy ứng dụng
1. Click **New app**
2. Chọn:
   - **Repository:** `your-username/langgraph-multi-agent`
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. Click **Advanced settings** (Optional):
   - **Python version:** 3.11
4. Click **Deploy!**

### 3.3. Thêm API Key vào Secrets
1. Trong app dashboard, click **⚙️ Settings**
2. Chọn tab **Secrets**
3. Paste nội dung:
```toml
OPENAI_API_KEY = "sk-proj-your-actual-key-here"
MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = "0.7"
```
4. Click **Save**
5. App sẽ tự động restart

---

## 🎉 Bước 4: Truy cập ứng dụng

URL sẽ có dạng:
```
https://your-username-langgraph-multi-agent-app-xxxxx.streamlit.app
```

**Share link này cho bất kỳ ai!** Họ có thể dùng từ:
- ✅ Laptop/PC
- ✅ Điện thoại
- ✅ Tablet
- ✅ Bất kỳ đâu có Internet

---

## 🔄 Cập nhật code

### Quy trình update tự động:

Mỗi khi push code lên GitHub, Streamlit Cloud **tự động deploy** version mới!

#### Bước 1: Sửa code và test local
```powershell
# Sửa code của bạn...

# Test trước khi deploy
streamlit run app.py
```

#### Bước 2: Commit và push
```powershell
# Xem các thay đổi
git status

# Thêm files
git add .

# Commit với message rõ ràng
git commit -m "Update: mô tả thay đổi của bạn"

# Push lên GitHub
git push origin main
```

#### Bước 3: Theo dõi deployment
1. Mở https://share.streamlit.io/
2. Click vào app của bạn
3. Xem Logs để đảm bảo deploy thành công
4. App tự động restart (mất 1-3 phút)

### Cập nhật API Keys hoặc Secrets:

1. Dashboard → App → **⚙️ Settings** → **Secrets**
2. Sửa nội dung secrets
3. Click **Save**
4. App tự động restart

### Update Dependencies:

Nếu thêm package mới vào `requirements.txt`:
```powershell
# Sửa requirements.txt
git add requirements.txt
git commit -m "Update: thêm package XYZ"
git push
```
→ Streamlit Cloud tự động cài đặt dependencies mới!

**📚 Xem hướng dẫn chi tiết:** [UPDATE_GUIDE.md](UPDATE_GUIDE.md) để biết thêm về:
- Rollback về version cũ khi có lỗi
- Versioning và backup strategies
- CI/CD automation
- Zero-downtime deployment

---

## 🔐 Bảo mật

### ⚠️ QUAN TRỌNG:

1. **KHÔNG COMMIT** file `.env` vào Git!
2. **KHÔNG HARD-CODE** API key trong code
3. **Luôn dùng** Streamlit Secrets cho API keys
4. **Public repo?** → Đảm bảo không có API key trong code

### Kiểm tra:
```powershell
# Xem file nào sẽ được commit
git status

# Đảm bảo .env KHÔNG có trong danh sách
# Nếu có, thêm vào .gitignore
```

---

## 📊 Quản lý App

### Dashboard: https://share.streamlit.io/

Tính năng:
- ✅ Xem logs
- ✅ Restart app
- ✅ Xem analytics (views, users)
- ✅ Manage secrets
- ✅ Custom domain (nếu cần)

---

## 💰 Chi phí

### Streamlit Cloud Free tier:
- ✅ 1 private app
- ✅ Unlimited public apps
- ✅ 1 GB RAM
- ✅ Unlimited users

→ **Hoàn toàn miễn phí!**

### OpenAI API:
- Chi phí dựa trên usage
- `gpt-4o-mini`: ~$0.15 / 1M tokens (rất rẻ)
- `gpt-4o`: ~$2.50 / 1M tokens

---

## 🔧 Troubleshooting

### App crash hoặc error:

1. **Xem logs:**
   - Click vào app trong dashboard
   - Click **Manage app** → **Logs**

2. **Thường gặp:**
   - ❌ Thiếu package → Thêm vào `requirements.txt`
   - ❌ API key sai → Kiểm tra Secrets
   - ❌ Import error → Kiểm tra code

3. **Restart app:**
   - Click **⋮** → **Reboot app**

### Quota vượt mức (Streamlit):
- Free tier: 1GB RAM
- Nếu vượt → Optimize code hoặc upgrade plan

---

## 🌟 Custom Domain (Optional)

### Nếu muốn domain riêng:

1. Mua domain (GoDaddy, Namecheap...)
2. Trong Streamlit dashboard:
   - Settings → **Custom domain**
   - Nhập domain của bạn
   - Cấu hình DNS theo hướng dẫn

→ App có thể truy cập qua `https://yourdomain.com`

---

## 💡 Best Practices

1. **Versioning:** Dùng Git tags cho releases
2. **Testing:** Test kỹ local trước khi push
3. **Monitoring:** Thường xuyên check logs
4. **Security:** Rotate API keys định kỳ
5. **Backup:** Backup code và config

---

## 🚀 Next Steps

### Mở rộng:
- Thêm authentication (nếu cần private)
- Tích hợp database để lưu history
- Add caching để giảm cost
- Monitor usage và optimize

---

## 📞 Hỗ trợ

- Streamlit Docs: https://docs.streamlit.io/
- Community Forum: https://discuss.streamlit.io/
- GitHub Issues: https://github.com/streamlit/streamlit/issues

---

## 🚀 Next Steps

- ✅ App đã deploy thành công lên Streamlit Cloud!
- 🔄 Xem [UPDATE_GUIDE.md](UPDATE_GUIDE.md) để biết cách cập nhật app
- 🐳 Hoặc xem [DEPLOY_DOCKER.md](DEPLOY_DOCKER.md) để deploy với Docker

---

Chúc deploy thành công! 🎉
