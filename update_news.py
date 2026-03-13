import feedparser
import datetime

# 取得したいITニュースのRSSフィードリスト
RSS_URLS = [
    "https://jp.techcrunch.com/feed/",
    "https://www.itmedia.co.jp/news/rss/2.0/news_bursts.xml",
    "https://publickey1.jp/atom.xml"
]

def fetch_news():
    news_items = []
    for url in RSS_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]: # 各サイト上位5件
            news_items.append({
                'title': entry.title,
                'link': entry.link,
                'date': entry.get('published', '不明')
            })
    return news_items

def generate_html(news_items):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # ニュース項目のHTML生成
    cards_html = ""
    for item in news_items:
        cards_html += f"""
        <article class="card">
            <div class="card-content">
                <span class="date">{item['date'][:10]}</span>
                <h2 class="title">{item['title']}</h2>
                <a href="{item['link']}" class="button" target="_blank">記事を読む</a>
            </div>
        </article>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tech Pulse | Daily IT News</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --bg-color: #0f172a;
                --card-bg: #1e293b;
                --text-main: #f8fafc;
                --text-muted: #94a3b8;
                --accent: #38bdf8;
                --hover: #0ea5e9;
            }}
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                background-color: var(--bg-color);
                color: var(--text-main);
                font-family: 'Inter', -apple-system, sans-serif;
                line-height: 1.6;
                padding: 2rem 1rem;
            }}
            .container {{ max-width: 800px; margin: 0 auto; }}
            header {{
                text-align: center;
                margin-bottom: 3rem;
                border-bottom: 1px solid var(--card-bg);
                padding-bottom: 2rem;
            }}
            h1 {{ font-size: 2.5rem; letter-spacing: -1px; margin-bottom: 0.5rem; }}
            .last-updated {{ color: var(--text-muted); font-size: 0.9rem; }}
            
            .news-grid {{ display: grid; gap: 1.5rem; }}
            .card {{
                background: var(--card-bg);
                border-radius: 12px;
                overflow: hidden;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                border: 1px solid rgba(255,255,255,0.05);
            }}
            .card:hover {{
                transform: translateY(-4px);
                box-shadow: 0 10px 20px rgba(0,0,0,0.3);
                border-color: var(--accent);
            }}
            .card-content {{ padding: 1.5rem; }}
            .date {{ color: var(--accent); font-size: 0.8rem; font-weight: bold; text-transform: uppercase; }}
            .title {{ margin: 0.5rem 0 1.2rem; font-size: 1.25rem; line-height: 1.4; }}
            
            .button {{
                display: inline-block;
                color: var(--accent);
                text-decoration: none;
                font-weight: 700;
                font-size: 0.9rem;
                border: 1px solid var(--accent);
                padding: 0.5rem 1rem;
                border-radius: 6px;
                transition: all 0.2s;
            }}
            .button:hover {{
                background: var(--accent);
                color: var(--bg-color);
            }}
            footer {{
                text-align: center;
                margin-top: 4rem;
                color: var(--text-muted);
                font-size: 0.8rem;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>Tech Pulse</h1>
                <p class="last-updated">最終更新: {now}</p>
            </header>
            <main class="news-grid">
                {cards_html}
            </main>
            <footer>
                &copy; {datetime.datetime.now().year} Daily IT News Aggregator<br>
                Powered by GitHub Actions & Python
            </footer>
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
if __name__ == "__main__":
    items = fetch_news()
    generate_html(items)
