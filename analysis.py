import  os
from turtle import st
import stratz
import requests

def review_player(steam_id: int, match_id: int):
    player_data = stratz.get_player_data(steam_id, match_id)

    if not player_data or "data" not in player_data:
        return "未能获取玩家数据"

    match = player_data["data"]["match"]
    if not match and not match.get("players"):
        return "未能找到该玩家的比赛数据"

    player = match["players"][0]

    prompt = f"""
    请根据以下Dota2比赛数据, 专业、犀利地评价该玩家的表现, 指出优点和不足, 并给出改进建议：
    - 击杀: {player['kills']}
    - 死亡: {player['deaths']}
    - 助攻: {player['assists']}
    - 补刀: {player['numLastHits']}
    - 反补: {player['numDenies']}
    - 等级: {player['level']}
    - 净资产: {player['networth']}
    - 英雄伤害: {player['heroDamage']}
    - 建筑伤害: {player['towerDamage']}
    - 治疗量: {player['heroHealing']}
    - 比赛时长: {match['durationSeconds']//60}分{match['durationSeconds']%60}秒
    """

    api_key = os.getenv("DEEPSEEK_API_KEY")
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"请求失败, 状态码: {response.status_code}, 错误信息: {response.text}"

if __name__ == "__main__":
    steam_id = int(os.getenv("STEAM_ACCOUNT_ID"))
    match_id = int(os.getenv("MATCH_ID"))
    review = review_player(steam_id, match_id)
    print("AI锐评: ", review)