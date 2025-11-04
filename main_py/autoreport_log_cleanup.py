"""==============
■起動ログの自動クリーンアップ
=============="""

import os
from datetime import datetime, timedelta
from pathlib import Path


def get_daytime(line):
    """ログの"→"以降の部分を日時として取得

    Args:
        line (str): 記録されたログの1文

    Returns:
        str:ログが記載された日時
    """
    timestamp_str = line.split("→")[-1].strip()
    log_date = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
    return log_date


def main():
    """30日以上前の起動ログを選択して削除する"""
    # logファイルのパス
    try:
        PROJECT_ROOT = Path(__file__).resolve().parent.parent
    except NameError:
        PROJECT_ROOT = Path.cwd()
    log_file = PROJECT_ROOT / "logs" / "autoreport_tostuff.text"
    temp_file = log_file.with_name(log_file.name + ".tmp")

    # 保持する期間
    retention_days = 30
    cutoff_date = datetime.now() - timedelta(days=retention_days)

    with (
        open(log_file, "r", encoding="utf-8") as f,
        open(temp_file, "w", encoding="utf-8") as out,
    ):
        for line in f:
            # ログの書式は"〇〇の報告PRGが実行されました → YYYY-MM-DD HH:MM:SS.microseconds"を想定
            if "→" in line:
                try:
                    log_date = get_daytime(line)
                    if log_date >= cutoff_date:
                        out.write(line)
                except Exception as e:
                    # パース失敗時はエラーメッセージを出し、出力
                    print(f"タイムスタンプ解析エラー： {line} ({e})")
                    out.write(line)
            else:
                # フォーマットが想定外の場合は削除せず残す
                out.write(line)

    # 一時ファイルを元のファイルに置き換える
    os.replace(temp_file, log_file)


if __name__ == "__main__":
    main()
