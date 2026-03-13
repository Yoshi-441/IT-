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
    now = datetime.datetime.now()
    date_str = now.strftime('%Y年（令和%y年）%m月%d日')
    time_str = now.strftime('%H時%M分 発行')
    
    # 記事の生成（最初の1件を「一面トップ」にする）
    articles_html = ""
    for i, item in enumerate(news_items):
        is_top = "top-news" if i == 0 else ""
        articles_html += f"""
        <article class="article {is_top}">
            <h2 class="headline"><a href="{item['link']}" target="_blank">{item['title']}</a></h2>
            <div class="meta">{item['date'][:10]}配信 — IT新聞速報</div>
            <p class="summary">【IT界隈】最新の技術動向が報告された。関係者によると、本件は今後の業界標準に大きな影響を与える可能性があるという... <a href="{item['link']}" class="read-more">［続きを読む］</a></p>
        </article>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IT新聞 デジタル版</title>
        <link href="https://fonts.googleapis.com/css2?family=Sawarabi+Mincho&family=Shippori+Mincho:wght@700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --paper-bg: #f9f7f2;
                --ink-black: #1a1a1a;
                --news-red: #b90000;
            }}
            * {{ box-sizing: border-box; }}
            body {{
                background-color: #ddd;
                color: var(--ink-black);
                font-family: 'Sawarabi Mincho', serif;
                margin: 0;
                padding: 20px;
                line-height: 1.7;
            }}
            /* 紙面全体 */
            .paper {{
                background-color: var(--paper-bg);
                max-width: 900px;
                margin: 0 auto;
                padding: 30px;
                box-shadow: 0 0 20px rgba(0,0,0,0.2);
                border: 1px solid #ccc;
            }}
            /* 題字（新聞名） */
            header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                border: 4px double var(--ink-black);
                padding: 10px 20px;
                margin-bottom: 20px;
            }}
            .masthead h1 {{
                font-family: 'Shippori Mincho', serif;
                font-size: 3.5rem;
                margin: 0;
                letter-spacing: 5px;
            }}
            .issue-info {{
                text-align: right;
                font-size: 0.9rem;
                border-left: 1px solid #ccc;
                padding-left: 15px;
            }}
            .red-tag {{
                color: white;
                background: var(--news-red);
                padding: 2px 8px;
                font-weight: bold;
                font-size: 0.8rem;
                display: inline-block;
                margin-bottom: 5px;
            }}

            /* 紙面構成（多段組み） */
            main {{
                display: grid;
                grid-template-columns: 2fr 1fr;
                gap: 30px;
                border-top: 2px solid var(--ink-black);
                padding-top: 20px;
            }}
            @media (max-width: 768px) {{
                main {{ grid-template-columns: 1fr; }}
            }}

            /* 記事スタイル */
            .article {{
                border-bottom: 1px dotted #888;
                padding-bottom: 20px;
                margin-bottom: 20px;
            }}
            .top-news {{
                grid-column: 1 / -1;
                border-bottom: 3px solid var(--ink-black);
            }}
            .top-news .headline {{
                font-size: 2.2rem;
                line-height: 1.2;
            }}
            .headline {{
                margin: 0 0 10px 0;
                font-family: 'Shippori Mincho', serif;
            }}
            .headline a {{
                color: var(--ink-black);
                text-decoration: none;
            }}
            .headline a:hover {{
                color: var(--news-red);
                text-decoration: underline;
            }}
            .meta {{
                font-size: 0.85rem;
                color: #555;
                margin-bottom: 10px;
            }}
            .summary {{
                font-size: 0.95rem;
                text-align: justify;
            }}
            .read-more {{
                color: var(--news-red);
                text-decoration: none;
                font-size: 0.8rem;
            }}

            footer {{
                margin-top: 30px;
                padding-top: 10px;
                border-top: 1px solid var(--ink-black);
                text-align: center;
                font-size: 0.8rem;
            }}
            .disclaimer {{
                font-size: 0.7rem;
                color: #777;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="paper">
            <header>
                <div class="masthead">
                    <span class="red-tag">電子版速報</span>
                    <h1>ＩＴ新聞</h1>
                </div>
                <div class="issue-info">
                    <div>{date_str}</div>
                    <div>{time_str}</div>
                    <div style="font-weight:bold; font-size: 1.1rem; border-top: 1px solid #000; margin-top:5px;">第80451号</div>
                </div>
            </header>

            <main>
                {articles_html}
            </main>

            <footer>
                <div>&copy; {now.year} IT新聞社 編集局自動生成課</div>
                <div class="disclaimer">※このサイトはGitHub Actionsによって自動生成されています。掲載記事の真偽はリンク先をご確認ください。</div>
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
