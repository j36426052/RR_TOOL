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
        "FaW_WlA-9IraPO13OFUmS4pT_aVpF1SfaYGlyAiJmUejRYXZe4TVg2j6Sg": "Q蛇",
        "CF-pD_Fpj3n1M6b37kTstf40nkgUeKILduoNFYwhjL32_CEbbO00ij9dyA": "礎揚",
        "oLe6-syjTgTnJwjqGpRLBVyxLsBZiB0l6mQ3Czd3bPB5dyYAND8zOOpXPA": "雞塊",
        "sZpc3ivqqHEsrajxAY-yMChsNmR_YxJQ7mrE4JO_b8GgQQ8BIMji4dBKZQ": "承育",
        "mXP21reqkRfE8iwIjMDWphncopScfMXdFVCc1X0DA1fkaYHiwcKgU1vytA": "俊暉",
        "yeHhi8Rta1O9h1VxUDqwVtD0M_xej3kSKtYlw1te8qB-lkf560fVEvqBwg": "柏維",
        "nDkCarIOAAl8z5zBWhoe22LBv4F8pgE6GKPh7s_lCM9NcCJzuYd7hYVdFg": "西瓜",
        "_qH-DGKcQs-ykgXibkR7WWDiOpEPfYWk2uycllY_GSWEj2vNnThp0VnOlA": "子郡",
        "h4tnXW4opIzxM9wenaXOGOisJKgyC5D7fLouW_eAiXmDiXUYPXyLASjcnQ": "所代"
    }

    all_data = {}
    
    for summoner_id, nickname in SUMMONER_IDS.items():
        url = f"{BASE_URL}{summoner_id}"
        params = {"api_key": "RGAPI-a847ed6c-78b1-480d-85f3-4d3969e7130a"}
        #RGAPI-a847ed6c-78b1-480d-85f3-4d3969e7130a
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
