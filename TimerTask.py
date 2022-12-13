# coding: utf-8
import Config
import time
import SimulateHelper
import DBHelper
import traceback


def watch_and_read(mobile, location, tv, video_num, article_num):
    has_watched_local_video = DBHelper.get_record_from_db(mobile, Config.TODAY, "watch_local_video")
    if has_watched_local_video is None:
        _watch_local_video_(location, tv)
        DBHelper.insert_record_to_db(mobile, Config.TODAY, "watch_local_video")

    has_watched_video = DBHelper.get_record_from_db(mobile, Config.TODAY, "watch_video")
    if has_watched_video is None:
        _watch_video_(video_num,mobile)
        DBHelper.insert_record_to_db(mobile, Config.TODAY, "watch_video")

    has_read_articles = DBHelper.get_record_from_db(mobile, Config.TODAY, "read_articles")
    if has_read_articles is None:
        _read_articles_(article_num,mobile)
        DBHelper.insert_record_to_db(mobile, Config.TODAY, "read_articles")
def _watch_local_video_(location, tv):
    Config.DRIVER(text=location).click()
    time.sleep(8)
    Config.DRIVER(text=tv).click()
    print("观看本地频道...")
    time.sleep(20)
    print("本地频道结束.")
    Config.DRIVER.press("back")
def _read_articles_(num,mobile):
    time.sleep(2)
    # 切换到要闻界面
    Config.DRIVER(resourceId="cn.xuexi.android:id/home_bottom_tab_button_work").click()
    Config.DRIVER(text='要闻').click()
    __autoJob__(mobile=mobile,tv="阅读文章", sum=num, sleep_time=60)
    print("阅读文章结束.")

def _watch_video_(num,mobile):
    time.sleep(2)
    # 切换到百灵页面
    Config.DRIVER(resourceId="cn.xuexi.android:id/home_bottom_tab_button_ding").click()
    Config.DRIVER(text="党史").click()
    __autoJob__(mobile = mobile,tv="观看视频", sleep_time=60, sum=num, discuss=False)
    print("观看视频结束.")


def __autoJob__(mobile,tv, sleep_time, sum=6, discuss=True):
    count_click = 0
    count = 0
    read_articles = DBHelper.find_article_from_db(mobile)
    for _ in range(100):
        try:
            text_lists = Config.DRIVER(className='android.widget.TextView')
            for i in range(len(text_lists)):
                txt = text_lists[i].info['text']
                if len(txt) > 10 and txt not in read_articles and count < sum:
                    Config.DRIVER(text=txt).click()
                    # 分享，收藏，评论
                    if discuss and count_click < 1:
                        # 评论
                        time.sleep(3)
                        Config.DRIVER(text="欢迎发表你的观点").click()
                        SimulateHelper.send_keys("Chinese is good")
                        Config.DRIVER.press('enter')
                        time.sleep(2)
                        Config.DRIVER(text="发布").click()
                        time.sleep(1)
                        count_click = count_click + 1
                        # 删除发布的评论
                        time.sleep(2)
                        Config.DRIVER(text="删除").click()
                        time.sleep(2)
                        Config.DRIVER(text="确认").click()

                    count = count + 1
                    print("正在" + tv + "...", txt)
                    time.sleep(sleep_time)
                    Config.DRIVER.press("back")
                    time.sleep(3)
                    DBHelper.insert_article_to_db(mobile,txt)
            if count >= sum:
                break
            SimulateHelper.swipe_down()
        except Exception:
            traceback.print_exc()
            continue