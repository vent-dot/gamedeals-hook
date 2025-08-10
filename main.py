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
    if response.status_code == 429:  # Rate limited
        retry_after = response.json().get('retry_after', 5)
        print(f"Rate limited, retrying after {retry_after} seconds")
        time.sleep(retry_after)
        return send(title, url)
    elif response.status_code != 204:
        print(f"Failed to send webhook: {response.status_code} {response.text}")
    else:
        print(f"Sent: {title}")

while True:
    feed = feedparser.parse(RSS_URL)
    for entry in feed.entries:
        post_id = entry.id
        if post_id not in sent_posts:
            send(entry.title, entry.link)
            sent_posts.add(post_id)
            time.sleep(1)  # small delay between webhook messages
    print("Sleeping for 300 seconds before next fetch...")
    time.sleep(300)  # 5 minutes delay between RSS fetches
