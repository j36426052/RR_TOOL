const playersContainer = document.getElementById('players-container');
let currentQueueType = 'RANKED_TFT'; // 預設為單人排位

function updatePlayerData() {
    fetch('/api/tft-data')
        .then(response => response.json())
        .then(data => {
            // console.log(data); // 查看獲取的數據

            const container = document.getElementById('players-container');
            container.innerHTML = '';

            const sortedPlayers = Object.entries(data).sort((a, b) => {
                // 確保 a 和 b 都有玩家資料

                // console.log(a,b);
                const playerA = a[1].find(p => p.queueType === currentQueueType);
                const playerB = b[1].find(p => p.queueType === currentQueueType);

                if (!playerA && !playerB) {
                    return 0; // 都沒有玩家資料，保持原來順序
                }
                if (!playerA) {
                    return 1; // a 沒有玩家資料，放到最後
                }
                if (!playerB) {
                    return -1; // b 沒有玩家資料，放到最後
                }

                // 排位順序
                const rankOrder = ['CHALLENGER', 'GRANDMASTER', 'MASTER', 'DIAMOND','EMERALD', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE', 'IRON'];
                const divisionOrder = ['I', 'II', 'III', 'IV'];

                const rankA = playerA.tier;
                const rankB = playerB.tier;

                // 首先比較 tier
                const tierComparison = rankOrder.indexOf(rankA) - rankOrder.indexOf(rankB);
                // console.log(rankA,rankOrder.indexOf(rankA));
                // console.log(rankB,rankOrder.indexOf(rankB));
                if (tierComparison !== 0) {
                    return tierComparison; // 如果 tier 不同，則按照 tier 排序
                }

                // 如果 tier 相同，則比較 rank
                const divA = playerA.rank;
                const divB = playerB.rank;
                const divisionComparison = divisionOrder.indexOf(divA) - divisionOrder.indexOf(divB);
                if (divisionComparison !== 0) {
                    return divisionComparison; // 如果 rank 不同，則按照 rank 排序
                }

                // 如果 tier 和 rank 都相同，則比較 LP
                return playerB.leaguePoints - playerA.leaguePoints; // 按 LP 降序排列
            });

            sortedPlayers.forEach(([name, playerData]) => {
                const nameMapping = {
                    "Q蛇": "Q蛇醬與鼠牛虎兔龍蛇馬羊猴雞狗豬",
                    "礎揚": "細微的鐵牌操作",
                    "雞塊": "蔡英雯玲",
                    "承育": "符號動態系統",
                    "俊暉": "天才945",
                    "柏維": "政治大學大英明神武羽球王子鄒礎揚",
                    "西瓜": "章魚大西瓜",
                    "子郡": "勒貝格測度",
                    "所代": "政治大學動態系統第二把交椅蔡承育"
                };

                // 根據當前排位類型選擇正確的玩家資料
                const player = playerData.find(p => p.queueType === currentQueueType); // 找到符合 queueType 的玩家資料

                const urlName = nameMapping[name] || name; // 使用 nameMapping 獲取描述
                // console.log(urlName);
                const card = document.createElement('div');
                card.className = 'player-card';

                if (player && player.tier) {
                    card.innerHTML = `
                        <img src="/static/images/${player.tier.toLowerCase()}.png" alt="${player.tier}" class="rank-icon">
                        <div class="player-info">
                            <div class="player-name">
                                <a href="https://tactics.tools/player/tw/${encodeURIComponent(urlName)}" style="text-decoration: none; color: inherit;">
                                    ${urlName} <!-- 顯示映射後的玩家名稱 -->
                                </a>
                            </div>
                            <div class="player-rank">${player.rank}</div>
                            <span class="spacer"></span>
                            <div class="player-lp">${player.leaguePoints} LP</div>
                        </div>
                    `;
                } else {
                    // 如果 player 不存在或 tier 不存在，顯示替代內容
                    card.innerHTML = `
                        <div class="player-info">
                            <div class="player-name">
                                <a href="https://tactics.tools/player/tw/${encodeURIComponent(urlName)}" style="text-decoration: none; color: inherit;">
                                    ${urlName} <!-- 顯示映射後的玩家名稱 -->
                                </a>
                            </div>
                            <div class="player-rank">這季沒有玩</div>
                        </div>
                    `;
                }

                container.appendChild(card);
            });
        })
        .catch(error => console.error('Error fetching player data:', error));
}

// 切換到單人排位
document.getElementById('single-player-btn').addEventListener('click', () => {
    currentQueueType = 'RANKED_TFT'; // 設置為單人排位
    updatePlayerData(); // 更新資料
    setActiveButton('single-player-btn'); // 設置按鈕狀態
});

// 切換到雙人排位
document.getElementById('double-player-btn').addEventListener('click', () => {
    currentQueueType = 'RANKED_TFT_DOUBLE_UP'; // 設置為雙人排位
    updatePlayerData(); // 更新資料
    setActiveButton('double-player-btn'); // 設置按鈕狀態
});

document.getElementById('mode-toggle').addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
    this.textContent = document.body.classList.contains('dark-mode') ? '切換到淺色模式' : '切換到深色模式';
});


// 設置按鈕狀態
function setActiveButton(activeButtonId) {
    const buttons = document.querySelectorAll('.player-btn'); // 確保選擇到所有按鈕
    buttons.forEach(button => {
        button.classList.remove('active'); // 移除所有按鈕的高亮狀態
    });
    document.getElementById(activeButtonId).classList.add('active'); // 為當前按鈕添加高亮狀態
}


// 初始更新
updatePlayerData();

// 每5分鐘更新一次
setInterval(updatePlayerData, 5 * 60 * 1000);
