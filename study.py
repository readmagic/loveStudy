# coding: utf-8
import re
import sys
from email.mime.text import MIMEText

import uiautomator2 as u2
import numpy as np
import time
import os
import requests
from urllib.parse import quote
from pymongo import MongoClient
import string

import secrets

# 从 secrets 模块获取 SystemRandom 实例
_inst = secrets.SystemRandom()
api_url = "https://api.myue.gq/xuexi/answer.php"
driver = u2.connect("172.16.24.80:5555")
Height = 1280
Width = 720
all_of_list = []
if os.path.isfile("db.npy"):
    all_of_list = np.load("db.npy").tolist()

client = MongoClient("172.16.24.80", 27017)
db = client.fuck_study
question_collection = db.question


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


def _query_api_(content, options=None):
    if options is None:
        options = []
    params = {
        "question": "".join(content.split()),
        "version": "2.3.3"
    }

    question = _query_from_mongodb_(content, options)
    if (question is not None):
        return question['answer']
    try:
        resp = requests.post(api_url, data=params).json()
        if (len(resp) == 0):
            return None

        answer = resp[0]["answer"]
        if "选择词语的正确词形" in question:
            for i in resp:
                if i["answer"] in options:
                    answer = i["answer"]
                    break

        _save_to_mongodb_(content, options, answer)
        return answer
    except Exception:
        return None


def _save_to_mongodb_(question, options, answer):
    exist = _query_from_mongodb_(question, options)
    if (exist is None):
        x = []
        for option in options:
            x.append(
                option.replace("A. ", "").replace("B. ", "").replace("C. ", "").replace("D. ", "").replace("E. ", ""))
        data = {"question": question, "options": "|".join(x), "answer": answer}
        question_collection.insert_one(data)
        print("存储到数据库:题目:" + data['question'])
        print("存储到数据库:选项:" + data['options'])
        print("存储到数据库:答案:" + data['answer'])


def _query_from_mongodb_(question, options):
    x = []
    for option in options:
        x.append(option.replace("A. ", "").replace("B. ", "").replace("C. ", "").replace("D. ", "").replace("E. ", ""))
    query = {
        'question': question,
        'options': "|".join(x)
    }
    return question_collection.find_one(query)


def send_email(content):
    from email.header import Header
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header('学习强国', 'utf-8').encode()
    msg['from'] = '249113537@163.com'
    msg['to'] = '303734023@qq.com'
    user = '249113537@163.com'
    password = 'DSFRXHYIZUWQYODP'
    smtp_server = 'smtp.163.com'
    to_addr = '303734023@qq.com'
    import smtplib
    server = smtplib.SMTP(smtp_server, 25)  # Smtp协议默认窗口是25
    server.login(user, password)
    server.sendmail(user, to_addr, msg.as_string())
    server.quit()


# ==================================================================================
def login(pwd):
    try:
        driver(text="登录").click()
        driver.click(0.5 * Width, 0.42 * Height)
        time.sleep(1)
        driver.send_keys(pwd)
        time.sleep(1)
        driver(text="登录").click()
        time.sleep(2)
    except BaseException:
        print("已登录")
    else:
        print('正在登录')


def autoJob(tv, sleep_time, sum=6, click=True):
    count_click = 0
    count = 0
    drag_str = 'adb shell input swipe ' + str(Width * 0.5) + ' ' + str(Height * 0.88) + ' ' + str(
        Width * 0.5) + ' ' + str(Height * 0.3)
    for _ in range(100):
        try:
            text_lists = driver(className='android.widget.TextView')
            for i in range(len(text_lists)):
                txt = text_lists[i].info['text']
                if len(txt) > 11 and txt not in all_of_list and count < sum:
                    driver(text=txt).click()
                    # 分享，收藏，评论
                    if click and count_click < 2:
                        # 分享
                        time.sleep(4)
                        driver.click(0.94 * Width, 0.975 * Height)
                        time.sleep(2)
                        driver(text="分享到学习强国").click()
                        time.sleep(2)
                        driver.press("back")
                        # 评论
                        time.sleep(1)
                        driver(text="欢迎发表你的观点").click()
                        time.sleep(2)
                        driver.set_fastinput_ime(True)
                        driver.send_keys("中国加油！全力支持")
                        driver.set_fastinput_ime(False)
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
                    all_of_list.append(txt)
                    print("正在" + tv + "...", txt)
                    time.sleep(sleep_time)
                    driver.press("back")
                    time.sleep(3)
            if count >= sum:
                break
            os.system(drag_str)
        except Exception:
            continue


