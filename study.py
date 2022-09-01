# coding: utf-8
import sys
import traceback

import uiautomator2 as u2
import time
import os
from requests_html import HTMLSession
from urllib.parse import quote
import string
import requests
import secrets
import random
import difflib
import sqlite3
from datetime import date
import base64
import hashlib

# 从 secrets 模块获取 SystemRandom 实例
_inst = secrets.SystemRandom()
#设备的实例号,通过 adb devices获得
driver = u2.connect("8106493f")
session = HTMLSession()
my_conn = sqlite3.connect('records.db')
my_cursor = my_conn.cursor()
token = 'xxx'  # 在pushpush网站中可以找到
today = date.today()
max_try = 2  # 所有任务是否都完成,没有完成尝试的次数

# 百度ocr
API_KEY = 'xxx'
SECRET_KEY = 'xxx'
OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'
TWO_FOUR_ANSWER ='https://raw.gh.fakev.cn/Pandaver/XXQG_TiKu_Transform/main/question'

hard_line = {
    'D 离别是中国古典诗词中常用的主题，以下诗句中无离别之意的是“        ”。 海内存知己，天涯若比邻。	燕燕于飞，差池其羽。之子于归，远送于野。	莫愁前路无知己，天下谁人不识君。	返景入深林，复照青苔上。':("离别是中国古典诗词中常用的主题，以下诗句中无离别之意的是“        ”。",[" 海内存知己，天涯若比邻。","燕燕于飞，差池其羽。之子于归，远送于野。","莫愁前路无知己，天下谁人不识君。","返景入深林，复照青苔上。"],"D"),
    'B 世界第一个永久极地考察站是         俄罗斯站	奥尔卡德斯站	长城站	阿蒙森-斯科特站':("世界第一个永久极地考察站是         俄罗斯站",["奥尔卡德斯站","长城站","阿蒙森-斯科特站"],"B"),
    "C “学习强国”APP的开机页提示语是《论语》中的哪一句话？         三人行，必有我师焉。	学而不思则罔，思而不学则殆。	学而时习之，不亦说乎。	敏而好学，不耻下问。":("学习强国”APP的开机页提示语是《论语》中的哪一句话？",["三人行，必有我师焉。","学而不思则罔，思而不学则殆。","学而时习之，不亦说乎。","敏而好学，不耻下问。"],"C"),
    "C 以下诗句由王勃所作的是“        ”。 君自故乡来，应知故乡事。	海上生明月，天涯共此时。	海内存知己，天涯若比邻。	红豆生南国，春来发几枝。":("以下诗句由王勃所作的是“        ”。",["君自故乡来，应知故乡事。","海上生明月，天涯共此时。","红豆生南国，春来发几枝。"],"C"),
    "A “山近月远觉月小，便道此山大于月。若有人眼大如天，当见山高月更阔。”这是明代思想家王守仁的《蔽月山房》，与此中哲理最接近的是“        ”。 不识庐山真面目，只缘身在此山中。	纸上得来终觉浅，绝知此事要躬行。	若言声在指头上，何不于君指上听？	问渠那得清如许，为有源头活水来。": ("“山近月远觉月小，便道此山大于月。若有人眼大如天，当见山高月更阔。”这是明代思想家王守仁的《蔽月山房》，与此中哲理最接近的是“        ”。", ["不识庐山真面目，只缘身在此山中。","纸上得来终觉浅，绝知此事要躬行。","若言声在指头上，何不于君指上听？","问渠那得清如许，为有源头活水来。"], "A"),
    "D 离别是中国古典诗词中常用的主题。以下诗句中，无离别之意的是？         海内存知己，天涯若比邻。	燕燕于飞，差池其羽。之子于归，远送于野。	莫愁前路无知己，天下谁人不识君。	返景入深林，复照青苔上。": ("离别是中国古典诗词中常用的主题。以下诗句中，无离别之意的是？", ["海内存知己，天涯若比邻。","燕燕于飞，差池其羽。之子于归，远送于野。","莫愁前路无知己，天下谁人不识君。","返景入深林，复照青苔上。"], "D"),
    "B 青头潜鸭是国家I级重点保护动物，IUCN（世界自然保护联盟）物种红色名录濒危等级——        。来源：《江苏珍稀特色动植物图鉴》（南京师范大学出版社2021年版） 易危（VU）	极危（CR）	濒危（EN）	近危（NT）":("青头潜鸭是国家I级重点保护动物，IUCN（世界自然保护联盟）物种红色名录濒危等级——",["易危（VU）","极危（CR）","濒危（EN）","近危（NT）"],"B"),
    "C 云冈石窟是中国北方地区的佛教石窟寺，与        、        并为中国北朝大石窟的代表，1961年国务院公布为全国重点文物保护单位。来源：《中国大百科全书（考古学）》（第一版）（中国大百科全书出版社） 响堂山石窟 龙门石窟	敦煌石窟 响堂山石窟	敦煌石窟 龙门石窟":("云冈石窟是中国北方地区的佛教石窟寺，与        、        并为中国北朝大石窟的代表，1961年国务院公布为全国重点文物保护单位。",["响堂山石窟 龙门石窟","敦煌石窟 响堂山石窟","敦煌石窟 龙门石窟"],"C"),
    "B 内分泌疾病        ，主要指甲状腺在多种因素作用下，合成和分泌甲状腺素的量减少，从而出现诸多器官功能降低的症状和体征，如心率减慢、腹胀、记忆力减退、头发干燥、皮肤粗糙和反应迟缓等。来源：《十万个为什么》（第六版）（上海世纪出版股份有限公司少年儿童出版社2014年版） 甲状腺功能亢进症（简称甲亢）	甲状腺功能减退症（简称甲减）":("内分泌疾病        ，主要指甲状腺在多种因素作用下，合成和分泌甲状腺素的量减少，从而出现诸多器官功能降低的症状和体征，如心率减慢、腹胀、记忆力减退、头发干燥、皮肤粗糙和反应迟缓等。",["甲状腺功能亢进症（简称甲亢）","甲状腺功能减退症（简称甲减）"],"B")
}


