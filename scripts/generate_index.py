from datetime import datetime, date, timedelta
import os

START = 212
ABC400 = datetime(2025, 4, 5).date()
today = date.today()
DAYS_IN_WEEK = 7
DAYS_IN_WEEKDAY = 5
WEEKS_IN_MONTH = 4
END = 400 + (today-ABC400).days//DAYS_IN_WEEK - WEEKS_IN_MONTH
MONDAY = 0
next_monday_delta = timedelta((MONDAY-today.weekday())%DAYS_IN_WEEK)
ONEDAY = timedelta(days = 1)
next_monday = today + next_monday_delta
DAYS = [next_monday]
for _ in range(DAYS_IN_WEEKDAY-1): DAYS.append(DAYS[-1] + ONEDAY)
URLS = [
    os.environ.get("ID_MON", "https://kenkoooo.com/atcoder/#/contest/recent"),
    os.environ.get("ID_TUE", "https://kenkoooo.com/atcoder/#/contest/recent"),
    os.environ.get("ID_WED", "https://kenkoooo.com/atcoder/#/contest/recent"),
    os.environ.get("ID_THU", "https://kenkoooo.com/atcoder/#/contest/recent"),
    os.environ.get("ID_FRI", "https://kenkoooo.com/atcoder/#/contest/recent")
]

def create_index_html():
    buttons_html = ""
    for day, url in zip(DAYS, URLS):
        buttons_html += f"""
        <a href="{url}" class="btn">
            <span class="day">{day.strftime("%Y/%m/%d")}</span>
        </a>
        """

    html_template = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ADT Nightmare コンテスト情報</title>
        <style>
            body {{ font-family: 'Helvetica Neue', Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; padding: 20px; }}
            .container {{ width: 100%; max-width: 400px; }}
            h1 {{ text-align: center; color: #1a1a1a; font-size: 1.5rem; margin-bottom: 20px; }}
            .btn {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: white;
                color: #333;
                text-decoration: none;
                padding: 15px 20px;
                margin-bottom: 10px;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                transition: transform 0.2s, box-shadow 0.2s;
                border-left: 5px solid #3498db;
            }}
            .btn:hover {{ transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.1); background: #f8f9fa; }}
            .day {{ font-weight: bold; font-size: 1.1rem; }}
            .num {{ background: #eee; padding: 4px 10px; border-radius: 20px; font-size: 0.9rem; color: #666; }}
            .footer {{ text-align: center; font-size: 0.8rem; color: #999; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏆 ADT Nightmare</h1>
            {buttons_html}
            <div class="footer">
                最終更新: 2026年4月1日<br>
                ※GitHub Actionsにより毎週手動更新されます
            </div>
        </div>
    </body>
    </html>
    """
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)

import requests
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

def urls_text(urls):
    return "\n".join([f"### {day.strftime("%Y/%m/%d")}\n {url} " for day, url in zip(DAYS, urls)])

def send_discord_notification():
    content = urls_text(URLS)
    
    data = {"content": content}
    response = requests.post(WEBHOOK_URL, json=data)
    
    if response.status_code == 204:
        print("Discord通知に成功しました。")
    else:
        print(f"Discord通知に失敗しました: {response.status_code}")

def main():
    create_index_html()
    send_discord_notification()

if __name__ == "__main__":
    main()