def watch_local():
    driver(text='北京').click()
    time.sleep(2)
    driver(text='北京卫视').click()
    print("观看本地频道...")
    time.sleep(20)
    print("本地频道结束.")
    driver.press("back")


def read_articles():
    time.sleep(2)
    # 切换到要闻界面
    driver(resourceId="cn.xuexi.android:id/home_bottom_tab_icon_large").click()
    driver(text='新思想').click()
    autoJob(tv="阅读文章", sum=14, sleep_time=30)
    print("阅读文章结束.")


def watch_video():
    time.sleep(2)
    # 切换到电视台页面
    driver(resourceId="cn.xuexi.android:id/home_bottom_tab_button_contact").click()
    driver(text="联播频道").click()
    autoJob(tv="观看视频", sleep_time=60, sum=7, click=False)
    print("观看视频结束.")


# ==================================================================================


def goto_score_page(swipe = True):
    driver(resourceId="cn.xuexi.android:id/comm_head_xuexi_mine").click()
    time.sleep(2)
    driver.xpath('//*[@resource-id="cn.xuexi.android:id/my_recycler_view"]/android.widget.LinearLayout[1]/android.widget.ImageView[1]').click()
    time.sleep(10)
    if swipe:
        drag_str = 'adb shell input swipe ' + str(Width * 0.5) + ' ' + str(Height * 0.85) + ' ' + str(Width * 0.5) + ' ' + str(Height * 0.3)
        os.system(drag_str)
        time.sleep(5)


def daily_question():
    print("每日答题开始.")

    def get_question(views):
        i = 4
        question = views[4].info['contentDescription']
        while (len(question) < 5):
            i = i + 1
            question = views[i].info['contentDescription']
        return question

    def daily_question_answer():
        time.sleep(5)

        views = driver(className="android.view.View")
        question_type = views[2].info['contentDescription']
        if question_type == "":
            question_type = views[3].info['contentDescription']
        # 单选题 多选题 填空题
        question = get_question(views)
        print(question)
        if ("单选题" == question_type):
            list_views = driver(className="android.widget.ListView").child(className="android.view.View")
            options = []
            for i in range(len(list_views)):
                i = 2 + 3 * (i)
                if i > len(list_views): break
                options.append(list_views[i].info['contentDescription'])
            answer = _query_api_(question, options)
            if (answer is not None and driver(description=answer).exists):
                driver(description=answer).click()
            else:
                tips = _search_(question, options)
                driver(description=tips).click()
            time.sleep(5)
            driver(description="确定").click()
            time.sleep(5)
            if (driver(description="下一题").exists(timeout=5)): driver(description="下一题").click()
            if (driver(description="完成").exists(timeout=5)): driver(description="完成").click()
        elif ("多选题" == question_type):
            list_views = driver(className="android.widget.ListView").child(className="android.view.View")
            options = []
            for i in range(len(list_views)):
                i = 2 + 3 * (i)
                if i > len(list_views): break
                options.append(list_views[i].info['contentDescription'])
            for option in options:
                driver(description=option).click()
            time.sleep(5)
            driver(description="确定").click()
            time.sleep(5)
            if (driver(description="下一题").exists(timeout=5)): driver(description="下一题").click()
            if (driver(description="完成").exists(timeout=5)): driver(description="完成").click()
        elif ("填空题" == question_type):
            answer = _query_api_(question)
            print("查询的答案是:%s" % answer)
            if (answer is not None):
                driver(description=question_type).click()
                time.sleep(3)
                driver(description=question).sibling(className="android.view.View")[1].click()
                time.sleep(3)
                driver.set_fastinput_ime(True)
                driver.send_keys(answer)
                driver.set_fastinput_ime(False)
                driver(description="确定").click()
                time.sleep(5)
                if (driver(description="下一题").exists(timeout=5)): driver(description="下一题").click()
                if (driver(description="完成").exists(timeout=5)): driver(description="完成").click()
            else:
                print(question)
                driver(description="查看提示").click()
                time.sleep(3)
                tmp = driver(descriptionStartsWith=question)
                if (len(tmp) >= 2):
                    tips = tmp[1].info['contentDescription']
                    print(tips)
                    tips = tips.replace(question, "")
                    driver(description=question_type).click()
                    time.sleep(3)
                    driver(description=question).sibling(className="android.view.View")[1].click()
                    time.sleep(5)
                    driver.set_fastinput_ime(True)
                    driver.send_keys(tips)
                    driver.set_fastinput_ime(False)
                    time.sleep(5)
                    driver(description="确定").click()
                    time.sleep(5)
                    if (driver(description="下一题").exists(timeout=5)): driver(description="下一题").click()
                    if (driver(description="完成").exists(timeout=5)): driver(description="完成").click()
                else:
                    driver(description=question_type).click()
                    time.sleep(3)
                    driver(description=question).sibling(className="android.view.View")[1].click()
                    time.sleep(3)
                    driver.set_fastinput_ime(True)
                    driver.send_keys("我不知道这个答案")
                    driver.set_fastinput_ime(False)
                    driver(description="确定").click()
                    time.sleep(5)
                    if (driver(description="下一题").exists(timeout=5)): driver(description="下一题").click()
                    if (driver(description="完成").exists(timeout=5)): driver(description="完成").click()

    driver(description="每日答题").sibling(className="android.view.View")[3].click()
    time.sleep(5)
    for i in range(5):
        try:
            daily_question_answer()
        except:
            driver.press("back")
            break
    time.sleep(5)
    if driver(description="返回"): driver(description="返回").click()
    print("每日答题结束.")


