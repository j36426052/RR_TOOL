function updatePlayerData() {
    fetch('/api/tft-data')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('players-container');
            container.innerHTML = '';

            const sortedPlayers = Object.entries(data).sort((a, b) => {
                const rankOrder = ['CHALLENGER', 'GRANDMASTER', 'MASTER', 'DIAMOND', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE', 'IRON'];
                const rankA = a[1][0].tier;
                const rankB = b[1][0].tier;
                const divisionOrder = ['I', 'II', 'III', 'IV'];
                const lpA = a[1][0].leaguePoints;
                const lpB = b[1][0].leaguePoints;
                const divA = a[1][0].rank;
                const divB = b[1][0].rank;

                if (rankA === rankB) {
                    if (divA == divB){
                        return lpB - lpA;
                    }
                    return divisionOrder.indexOf(divA) - divisionOrder.indexOf(divB);

                    //return lpB - lpA;
                }
                return rankOrder.indexOf(rankA) - rankOrder.indexOf(rankB);
            });

            sortedPlayers.forEach(([name, playerData]) => {
                const nameMapping = {
                "Q蛇":"Q蛇醬與鼠牛虎兔龍蛇馬羊猴雞狗豬",
                "礎揚":"細微的鐵牌操作",
                "雞塊":"蔡英雯玲",
                "承育":"符號動態系統",
                "俊暉":"天才945",
                "柏維":"政治大學大英明神武羽球王子鄒礎揚",
                "西瓜":"章魚大西瓜",
                "子郡":"勒貝格測度",
                "所代":"政治大學動態系統第二把交椅蔡承育"}

                const player = playerData[0];
                const urlName = nameMapping[name] || name; // 如果在字典中找不到對應，就使用原名
                const card = document.createElement('div');
    card.className = 'player-card';
    
    card.innerHTML = `
        <img src="/static/images/${player.tier.toLowerCase()}.webp" alt="${player.tier}" class="rank-icon">
        <div class="player-info">
            <div class="player-name">
                <a href="https://tactics.tools/player/tw/${encodeURIComponent(urlName)}" style="text-decoration: none; color: inherit;">
                    ${name}
                </a>
            </div>
            <div class="player-rank">${player.rank}</div>
            <span class="spacer"></span>
            <div class="player-lp">${player.leaguePoints} LP</div>
        </div>
    `;
    
    container.appendChild(card);
});
        });
}

// 初始更新
updatePlayerData();

// 每5分鐘更新一次
setInterval(updatePlayerData, 5 * 60 * 1000);
