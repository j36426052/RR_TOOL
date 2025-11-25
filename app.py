from flask import Flask, render_template, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import os

app = Flask(__name__)

# 使用環境變數讀取 Riot API Key（未設定則僅顯示空資料，不抓取）
RIOT_API_KEY = "RGAPI-a847ed6c-78b1-480d-85f3-4d3969e7130a"

# 全局變量來存儲 TFT 數據
tft_data = {}

def get_tft_data():
    """抓取玩家 TFT 資料。若未設定 RIOT_API_KEY 則跳過。"""
    # if not RIOT_API_KEY:
    #     print("[WARN] RIOT_API_KEY 未設定，跳過資料抓取。")
    #     return

    BASE_URL = "https://tw2.api.riotgames.com/tft/league/v1/by-puuid/"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept-Language": "zh-TW,zh;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com"
    }

    SUMMONER_IDS = {
    "D1oA9FEYgaf_dgQSYycwycfr2ofzC-5kAQofR8aC1Bh4dV1Y6pWsEn4ca2c7qx_7-OLYPEF5upPnZA": "Q蛇醬與鼠牛虎兔龍蛇馬羊猴雞狗豬",
    "MYOOriHSwafTIcXZhFI68Bttw7xIssbdAAzksXFWQ22P22jYt2cCFsANjltEfNm0gK5syCyDjjOX_A": "阿狗汪汪汪",
    "ANT1O8g7O3iRxXuzjzboqrtrqQsvCJIKFBdGzv7WPEu4qoZdwu0c8dp-cWjQAzsJVGqZS9KkETeX5w": "符號動態系統",
    "kGbiax6rXZtSQ4GzgxYAtkrSG7lop2drr5Ed4xvlFgsc53NddAjfKfArvfEra-vOnYnERDFD0bt-GQ": "章魚大西瓜",
    "Md_IP-yX5ctUuovYF29cs0TMj9byZQnVtZLwCi-wvXFZfJz_EZ64vNUsp3lSlE71vWMTNCk-3J65IQ": "ouo",
    "prAsjWl-4yZLjZNXuUnMH9XRodwBzrcEtpcRDSsw1S6Yz6zCD09ov_3U-qjb4SjBZ3D9SPsS2S_ZyA": "政治大學動態系統第二把交椅蔡承育",
    "SPFdseU0DOtsnX4ogzEyUNGgmBYjPfEmt_6evemjvF3vxi2ODNdx_d5VAx5fZxOy9sLOAvgJ3Y84ZQ": "蔡英雯玲",
    "jBd7fhBd24mGf1vCaPT2xBqJzpG9GgLLFSF9F81SnnfOhmKAWpcYLEIkDCVEibKkrQbd9dbXwnP0Vw": "天才945",
    "70UBOFt2eYvIS0w9Gmd-SVEAeNQdnbN5Dy_KgMtfzq3I0vxCBPl-5g9qymGpkvXGANx88vKng58ahg": "勒貝格測度",
    "sCX0I4jdS9btpVngUDHW-7HCb_QsnFeCzbh9XVWsj__emjMvb-XYRnt6buLuT6HYPhtx9OphqAfvOA": "細微的鐵牌操作"
}


    all_data = {}
    for summoner_id, nickname in SUMMONER_IDS.items():
        url = f"{BASE_URL}{summoner_id}"
        params = {"api_key": RIOT_API_KEY}
        try:
            response = requests.get(url, headers=HEADERS, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            print(data)

            all_data[nickname] = data
        except requests.RequestException as e:
            print(f"[ERROR] 抓取 {nickname} (ID: {summoner_id}) 失敗: {e}")
            all_data[nickname] = None

    global tft_data
    tft_data = all_data

# 設置定時任務，每5分鐘更新一次數據
scheduler = BackgroundScheduler()
scheduler.add_job(func=get_tft_data, trigger="interval", minutes=5)
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tft-data')
def api_tft_data():
    return jsonify(tft_data)

@app.route('/plain')
def plain():
    """純文字測試端點，用於診斷瀏覽器 403 問題。"""
    return "OK", 200, {"Content-Type": "text/plain; charset=utf-8"}

@app.after_request
def log_response(resp):
    # 基礎存取日誌：方法 路徑 狀態碼
    try:
        print(f"[ACCESS] {resp.status_code} {resp.request.method} {resp.request.path}")
    except Exception:
        pass
    return resp

if __name__ == '__main__':
    get_tft_data()
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    port = int(os.environ.get("PORT", "5004"))
    # 綁定 0.0.0.0 方便容器外部存取；停用 reloader 避免 APScheduler 重複
    app.run(host="0.0.0.0", port=port, debug=debug, use_reloader=False)