def weekly_question():
    print("每周答题开始.")

    def weekly_question_answer():
        time.sleep(5)
        list_views = driver(className="android.widget.ListView").child(className="android.view.View")
        selects = []
        for i in range(len(list_views)):
            i = 2 + 3 * (i)
            if i > len(list_views): break
            selects.append(list_views[i].info['contentDescription'])
        for select in selects:
            driver(description=select).click()
        time.sleep(5)
        print(selects)
        # 正确情况
        if (driver(description="确定").exists(timeout=5)): driver(description="确定").click()
        # 错误情况
        if (driver(description="下一题").exists(timeout=5)): driver(description="下一题").click()
        if (driver(description="完成").exists(timeout=5)): driver(description="完成").click()

    driver(description="每周答题").sibling(className="android.view.View")[3].click()
    time.sleep(5)
    if (driver(description="未作答").exists(timeout=5)):
        driver(description="未作答").click()
        for i in range(5):
            weekly_question_answer()
        time.sleep(5)
        driver(description="返回").click()
    driver.press("back")
    print("每周答题结束.")


def special_question():
    print("专项答题开始.")

    def special_question_answer():
        time.sleep(5)
        views = driver(className="android.view.View")
        i = 0
        question_type = ""
        for view in views:
            question_type = view.info['contentDescription']
            if "分" in question_type:
                break
            i = i + 1
        if ("单选题" in question_type):
            question = views[i + 2].info['contentDescription']
            print(question)
            list_views = driver(className="android.widget.ListView").child(className="android.view.View")
            options = []
            for i in range(len(list_views)):
                i = 2 + 3 * (i)
                if i > len(list_views): break
                options.append(list_views[i].info['contentDescription'])
            answer = _query_api_(question, options)
            if (answer is not None and driver(description=answer).exists):
                driver(description=answer).click()
            else:
                tips = _search_(question, options)
                driver(description=tips).click()
            time.sleep(5)
            if (driver(description="下一题").exists(timeout=5)): driver(description="下一题").click()
            if (driver(description="完成").exists(timeout=5)): driver(description="完成").click()
        elif ("多选题" in question_type):
            question = views[i + 2].info['contentDescription']
            print(question)
            list_views = driver(className="android.widget.ListView").child(className="android.view.View")
            options = []
            for i in range(len(list_views)):
                i = 2 + 3 * (i)
                if i > len(list_views): break
                options.append(list_views[i].info['contentDescription'])
            for option in options:
                driver(description=option).click()
            time.sleep(5)
            if (driver(description="下一题").exists(timeout=5)): driver(description="下一题").click()
            if (driver(description="完成").exists(timeout=5)): driver(description="完成").click()
        elif ("填空题" in question_type):
            question = views[i + 3].info['contentDescription']
            print(question)
            answer = _query_api_(question)
            print("查询的答案是:%s" % answer)
            if (answer is not None):
                driver(description=question_type).click()
                time.sleep(3)
                driver(description=question).sibling(className="android.view.View")[1].click()
                time.sleep(3)
                driver.set_fastinput_ime(True)
                driver.send_keys(answer)
                driver.set_fastinput_ime(False)
                time.sleep(5)
                if (driver(description="下一题").exists(timeout=5)): driver(description="下一题").click()
                if (driver(description="完成").exists(timeout=5)): driver(description="完成").click()
            else:
                print(question)
                driver(description="查看提示").click()
                time.sleep(3)
                tmp = driver(descriptionStartsWith=question)
                if (len(tmp) >= 2):
                    tips = tmp[1].info['contentDescription']
                    print(tips)
                    tips = tips.replace(question, "")
                    driver(description=question_type).click()
                    time.sleep(3)
                    driver(description=question).sibling(className="android.view.View")[1].click()
                    time.sleep(5)
                    driver.set_fastinput_ime(True)
                    driver.send_keys(tips)
                    driver.set_fastinput_ime(False)
                    time.sleep(5)
                    if (driver(description="下一题").exists(timeout=5)): driver(description="下一题").click()
                    if (driver(description="完成").exists(timeout=5)): driver(description="完成").click()
                else:
                    driver(description=question_type).click()
                    time.sleep(3)
                    driver(description=question).sibling(className="android.view.View")[1].click()
                    time.sleep(3)
                    driver.set_fastinput_ime(True)
                    driver.send_keys("我不知道这个答案")
                    driver.set_fastinput_ime(False)
                    time.sleep(5)
                    if (driver(description="下一题").exists(timeout=5)): driver(description="下一题").click()
                    if (driver(description="完成").exists(timeout=5)): driver(description="完成").click()

    driver(description="专项答题").sibling(className="android.view.View")[3].click()
    time.sleep(5)
    if (driver(description="开始答题").exists(timeout=5)):
        driver(description="开始答题").click()
        for i in range(10):
            special_question_answer()
        time.sleep(5)
        driver.press("back")
    driver.press("back")
    print("专项答题结束.")