def parse_hard_line(line):
    hard_result = hard_line.get(line)
    if hard_result is not None:
        question = hard_result[0]
        options = hard_result[1]
        answer = hard_result[2]
        return (question, options, options[ord(answer) - 65])
    return(None,None,None)


def parse_line(line):
    if '来源：' in line:
        x = line.split("来源：")
        question_and_answer= x[0]
        answer = question_and_answer.split(" ")[0]
        question = question_and_answer.replace(answer+" ","")
        right_paren_index = x[1].count("）")
        if right_paren_index >2:
            right_paren_index = 2
        options = x[1].split("）")[right_paren_index].split()
        if line.endswith("）"):
            options[len(options)-1] = options[len(options)-1]+"）"
        return (question,options, options[ord(answer)-65])
    if "。" in line:
        full_stop_index = line.count("。")
        x = line.split("。")
        question_and_answer= ''
        z = 0
        for i in x:
            if z != full_stop_index:
                question_and_answer = question_and_answer+i+"。"
            z = z+1
        answer = question_and_answer.split(" ")[0]
        question = question_and_answer.replace(answer + " ", "")
        options = x[full_stop_index].split()
        return (question, options, options[ord(answer) - 65])
    if "？" in line:
        full_stop_index = line.count("？")
        x = line.split("？")
        question_and_answer = ''
        z = 0
        for i in x:
            if z != full_stop_index:
                question_and_answer = question_and_answer + i + "。"
            z = z + 1
        answer = question_and_answer.split(" ")[0]
        question = question_and_answer.replace(answer + " ", "")
        options = x[full_stop_index].split()
        return (question, options, options[ord(answer) - 65])
    if line in hard_line:
        parse_hard_line(line)


def two_four_answer_update():
    def exist(question):
        str = "SELECT id FROM two_four_question WHERE question='%s'" % (question)
        rows = my_cursor.execute(str)
        for row in rows:
            return row[0]
        return None

    def insert_db(question,options,answer):
        if exist(question) is None:
            str = "INSERT INTO two_four_question (question,options,answer) VALUES ('%s','%s','%s')" % (question,"|".join(options),answer)
            my_cursor.execute(str)
            my_conn.commit()
    def parse_and_insert(rows):
        for row in rows.split("\n"):
            try:
                (question,options,answer) =parse_line(row)
            except:
                (question,options,answer) = parse_hard_line(row)
            if question is not None:
                insert_db(question,options,answer)
            else:
                print(row)

    response = requests.get(TWO_FOUR_ANSWER)
    md5 = hashlib.md5(response.text.encode(encoding='UTF-8')).hexdigest()
    version = get_version_from_db(md5,"TWO_FOUR_ANSWER")
    if version is None:
        parse_and_insert(response.text)
        insert_version_to_db(md5,"TWO_FOUR_ANSWER")


