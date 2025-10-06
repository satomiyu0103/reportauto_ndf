"""==============
NDFの開始報告をExcelに記入したデータを使って自動でSlackに送信するコード
=============="""

from modules.ndf_report_core import (
    get_keys,
    get_excel_data,
    get_today_report,
    upack_report,
)
from modules.ndf_report_utils import write_ed_msg
from modules.ndf_report_delivery import send_report, write_log


def main():
    EXCEL_FILE_PATH, SLACK_WEBHOOK_URL_TOME, SLACK_WEBHOOK_URL_TOSTUFF = get_keys()
    ws = get_excel_data(EXCEL_FILE_PATH)
    report = get_today_report(ws)
    report_dict = upack_report(report)
    if report_dict["通所形態"] == "休日":
        pass
    else:
        message = write_ed_msg(report_dict)
        send_report(message, SLACK_WEBHOOK_URL_TOSTUFF)
        write_log()


if __name__ == "__main__":
    main()
