# AI-Deploy-Hello

这是我的第一个 AI 部署项目，目标是打通“Python API + Docker 容器化”的全流程。

## 技术栈
- Python 3.10
- FastAPI & Uvicorn
- Docker

## 运行步骤
1. 构建镜像: `docker build -t fastapi-deploy:v1 .`
2. 启动容器: `docker run -d -p 8000:8000 --name my_api fastapi-deploy:v1`
3. 浏览器访问: `http://localhost:8000/docs`
