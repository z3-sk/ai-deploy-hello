# 使用 NVIDIA 提供的包含 CUDA 11.8 的 Python 3.10 镜像
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

# 安装 Python 和 pip
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app

COPY requirements.txt .
# 安装依赖（利用清华源加速）
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]