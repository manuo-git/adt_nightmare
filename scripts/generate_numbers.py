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

HISTORY_FILE = "used_number.txt"
README_FILE = 'README.md'
from random import sample

def pick(ng):
    ok = [n for n in range(START, END+1) if n not in ng]
    res = sample(ok, len(DAYS)*2)
    return res

def days_task(D, E, F):
    res = []
    for i in range(len(DAYS)):
        nums = [D[2*i], D[2*i+1], E[2*i], E[2*i+1], F[2*i], F[2*i+1]]
        res.append(nums)
    return res

TYPE = "DDEEFF"

def to_str(nums):
    res = []
    for type, num in zip(list(TYPE), nums):
        res.append(f"`{num}_{type}`")
    text = ", ".join(res)
    return text

def problems_text(task):
    return "\n".join(["## 今週の問題"]+[f"### AtCoder Daily Training NIGHTMARE {day.strftime("%Y/%m/%d")} 21:00start\n {to_str(num)} " for day, num in zip(DAYS, task)])

import requests
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

def send_discord_notification(task):
    
    content = problems_text(task)
    
    data = {"content": content}
    response = requests.post(WEBHOOK_URL, json=data)
    
    if response.status_code == 204:
        print("Discord通知に成功しました。")
    else:
        print(f"Discord通知に失敗しました: {response.status_code}")

def main():
    D = []
    E = []
    F = []
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            for line in f.readlines():
                nums = list(map(int, line.split(",")))
                history.append(nums)
                D.extend(nums[0:2])
                E.extend(nums[2:4])
                F.extend(nums[4:6])
    newD = pick(D)
    newE = pick(E)
    newF = pick(F)
    task = days_task(newD, newE, newF)
    history.extend(task)
    updated_history = history[-20:]

    with open(HISTORY_FILE, "w") as f:
        for t in updated_history:
            text = ",".join(map(str, t))
            f.write(f"{text}\n")
    
    readme_content = f"""# Weekly ADT Nightmare Problems Picker
{problems_text(task)}

https://github.com/manuo-git/adt_nightmare/tree/main
---
*最終更新日: {today.year}年{today.month}月{today.day}日 (UTC)*
*※このファイルは GitHub Actions により自動生成されています。*
"""
    with open(README_FILE, 'w', encoding='utf-8') as f:
        f.write(readme_content)
        
    send_discord_notification(task)

if __name__ == "__main__":
    main()