def ocr(file_path):
    def fetch_token():
        params = {'grant_type': 'client_credentials',
                  'client_id': API_KEY,
                  'client_secret': SECRET_KEY}
        response = requests.post(TOKEN_URL, params)
        result = response.json()
        return result['access_token']

    def read_file(image_path):
        f = None
        try:
            f = open(image_path, 'rb')
            return f.read()
        except:
            return None
        finally:
            if f:
                f.close()

    # 获取access token
    token = fetch_token()

    # 拼接通用文字识别高精度url
    image_url = OCR_URL + "?access_token=" + token

    try:
        question = None
        options = []
        # 读取书籍页面图片
        file_content = read_file(file_path)
        # 调用文字识别服务
        params = {'image': base64.b64encode(file_content)}
        result = requests.post(image_url, params)
        # 解析返回结果

        result_json = result.json()
        for words_result in result_json["words_result"]:
            words = words_result["words"]
            for i in range(10):
                if words.startswith(str(i)):
                    question = words.replace(str(i) + ".", "")
                    break
            if words.startswith('A') or \
                    words.startswith('B') or \
                    words.startswith('C') or \
                    words.startswith('D') or \
                    words.startswith('E') or \
                    words.startswith('F'):
                options.append(words.split(".")[1])
        return question, options
    except:
        traceback.print_exc()
        print("ocr识别失败")
        return None


def _search_(content, options):
    content = "".join(content.split())
    # 职责 网上搜索
    print(f'搜索 {content}')
    print(f"选项 {options}")
    if options[-1].startswith("以上"):
        print(f'根据经验: {chr(len(options) + 64)} 很可能是正确答案')
        return chr(len(options) + 64)
    url = quote('https://www.baidu.com/s??ie=UTF-8&wd=' + content, safe=string.printable)
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.baidu.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    response = requests.get(url, headers=headers).text
    counts = []
    i = 0
    for option in options:
        x = option.replace("A. ", "").replace("B. ", "").replace("C. ", "").replace("D. ", "").replace("E. ", "")
        count = response.count(x)
        counts.append((count, i))
        print(f'{i}. {option}: {count} 次')
        i = i + 1
    counts = sorted(counts, key=lambda x: x[0], reverse=True)
    c, i = counts[0]
    if 0 == c:
        # 替换了百度引擎为搜狗引擎，结果全为零的机会应该会大幅降低
        _, i = _inst.choice(counts)
        print(f'搜索结果全0，随机一个 {i}')
    print(f'根据搜索结果: {i} 很可能是正确答案')
    return options[i]


def get_record_from_db(date, key):
    str = "SELECT id FROM records WHERE date='%s' AND key='%s'" % (date, key)
    rows = my_cursor.execute(str)
    for row in rows:
        return row[0]
    return None


def insert_record_to_db(date, key):
    str = "INSERT INTO records (DATE,KEY) VALUES ('%s','%s')" % (date, key)
    my_cursor.execute(str)
    my_conn.commit()

def get_version_from_db(md5, key):
    str = "SELECT id FROM version WHERE md5='%s' AND key='%s'" % (md5, key)
    rows = my_cursor.execute(str)
    for row in rows:
        return row[0]
    return None

def insert_version_to_db(md5, key):
    str = "INSERT INTO version (md5,KEY) VALUES ('%s','%s')" % (md5, key)
    my_cursor.execute(str)
    my_conn.commit()


# 从问题中分割出连续的语句作为关键词
def get_keywords(question):
    splitters = ["，", "。", "（", "）", "？", "、", " ", "　", "共产党"]  # www.syiban.com 的搜索不支持以上几种符号以及屏蔽了某些关键词
    question = "".join(question.split())  # 删除 u+00a0 空格, 该空格被作为答案占位符使用
    if '来源' in question:
        question = question.split("来源")[0]

    keywords = []
    for splitter in splitters:
        if (splitter in question):
            tmp = question.split(splitter)
            for x in tmp:
                if x not in keywords and len(x) > 0:
                    if len(x) > 10:
                        x = x[0:10]
                    keywords.append(x)
    result = sorted(keywords, key=len, reverse=True)
    if (len(result) == 0):
        return question[0:10]
    elif (len(result) < 5):
        return result
    else:
        return result[0:5]


def str_similar(answer, options):
    result = options[0]
    x = 0
    for option in options:
        y = difflib.SequenceMatcher(None, answer, option).quick_ratio()
        if y > x:
            y = x
        result = option
    return result


