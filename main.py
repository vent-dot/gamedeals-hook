import requests
import time
import feedparser

WEBHOOK_URL = "https://discord.com/api/webhooks/1403813620894142494/3vQUnlo2_hAhlkovMef98-XsOIrCiA9bRgM9aMuuiTl-nKVl177MyFkloF5_XpGLtIfT"
RSS_URL = "https://www.reddit.com/r/gamedeals/new/.rss"

def send(title, url):
    data = {
        "content": f"**{title}**\n{url}"
    }

    response = requests.post(WEBHOOK_URL, json=data)

while True:
    feed = feedparser.parse(RSS_URL)
    for entry in feed.entries:
        send(entry.title, entry.link)
        time.sleep(500)
