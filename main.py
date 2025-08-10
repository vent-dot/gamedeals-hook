import requests
import time
import feedparser
import os

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
RSS_URL = "https://www.reddit.com/r/gamedeals/new/.rss"

sent_posts = set()

def send(title, url):
    content = f"**[{title}]({url})**\n{url}"
    data = {"content": content}
    r = requests.post(WEBHOOK_URL, json=data)
    if r.status_code == 429:
        retry = r.json().get('retry_after', 5)
        time.sleep(retry)
        return send(title, url)
    elif r.status_code != 204:
        print(f"Webhook error {r.status_code}: {r.text}")
    else:
        print(f"Sent: {title}")

while True:
    feed = feedparser.parse(RSS_URL)
    for entry in reversed(feed.entries):
        if entry.id not in sent_posts:
            send(entry.title, entry.link)
            sent_posts.add(entry.id)
            time.sleep(1)
    time.sleep(300)
