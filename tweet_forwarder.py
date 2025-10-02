import os
import requests
import subprocess
import json

# === 設定 ===
USERNAME = "WOS_Japan"               # 本番アカウント
KEYWORDS = ["ギフトコード", "🎁"]  # 本番用キーワード
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# ツイートを取得（snscrape使用）
def get_latest_tweets(username, limit=5):
    result = subprocess.run(
        ["snscrape", "--jsonl", "--max-results", str(limit), f"twitter-user:{username}"],
        capture_output=True, text=True
    )
    tweets = []
    for line in result.stdout.splitlines():
        tweets.append(json.loads(line))
    return tweets

# Discordに送信
def send_to_discord(content):
    data = {"content": content}
    requests.post(DISCORD_WEBHOOK_URL, json=data)

if __name__ == "__main__":
    tweets = get_latest_tweets(USERNAME, 10)
    for tweet in tweets:
        text = tweet["content"]
        url = tweet["url"]

        if any(keyword in text for keyword in KEYWORDS):
            message = f"🎁 新しい投稿！\n{text}\n{url}"
            send_to_discord(message)
            break
