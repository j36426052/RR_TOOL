import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def get_tft_rankings(player_ids: List[str]) -> List[Dict]:
    base_url = "https://lol.moa.tw/Ajax/rankeddashboard/{}/RANKED_TFT"
    headers = {
        "accept-language": "zh-TW,zh;q=0.5",
    }
    data = {
        "esnesda": "",
        "has": "false"
    }

    players_info = []

    for player_id in player_ids:
        url = base_url.format(player_id)
        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code == 200:
            try:
                html_content = response.content.decode('big5')
            except UnicodeDecodeError:
                html_content = response.text
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 提取玩家信息
            league_queue = soup.find('td', id='league_queue')
            league_tier = soup.find('td', id='league_tier')
            league_rank = soup.find('td', id='league_rank')
            league_point = soup.find('td', id='league_point')
            
            # 提取上次更新時間
            update_time = soup.find('div', class_='label label-info')
            
            if all([league_queue, league_tier, league_rank, league_point]):
                player_info = {
                    "id": player_id,
                    "類型": league_queue.text,
                    "階級": league_tier.text,
                    "段位": league_rank.text,
                    "積分": int(league_point.text),
                    "更新時間": update_time.text.strip() if update_time else "未知"
                }
                players_info.append(player_info)
        else:
            print(f"請求失敗，玩家ID：{player_id}，狀態碼：{response.status_code}")

    # 定義排序順序
    tier_order = {"白金": 4, "黃金": 3, "白銀": 2, "青銅": 1}
    rank_order = {"I": 4, "II": 3, "III": 2, "IV": 1}

    # 排序函數
    def sort_key(player):
        return (
            tier_order.get(player['階級'], 0),
            rank_order.get(player['段位'], 0),
            player['積分']
        )

    # 排序玩家信息
    sorted_players = sorted(players_info, key=sort_key, reverse=True)

    return sorted_players

# 使用函數
player_ids = [
    "3112518933374432",  # Q
    "3136473615689408",  # young
    "3280289453515872",  # 學姊
    "3151134851507328",  # BW
    "3130129298974592",  # CY
    "3303534112900864"   # JY
]

player_names = {
    "3112518933374432":"Ｑ蛇",  # Q
    "3136473615689408":"礎揚",  # young
    "3280289453515872":"學姊",  # 學姊
    "3151134851507328":"柏維",  # BW
    "3130129298974592":"承育",  # CY
    "3303534112900864":"俊暉"   # JY
}

rankings = get_tft_rankings(player_ids)

# 打印排序後的結果
for rank, player in enumerate(rankings, 1):
    print(f"排名 {rank}:")
    print(f"ID: {player_names[player['id']]}")
    print(f"類型: {player['類型']}")
    print(f"階級: {player['階級']}")
    print(f"段位: {player['段位']}")
    print(f"積分: {player['積分']}")
    print(f"更新時間: {player['更新時間']}")
    print()
