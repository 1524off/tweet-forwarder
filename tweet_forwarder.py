name: Tweet Forwarder

on:
  schedule:
    - cron: "*/30 * * * *"   # 30分ごとに実行（無料枠に収まる）
  workflow_dispatch:         # 手動実行も可能

jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install requests
          pip install git+https://github.com/JustAnotherArchivist/snscrape.git

      - name: Run script
        env:
          DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}
        run: python ./tweet_forwarder.py
