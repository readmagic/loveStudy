# coding: utf-8
import sys

from uiautomator import device as driver
import qrcode
import os

Height = 1280
Width = 720
EXE = 'D:\\xxqg\\study.exe'
TOKEN='D:\\xxqg\\token.txt'


def login(pwd):
    try:
        driver(text="登录").click()
        driver.click(0.5 * Width, 0.42 * Height)
        time.sleep(1)
        os.system("adb shell am broadcast -a ADB_INPUT_TEXT --es msg '%s'" % pwd)
        time.sleep(1)
        driver(text="登录").click()
        time.sleep(2)
    except BaseException:
        print("已登录")
    else:
        print('正在登录')


def send_email():
    from email.header import Header
    from email.mime.multipart import MIMEMultipart
    from email.mime.image import MIMEImage
    msg = MIMEMultipart()
    msg['Subject'] = Header('学习强国', 'utf-8').encode()
    msg['from'] = '249113537@163.com'
    msg['to'] = '303734023@qq.com'

    file = open("a.png", "rb")
    img_data = file.read()
    file.close()
    img = MIMEImage(img_data)
    img.add_header('Content-Disposition', 'attachment', filename="a.png")
    msg.attach(img)

    user = '249113537@163.com'
    password = 'DSFRXHYIZUWQYODP'
    smtp_server = 'smtp.163.com'
    to_addr = 'jinrongfrandy@qq.com'
    import smtplib
    server = smtplib.SMTP(smtp_server, 25)  # Smtp协议默认窗口是25
    server.login(user, password)
    server.sendmail(user, to_addr, msg.as_string())
    server.quit()


def autoJob(tv, sleep_time, sum=6, click=True):
    count_click = 0
    count = 0
    drag_str = 'adb shell input swipe ' + str(Width * 0.5) + ' ' + str(Height * 0.88) + ' ' + str(
        Width * 0.5) + ' ' + str(Height * 0.3)
    for _ in range(100):
        text_lists = driver(className='android.widget.TextView')
        try:
            for i in range(len(text_lists)):
                txt = text_lists[i].text
                if len(txt) > 11  and count < sum:
                    driver(text=txt, className='android.widget.TextView').click()
                    # 分享，收藏，评论
                    if click and count_click < 2:
                        # 分享
                        time.sleep(4)
                        driver.click(0.94 * Width, 0.975 * Height)
                        time.sleep(2)
                        driver(text="分享到学习强国").click()
                        time.sleep(2)
                        driver.press.back()
                        # 评论
                        time.sleep(1)
                        driver(text="欢迎发表你的观点").click()
                        time.sleep(2)
                        os.system("adb shell am broadcast -a ADB_INPUT_TEXT --es msg '中国加油！全力支持'")
                        os.system("adb shell input keyevent 66")  # 不知道为什么输入一个回车，点击发布才有反应
                        time.sleep(2)
                        driver.click(0.94 * Width, 0.864 * Height)
                        count_click = count_click + 1
                        # 删除发布的评论
                        time.sleep(2)
                        driver(text="删除").click()
                        time.sleep(2)
                        driver(text="确认").click()

                    count = count + 1
                    print("正在" + tv + "...", txt)
                    time.sleep(sleep_time)
                    driver.press.back()
        except BaseException:
            print("抛出异常，程序继续执行...")
        if count >= sum:
            break
        os.system(drag_str)


def watch_local():
    driver(text='北京').click()
    time.sleep(2)
    driver(text='北京卫视').click()
    print("观看本地频道...")
    time.sleep(20)
    print("本地频道结束")
    driver.press.back()


# 阅读文章,阅读6个文章，每个文章停留130秒
def read_articles():
    time.sleep(2)
    # 切换到要闻界面
    driver(text='新思想').click()
    autoJob(tv="阅读文章",sum=2, sleep_time=30)




def end_program(pro_name):
    os.system('%s%s' % ("taskkill /F /IM ", pro_name))


import requests, time, logging


def retry(times: int, interval: int):
    def wrapper(func):
        def inner(*args, **kwarys):
            v = None
            for _ in range(times):
                try:
                    v = func(*args, **kwarys)
                except Exception as err:
                    logging.error(str(err))
                    time.sleep(interval)
                    continue
                break
            return v

        return inner

    return wrapper


session = requests.Session()


@retry(times=100, interval=1)
def getQrcode():
    qr = session.get('https://login.xuexi.cn/user/qrcode/generate').json()['result']
    url = "https://login.xuexi.cn/login/qrcommit?showmenu=false&code={qr}&appId=dingoankubyrfkttorhpou".format(qr=qr)
    img = qrcode.make(url)
    img.save("a.png")
    return qr


@retry(times=100, interval=1)
def getTmpCode(qrcode: str):
    url = 'https://login.xuexi.cn/login/login_with_qr'
    res = session.post(url, data={
        "qrCode": qrcode,
        "goto": "https://oa.xuexi.cn",
        "pdmToken": ""
    }).json()
    if not res['success']:
        raise Exception(str(res))
    data = res['data']
    key = "loginTmpCode="
    tmpCode = data[data.index(key) + len(key):]
    return tmpCode


@retry(times=100, interval=1)
def getCookies(tmpCode: str):
    url = 'https://pc-api.xuexi.cn/login/secure_check?code={tmpCode}&state=06d81817e84a430fRn3K4e9Temmx7XsXcJVvnBCy7b8DrBR0vkAIQQtA0wCDp0owW5W1o9XkX7aUUZ16'.format(
        tmpCode=tmpCode)
    res = session.get(url)
    cookies = res.cookies
    res = res.json()
    if not res['success']:
        raise Exception(str(res))
    return [{'name': c.name, 'value': c.value, 'domain': c.domain, 'path': c.path} for c in cookies]


@retry(times=100000, interval=1)
def web_login():
    qr = getQrcode()
    send_email()
    tmpCode = getTmpCode(qr)
    cookies = getCookies(tmpCode)
    return cookies


if __name__ == '__main__':
    try:
        password = sys.argv[1]
        # #自动打开学习强国
        os.system('adb shell am start cn.xuexi.android/com.alibaba.android.rimet.biz.SplashActivity')
        time.sleep(5)
        # #屏幕高度
        Height = driver.info['displayHeight']
        Width = driver.info['displayWidth']
        # 切换adb输入法
        os.system('adb shell ime set com.android.adbkeyboard/.AdbIME')
        # login(password)
        # watch_local()
        read_articles()
        # watch_video()
        # 关闭app
        os.system('adb shell am force-stop cn.xuexi.android')
    except Exception:
        print("执行手机端app报错")

    cookies = web_login()
    for cookie in cookies:
        if cookie['name'] == 'token':
            token = cookie['value']
            fo = open(TOKEN, "w")
            fo.write("token=" + token + "; domain=.xuexi.cn; path=/")
            fo.close()
            break
    os.system('start ' + EXE)
    time.sleep(500)
    end_program('study.exe')

