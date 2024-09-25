from flask import Flask, render_template, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import os

app = Flask(__name__)

# 全局變量來存儲 TFT 數據
tft_data = {}

def get_tft_data():
    # 基礎 URL
    BASE_URL = "https://tw2.api.riotgames.com/tft/league/v1/entries/by-summoner/"

    # 請求頭
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept-Language": "zh-TW,zh;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com"
    }

    # 玩家 ID 和暱稱的映射
    SUMMONER_IDS = {
        "7_58-FG0wG1MyLrDeP1aHQgJ8tj-Igb3YdTGO9RAoLSmNMTNkCBmm8LVZQ": "Q蛇",
        "-gBAzolMXyy7LA3K2Q37vlRb6dkmJk8lbl1mtCOuBdktrrn-3hO0RvQYLA": "礎揚",
        "XXHjQ-hMizN0uuYVS4eQom6m8bqhBuNRG4yiiU8RKpChEi0RG1hlZx4Dmw": "學姊",
        "dUwDc88RO_-_-DkENeDmH8AM1Cv7msk7LKOD0k9ERAAAUbSd00fxvmoLPQ": "承育",
        "g70Q_AC1Ljb3u7uJvbnhzQNDowUjzAbX9cRMYqCUqd8Qz42dzRRL0IG3-Q": "俊暉"
    }

    all_data = {}
    
    for summoner_id, nickname in SUMMONER_IDS.items():
        url = f"{BASE_URL}{summoner_id}"
        params = {"api_key": "RGAPI-86e70caa-cea5-46c5-b2e3-862f895475e7"}
        
        try:
            response = requests.get(url, headers=HEADERS, params=params)
            response.raise_for_status()  # 如果請求不成功則拋出異常
            data = response.json()
            all_data[nickname] = data
        except requests.RequestException as e:
            print(f"Error fetching data for {nickname} (ID: {summoner_id}): {str(e)}")
            all_data[nickname] = None
    #return all_data

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

if __name__ == '__main__':
    # 初始化數據
    get_tft_data()
    app.run(debug=True)
