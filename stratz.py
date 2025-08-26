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
    :return: 包含玩家数据的字典
    """

    print("🔧 [TOOL] get_player_data 被调用")
    print(f"📊 [TOOL] 参数: steam_id={steam_id}, match_id={match_id}")

    load_dotenv()

    url = "https://api.stratz.com/graphql"
    api_token = os.getenv("STRATZ_API_KEY")

    if not api_token:
        print("❌ [TOOL] 未找到 STRATZ_API_KEY")
        return {"error": "STRATZ_API_KEY not configured"}

    print(f"✅ [TOOL] API Key 已配置: {api_token[:10]}...")

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

    print(f"🌐 [TOOL] 发送请求到: {url}")

    scraper = cloudscraper.create_scraper()

    try:
        response = scraper.post(
            url=url,
            headers=headers,
            json={"query": query, "variables": variables},
        )

        print(f"📡 [TOOL] API 响应状态: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("✅ [TOOL] 成功获取数据")

            # 检查是否有错误
            if "errors" in data:
                print(f"⚠️  [TOOL] GraphQL 错误: {data['errors']}")
                return {"error": "GraphQL errors", "details": data["errors"]}

            # 检查是否有数据
            if "data" in data and data["data"]:
                match_data = data["data"].get("match")
                if match_data:
                    players = match_data.get("players", [])
                    print(f"📊 [TOOL] 找到 {len(players)} 个玩家数据")
                    return data
                else:
                    print("❌ [TOOL] 未找到比赛数据")
                    return {"error": "Match not found"}
            else:
                print("❌ [TOOL] 响应中无数据")
                return {"error": "No data in response"}
        else:
            print(f"❌ [TOOL] API 请求失败: {response.status_code}")
            print(f"响应内容: {response.text[:200]}...")
            return {"error": f"API request failed with status {response.status_code}"}

    except Exception as e:
        print(f"❌ [TOOL] 请求异常: {e}")
        return {"error": f"Request exception: {str(e)}"}
