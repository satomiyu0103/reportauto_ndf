"""==============
■レポート配信とログ記録
=============="""

from datetime import datetime
import requests
from pathlib import Path


def send_report(message: str, SLACK_WEBHOOK_URL: str):
    """日報データをSlackに送信する

    Args:
        message (_str_): 送信用のメッセージ文
        SLACK_WEBHOOK_URL (_str_): .envファイル記載のURL
    """
    if message:
        payload = {"text": message}
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)

        if response.status_code == 200:
            print("slackへ投稿しました")
        else:
            print("投稿に失敗しました")
    else:
        print("本日分の報告が未記入です")


def write_log(logs_path, logs_message):
    # 起動ログを取る
    Path(logs_path).parent.mkdir(parents=True, exist_ok=True)

    line = logs_message if isinstance(logs_message, str) else "実行されたよ！"
    with Path(logs_path).open(mode="a", encoding="utf-8", newline="\n") as f:
        f.write(f"{line} →  {datetime.now()} \n")
