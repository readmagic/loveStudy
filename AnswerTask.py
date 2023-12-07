# coding: utf-8
import QuestionUtil
import SimulateHelper
import AnswerHelper
import DBHelper
import Config
import time
import random


def answer(mobile):
    def get_weekday():
        weekday = time.strftime("%w")
        return weekday

    weekday = get_weekday()

    # 去积分页面
    SimulateHelper.goto_score_page()
    SimulateHelper.swipe_question()

    Config.DRIVER(text="去看看").click()
    time.sleep(2)

    if weekday == '4':
        # 四人对战
        has_four_fight_question = DBHelper.get_record_from_db(mobile, Config.TODAY, "interest_question")
        if has_four_fight_question is None:
            for i in range(2):
                is_ok = __four_fight_question__()
                if is_ok:
                    DBHelper.insert_record_to_db(mobile, Config.TODAY, "interest_question")
                    break

    # # 每日答题
    # has_daily_question = DBHelper.get_record_from_db(mobile, Config.TODAY, "interest_question")
    # if has_daily_question is None:
    #     if __daily_question__():
    #         DBHelper.insert_record_to_db(mobile, Config.TODAY, "interest_question")
    #
    # time.sleep(8)
    # # 专项答题
    # has_special_question = DBHelper.get_record_from_db(mobile, Config.TODAY, "interest_question")
    # if has_special_question is None:
    #     if __special_question__():
    #         DBHelper.insert_record_to_db(mobile, Config.TODAY, "interest_question")
    # # 挑战答题
    # has_challenge_question = DBHelper.get_record_from_db(mobile, Config.TODAY, "interest_question")
    # if has_challenge_question is None:
    #     if __challenge_question__():
    #         DBHelper.insert_record_to_db(mobile, Config.TODAY, "interest_question")
    #
    # if Config.MOBILE_TYPE == "MI6":
    #     SimulateHelper.swipe_down_small()
    #
    # if Config.MOBILE_TYPE == "MI6":
    #     SimulateHelper.swipe_down_small()
    # # 双人对战
    # has_two_fight_question = DBHelper.get_record_from_db(mobile, Config.TODAY, "interest_question")
    # if has_two_fight_question is None:
    #     if __two_fight_question__():
    #         DBHelper.insert_record_to_db(mobile, Config.TODAY, "interest_question")


