# 使用官方 Python 3.10 轻量级镜像（与你刚才的 conda 环境版本一致）
FROM python:3.10-slim

# 设置容器内的工作目录
WORKDIR /app

# 复制依赖清单到容器内
COPY requirements.txt .

# 在容器内安装依赖（使用清华源加速）
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制当前目录下的所有代码到容器内的 /app 目录
COPY . .

# 暴露容器的 8000 端口
EXPOSE 8000

# 启动容器时执行的命令（注意这里 host 必须是 0.0.0.0，不能是 127.0.0.1）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]