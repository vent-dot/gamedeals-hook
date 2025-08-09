import requests
import time
import feedparser
import os

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
RSS_URL = "https://www.reddit.com/r/gamedeals/new/.rss"

sent_posts = set()

def send(title, url):
    data = {
        "content": f"**{title}**\n{url}"
    }

    response = requests.post(WEBHOOK_URL, json=data)

while True:
    feed = feedparser.parse(RSS_URL)
    for entry in feed.entries:
        post_id = entry.id
        if post_id not in sent_posts:
            send(entry.title, entry.link)
            sent_posts.add(post_id)
        time.sleep(500)
