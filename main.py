import json
from datetime import date
from datetime import datetime, timedelta

from lunardate import LunarDate
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage
import requests
import os


# 哪天在一起的
start_date = os.environ['START_DATE']

# 生日
birthday = os.environ['BIRTHDAY']
# 微信公众号的appid和app_secret
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
# 微信公众号的user_id,多个用;（分号）隔开
user_ids = os.environ["USER_IDS"]
# 白天模板id
template_id_day = os.environ["TEMPLATE_ID_DAY"]
# 晚上模板id
template_id_night = os.environ["TEMPLATE_ID_NIGHT"]
# 呢称
name = os.environ['NAME']
# 城市
city = os.environ['CITY']

# 当前时间
today = datetime.now()
# YYYY年MM月DD日
today_date = today.strftime("%Y年%m月%d日")


# 在一起多天计算
def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days+1


# 生日计算
def get_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
      next = next.replace(year=next.year + 1)
    return (next - today).days


# 彩虹屁接口
def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    text = words.json()['data']['text']

    # 按照20个字符分割字符串
    chunk_size = 20
    split_notes = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    # 分配note N 如果split_notes元素少于5，则用空字符串填充
    [note1, note2, note3, note4, note5] = (split_notes + [""] * 5)[:5]
    return note1, note2, note3, note4, note5


if __name__ == '__main__':
    # 获取微信客户端
    client = WeChatClient(app_id, app_secret)

    # 获取微信模板消息接口
    wm = WeChatMessage(client)

    # 获取彩虹屁
    note1, note2, note3, note4, note5 = get_words()

    # 获取当前UTC时间
    now_utc = datetime.utcnow()
    # 转换为北京时间（UTC+8）
    beijing_time = now_utc + timedelta(hours=8)
    # 获取当前小时数
    hour_of_day = beijing_time.hour
    # 默认发当天
    strDay = "today"
    # 如果当前时间大于15点，也就是晚上，则发送明天天气
    if hour_of_day > 15:
        strDay = "tomorrow"
        template_id_day = template_id_night

    print("当前时间：" + str(beijing_time)+"即将推送："+strDay+"信息")

    data = {"name": {"value": name},
            "today": {"value": today_date},
            "city": {"value": city},
            "weather": {"value": globals()[f'day_forecast_{strDay}_weather']},
            "now_temperature": {"value": now_temperature},
            "min_temperature": {"value": globals()[f'day_forecast_{strDay}_temperature_min']},
            "max_temperature": {"value": globals()[f'day_forecast_{strDay}_temperature_max']},
            "love_date": {"value": get_count()},
            "birthday": {"value": get_birthday()},
            "diff_date1": {"value": days_until_spring_festival()},
            "sunrise": {"value": globals()[f'day_forecast_{strDay}_sunrise']},
            "sunset": {"value": globals()[f'day_forecast_{strDay}_sunset']},
            "textNight": {"value": globals()[f'day_forecast_{strDay}_night']},
            "windDirDay": {"value": globals()[f'day_forecast_{strDay}_windDirDay']},
            "windDirNight": {"value": globals()[f'day_forecast_{strDay}_windDirNight']},
            "windScaleDay": {"value": globals()[f'day_forecast_{strDay}_windScaleDay']},
            "note1": {"value": note1},
            "note2": {"value": note2},
            "note3": {"value": note3},
            "note4": {"value": note4},
            "note5": {"value": note5}
            }
    # print(data)

    # 拆分user_ids
    user_ids = user_ids.split(";")
    for e in user_ids:
        res = wm.send_template(e, template_id_day, data)
        print(res)