def __daily_question__():
    print("每日答题开始.")

    def daily_question_answer():
        time.sleep(5)
        views = Config.DRIVER(className="android.view.View")

        question_type = QuestionUtil.get_question_type(views)
        # 单选题 多选题 填空题
        question = QuestionUtil.get_question_text(views)
        print(question)
        if ("单选题" == question_type):
            list_views = Config.DRIVER(className="android.widget.ListView").child(className="android.view.View")
            options = QuestionUtil.get_answer_option(list_views)
            answer = AnswerHelper.query_answer(question, options)
            if (answer is not None and Config.DRIVER(text=answer).exists):
                Config.DRIVER(text=answer).click()
            else:
                tips = AnswerHelper.search_answer(question, options)
                Config.DRIVER(text=tips).click()
            time.sleep(5)
            Config.DRIVER(text="确定").click()
            time.sleep(5)
            if (Config.DRIVER(text="下一题").exists(timeout=5)): Config.DRIVER(text="下一题").click()
            if (Config.DRIVER(text="完成").exists(timeout=5)): Config.DRIVER(text="完成").click()
        elif ("多选题" == question_type):
            list_views = Config.DRIVER(className="android.widget.ListView").child(className="android.view.View")
            options = QuestionUtil.get_answer_option(list_views)
            for option in options:
                Config.DRIVER(text=option).click()
            time.sleep(5)
            Config.DRIVER(text="确定").click()
            time.sleep(5)
            if (Config.DRIVER(text="下一题").exists(timeout=5)): Config.DRIVER(text="下一题").click()
            if (Config.DRIVER(text="完成").exists(timeout=5)): Config.DRIVER(text="完成").click()
        elif ("填空题" == question_type):
            answer = AnswerHelper.query_answer(question)
            print("查询的答案是:%s" % answer)
            if (answer is not None):
                Config.DRIVER(text=question_type).click()
                time.sleep(3)
                Config.DRIVER(text=question).sibling(text="")[2].click()
                SimulateHelper.send_keys(answer)
                Config.DRIVER(text="确定").click()
                time.sleep(5)
                if (Config.DRIVER(text="下一题").exists(timeout=5)): Config.DRIVER(text="下一题").click()
                if (Config.DRIVER(text="完成").exists(timeout=5)): Config.DRIVER(text="完成").click()
            else:
                print(question)
                Config.DRIVER(text="查看提示").click()
                time.sleep(3)
                tmp = Config.DRIVER(textStartsWith=question)
                if (len(tmp) >= 2):
                    tips = tmp[1].info['text']
                    print(tips)
                    tips = tips.replace(question, "")
                    Config.DRIVER(text=question_type).click()
                    time.sleep(3)
                    Config.DRIVER(text=question).sibling(text="")[2].click()
                    SimulateHelper.send_keys(tips)
                    Config.DRIVER(text="确定").click()
                    time.sleep(5)
                    if (Config.DRIVER(text="下一题").exists(timeout=5)): Config.DRIVER(text="下一题").click()
                    if (Config.DRIVER(text="完成").exists(timeout=5)): Config.DRIVER(text="完成").click()
                else:
                    Config.DRIVER(text=question_type).click()
                    time.sleep(3)
                    Config.DRIVER(text=question).sibling(text="")[2].click()
                    SimulateHelper.send_keys("I Have No Answer")
                    Config.DRIVER(text="确定").click()
                    time.sleep(5)
                    if (Config.DRIVER(text="下一题").exists(timeout=5)): Config.DRIVER(text="下一题").click()
                    if (Config.DRIVER(text="完成").exists(timeout=5)): Config.DRIVER(text="完成").click()

    x, y = SimulateHelper.getMobileXY('daily_question')
    x1, y1 = SimulateHelper.getXY(x, y)
    # SimulateHelper.swipe_down_small()
    Config.DRIVER.click(x1, y1)
    time.sleep(5)
    is_ok = True
    for i in range(5):
        try:
            daily_question_answer()
        except:
            Config.DRIVER.press("back")
            is_ok = False
            break
    time.sleep(5)
    if Config.DRIVER(text="返回"): Config.DRIVER(text="返回").click()
    print("每日答题结束.")
    return is_ok


def __special_question__():
    print("专项答题开始.")

    def special_question_answer():
        time.sleep(5)
        views = Config.DRIVER(className="android.view.View")
        question_type = QuestionUtil.get_question_type(views)
        question = QuestionUtil.get_question_text(views)
        print(question)
        SimulateHelper.swipe_down()
        if question_type is None:
            return
        if ("单选题" in question_type):
            list_views = Config.DRIVER(className="android.widget.ListView").child(className="android.view.View")
            options = QuestionUtil.get_answer_option(list_views)
            answer = AnswerHelper.query_answer(question, options)
            if (answer is not None and Config.DRIVER(text=answer).exists):
                Config.DRIVER(text=answer).click()
            else:
                tips = AnswerHelper.search_answer(question, options)
                Config.DRIVER(text=tips).click()
            time.sleep(5)
            if (Config.DRIVER(text="下一题").exists(timeout=5)): Config.DRIVER(text="下一题").click()
            if (Config.DRIVER(text="完成").exists(timeout=5)): Config.DRIVER(text="完成").click()
        elif ("多选题" in question_type):
            list_views = Config.DRIVER(className="android.widget.ListView").child(className="android.view.View")
            options = QuestionUtil.get_answer_option(list_views)
            for option in options:
                Config.DRIVER(text=option).click()
            time.sleep(5)
            if (Config.DRIVER(text="下一题").exists(timeout=5)): Config.DRIVER(text="下一题").click()
            if (Config.DRIVER(text="完成").exists(timeout=5)): Config.DRIVER(text="完成").click()
        elif ("填空题" in question_type):
            answer = AnswerHelper.query_answer(question)
            print("查询的答案是:%s" % answer)
            if (answer is not None):
                Config.DRIVER(text=question_type).click()
                time.sleep(3)
                Config.DRIVER(text=question).sibling(text="")[2].click()
                SimulateHelper.send_keys(answer)
                if (Config.DRIVER(text="下一题").exists(timeout=5)): Config.DRIVER(text="下一题").click()
                if (Config.DRIVER(text="完成").exists(timeout=5)): Config.DRIVER(text="完成").click()
            else:
                print(question)
                Config.DRIVER(text="查看提示").click()
                time.sleep(3)
                tmp = Config.DRIVER(textStartsWith=question)
                if (len(tmp) >= 2):
                    tips = tmp[1].info['text']
                    print(tips)
                    tips = tips.replace(question, "")
                    Config.DRIVER(text=question_type).click()
                    time.sleep(3)
                    Config.DRIVER(text=question).sibling(text="")[2].click()
                    SimulateHelper.send_keys(tips)
                    if (Config.DRIVER(text="下一题").exists(timeout=5)): Config.DRIVER(text="下一题").click()
                    if (Config.DRIVER(text="完成").exists(timeout=5)): Config.DRIVER(text="完成").click()
                else:
                    Config.DRIVER(text=question_type).click()
                    time.sleep(3)
                    Config.DRIVER(text=question).sibling(text="")[2].click()
                    SimulateHelper.send_keys("I Have No Answer")
                    if (Config.DRIVER(text="下一题").exists(timeout=5)): Config.DRIVER(text="下一题").click()
                    if (Config.DRIVER(text="完成").exists(timeout=5)): Config.DRIVER(text="完成").click()

    Config.DRIVER.click(0.864, 0.702)
    time.sleep(5)
    is_ok = True

    def search_start_question(i):
        if (Config.DRIVER(text="开始答题").exists(timeout=2)):
            Config.DRIVER(text="开始答题").click()
            for i in range(10):
                try:
                    special_question_answer()
                except:
                    Config.DRIVER.press("back")
                    break
            time.sleep(5)
            Config.DRIVER.press("back")
        else:
            if i > Config.SCORE_TIMES:
                Config.DRIVER.press("back")
            else:
                SimulateHelper.swipe_down()
                search_start_question(i + 1)

    search_start_question(0)
    Config.DRIVER.press("back")
    print("专项答题结束.")
    return is_ok