def _query_from_syiban_(question, keywords, options):
    for keyword in keywords:
        response = session.get("http://www.syiban.com/search/index/init.html?modelid=1&q=" + keyword)
        html = response.html
        results = html.find('div.yzm-news-right')
        question_answer = {}
        if (len(results) == 0):
            continue
        for result in results:
            result_question = result.find('span.title_color', first=True).text.replace('http://www.syiban.com', '')
            result_answer = result.find('p span', first=True).text
            if ("、" in result_answer):
                result_answer = result_answer.split("、")[1]
            elif ("." in result_answer):
                result_answer = result_answer.split(".")[1]
            else:
                result_answer = str_similar(result_answer, options)
            question_answer[result_question] = result_answer
        if (len(question_answer) == 1):
            x = list(question_answer.values())[0]
            print("syiban得到的答案:")
            print(x)
            return x
        return None


def _query_api_(question, options=None):
    if ("词形" in question or "读音" in question):
        keywords = options
    else:
        keywords = get_keywords(question)
    if options is None:
        options = []
    answer = _query_from_syiban_(question, keywords, options)
    if answer is None:
        answer = _query_tiku(question,options)
    return answer

def _query_two_four_question_(question,options):
    str = "SELECT answer FROM two_four_question WHERE question LIKE '%s'" % ('%'+question+'%')
    rows = my_cursor.execute(str)
    for row in rows:
         if row[0] in options:
             return row[0]
    return None

def _query_tiku(question,options):
    str = "SELECT answer FROM tiku WHERE question LIKE '%s'" % ('%'+question+'%')
    rows = my_cursor.execute(str)
    for row in rows:
         if row[0] in options:
             return row[0]
    return None



# ==================================================================================
def login(pwd):
    try:
        driver(text="登录").click()
        driver.click(0.5 * Width, 0.42 * Height)
        send_keys(pwd)
        driver(text="登录").click()
        time.sleep(2)
    except BaseException:
        print("已登录")
    else:
        print('正在登录')


def _autoJob_(tv, sleep_time, sum=6, click=True):
    count_click = 0
    count = 0
    read_articles = []
    for _ in range(100):
        try:
            text_lists = driver(className='android.widget.TextView')
            z = 0
            for i in range(len(text_lists)):
                txt = text_lists[i].info['text']
                if len(txt) > 10 and txt not in read_articles and count < sum:
                    z = z + 1
                    if z > 5:
                        break
                    driver(text=txt).click()
                    # 分享，收藏，评论
                    if click and count_click < 1:
                        # 分享
                        # time.sleep(4)
                        # driver.click(0.94 * Width, 0.975 * Height)
                        # time.sleep(2)
                        # driver(text="分享到学习强国").click()
                        # time.sleep(2)
                        # driver.press("back")
                        # 评论
                        time.sleep(1)
                        driver(text="欢迎发表你的观点").click()
                        send_keys("Chinese is good")
                        driver.press('enter')
                        time.sleep(2)
                        driver(text="发布").click()
                        time.sleep(1)
                        count_click = count_click + 1
                        # 删除发布的评论
                        time.sleep(2)
                        driver(text="删除").click()
                        time.sleep(2)
                        driver(text="确认").click()

                    count = count + 1
                    print("正在" + tv + "...", txt)
                    time.sleep(sleep_time)
                    driver.press("back")
                    time.sleep(3)
                    read_articles.append(txt)
            if count >= sum:
                break
            swipe_down()
        except Exception:
            continue


def watch_local_video(location, tv):
    driver(text=location).click()
    time.sleep(2)
    driver(text=tv).click()
    print("观看本地频道...")
    time.sleep(20)
    print("本地频道结束.")
    driver.press("back")


def read_articles(num):
    time.sleep(2)
    # 切换到要闻界面
    driver(resourceId="cn.xuexi.android:id/home_bottom_tab_button_work").click()
    driver(text='综合').click()
    _autoJob_(tv="阅读文章", sum=num, sleep_time=60)
    print("阅读文章结束.")


def watch_video(num):
    time.sleep(2)
    # 切换到百灵页面
    driver(resourceId="cn.xuexi.android:id/home_bottom_tab_button_ding").click()
    driver(text="推荐").click()
    _autoJob_(tv="观看视频", sleep_time=60, sum=num, click=False)
    print("观看视频结束.")


# ==================================================================================

def send_keys(tips):
    driver.set_fastinput_ime(True)
    time.sleep(5)
    driver.send_keys(tips)
    time.sleep(5)
    driver.set_fastinput_ime(False)



def swipe_down():
    x1 = random.randint(int(Width / 10) * 3, int(Width / 10) * 7)
    y1 = random.randint(int(Height / 20) * 16, int(Height / 20) * 17)
    x2 = random.randint(int(Width / 10) * 3, int(Width / 10) * 7)
    y2 = random.randint(int(Height / 20) * 2, int(Height / 20) * 3)
    drag_str = 'adb shell input swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(
        x2) + ' ' + str(y2)
    os.system(drag_str)
    time.sleep(5)


