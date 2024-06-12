# 使用官方 Python 3.10.15 镜像
FROM python:3.10.15-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 并安装依赖
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码到容器中
COPY . /app/


# 复制和映射数据文件夹
VOLUME ["/app/data"]

# 暴露8000端口
EXPOSE 8000

# 复制并设置入口点脚本
COPY entrypoint.sh /app/
RUN chmod +x entrypoint.sh

# 设置入口点脚本作为容器启动命令
ENTRYPOINT ["./entrypoint.sh"]
