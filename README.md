# RR_TOOL Docker 化說明

## 專案簡介
一個使用 Flask + APScheduler 定時抓取 Riot TFT 資料並透過 `index.html` 顯示的簡易工具。透過 Docker 可在任何環境快速啟動。

## 環境變數
| 變數 | 說明 | 預設 |
|------|------|------|
| RIOT_API_KEY | Riot 開發者 API Key（必填，未設定時不會抓資料） | 無 |
| PORT | 服務埠號 | 5000 |
| FLASK_DEBUG | 是否啟用 Debug (1/0) | 0 |

## 建置映像
```bash
# 於專案根目錄
docker build -t rr_tool:latest .
```

## 執行容器
```bash
docker run --rm -p 5000:5000 \
  -e RIOT_API_KEY="你的 key" \
  -e PORT=5000 \
  --name rr_tool rr_tool:latest
```

開啟瀏覽器前往：`http://localhost:5000`
API JSON：`http://localhost:5000/api/tft-data`

## 排程與注意事項
目前 APScheduler 於程式載入即啟動，每 5 分鐘抓取一次資料。若日後改用 `gunicorn` 多 worker，須避免多重排程同時觸發。建議：
1. 將排程獨立為背景服務（Celery / Cron）。
2. 或強制使用單一 gunicorn worker。

## 開發模式（不透過 Docker）
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export RIOT_API_KEY="你的 key"
python app.py
```

## 後續可優化項目
- 使用 gunicorn + gevent 提升生產環境性能。
- 將 API Key 改存放於 Docker secrets 或雲端密鑰管理。
- 增加錯誤重試與快取，減少對 Riot API 的壓力。
- 加入基本測試與健康檢查端點。

## 授權
僅供學習/內部使用。請遵守 Riot API 服務條款。