def two_fight_question():
    print("双人对战开始.")

    def get_question(views):
        i = 7
        question = views[i].info['contentDescription']
        while len(question) < 5 or question in '还有一题就赢了，冲啊' or question in'快赢了，同学你要加油鸭！':
            i = i + 1
            question = views[i].info['contentDescription']
        return question

    def two_fight_answer():
        views = driver(className="android.view.View")
        views[8].click()
        time.sleep(10)
        score = "0"
        try:
            while score != "100":
                views = driver(className="android.view.View")
                time.sleep(3)
                score = views[3].info['contentDescription']
                print("当前得分:" + score)
                question = get_question(views)
                list_views = driver(className="android.widget.ListView").child(className="android.view.View")
                options = []
                for i in range(len(list_views)):
                    i = 1 + 2 * (i)
                    if i > len(list_views): break
                    options.append(list_views[i].info['contentDescription'])
                answer = _query_api_(question.split(".")[1], options)
                print("查询的答案是:%s" % answer)
                if (answer is not None):
                    for option in options:
                        if answer in option:
                            driver(description=option).click()
                            break
                    driver(description=options[0]).click()
                else:
                    tip = _search_(question, options)
                    driver(description=tip).click()
        except:
            print("出错")
        finally:
            driver.press("back")

    driver(description="双人对战").sibling(className="android.view.View")[3].click()
    time.sleep(3)
    two_fight_answer()
    time.sleep(3)
    driver.press("back")
    if (driver(description="退出").exists(timeout=5)):
        driver(description="退出").click()
    print("双人对战结束.")