def swipe_question():
    x1 = Width / 10 * 3
    y1 = Height / 20 * 12
    x2 = Width / 10 * 3
    y2 = Height / 20 * 2
    drag_str = 'adb shell input swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(
        x2) + ' ' + str(y2)
    os.system(drag_str)
    time.sleep(5)


def goto_score_page():
    driver(resourceId="cn.xuexi.android:id/comm_head_xuexi_mine").click()
    time.sleep(2)
    driver.xpath(
        '//*[@resource-id="cn.xuexi.android:id/my_recycler_view"]/android.widget.LinearLayout[1]/android.widget.ImageView[1]').click()
    time.sleep(10)


def __get_question__(views):
    for view in views:
        text = view.info['text']
        if len(text) > 5 and \
                '填空题' not in text and \
                '多选题' not in text and \
                '单选题' not in text:
            return text


def __get_question_type__(views):
    for view in views:
        text = view.info['text']
        if '填空题' in text:
            return '填空题'
        if '多选题' in text:
            return '多选题'
        if '单选题' in text:
            return '单选题'


def __get_answer__(views):
    options = []
    for view in views:
        text = view.info['text']
        if len(text) > 0:
            if 'A' not in text and \
                    'B' not in text and \
                    'C' not in text and \
                    'D' not in text and \
                    'E' not in text and \
                    'F' not in text:
                options.append(text)
    return options


def daily_question():
    print("每日答题开始.")

    def daily_question_answer():
        time.sleep(5)
        views = driver(className="android.view.View")

        question_type = __get_question_type__(views)
        # 单选题 多选题 填空题
        question = __get_question__(views)
        print(question)
        if ("单选题" == question_type):
            list_views = driver(className="android.widget.ListView").child(className="android.view.View")
            options = __get_answer__(list_views)
            answer = _query_api_(question, options)
            if (answer is not None and driver(text=answer).exists):
                driver(text=answer).click()
            else:
                tips = _search_(question, options)
                driver(text=tips).click()
            time.sleep(5)
            driver(text="确定").click()
            time.sleep(5)
            if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
            if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
        elif ("多选题" == question_type):
            list_views = driver(className="android.widget.ListView").child(className="android.view.View")
            options = __get_answer__(list_views)
            for option in options:
                driver(text=option).click()
            time.sleep(5)
            driver(text="确定").click()
            time.sleep(5)
            if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
            if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
        elif ("填空题" == question_type):
            answer = _query_api_(question)
            print("查询的答案是:%s" % answer)
            if (answer is not None):
                driver(text=question_type).click()
                time.sleep(3)
                driver(text=question).sibling(text="")[2].click()
                send_keys(answer)
                driver(text="确定").click()
                time.sleep(5)
                if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
                if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
            else:
                print(question)
                driver(text="查看提示").click()
                time.sleep(3)
                tmp = driver(textStartsWith=question)
                if (len(tmp) >= 2):
                    tips = tmp[1].info['text']
                    print(tips)
                    tips = tips.replace(question, "")
                    driver(text=question_type).click()
                    time.sleep(3)
                    driver(text=question).sibling(text="")[2].click()
                    send_keys(tips)
                    driver(text="确定").click()
                    time.sleep(5)
                    if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
                    if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
                else:
                    driver(text=question_type).click()
                    time.sleep(3)
                    driver(text=question).sibling(text="")[2].click()
                    send_keys("我不知道这个答案")
                    driver(text="确定").click()
                    time.sleep(5)
                    if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
                    if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()

    # 每日答题坐标 0.851, 0.163
    x, y = getXY(2.04, 0.28)
    driver.click(x, y)
    time.sleep(5)
    is_ok = True
    for i in range(5):
        try:
            daily_question_answer()
        except:
            driver.press("back")
            is_ok =False
            break
    time.sleep(5)
    if driver(text="返回"): driver(text="返回").click()
    print("每日答题结束.")
    return is_ok


