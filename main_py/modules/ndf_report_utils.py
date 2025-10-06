"""==============
■データ変換・メッセージ生成
=============="""


def temp_conv(report_dict: dict):
    """report_dictの内、体温の値をfloat型に整える

    Args:
        report_dict (_dict_): 日報データ

    Returns:
        _float_: float型に変換した体温の値
    """
    ## 体温を小数点以下まで表示
    try:
        if not report_dict["体温"]:
            return ""
        else:
            return f"{float(report_dict['体温']):.1f}"
    except (ValueError, TypeError) as e:
        print(f"体温が正しくありません。{e}")
        return "99.9"


def time_conv(report_dict: dict):
    """時刻をstring型に変換する

    Args:
        report_dict (_dict_): 日報データの辞書

    Returns:
        _str_: string型に変換したそれぞれの時刻の値
    """
    ## 時刻をstr型(00:00)に変換
    type_check_times = [
        report_dict["開始予定時刻"],
        report_dict["終了予定時刻"],
        report_dict["開始時刻"],
        report_dict["終了時刻"],
        report_dict["就寝時刻"],
        report_dict["起床時刻"],
    ]
    converted_times = []
    for t in type_check_times:
        try:
            if not isinstance(t, str):
                t = t.strftime("%H:%M")
            converted_times.append(t)
        except Exception as e:
            print(f"{t}の時刻の変換でエラーが発生しました: ", e)
            converted_times.append("18:00")  # エラー時のデフォルト
    return converted_times


def data_conv(report_dict: dict):
    """体温・時刻データを整える

    Args:
        report_dict (_dict_): 日報データ

    Returns:
        _float/string_: それぞれ整えたデータ
    """
    report_dict["体温"] = temp_conv(report_dict)
    keys = [
        "開始予定時刻",
        "終了予定時刻",
        "開始時刻",
        "終了時刻",
        "就寝時刻",
        "起床時刻",
    ]
    times = time_conv(report_dict)
    for key, time_val in zip(keys, times):
        report_dict[key] = time_val
    return (report_dict["体温"], *[report_dict[k] for k in keys])


def write_op_msg(report_dict: dict) -> str:
    """送信用のメッセージ文を作成

    Args:
        report_dict (_dict_): 日報データ

    Returns:
        _str_: 午前送信用のメッセージ文
    """
    (
        report_dict["体温"],
        report_dict["開始予定時刻"],
        report_dict["終了予定時刻"],
        report_dict["開始時刻"],
        report_dict["終了時刻"],
        report_dict["就寝時刻"],
        report_dict["起床時刻"],
    ) = data_conv(report_dict)
    msg = f"""【定時報告】
①体調｜{report_dict["体調"]}（理由：{report_dict["体調の理由"]}）
②{report_dict["通所形態"]}
　午前｜{report_dict["午前予定"]}
　午後｜{report_dict["午後予定"]}
③体温｜{report_dict["体温"]}℃　{report_dict["起床時刻"]}
④ルーティン
　昨日｜散歩{report_dict["歩数"]}歩　自学習{report_dict["自習時間"]}分
　　　｜入浴{report_dict["入浴"]}　ストレッチ{report_dict["ストレッチ"]}　就寝(7h↑){report_dict["睡眠"]}
　今日｜測定(体温・体重・腹囲){report_dict["測定"]}　朝食(1.食べた 2.食べてない){report_dict["朝食"]}
"""
    return msg


def write_ed_msg(report_dict: dict) -> str:
    """送信用のメッセージ文を作成

    Args:
        report_dict (_dict_): 日報データ

    Returns:
        _str_: 午後送信用のメッセージ文
    """
    (
        report_dict["体温"],
        report_dict["開始予定時刻"],
        report_dict["終了予定時刻"],
        report_dict["開始時刻"],
        report_dict["終了時刻"],
        report_dict["就寝時刻"],
        report_dict["起床時刻"],
    ) = data_conv(report_dict)
    msg = f"""【終了報告】
〇学習内容/進捗
・午前｜{report_dict["午前業務"]}
・午後｜{report_dict["午後業務"]}

〇感想
{report_dict["日報"]}

〇ルーティン/仕事術
・わんこそば仕事術　{report_dict["わんこそば仕事術"]}％
・一極集中仕事術　{report_dict["一極集中仕事術"]}％
・耳と目で確認するミス防止術　{report_dict["耳目確認"]}％
・フォルダ命名規則を作る仕事術　{report_dict["ファイル命名規則"]}％

〇次回の目標/ToDo
{report_dict["次回活動予定"]}を進めます。
"""
    return msg
