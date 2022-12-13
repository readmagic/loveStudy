# coding: utf-8
import Config
import time
import random
import os
WIDTH=0
HEIGHT = 0
def send_keys(tips):
    time.sleep(5)
    Config.DRIVER.set_fastinput_ime(True)
    time.sleep(5)
    Config.DRIVER.send_keys(tips)

def swipe_down():

    x1 = random.randint(int(WIDTH / 10) * 3, int(WIDTH / 10) * 7)
    y1 = random.randint(int(HEIGHT / 20) * 16, int(HEIGHT / 20) * 17)
    x2 = random.randint(int(WIDTH / 10) * 3, int(WIDTH / 10) * 7)
    y2 = random.randint(int(HEIGHT / 20) * 2, int(HEIGHT / 20) * 3)
    drag_str = Config.ADB_PATH + ' shell input swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(
        x2) + ' ' + str(y2)
    os.system(drag_str)
    time.sleep(5)

def getXY(x, y):
    return (WIDTH / 560 - x, HEIGHT / 1800 - 1 - y)

def goto_score_page():
    Config.DRIVER(resourceId="cn.xuexi.android:id/comm_head_xuexi_score").click()
    time.sleep(10)
def swipe_question():
    x1 = WIDTH / 10 * 3
    y1 = HEIGHT / 20 * 12
    x2 = WIDTH / 10 * 3
    y2 = HEIGHT / 20 * 2
    drag_str = Config.ADB_PATH + ' shell input swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(
        x2) + ' ' + str(y2)
    os.system(drag_str)
    time.sleep(5)
def swipe_down_small():
    x1 = 300
    y1 = 1600
    x2 = 200
    y2 = 1300
    drag_str = Config.ADB_PATH + ' shell input swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(
        x2) + ' ' + str(y2)
    os.system(drag_str)
    time.sleep(5)

def getMobileXY(key):
    MI_11_XY = {
        # 0.851, 0.163
        "daily_question": (2.04, 0.28),
        # 0.858, 0.305
        "special_question": (2.04, 0.13),
        # 0.895, 0.728
        "two_fight_question": (2.0, -0.3),
        # 0.851, 0.588
        "four_fight_question": (2.04, -0.16),
        # 0.888, 0.458
        "challenge_question": (2.0, 0),
        # 0.885, 0.858
        "subscribe": (2.01, -0.42),
        # 0.871, 0.874
        "weekly_question": (2.02, -0.43),
    }
    MI_6_XY = {
        # 0.9, 0.514
        "daily_question": (1.05, -0.428),
        # 0.897, 0.696
        "special_question": (1.02, -0.6),
        # 0.894, 0.934
        "two_fight_question": (1.02, -0.85),
        # 0.867, 0.901
        "four_fight_question": (1.05, -0.82),
        # 0.878, 0.915
        "challenge_question": (1.05, -0.83),

        "subscribe": (2.01, -0.42),
        "weekly_question": (2.02, -0.43),
    }

    if Config.MOBILE_TYPE == "MI11":
        return MI_11_XY[key]
    else:
        return MI_6_XY[key]