def special_question():
    print("专项答题开始.")

    def special_question_answer():
        time.sleep(5)
        views = driver(className="android.view.View")
        question_type = __get_question_type__(views)
        question = __get_question__(views)
        print(question)
        if question_type is None:
            return
        if ("单选题" in question_type):
            list_views = driver(className="android.widget.ListView").child(className="android.view.View")
            options = __get_answer__(list_views)
            answer = _query_api_(question, options)
            if (answer is not None and driver(text=answer).exists):
                driver(text=answer).click()
            else:
                tips = _search_(question, options)
                driver(text=tips).click()
            time.sleep(5)
            if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
            if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
        elif ("多选题" in question_type):
            list_views = driver(className="android.widget.ListView").child(className="android.view.View")
            options = __get_answer__(list_views)
            for option in options:
                driver(text=option).click()
            time.sleep(5)
            if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
            if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
        elif ("填空题" in question_type):
            answer = _query_api_(question)
            print("查询的答案是:%s" % answer)
            if (answer is not None):
                driver(text=question_type).click()
                time.sleep(3)
                driver(text=question).sibling(text="")[2].click()
                send_keys(answer)
                if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
                if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
            else:
                print(question)
                driver(text="查看提示").click()
                time.sleep(3)
                tmp = driver(textStartsWith=question)
                if (len(tmp) >= 2):
                    tips = tmp[1].info['text']
                    print(tips)
                    tips = tips.replace(question, "")
                    driver(text=question_type).click()
                    time.sleep(3)
                    driver(text=question).sibling(text="")[2].click()
                    send_keys(tips)
                    if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
                    if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
                else:
                    driver(text=question_type).click()
                    time.sleep(3)
                    driver(text=question).sibling(text="")[2].click()
                    send_keys("我不知道这个答案")
                    if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
                    if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()

    # 专项答题坐标 0.858, 0.305
    x, y = getXY(2.04, 0.13)
    driver.click(x, y)
    time.sleep(5)
    is_ok = True
    if (driver(text="开始答题").exists(timeout=5)):
        driver(text="开始答题").click()
        for i in range(10):
            try:
                special_question_answer()
            except:
                driver.press("back")
                is_ok = False
                break
        time.sleep(5)
        driver.press("back")
    driver.press("back")
    print("专项答题结束.")
    return is_ok


def weekly_question():
    print("每周答题开始.")

    def weekly_question_answer():
        time.sleep(5)
        views = driver(className="android.view.View")
        question_type = __get_question_type__(views)
        question = __get_question__(views)
        print(question)
        if question_type is None:
            return
        if ("单选题" in question_type):
            list_views = driver(className="android.widget.ListView").child(className="android.view.View")
            options = __get_answer__(list_views)
            answer = _query_api_(question, options)
            if (answer is not None and driver(text=answer).exists):
                driver(text=answer).click()
            else:
                tips = _search_(question, options)
                driver(text=tips).click()
            time.sleep(5)
            if (driver(text="确定").exists(timeout=5)): driver(text="确定").click()
            if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
            if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
        elif ("多选题" in question_type):
            list_views = driver(className="android.widget.ListView").child(className="android.view.View")
            options = __get_answer__(list_views)
            for option in options:
                driver(text=option).click()
            time.sleep(5)
            if (driver(text="确定").exists(timeout=5)): driver(text="确定").click()
            if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
            if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
        elif ("填空题" in question_type):
            answer = _query_api_(question)
            print("查询的答案是:%s" % answer)
            if (answer is not None):
                driver(text=question_type).click()
                time.sleep(3)
                driver(text=question).sibling(text="")[2].click()
                send_keys(answer)
                if (driver(text="确定").exists(timeout=5)): driver(text="确定").click()
                if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
                if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
            else:
                print(question)
                driver(text="查看提示").click()
                time.sleep(3)
                tmp = driver(textStartsWith=question)
                if (len(tmp) >= 2):
                    tips = tmp[1].info['text']
                    print(tips)
                    tips = tips.replace(question, "")
                    driver(text=question_type).click()
                    time.sleep(3)
                    driver(text=question).sibling(text="")[2].click()
                    send_keys(tips)
                    if (driver(text="确定").exists(timeout=5)): driver(text="确定").click()
                    if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
                    if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
                else:
                    driver(text=question_type).click()
                    time.sleep(3)
                    driver(text=question).sibling(text="")[2].click()
                    send_keys("我不知道这个答案")
                    if (driver(text="确定").exists(timeout=5)): driver(text="确定").click()
                    if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
                    if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()

    # 每周答题坐标 0.871, 0.874
    x, y = getXY(2.02, -0.43)
    driver.click(x, y)
    time.sleep(5)
    if (driver(text="未作答").exists(timeout=5)):
        driver(text="未作答").click()
        for i in range(5):
            weekly_question_answer()
        time.sleep(5)
        driver(text="返回").click()
    driver.press("back")
    print("每周答题结束.")


