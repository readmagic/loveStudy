# coding: utf-8
import uiautomator2 as u2
import secrets
import sqlite3
from datetime import date
from requests_html import HTMLSession
# 从 secrets 模块获取 SystemRandom 实例
INST = secrets.SystemRandom()
# 设备id，adb device得到
DRIVER = u2.connect("22bcd43d")
SESSION = HTMLSession()
MY_CONN = sqlite3.connect('records.db')
MY_CURSOR = MY_CONN.cursor()
PUSHPUSH_TOKEN = 'XXXXXX'  # 在pushpush网站中可以找到
TODAY = date.today()
MAX_TRY = 3  # 所有任务是否都完成,没有完成尝试的次数
MOBILE_TYPE = "MI6"  # 手机型号
#adb的路径
ADB_PATH = "/opt/homebrew/bin/adb"
SCHEDULE_TIME="10:30"

# 百度ocr
API_KEY = 'XXXXXXX'
SECRET_KEY = 'XXXXXXX'
OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'
TWO_FOUR_ANSWER = 'https://raw.gh.fakev.cn/Pandaver/XXQG_TiKu_Transform/main/question'
CHALLENGE_ANSWER= 'https://raw.githubusercontent.com/mondayfirst/XXQG_TiKu/main/%E9%A2%98%E5%BA%93_%E6%8E%92%E5%BA%8F%E7%89%88.json'
SCORE_TIMES=3
#登录手机号
ACCOUNTS = ['13222222222','13111111111']
#登录密码
PWD='XXXXXX'

