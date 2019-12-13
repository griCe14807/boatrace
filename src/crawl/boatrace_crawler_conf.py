# -*- coding=utf8 =*-

from datetime import datetime
from datetime import timedelta
from http.client import RemoteDisconnected
from bs4 import BeautifulSoup
import urllib.request


# jcd no dictionary （会場コード）
def make_jcd_dict():
    jcd_dict = {"桐　生": "01", "戸　田": "02", "江戸川": "03", "平和島": "04", "多摩川": "05", "浜名湖": "06", "蒲　郡": "07", "常　滑": "08",
                "　津　": "09", "三　国": "10", "びわこ": "11", "住之江": "12", "尼　崎": "13", "鳴　門": "14", "丸　亀": "15", "児　島": "16",
                "宮　島": "17", "徳　山": "18", "下　関": "19", "若　松": "20", "芦　屋": "21", "福　岡": "22", "唐　津": "23", "大　村": "24"
                }
    return jcd_dict

def make_hd_list(date_from, date_to):

    """
    期間の始まりと終わりをインプットすることで、
    boatrace_crawler_conf.make_urlへのインプットの一部であるクロール対象日付のリストを作成する

    :param date_from: crawleの開始日。"yyyymmdd" の形で入力
    :param date_to: この日の前日のレースまでcrawleを行う。"yyyymmdd" の形で入力
    :return: クロール対象日付のリスト。例えば、['2019/04/09', '2019/04/10']のような形。

    """

    start_date = datetime.strptime(date_from, '%Y%m%d').date()
    end_date = datetime.strptime(date_to, '%Y%m%d').date()

    hd_list = [i.strftime('%Y/%m/%d') for i in daterange(start_date, end_date)]

    return hd_list


def daterange(_start, _end):
    for n in range((_end - _start).days):
        yield _start + timedelta(n)


def make_url(what, rno, jcd, hd):
    """
    :param what: 何をcrawleするか。選択肢は、"odds3t"（オッズ）, "racelist"(出走表）,
    "beforeinfo" (直前情報）もしくは"raceresult" (レース結果)
    :param rno: レース番号。8Rなど、1-12の数字 + R をstrで
    :param jcd: 会場名。"桐　生"、"びわこ"など
    :param hd: holding day (レース開催日)、2019/03/28などyyyy/mm/ddの形で入力（strで）
    :return dds_url: 公式サイト最終オッズが書かれているページのurl. これを使ってcrawlする
    """
    jcd_dict = make_jcd_dict()
    rno = rno[:-1]
    hd = hd[0:4] + hd[5:7] + hd[8:10]

    odds_url = "http://boatrace.jp/owpc/pc/race/" + what + "?rno=" + rno + "&jcd=" + jcd_dict[jcd] + "&hd=" + hd

    return odds_url


def html_parser(site_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
    }

    try:
        request = urllib.request.Request(url=site_url, headers=headers)
        response = urllib.request.urlopen(request)

        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')

    # データベース作成の際、remotedisconnectedになった場合,そのレースをパス
    except RemoteDisconnected:
        print("remote disconnected error !")
        return None

    except ConnectionResetError:
        print("Connection Reset error !")
        return None

    return soup