def two_fight_question():
    print("双人对战开始.")

    def two_fight_answer():
        driver(text="随机匹配").sibling()[0].click()
        time.sleep(10)
        score = "0"
        try:
            while score != "100":
                views = driver(className="android.view.View")
                time.sleep(2)
                score = views[11].info['text']
                print("当前得分:" + score)
                optionsEL = driver(className="android.widget.RadioButton")
                if len(optionsEL) == 0:
                    driver.press("back")
                try:
                    time.sleep(2)
                    driver().screenshot().save("ocr.png")
                    (question, options) = ocr("ocr.png")
                    if question is not None and len(question) > 0 and len(options) > 0:
                        print("题目:" + question)
                        answer = _query_two_four_question_(question, options)
                        print("答案是" + answer)
                        if (answer is not None):
                            i = 0
                            for option in options:
                                if answer in option:
                                    i = options.index(option)
                                    break
                            optionsEL[i].click()
                        else:
                            optionsEL[random.randint(0, len(optionsEL) - 1)].click()
                    else:
                        optionsEL[random.randint(0, len(optionsEL) - 1)].click()
                except:
                    optionsEL[random.randint(0, len(optionsEL) - 1)].click()
        except:
            print("出错")
        finally:
            driver.press("back")

    # 双人对战坐标 0.895, 0.728
    x, y = getXY(2.0, -0.3)
    driver.click(x, y)
    time.sleep(3)
    is_ok = True
    two_fight_answer()
    time.sleep(3)
    driver.press("back")
    if (driver(text="退出").exists(timeout=5)):
        driver(text="退出").click()
    print("双人对战结束.")
    return is_ok


def four_fight_question():
    print("四人对战开始.")

    def four_fight_answer():
        driver(text="开始比赛").click()
        time.sleep(10)
        score = "0"
        try:
            while score != "100":
                views = driver(className="android.view.View")
                time.sleep(2)
                score = views[10].info['text']
                print("当前得分:" + score)
                optionsEL = driver(className="android.widget.RadioButton")
                if len(optionsEL) == 0:
                    driver.press("back")
                try:
                    time.sleep(2)
                    driver().screenshot().save("ocr.png")
                    (question, options) = ocr("ocr.png")
                    if question is not None and len(question) > 0 and len(options) > 0:
                        print("题目:" + question)
                        answer = _query_two_four_question_(question, options)
                        print("答案是" + answer)
                        if (answer is not None):
                            i = 0
                            for option in options:
                                if answer in option:
                                    i = options.index(option)
                                    break
                            optionsEL[i].click()
                        else:
                            optionsEL[random.randint(0, len(optionsEL) - 1)].click()
                    else:
                        optionsEL[random.randint(0, len(optionsEL) - 1)].click()
                except:
                    optionsEL[random.randint(0, len(optionsEL) - 1)].click()

        except:
            # traceback.print_exc()
            print("出错")

    time.sleep(3)
    # 四人赛 坐标 0.851, 0.588
    x, y = getXY(2.04, -0.16)
    driver.click(x, y)
    time.sleep(3)
    is_ok = True
    four_fight_answer()
    driver.press("back")
    print("四人对战结束.")
    return  is_ok


def getXY(x, y):
    return (Height / 1000.0 - x, Width / 1000.0 - 1 - y)


def challenge_question():
    print("挑战答题开始.")

    def challenge_question_answer():
        views = driver(className="android.view.View")
        question = views[14].info['text']
        print(question)
        list_views = driver(className="android.widget.ListView").child(className="android.view.View")
        options = []
        for i in range(len(list_views)):
            if i > len(list_views): break
            if (len(list_views[i].info['text'])) > 0:
                options.append(list_views[i].info['text'])
        answer = _query_api_(question, options)
        if (answer is not None and driver(text=answer).exists):
            driver(text=answer).click()
        else:
            tips = _search_(question, options)
            driver(text=tips).click()
        time.sleep(3)
        if (driver(text="结束本局").exists(timeout=5)): driver(text="结束本局").click()

    # 挑战答题坐标 0.888, 0.458
    x, y = getXY(2.0, 0)
    driver.click(x, y)
    time.sleep(5)
    is_ok = True
    for i in range(6):
        try:
            challenge_question_answer()
        except:
            is_ok = False
            # traceback.print_exc()
            print("出错")
        finally:
            continue
    time.sleep(50)
    if (driver(text="结束本局").exists(timeout=5)): driver(text="结束本局").click()
    time.sleep(3)
    driver.press("back")
    print("挑战答题结束.")
    return is_ok


