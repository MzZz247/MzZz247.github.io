import requests
from feedgen.feed import FeedGenerator
from datetime import datetime

# ========== 【你必须修改这里】 ==========
WX_ID = "替换成公众号微信号"
TRANSFER_API = f"https://api.rss.app/wechat/{WX_ID}"
OUTPUT_FILE = "rss.xml"
FEED_TITLE = "公众号文章RSS订阅源"
FEED_LINK = "https://mzzz247.github.io/wechat-rss-bot/rss.xml"
FEED_DESC = "Github Action定时抓取公众号文章生成"
# =====================================

def get_wechat_articles():
    resp = requests.get(TRANSFER_API, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get("items", [])

def build_rss(articles):
    fg = FeedGenerator()
    fg.title(FEED_TITLE)
    fg.link(href=FEED_LINK, rel="self")
    fg.description(FEED_DESC)
    fg.language("zh-CN")

    for item in articles:
        fe = fg.add_entry()
        fe.title(item.get("title", ""))
        fe.link(href=item.get("url", ""))
        fe.description(item.get("summary", ""))
        fe.pubDate(item.get("pubDate", ""))
    fg.rss_file(OUTPUT_FILE)

if __name__ == "__main__":
    articles = get_wechat_articles()
    build_rss(articles)
    print(f"✅ RSS生成完成，共 {len(articles)} 篇文章，保存至 {OUTPUT_FILE}")
