import os
import cloudscraper

from langchain.tools import tool
from dotenv import load_dotenv


@tool
def get_player_data(steam_id: int, match_id: int):
    """
    获取玩家在指定比赛中的数据(playerSlot, kills, deaths, assists, networth, numLastHits, numDenies, level, heroDamage, towerDamage, heroHealing)
    :param steam_id: 玩家的 steam id
    :param match_id: 比赛 id
    :return: 包含玩家数据的元组
    """

    load_dotenv()

    url = "https://api.stratz.com/graphql"
    api_token = os.getenv("STRATZ_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    query = """
    query GetMatchData($id: Long!, $steamAccountId: Long!){
        match(id: $id) {
            durationSeconds
            didRadiantWin
            players(steamAccountId: $steamAccountId) {
                playerSlot
                kills
                deaths
                assists
                networth
                numLastHits
                numDenies
                level
                heroDamage
                towerDamage
                heroHealing
                goldPerMinute
                experiencePerMinute
                hero {
                    displayName
                    shortName
                }
                items {
                    itemId
                    item {
                        displayName
                    }
                }
                stats {
                    killsPerMinute
                    deathsPerMinute
                    assistsPerMinute
                    creepScore
                    neutralScore
                }
            }
            players {
                playerSlot
                kills
                deaths
                assists
                networth
                hero {
                    displayName
                }
            }
        }
    }
    """

    variables = {"id": match_id, "steamAccountId": steam_id}

    scraper = cloudscraper.create_scraper()
    response = scraper.post(
        url=url,
        headers=headers,
        json={"query": query, "variables": variables},
    )

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching player data: {response.status_code}")
        print(response.text)
        return None
