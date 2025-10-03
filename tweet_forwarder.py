import os
import subprocess
import requests
import json

print("🚀 Script started")

def get_latest_tweet():
    print("🔎 Fetching tweets...")
    try:
        # 「ギフト」「ギフトコード」「🎁」を含む最新ツイートを検索
        cmd = [
            "snscrape", "--jsonl", "--max-results", "1",
            "twitter-search", "from:WOS_Japan ギフト OR ギフトコード OR 🎁"
        ]
        result = subprocess.check_output(cmd, text=True)
        if result.strip():
            print("✅ Tweet found (raw json):", result)
            # JSONとしてパース
            try:
                tweet = json.loads(result.splitlines()[0])
                print("📝 Tweet content:", tweet.get("content", ""))
                return tweet
            except Exception as e:
                print("⚠️ Could not parse tweet JSON:", e)
                return None
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
    try:
        response = requests.post(webhook_url, json={"content": message})
        print("📡 Discord response:", response.status_code, response.text)
    except Exception as e:
        print("❌ Error posting to Discord:", e)

if __name__ == "__main__":
    tweet = get_latest_tweet()
    if tweet:
        content = tweet.get("content", "")
        url = tweet.get("url", "")
        message = f"🎁 新しいギフト関連ツイートが見つかりました！\n{content}\n{url}"
        post_to_discord(message)
    else:
        print("🚫 Nothing to send")

print("🏁 Script finished")
