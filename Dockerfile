# AgriRS-Agent-MVP - Docker 生产部署镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY requirements.txt .
COPY . .

# 安装依赖（无缓存，减少镜像体积）
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Streamlit 默认端口
EXPOSE 8501

# 健康检查
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 启动命令（支持0.0.0.0绑定，适合Docker/K8s）
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
