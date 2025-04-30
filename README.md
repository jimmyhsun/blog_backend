# Blog Backend 專案（使用 Docker + Django）

本專案為一個使用 Django + DRF 的後端服務，使用 `docker-compose` 進行環境建置與啟動，並整合了 API 文件生成功能。

---

## 🐳 使用 Docker Compose 啟動專案

### 建立並啟動容器

```
docker compose up -d
```

### 查看Swagger文件

```
http://localhost:8000/api/docs/
```

