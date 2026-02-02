# 🔄 Hướng dẫn Cập nhật Ứng dụng Sau Khi Deploy

Hướng dẫn chi tiết cách cập nhật ứng dụng sau khi đã deploy theo các phương thức khác nhau.

---

## 📋 Mục lục

1. [Cập nhật với Streamlit Cloud](#1-cập-nhật-với-streamlit-cloud)
2. [Cập nhật với Docker Compose](#2-cập-nhật-với-docker-compose)
3. [Cập nhật với Docker thuần](#3-cập-nhật-với-docker-thuần)
4. [Cập nhật trên Server/VPS](#4-cập-nhật-trên-servervps)
5. [Rollback khi có lỗi](#5-rollback-khi-có-lỗi)
6. [Best Practices](#6-best-practices)

---

## 1. Cập nhật với Streamlit Cloud

### Quy trình cập nhật (Tự động)

Streamlit Cloud tự động deploy mỗi khi bạn push code lên GitHub!

#### Bước 1: Sửa code trên máy local
```powershell
# Sửa code của bạn...
# Ví dụ: chỉnh sửa app.py, agents/, prompts/, etc.
```

#### Bước 2: Test local trước khi deploy
```powershell
# Chạy thử local
streamlit run app.py

# Hoặc
python app.py
```

#### Bước 3: Commit và push lên GitHub
```powershell
# Xem các file đã thay đổi
git status

# Thêm các file cần commit
git add .

# Commit với message mô tả thay đổi
git commit -m "Update: thêm tính năng XYZ"

# Push lên GitHub
git push origin main
```

#### Bước 4: Theo dõi deployment
1. Mở Streamlit Cloud dashboard: https://share.streamlit.io/
2. Click vào app của bạn
3. Xem logs để đảm bảo deploy thành công
4. App sẽ tự động restart với code mới

### Cập nhật Secrets (API Keys)

Nếu cần thay đổi API key hoặc environment variables:

1. Vào Streamlit Cloud dashboard
2. Click vào app → **⚙️ Settings**
3. Tab **Secrets**
4. Sửa nội dung:
```toml
OPENAI_API_KEY = "sk-new-api-key-here"
MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = "0.7"
```
5. Click **Save**
6. App tự động restart

### Cập nhật Dependencies

Nếu thêm/sửa packages trong `requirements.txt`:

```powershell
# Sửa requirements.txt
nano requirements.txt

# Commit và push
git add requirements.txt
git commit -m "Update: thêm package XYZ"
git push
```

→ Streamlit Cloud sẽ tự động cài đặt dependencies mới!

### Thời gian deploy

- Deployment mất khoảng **1-3 phút**
- Có thể xem progress trong Logs
- App sẽ hiện "Please wait..." trong lúc deploy

---

## 2. Cập nhật với Docker Compose

### Quy trình cập nhật nhanh

#### Bước 1: Sửa code
```powershell
# Sửa code của bạn...
```

#### Bước 2: Rebuild và restart
```powershell
# Dừng container hiện tại
docker-compose down

# Rebuild image với code mới
docker-compose build

# Chạy lại với image mới
docker-compose up -d
```

### One-liner (rebuild và restart)
```powershell
docker-compose down && docker-compose build && docker-compose up -d
```

### Cập nhật nhanh hơn (không rebuild)

Nếu chỉ sửa **prompts** hoặc file không cần rebuild:

```powershell
# Chỉ restart container
docker-compose restart
```

**Lưu ý:** Điều này chỉ hoạt động vì prompts được mount như volumes trong docker-compose.yml

### Cập nhật Dependencies

Nếu thêm packages mới vào `requirements.txt`:

```powershell
# Rebuild image (bắt buộc)
docker-compose build --no-cache

# Restart
docker-compose up -d
```

### Xem logs khi update

```powershell
# Xem logs realtime
docker-compose logs -f

# Xem logs của service cụ thể
docker-compose logs -f app
```

### Cập nhật Environment Variables

Nếu cần đổi API key hoặc config:

```powershell
# Sửa file .env
nano .env

# Restart để áp dụng
docker-compose down && docker-compose up -d
```

---

## 3. Cập nhật với Docker thuần

### Quy trình cập nhật

#### Bước 1: Sửa code
```powershell
# Sửa code...
```

#### Bước 2: Dừng và xóa container cũ
```powershell
docker stop langgraph-multi-agent
docker rm langgraph-multi-agent
```

#### Bước 3: Rebuild image
```powershell
docker build -t langgraph-app .
```

#### Bước 4: Chạy container mới
```powershell
docker run -d `
  --name langgraph-multi-agent `
  -p 8501:8501 `
  --env-file .env `
  --restart unless-stopped `
  langgraph-app
```

### Cập nhật nhanh (script)

Tạo file `update.ps1` (Windows PowerShell):
```powershell
# update.ps1
Write-Host "Stopping old container..."
docker stop langgraph-multi-agent
docker rm langgraph-multi-agent

Write-Host "Rebuilding image..."
docker build -t langgraph-app .

Write-Host "Starting new container..."
docker run -d `
  --name langgraph-multi-agent `
  -p 8501:8501 `
  --env-file .env `
  --restart unless-stopped `
  langgraph-app

Write-Host "Done! Checking status..."
docker ps | Select-String "langgraph"
docker logs --tail 20 langgraph-multi-agent
```

Chạy script:
```powershell
.\update.ps1
```

### Cập nhật trên Linux/Mac

Tạo file `update.sh`:
```bash
#!/bin/bash
echo "Stopping old container..."
docker stop langgraph-multi-agent
docker rm langgraph-multi-agent

echo "Rebuilding image..."
docker build -t langgraph-app .

echo "Starting new container..."
docker run -d \
  --name langgraph-multi-agent \
  -p 8501:8501 \
  --env-file .env \
  --restart unless-stopped \
  langgraph-app

echo "Done! Checking status..."
docker ps | grep langgraph
docker logs --tail 20 langgraph-multi-agent
```

```bash
# Cấp quyền thực thi
chmod +x update.sh

# Chạy
./update.sh
```

---

## 4. Cập nhật trên Server/VPS

### Phương pháp 1: Sử dụng Git (Khuyên dùng)

#### Setup lần đầu trên server:
```bash
# Clone repository
git clone https://github.com/your-username/langgraph-multi-agent.git
cd langgraph-multi-agent

# Tạo .env với API keys
nano .env
```

#### Cập nhật sau này:
```bash
# SSH vào server
ssh user@your-server-ip

# Vào thư mục project
cd langgraph-multi-agent

# Pull code mới nhất
git pull origin main

# Rebuild và restart
docker-compose down
docker-compose build
docker-compose up -d

# Hoặc với Docker thuần
docker stop langgraph-multi-agent
docker rm langgraph-multi-agent
docker build -t langgraph-app .
docker run -d \
  --name langgraph-multi-agent \
  -p 8501:8501 \
  --env-file .env \
  --restart unless-stopped \
  langgraph-app
```

### Phương pháp 2: Sử dụng Docker Hub

#### Trên máy local:

```powershell
# Build image
docker build -t langgraph-app .

# Tag với version mới
docker tag langgraph-app your-username/langgraph-app:v1.2.0
docker tag langgraph-app your-username/langgraph-app:latest

# Push lên Docker Hub
docker push your-username/langgraph-app:v1.2.0
docker push your-username/langgraph-app:latest
```

#### Trên server:

```bash
# Pull image mới
docker pull your-username/langgraph-app:latest

# Dừng container cũ
docker stop langgraph-multi-agent
docker rm langgraph-multi-agent

# Chạy với image mới
docker run -d \
  --name langgraph-multi-agent \
  -p 8501:8501 \
  -e OPENAI_API_KEY=your_key \
  --restart unless-stopped \
  your-username/langgraph-app:latest

# Kiểm tra
docker ps
docker logs -f langgraph-multi-agent
```

### Phương pháp 3: Sử dụng CI/CD (Advanced)

#### Setup GitHub Actions

Tạo file `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Server

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd langgraph-multi-agent
            git pull origin main
            docker-compose down
            docker-compose build
            docker-compose up -d
```

Sau đó mỗi khi push code, server tự động update!

---

## 5. Rollback khi có lỗi

### Với Streamlit Cloud

#### Rollback về commit trước:
```powershell
# Xem lịch sử commits
git log --oneline

# Rollback về commit trước đó
git revert HEAD

# Hoặc reset về commit cụ thể
git reset --hard <commit-hash>

# Push
git push origin main --force
```

### Với Docker

#### Sử dụng image tag cũ:
```bash
# List images
docker images

# Chạy lại version cũ
docker stop langgraph-multi-agent
docker rm langgraph-multi-agent

docker run -d \
  --name langgraph-multi-agent \
  -p 8501:8501 \
  --env-file .env \
  your-username/langgraph-app:v1.1.0  # Version cũ
```

#### Sử dụng Docker commit backup:
```bash
# Trước khi update, backup container hiện tại
# Tạo tag với ngày hiện tại, ví dụ: langgraph-backup:20260202
docker commit langgraph-multi-agent langgraph-backup:$(date +%Y%m%d)

# Nếu cần rollback, sử dụng tag đã tạo
docker stop langgraph-multi-agent
docker rm langgraph-multi-agent
docker run -d \
  --name langgraph-multi-agent \
  -p 8501:8501 \
  langgraph-backup:20260202  # Thay bằng ngày backup của bạn
```

### Với Git trên Server

```bash
# Xem commits
git log --oneline -10

# Rollback về commit trước
git reset --hard <commit-hash>

# Rebuild
docker-compose down
docker-compose build
docker-compose up -d
```

---

## 6. Best Practices

### ✅ Testing trước khi deploy

```powershell
# 1. Test local
streamlit run app.py

# 2. Test với Docker
docker-compose up

# 3. Nếu OK, mới deploy production
```

### ✅ Versioning

```powershell
# Sử dụng Git tags cho mỗi version
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0

# Build Docker image với tag version
docker build -t langgraph-app:v1.2.0 .
```

### ✅ Backup

```bash
# Backup code
git clone --mirror https://github.com/your-username/langgraph-multi-agent.git backup-repo

# Backup Docker image
docker save langgraph-app:latest > langgraph-app-backup.tar

# Restore
docker load < langgraph-app-backup.tar
```

### ✅ Monitoring

```bash
# Health check
curl http://localhost:8501/_stcore/health

# Monitor logs
docker logs -f langgraph-multi-agent

# Monitor resource usage
docker stats langgraph-multi-agent
```

### ✅ Zero-downtime deployment (Advanced)

Sử dụng blue-green deployment:

```yaml
# docker-compose.blue-green.yml
services:
  app-blue:
    build: .
    ports:
      - "8501:8501"
    
  app-green:
    build: .
    ports:
      - "8502:8501"

  nginx:
    image: nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

### ✅ Automated testing

Tạo file `test_deploy.sh`:
```bash
#!/bin/bash

# Wait for app to start
sleep 10

# Test health endpoint
if curl -f http://localhost:8501/_stcore/health; then
    echo "✅ App is healthy"
    exit 0
else
    echo "❌ App health check failed"
    exit 1
fi
```

### ✅ Changelog

Tạo file `CHANGELOG.md` để track changes:
```markdown
# Changelog

## [1.2.0] - 2024-02-15
### Added
- Thêm tính năng XYZ

### Changed
- Cải thiện performance

### Fixed
- Sửa lỗi ABC
```

---

## 📊 Quy trình update khuyên dùng

### Development workflow:

```
1. Code local → Test local
2. Commit → Push to feature branch
3. Create Pull Request
4. Review code
5. Merge to main
6. Auto deploy (Streamlit Cloud) hoặc Manual deploy (Docker)
7. Monitor logs
8. If error → Rollback
```

### Checklist trước khi update:

- [ ] Code đã test kỹ local
- [ ] Dependencies đã update trong requirements.txt
- [ ] .env có đầy đủ API keys
- [ ] Đã backup version hiện tại
- [ ] Đã chuẩn bị rollback plan
- [ ] Có thể monitor logs sau deploy
- [ ] Team đã được thông báo về deployment

---

## 🆘 Troubleshooting

### Update không có hiệu lực

```bash
# Clear Docker cache
docker-compose build --no-cache
docker-compose up -d

# Hoặc với Docker thuần
docker build --no-cache -t langgraph-app .
```

### Container không start sau update

```bash
# Xem logs để debug
docker logs langgraph-multi-agent

# Kiểm tra port conflict
netstat -ano | findstr :8501  # Windows
lsof -i :8501  # Linux/Mac
```

### Streamlit Cloud deployment failed

1. Check Logs trong dashboard
2. Verify requirements.txt format
3. Check Secrets configuration
4. Ensure Python version compatibility

---

## 📞 Liên hệ & Hỗ trợ

Nếu gặp vấn đề khi update:
1. Check logs trước tiên
2. Xem phần Troubleshooting
3. Rollback về version cũ
4. Tạo GitHub Issue với logs đầy đủ

---

**Chúc update thành công! 🚀**
