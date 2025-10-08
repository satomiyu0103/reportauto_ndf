"""==============
■データ取得・解析処理
=============="""

import openpyxl
from datetime import datetime
from dotenv import load_dotenv
import os
from pathlib import Path


def get_keys():
    # configファルダの中にある.envファイルの場所を指定する
    EXCEL_FILE_PATH = os.getenv("EXCEL_FILE_PATH")
    SLACK_WEBHOOK_URL_TOME = os.getenv("SLACK_WEBHOOK_URL_TOME")
    SLACK_WEBHOOK_URL_TOSTUFF = os.getenv("SLACK_WEBHOOK_URL_TOSTUFF")
    return EXCEL_FILE_PATH, SLACK_WEBHOOK_URL_TOME, SLACK_WEBHOOK_URL_TOSTUFF


def get_excel_data(EXCEL_FILE_PATH):
    """日報データのワークシートを取得する

    Args:
        EXCEL_FILE_PATH (_str_): 日報Excelのパス

    Returns:
        _openpyxl.worksheet.worksheet.Worksheet_: 日報データを記入しているワークシート
    """
    wb = openpyxl.load_workbook(EXCEL_FILE_PATH)
    ws = wb["日報DB"]
    return ws


def get_today_report(ws):
    """今日の日報データを取得する

    Args:
        ws (_openpyxl.worksheet.worksheet.Worksheet_): 日報データを記入しているワークシート

    Returns:
        _tuple_: 今日の日報データ
    """
    today_str = datetime.now().strftime("%Y/%m/%d")
    report = None
    for row_today in ws.iter_rows(min_row=2, values_only=True):
        if row_today[0] and row_today[0].strftime("%Y/%m/%d") == today_str:
            report = row_today
            break
    return report


def upack_report(report: tuple) -> dict:
    """タプル型の日報データにkeyを与え、辞書型へ変換する

    Args:
        report (_tuple_): 今日の日報データ

    Returns:
        _dict_: 辞書型の日報データ
    """
    keys = [
        "日付",
        "体調",
        "体調の理由",
        "通所形態",
        "開始予定時刻",
        "終了予定時刻",
        "午前予定",
        "午後予定",
        "就寝時刻",
        "起床時刻",
        "寝起き",
        "起床時のやる気",
        "体温",
        "体重",
        "腹囲",
        "歩数",
        "自習時間",
        "入浴",
        "ストレッチ",
        "睡眠",
        "測定",
        "昼食",
        "夕食",
        "朝食",
        "開始時刻",
        "終了時刻",
        "午前業務",
        "午後業務",
        "次回活動予定",
        "わんこそば仕事術",
        "一極集中仕事術",
        "耳目確認",
        "ファイル命名規則",
        "日報",
    ]
    return dict(zip(keys, report))
