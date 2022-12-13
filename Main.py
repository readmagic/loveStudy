# coding: utf-8
import time
import traceback
import AnswerTask
import AnswerUpdator
import Config
import DBHelper
import Notifier
import SimulateHelper
import TimerTask
import schedule


def login(mobile, pwd):
    try:
        time.sleep(4)
        if (Config.DRIVER(text="登录").exists(timeout=5)):
            Config.DRIVER.click(0.875, 0.424)
            time.sleep(4)
            Config.DRIVER.click(0.463, 0.425)
            SimulateHelper.send_keys(mobile)
            Config.DRIVER.click(0.433, 0.53)
            time.sleep(4)
            SimulateHelper.send_keys(pwd)
            time.sleep(2)
            Config.DRIVER(text="登录").click()
            time.sleep(2)
            print("登录完成")
        else:
            print("已登录")
    except BaseException:
        traceback.print_exc()
        print("已登录")


def task(mobile, password):
    Config.DRIVER.app_stop("cn.xuexi.android")
    time.sleep(3)
    Config.DRIVER.app_start('cn.xuexi.android')
    login(mobile, password)
    WIDTH = Config.DRIVER.info['displayWidth']
    HEIGHT = Config.DRIVER.info['displayHeight']
    SimulateHelper.WIDTH = WIDTH
    SimulateHelper.HEIGHT = HEIGHT

    # 取消新版本体验
    if (Config.DRIVER(text="取消").exists(timeout=5)):
        Config.DRIVER(text="取消").click()
        time.sleep(3)

    # 看上海本地视频,看10个视频,12篇文章
    TimerTask.watch_and_read(mobile, '上海', '东方卫视', 10, 12)
    AnswerTask.answer(mobile)
    # todo 每周答题
    # weekly_wapper()


def one_account(mobile, password):
    all_step = ["watch_local_video",
                "watch_video",
                "read_articles",
                "daily_question",
                "special_question",
                "challenge_question",
                "two_fight_question",
                "four_fight_question",
                # "weekly_question"
                ]
    for i in range(Config.MAX_TRY):
        if DBHelper.has_none_step(all_step, mobile) is False:
            try:
                task(mobile, password)
            except:
                traceback.print_exc()
                continue
    Notifier.notify(mobile)


def main():
    try:
        AnswerUpdator.update()
    except:
        traceback.print_exc()
    for account in Config.ACCOUNTS:
        try:
            one_account(account, Config.PWD)
        except:
            continue


schedule.every().day.at(Config.SCHEDULE_TIME).do(main)
if __name__ == '__main__':
    main()
    print("程序已启动,每天" + Config.SCHEDULE_TIME + "执行")
    while True:
        schedule.run_pending()  # 运行所有可以运行的任务
        time.sleep(1)
