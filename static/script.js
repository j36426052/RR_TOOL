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
                const player = playerData[0];
                const card = document.createElement('div');
                card.className = 'player-card';
                card.innerHTML = `
                    <img src="/static/images/${player.tier.toLowerCase()}.webp" alt="${player.tier}" class="rank-icon">
                    <div class="player-info">
                        <div class="player-name">${name}</div>
                        <div class="player-rank">${player.tier} ${player.rank}</div>
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
