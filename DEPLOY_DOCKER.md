# 🐳 Hướng dẫn Deploy với Docker

## 📋 Yêu cầu
- Docker Desktop đã cài đặt
- File `.env` với API key

## 🚀 Cách 1: Chạy với Docker Compose (Khuyên dùng)

### Bước 1: Build và chạy
```powershell
docker-compose up -d
```

### Bước 2: Truy cập
Mở trình duyệt: http://localhost:8501

### Dừng container
```powershell
docker-compose down
```

### Xem logs
```powershell
docker-compose logs -f
```

---

## 🔧 Cách 2: Chạy với Docker thuần

### Bước 1: Build image
```powershell
docker build -t langgraph-app .
```

### Bước 2: Chạy container
```powershell
docker run -d `
  --name langgraph-multi-agent `
  -p 8501:8501 `
  -e OPENAI_API_KEY=your_api_key_here `
  -e MODEL_NAME=gpt-4o-mini `
  langgraph-app
```

### Hoặc dùng file .env:
```powershell
docker run -d `
  --name langgraph-multi-agent `
  -p 8501:8501 `
  --env-file .env `
  langgraph-app
```

### Bước 3: Kiểm tra
```powershell
# Xem logs
docker logs -f langgraph-multi-agent

# Kiểm tra container
docker ps
```

### Dừng và xóa
```powershell
docker stop langgraph-multi-agent
docker rm langgraph-multi-agent
```

---

## 🌐 Deploy lên Server (VPS/Cloud)

### 1. Push image lên Docker Hub

```powershell
# Đăng nhập Docker Hub
docker login

# Tag image
docker tag langgraph-app your-username/langgraph-app:latest

# Push
docker push your-username/langgraph-app:latest
```

### 2. Trên server, pull và chạy

```bash
# Pull image
docker pull your-username/langgraph-app:latest

# Chạy với environment variables
docker run -d \
  --name langgraph-app \
  -p 8501:8501 \
  -e OPENAI_API_KEY=your_key \
  --restart unless-stopped \
  your-username/langgraph-app:latest
```

---

## 🔐 Bảo mật API Key

### Không commit .env vào Git!

Tạo file `.gitignore`:
```
.env
```

### Trên server, tạo .env riêng:
```bash
nano .env
# Paste API key vào
```

---

## 📊 Quản lý Container

### Xem resource usage
```powershell
docker stats langgraph-multi-agent
```

### Restart container
```powershell
docker restart langgraph-multi-agent
```

### Update code
```powershell
# Rebuild
docker-compose build

# Restart với image mới
docker-compose up -d
```

---

## 🌍 Truy cập từ máy khác (cùng mạng LAN)

1. Tìm IP của máy chạy Docker:
```powershell
ipconfig
# Tìm IPv4 Address
```

2. Trên máy khác, truy cập:
```
http://[IP-của-máy-chủ]:8501
```
Ví dụ: `http://192.168.1.100:8501`

---

## 🔧 Troubleshooting

### Lỗi port đã được sử dụng
```powershell
# Đổi port 8501 -> 8502
docker run -p 8502:8501 ...
```

### Container bị crash
```powershell
# Xem logs để debug
docker logs langgraph-multi-agent
```

### Rebuild từ đầu (no cache)
```powershell
docker-compose build --no-cache
docker-compose up -d
```

---

## 💡 Tips

- **Auto-restart:** Container tự động khởi động khi máy reboot (đã config trong docker-compose.yml)
- **Health check:** Docker tự động kiểm tra app có sống không
- **Volumes:** Prompts có thể chỉnh sửa mà không cần rebuild
- **Multi-platform:** Image chạy được trên Windows, Linux, Mac

---

## 🚀 Next Steps

Xem [DEPLOY_STREAMLIT_CLOUD.md](DEPLOY_STREAMLIT_CLOUD.md) để deploy miễn phí lên cloud!