# def weekly_question():
#     print("每周答题开始.")
#
#     def weekly_question_answer():
#         time.sleep(5)
#         views = driver(className="android.view.View")
#         question_type = __get_question_type__(views)
#         question = __get_question__(views)
#         print(question)
#         if question_type is None:
#             return
#         if ("单选题" in question_type):
#             list_views = driver(className="android.widget.ListView").child(className="android.view.View")
#             options = __get_answer__(list_views)
#             answer = _query_api_(question, options)
#             if (answer is not None and driver(text=answer).exists):
#                 driver(text=answer).click()
#             else:
#                 tips = _search_(question, options)
#                 driver(text=tips).click()
#             time.sleep(5)
#             if (driver(text="确定").exists(timeout=5)): driver(text="确定").click()
#             if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
#             if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
#         elif ("多选题" in question_type):
#             list_views = driver(className="android.widget.ListView").child(className="android.view.View")
#             options = __get_answer__(list_views)
#             for option in options:
#                 driver(text=option).click()
#             time.sleep(5)
#             if (driver(text="确定").exists(timeout=5)): driver(text="确定").click()
#             if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
#             if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
#         elif ("填空题" in question_type):
#             answer = _query_api_(question)
#             print("查询的答案是:%s" % answer)
#             if (answer is not None):
#                 driver(text=question_type).click()
#                 time.sleep(3)
#                 driver(text=question).sibling(text="")[2].click()
#                 send_keys(answer)
#                 if (driver(text="确定").exists(timeout=5)): driver(text="确定").click()
#                 if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
#                 if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
#             else:
#                 print(question)
#                 driver(text="查看提示").click()
#                 time.sleep(3)
#                 tmp = driver(textStartsWith=question)
#                 if (len(tmp) >= 2):
#                     tips = tmp[1].info['text']
#                     print(tips)
#                     tips = tips.replace(question, "")
#                     driver(text=question_type).click()
#                     time.sleep(3)
#                     driver(text=question).sibling(text="")[2].click()
#                     send_keys(tips)
#                     if (driver(text="确定").exists(timeout=5)): driver(text="确定").click()
#                     if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
#                     if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
#                 else:
#                     driver(text=question_type).click()
#                     time.sleep(3)
#                     driver(text=question).sibling(text="")[2].click()
#                     send_keys("我不知道这个答案")
#                     if (driver(text="确定").exists(timeout=5)): driver(text="确定").click()
#                     if (driver(text="下一题").exists(timeout=5)): driver(text="下一题").click()
#                     if (driver(text="完成").exists(timeout=5)): driver(text="完成").click()
#
#     x,y = getMobileXY("weekly_question")
#     x, y = getXY(x,y)
#     driver.click(x, y)
#     time.sleep(5)
#     if (driver(text="未作答").exists(timeout=5)):
#         driver(text="未作答").click()
#         for i in range(5):
#             weekly_question_answer()
#         time.sleep(5)
#         driver(text="返回").click()
#     driver.press("back")
#     print("每周答题结束.")


