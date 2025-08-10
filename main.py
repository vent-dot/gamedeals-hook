import requests
import time
import feedparser
import os

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
RSS_URL = "https://www.reddit.com/r/gamedeals/new/.rss"

sent_posts = set()

def send(title, content, url):
    message = f"{title} {url}"
    data = {"content": message}
    r = requests.post(WEBHOOK_URL, json=data)
    if r.status_code == 429:
        retry = r.json().get('retry_after', 5)
        time.sleep(retry)
        return send(title, content, url)
    elif r.status_code != 204:
        print(f"Webhook error {r.status_code}: {r.text}")
    else:
        print(f"Sent: {title}")

# On startup: fetch current posts and add their IDs to sent_posts (so they won't be resent)
initial_feed = feedparser.parse(RSS_URL)
for entry in initial_feed.entries:
    sent_posts.add(entry.id)

print(f"Initialized. Ignoring {len(sent_posts)} existing posts.")

while True:
    feed = feedparser.parse(RSS_URL)
    for entry in reversed(feed.entries):
        if entry.id not in sent_posts:
            content = entry.get('summary', 'No content')
            send(entry.title, content, entry.link)
            sent_posts.add(entry.id)
            time.sleep(1)
    time.sleep(300)
