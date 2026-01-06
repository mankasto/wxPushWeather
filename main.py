
# 哪天在一起的
start_date = os.environ['START_DATE']
# 和风天气key
# 和风天气key, host
appKey = os.environ['APP_KEY']
appHost = os.environ['APP_HOST']
# 生日
birthday = os.environ['BIRTHDAY']
# 微信公众号的appid和app_secret
@@ -43,21 +44,21 @@
}

# 根据城市名查找地理位置
url = "https://geoapi.qweather.com/v2/city/lookup"
url = f"https://{appHost}/geo/v2/city/lookup"
resp_json = json.loads(requests.get(url, params, headers=headers).text)
city_id = resp_json["location"][0]["id"]
params["location"] = city_id

# 根据城市地理位置获取当前实时天气
url = "https://devapi.qweather.com/v7/weather/now"
url = f"https://{appHost}/v7/weather/now"
realtime_json = json.loads(requests.get(url, params, headers=headers).text)
# 实时天气状况
realtime = realtime_json["now"]
# 当前温度 拼接 当前天气
now_temperature = realtime["temp"] + "℃" + realtime["text"]

# 根据城市地理位置获取3天天气状况
url = "https://devapi.qweather.com/v7/weather/3d"
url = f"https://{appHost}/v7/weather/3d"
day_forecast_json = json.loads(requests.get(url, params, headers=headers).text)

# -----------------------今天天气状况-----------------------------
@@ -228,4 +229,4 @@ def get_words():
    user_ids = user_ids.split(";")
    for e in user_ids:
        res = wm.send_template(e, template_id_day, data)
        print(res)
        print(res)
