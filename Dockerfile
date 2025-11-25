FROM python:3.11-slim

# 環境參數：減少無用輸出 & pip 行為
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_ROOT_USER_ACTION=ignore

WORKDIR /app

# 先複製 requirements 以利用 layer cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再複製其餘程式碼
COPY . .

# 建立非 root 使用者（避免以 root 跑應用）
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# 預設環境變數（可於 docker run/compose 覆寫）
ENV PORT=5000 \
    FLASK_DEBUG=0

EXPOSE 5000

# 預設啟動命令
CMD ["python", "app.py"]
