"""==============
NDFの開始報告をExcelに記入したデータを使って自動でSlackに送信するコード
=============="""

from pathlib import Path
from dotenv import load_dotenv

from modules.ndf_report_core import (
    get_keys,
    get_excel_data,
    get_today_report,
    upack_report,
)
from modules.ndf_report_utils import write_ed_msg
from modules.ndf_report_delivery import send_report, write_log


def main():
    try:
        PROJECT_ROOT = Path(__file__).resolve().parent.parent
    except NameError:
        PROJECT_ROOT = Path.cwd()
    env_path = PROJECT_ROOT / "config" / ".env"
    load_dotenv(env_path)
    EXCEL_FILE_PATH, SLACK_WEBHOOK_URL_TOME, SLACK_WEBHOOK_URL_TOSTUFF = get_keys()
    ws = get_excel_data(EXCEL_FILE_PATH)
    report = get_today_report(ws)
    report_dict = upack_report(report)
    if report_dict["通所形態"] in ["休日", "在宅(午前のみ)", "通所", "職場実習"]:
        pass
    else:
        message = write_ed_msg(report_dict)
        send_report(message, SLACK_WEBHOOK_URL_TOSTUFF)

        logs_dir = PROJECT_ROOT / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        logs_path = logs_dir / "autoreport_tostuff.text"
        logs_message = "夕方の報告PRGが実行されました"
        write_log(logs_path, logs_message)


if __name__ == "__main__":
    main()