def answer():
    # 去积分页面
    goto_score_page()
    swipe_question()
    # 每日答题
    has_daily_question = get_record_from_db(today, "daily_question")
    if has_daily_question is None:
        if daily_question():
            insert_record_to_db(today, "daily_question")
    # 专项答题
    has_special_question = get_record_from_db(today, "special_question")
    if has_special_question is None:
        if special_question():
            insert_record_to_db(today, "special_question")
    # 挑战答题
    has_challenge_question = get_record_from_db(today, "challenge_question")
    if has_challenge_question is None:
        if challenge_question():
            insert_record_to_db(today, "challenge_question")
    # 双人对战
    has_two_fight_question = get_record_from_db(today, "two_fight_question")
    if has_two_fight_question is None:
         if two_fight_question():
            insert_record_to_db(today, "two_fight_question")
    # 四人对战
    has_four_fight_question = get_record_from_db(today, "four_fight_question")
    if has_four_fight_question is None:
        is_ok = True
        for i in range(2):
            is_ok = four_fight_question()
        if is_ok:
            insert_record_to_db(today, "four_fight_question")


def upload(filePath):
    data = {'file': open(filePath, 'rb')}
    r = requests.post('https://www.imgurl.org/upload/aws_s3',files=data)
    return r.json()['url']


def get_score_and_push_wx():
    import json
    goto_score_page()
    driver().screenshot().save("score.png")
    url = upload('score.png')
    title = '自动学习通知'
    content = '<img src="' + url + '"/>'  # 改成你要的正文内容
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": token,
        "title": title,
        "content": content,
        "template": "html"
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    x = requests.post(url, data=body, headers=headers)
    print(x.json())
    os.remove('score.png')


def watch_and_read(location, tv, video_num, article_num):
    has_watched_local_video = get_record_from_db(today, "watch_local_video")
    if has_watched_local_video is None:
        watch_local_video(location, tv)
        insert_record_to_db(today, "watch_local_video")

    has_watched_video = get_record_from_db(today, "watch_video")
    if has_watched_video is None:
        watch_video(video_num)
        insert_record_to_db(today, "watch_video")

    has_read_articles = get_record_from_db(today, "read_articles")
    if has_read_articles is None:
        read_articles(article_num)
        insert_record_to_db(today, "read_articles")


def has_none_step():
    all_step = ["watch_local_video",
                "watch_video",
                "read_articles",
                "daily_question",
                "special_question",
                "challenge_question",
                "two_fight_question",
                "four_fight_question",
                "weekly_question"
                ]
    str = "SELECT id FROM records WHERE date='%s'" % (today)
    i = 0
    rows = my_cursor.execute(str)
    for row in rows:
        i = i + 1
    if (len(all_step) == i):
        return True
    return False


def weekly_wapper():
    driver.app_stop("cn.xuexi.android")
    time.sleep(3)
    driver.app_start('cn.xuexi.android')
    goto_score_page()
    swipe_question()
    swipe_question()
    # 每周答题
    has_weekly_question = get_record_from_db(today, "weekly_question")
    if has_weekly_question is None:
        weekly_question()
        insert_record_to_db(today, "weekly_question")
    driver.app_stop("cn.xuexi.android")


def subscribe():
    def do_subscribe():
        print("进入订阅")
        driver(text="地方媒体").click()
        pass

    print("订阅开始")
    # 订阅坐标 0.885, 0.858
    x, y = getXY(2.01, -0.42)
    driver.click(x, y)
    time.sleep(5)
    do_subscribe()
    print("订阅结束")



def task():
    driver.app_stop("cn.xuexi.android")
    time.sleep(3)
    driver.app_start('cn.xuexi.android')
    # 屏幕高度
    global Height
    Height = driver.info['displayHeight']
    global Width
    Width = driver.info['displayWidth']
    password = sys.argv[1]
    login(password)

    # 取消新版本体验
    if (driver(text="取消").exists(timeout=5)):
        driver(text="取消").click()
        time.sleep(3)

    # 看上海本地视频,看10个视频,12篇文章
    watch_and_read('上海', '东方卫视', 10, 12)
    answer()
    # 每周答题
    weekly_wapper()


def capture():
    driver.app_stop("cn.xuexi.android")
    time.sleep(3)
    driver.app_start('cn.xuexi.android')
    time.sleep(5)
    get_score_and_push_wx()
    driver.app_stop("cn.xuexi.android")


def test():
    driver.app_stop("cn.xuexi.android")
    time.sleep(3)
    driver.app_start('cn.xuexi.android')
    global Height
    Height = driver.info['displayHeight']
    global Width
    Width = driver.info['displayWidth']
    goto_score_page()
    swipe_question()
    four_fight_question()

if __name__ == '__main__':
    two_four_answer_update()
    for i in range(max_try):
        if has_none_step() is False:
            try:
                task()
            except:
                traceback.print_exc()
                continue
    capture()