def four_fight_question():
    print("四人对战开始.")

    def get_question(views):
        i = 18
        question = views[i].info['contentDescription']
        while len(question) < 5 or question in '还有一题就赢了，冲啊' or question in '快赢了，同学你要加油鸭！':
            i = i + 1
            question = views[i].info['contentDescription']
        return question

    def four_fight_answer():
        driver(description="开始比赛").click()
        time.sleep(10)
        score = "0"
        try:
            while score != "100":
                views = driver(className="android.view.View")
                time.sleep(3)
                score = views[3].info['contentDescription']
                question = get_question(views)
                list_views = driver(className="android.widget.ListView").child(className="android.view.View")
                options = []
                for i in range(len(list_views)):
                    i = 1 + 2 * (i)
                    if i > len(list_views): break
                    options.append(list_views[i].info['contentDescription'])
                if "." in question:
                    answer = _query_api_(question.split(".")[1], options)
                else:
                    answer = _query_api_(question, options)
                print("查询的答案是:%s" % answer)
                if (answer is not None):
                    for option in options:
                        if answer in option:
                            driver(description=option).click()
                            break
                    driver(description=options[0]).click()
                else:
                    tip = _search_(question, options)
                    driver(description=tip).click()
        except:
            print("出错")
        finally:
            driver.press("back")

    driver(description="四人赛").sibling(className="android.view.View")[3].click()
    time.sleep(3)
    four_fight_answer()
    driver.press("back")
    print("四人对战结束.")


def challenge_question():
    print("挑战答题开始.")

    def challenge_question_answer():
        views = driver(className="android.view.View")
        question = views[2].info['contentDescription']
        print(question)
        list_views = driver(className="android.widget.ListView").child(className="android.view.View")
        options = []
        for i in range(len(list_views)):
            i = 1 + 2 * (i)
            if i > len(list_views): break
            options.append(list_views[i].info['contentDescription'])
        answer = _query_api_(question, options)
        if (answer is not None and driver(description=answer).exists):
            driver(description=answer).click()
        else:
            tips = _search_(question, options)
            driver(description=tips).click()
        time.sleep(3)
        if (driver(description="结束本局").exists(timeout=5)): driver(description="结束本局").click()

    driver(description="挑战答题").sibling(className="android.view.View")[3].click()
    time.sleep(5)
    for i in range(6):
        try:
            challenge_question_answer()
        except:
            print("出错")
        finally:
            break
    time.sleep(50)
    if (driver(description="结束本局").exists(timeout=5)): driver(description="结束本局").click()
    time.sleep(3)
    driver.press("back")
    print("挑战答题结束.")


def answer():
    # 去积分页面
    goto_score_page()
    # 每日答题
    daily_question()
    # 每周答题
    weekly_question()
    # 专项答题
    special_question()
    # 挑战答题
    challenge_question()
    # 双人对战
    two_fight_question()
    # 四人对战
    for i in range(2):
        four_fight_question()


def get_score_and_send_email():
    driver.press("back")
    driver.press("back")
    goto_score_page(swipe=False)
    score = driver(descriptionContains="今日已累积").info['contentDescription']
    print(score)
    send_email(score)


if __name__ == '__main__':
    password = sys.argv[1]
    # 自动打开学习强国
    driver.app_start('cn.xuexi.android')
    time.sleep(5)
    # 屏幕高度
    Height = driver.info['displayHeight']
    Width = driver.info['displayWidth']
    login(password)
    watch_local()
    watch_video()
    read_articles()
    #
    # 100天后删除最早一天的记录
    text_list = np.array(all_of_list)
    if len(text_list) > 2500:
        text_list = text_list[25:]
    # 存储已看视频和文章
    np.save('db.npy', text_list)
    # 回答问题
    answer()
    # 获取今日积分并发送邮件
    get_score_and_send_email()
    # 关闭app
    driver.app_stop("cn.xuexi.android")
