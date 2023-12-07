# coding: utf-8
import Config
import time
import requests
import os
import SimulateHelper
def notify(mobile):
    Config.DRIVER.app_stop("cn.xuexi.android")
    time.sleep(3)
    Config.DRIVER.app_start('cn.xuexi.android')
    time.sleep(5)
    __get_score_and_push_wx__(mobile)
    Config.DRIVER.app_stop("cn.xuexi.android")

def __get_score_and_push_wx__(mobile):
    import json
    SimulateHelper.goto_score_page()
    Config.DRIVER().screenshot().save("score.png")
    url = __upload__('score.png')
    title = mobile+'自动学习通知'
    content = '<img src="' + url + '"/>'  # 改成你要的正文内容
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": Config.PUSHPLUS_TOKEN,
        "title": title,
        "content": content,
        "template": "html"
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    x = requests.post(url, data=body, headers=headers)
    print(x.json())
    os.remove('score.png')

def __upload__(filePath):
    data = {'file': open(filePath, 'rb')}
    r = requests.post('https://www.niupic.com/api/upload', files=data)
    return r.json()['data']
