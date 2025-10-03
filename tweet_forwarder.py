import os
import subprocess
import requests

def get_latest_tweet():
    print("🔎 Fetching tweets...")
    try:
        # 「ギフト」「ギフトコード」「🎁」のどれかを含む最新ツイートを取得
        cmd = [
            "snscrape", "--jsonl", "--max-results", "1",
            "twitter-search", "from:WOS_Japan ギフト OR ギフトコード OR 🎁"
        ]
        result = subprocess.check_output(cmd, text=True)
        if result.strip():
            print("✅ Tweet found:", result)
            return result
        else:
            print("⚠️ No tweets found")
            return None
    except Exception as e:
        print("❌ Error fetching tweets:", e)
        return None

def post_to_discord(message):
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("❌ No webhook URL set!")
        return
    print("📤 Posting to Discord...")
    response = requests.post(webhook_url, json={"content": message})
    print("📡 Discord response:", response.status_code, response.text)

if __name__ == "__main__":
    tweet = get_latest_tweet()
    if tweet:
        post_to_discord("🎁 Twitterでギフコ発見！\n" + tweet)
    else:
        print("🚫 Nothing to send")
