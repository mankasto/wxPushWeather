import os
from datetime import date, datetime, timedelta

import requests
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage


# ===== 环境变量 =====

# 在一起的开始日期
start_date = os.environ['START_DATE']

# 生日（MM-DD）
birthday = os.environ['BIRTHDAY']

# 微信公众号配置
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

# 用户ID（; 分隔）
user_ids = os.environ["USER_IDS"]

# 模板 ID
template_id_day = os.environ["TEMPLATE_ID_DAY"]
template_id_night = os.environ["TEMPLATE_ID_NIGHT"]

# 昵称
name = os.environ['NAME']

# 城市（现在只作为展示用，不再查天气）
city = os.environ['CITY']


# ===== 时间处理 =====

today = datetime.now()
today_date = today.strftime("%Y年%m月%d日")


def get_count():
    """在一起多少天"""
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days + 1


def get_birthday():
    """距离下次生日还有多少天"""
    next_birthday = datetime.strptime(
        f"{date.today().year}-{birthday}", "%Y-%m-%d"
    )
    if next_birthday < datetime.now():
        next_birthday = next_birthday.replace(year=next_birthday.year + 1)
    return (next_birthday - today).days


def get_words():
    """彩虹屁"""
    words = requests.get("https://api.shadiao.pro/chp", timeout=10)
    if words.status_code != 200:
        return get_words()

    text = words.json()['data']['text']
    chunk_size = 20
    split_notes = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    note1, note2, note3, note4, note5 = (split_notes + [""] * 5)[:5]
    return note1, note2, note3, note4, note5


if __name__ == '__main__':
    client = WeChatClient(app_id, app_secret)
    wm = WeChatMessage(client)

    # 彩虹屁
    note1, note2, note3, note4, note5 = get_words()

    # 当前北京时间
    beijing_time = datetime.utcnow() + timedelta(hours=8)
    hour_of_day = beijing_time.hour

    # 白天 / 晚上模板切换（只按时间，不再依赖天气）
    template_id = template_id_day
    if hour_of_day >= 18:
        template_id = template_id_night

    print(f"当前北京时间：{beijing_time}，使用模板：{template_id}")

    data = {
        "name": {"value": name},
        "today": {"value": today_date},
        "city": {"value": city},
        "love_date": {"value": get_count()},
        "birthday": {"value": get_birthday()},
        "note1": {"value": note1},
        "note2": {"value": note2},
        "note3": {"value": note3},
        "note4": {"value": note4},
        "note5": {"value": note5},
    }

    for uid in user_ids.split(";"):
        res = wm.send_template(uid, template_id, data)
        print(res)