def __two_fight_question__():
    print("双人对战开始.")

    def two_fight_answer():
        Config.DRIVER(text="随机匹配").sibling()[0].click()
        time.sleep(10)
        score = "0"
        try:
            while score != "100":
                views = Config.DRIVER(className="android.view.View")
                time.sleep(2)
                score = views[11].info['text']
                print("当前得分:" + score)
                optionsEL = Config.DRIVER(className="android.widget.RadioButton")
                if len(optionsEL) == 0:
                    Config.DRIVER.press("back")
                try:
                    time.sleep(2)
                    Config.DRIVER().screenshot().save("ocr.png")
                    (question, options) = AnswerHelper.ocr("ocr.png")
                    if question is not None and len(question) > 0 and len(options) > 0:
                        print("题目:" + question)
                        answer = DBHelper.get_two_four_question_from_db(question, options)
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
            Config.DRIVER.press("back")

    x, y = SimulateHelper.getMobileXY("two_fight_question")
    x1, y1 = SimulateHelper.getXY(x, y)
    Config.DRIVER.click(x1, y1)
    time.sleep(3)
    is_ok = True
    two_fight_answer()
    time.sleep(3)
    Config.DRIVER.press("back")
    if (Config.DRIVER(text="退出").exists(timeout=5)):
        Config.DRIVER(text="退出").click()
    print("双人对战结束.")
    return is_ok


def __four_fight_question__():
    print("四人对战开始.")

    def four_fight_answer():
        Config.DRIVER(text="开始比赛").click()
        time.sleep(10)
        score = "0"
        try:
            while score != "100":
                views = Config.DRIVER(className="android.view.View")
                time.sleep(2)
                score = views[10].info['text']
                print("当前得分:" + score)
                optionsEL = Config.DRIVER(className="android.widget.RadioButton")
                if len(optionsEL) == 0:
                    Config.DRIVER.press("back")
                try:
                    time.sleep(2)
                    Config.DRIVER().screenshot().save("ocr.png")
                    (question, options) = AnswerHelper.ocr("ocr.png")
                    if question is not None and len(question) > 0 and len(options) > 0:
                        print("题目:" + question)
                        answer = DBHelper.get_two_four_question_from_db(question, options)
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
    x, y = SimulateHelper.getMobileXY("four_fight_question")
    x1, y1 = SimulateHelper.getXY(x, y)
    Config.DRIVER.click(x1, y1)
    time.sleep(3)
    is_ok = True
    four_fight_answer()
    Config.DRIVER.press("back")
    print("四人对战结束.")
    return is_ok


def __challenge_question__():
    print("挑战答题开始.")

    def challenge_question_answer():
        views = Config.DRIVER(className="android.view.View")
        question = views[14].info['text']
        print(question)
        list_views = Config.DRIVER(className="android.widget.ListView").child(className="android.view.View")
        options = []
        for i in range(len(list_views)):
            if i > len(list_views): break
            if (len(list_views[i].info['text'])) > 0:
                options.append(list_views[i].info['text'])
        answer = AnswerHelper.query_answer(question, options)
        if (answer is not None and Config.DRIVER(text=answer).exists):
            Config.DRIVER(text=answer).click()
        else:
            tips = AnswerHelper.search_answer(question, options)
            Config.DRIVER(text=tips).click()
        time.sleep(3)
        if (Config.DRIVER(text="结束本局").exists(timeout=5)): Config.DRIVER(text="结束本局").click()

    x, y = SimulateHelper.getMobileXY("challenge_question")
    x1, y1 = SimulateHelper.getXY(x, y)
    Config.DRIVER.click(x1, y1)
    time.sleep(5)
    is_ok = True
    for i in range(6):
        try:
            challenge_question_answer()
        except:
            is_ok = False
            print("出错")
            continue
    time.sleep(50)
    if (Config.DRIVER(text="结束本局").exists(timeout=5)): Config.DRIVER(text="结束本局").click()
    time.sleep(3)
    Config.DRIVER.press("back")
    print("挑战答题结束.")
    return is_ok
