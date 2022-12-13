# coding: utf-8
import Config
import hashlib
import requests
import DBHelper
__HARD_LINE__ = {
    'D 离别是中国古典诗词中常用的主题，以下诗句中无离别之意的是“        ”。 海内存知己，天涯若比邻。	燕燕于飞，差池其羽。之子于归，远送于野。	莫愁前路无知己，天下谁人不识君。	返景入深林，复照青苔上。': (
        "离别是中国古典诗词中常用的主题，以下诗句中无离别之意的是“        ”。",
        [" 海内存知己，天涯若比邻。", "燕燕于飞，差池其羽。之子于归，远送于野。", "莫愁前路无知己，天下谁人不识君。",
         "返景入深林，复照青苔上。"], "D"),
    'B 世界第一个永久极地考察站是         俄罗斯站	奥尔卡德斯站	长城站	阿蒙森-斯科特站': (
        "世界第一个永久极地考察站是         俄罗斯站", ["奥尔卡德斯站", "长城站", "阿蒙森-斯科特站"], "B"),
    "C “学习强国”APP的开机页提示语是《论语》中的哪一句话？         三人行，必有我师焉。	学而不思则罔，思而不学则殆。	学而时习之，不亦说乎。	敏而好学，不耻下问。": (
        "学习强国”APP的开机页提示语是《论语》中的哪一句话？",
        ["三人行，必有我师焉。", "学而不思则罔，思而不学则殆。", "学而时习之，不亦说乎。", "敏而好学，不耻下问。"], "C"),
    "C 以下诗句由王勃所作的是“        ”。 君自故乡来，应知故乡事。	海上生明月，天涯共此时。	海内存知己，天涯若比邻。	红豆生南国，春来发几枝。": (
        "以下诗句由王勃所作的是“        ”。",
        ["君自故乡来，应知故乡事。", "海上生明月，天涯共此时。", "红豆生南国，春来发几枝。"], "C"),
    "A “山近月远觉月小，便道此山大于月。若有人眼大如天，当见山高月更阔。”这是明代思想家王守仁的《蔽月山房》，与此中哲理最接近的是“        ”。 不识庐山真面目，只缘身在此山中。	纸上得来终觉浅，绝知此事要躬行。	若言声在指头上，何不于君指上听？	问渠那得清如许，为有源头活水来。": (
        "“山近月远觉月小，便道此山大于月。若有人眼大如天，当见山高月更阔。”这是明代思想家王守仁的《蔽月山房》，与此中哲理最接近的是“        ”。",
        ["不识庐山真面目，只缘身在此山中。", "纸上得来终觉浅，绝知此事要躬行。", "若言声在指头上，何不于君指上听？",
         "问渠那得清如许，为有源头活水来。"], "A"),
    "D 离别是中国古典诗词中常用的主题。以下诗句中，无离别之意的是？         海内存知己，天涯若比邻。	燕燕于飞，差池其羽。之子于归，远送于野。	莫愁前路无知己，天下谁人不识君。	返景入深林，复照青苔上。": (
        "离别是中国古典诗词中常用的主题。以下诗句中，无离别之意的是？",
        ["海内存知己，天涯若比邻。", "燕燕于飞，差池其羽。之子于归，远送于野。", "莫愁前路无知己，天下谁人不识君。",
         "返景入深林，复照青苔上。"],
        "D"),
    "B 青头潜鸭是国家I级重点保护动物，IUCN（世界自然保护联盟）物种红色名录濒危等级——        。来源：《江苏珍稀特色动植物图鉴》（南京师范大学出版社2021年版） 易危（VU）	极危（CR）	濒危（EN）	近危（NT）": (
        "青头潜鸭是国家I级重点保护动物，IUCN（世界自然保护联盟）物种红色名录濒危等级——",
        ["易危（VU）", "极危（CR）", "濒危（EN）", "近危（NT）"], "B"),
    "C 云冈石窟是中国北方地区的佛教石窟寺，与        、        并为中国北朝大石窟的代表，1961年国务院公布为全国重点文物保护单位。来源：《中国大百科全书（考古学）》（第一版）（中国大百科全书出版社） 响堂山石窟 龙门石窟	敦煌石窟 响堂山石窟	敦煌石窟 龙门石窟": (
        "云冈石窟是中国北方地区的佛教石窟寺，与        、        并为中国北朝大石窟的代表，1961年国务院公布为全国重点文物保护单位。",
        ["响堂山石窟 龙门石窟", "敦煌石窟 响堂山石窟", "敦煌石窟 龙门石窟"], "C"),
    "B 内分泌疾病        ，主要指甲状腺在多种因素作用下，合成和分泌甲状腺素的量减少，从而出现诸多器官功能降低的症状和体征，如心率减慢、腹胀、记忆力减退、头发干燥、皮肤粗糙和反应迟缓等。来源：《十万个为什么》（第六版）（上海世纪出版股份有限公司少年儿童出版社2014年版） 甲状腺功能亢进症（简称甲亢）	甲状腺功能减退症（简称甲减）": (
        "内分泌疾病        ，主要指甲状腺在多种因素作用下，合成和分泌甲状腺素的量减少，从而出现诸多器官功能降低的症状和体征，如心率减慢、腹胀、记忆力减退、头发干燥、皮肤粗糙和反应迟缓等。",
        ["甲状腺功能亢进症（简称甲亢）", "甲状腺功能减退症（简称甲减）"], "B")
}

def __parse_hard_line__(line):
    hard_result = __HARD_LINE__.get(line)
    if hard_result is not None:
        question = hard_result[0]
        options = hard_result[1]
        answer = hard_result[2]
        return (question, options, options[ord(answer) - 65])
    return (None, None, None)

def __parse_line__(line):
    if '来源：' in line:
        x = line.split("来源：")
        question_and_answer = x[0]
        answer = question_and_answer.split(" ")[0]
        question = question_and_answer.replace(answer + " ", "")
        right_paren_index = x[1].count("）")
        if right_paren_index > 2:
            right_paren_index = 2
        options = x[1].split("）")[right_paren_index].split()
        if line.endswith("）"):
            options[len(options) - 1] = options[len(options) - 1] + "）"
        return (question, options, options[ord(answer) - 65])
    if "。" in line:
        full_stop_index = line.count("。")
        x = line.split("。")
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
    if line in __HARD_LINE__:
        __parse_hard_line__(line)

def __two_four_answer_update__():
    def exist(question):
        str = "SELECT id FROM two_four_question WHERE question='%s'" % (question)
        rows = Config.MY_CURSOR.execute(str)
        for row in rows:
            return row[0]
        return None

    def insert_db(question, options, answer):
        if exist(question) is None:
            str = "INSERT INTO two_four_question (question,options,answer) VALUES ('%s','%s','%s')" % (
                question, "|".join(options), answer)
            Config.MY_CURSOR.execute(str)
            Config.MY_CONN.commit()

    def parse_and_insert(rows):
        for row in rows.split("\n"):
            try:
                (question, options, answer) = __parse_line__(row)
            except:
                (question, options, answer) = __parse_hard_line__(row)
            if question is not None:
                insert_db(question, options, answer)
            else:
                print(row)

    response = requests.get(Config.TWO_FOUR_ANSWER)
    md5 = hashlib.md5(response.text.encode(encoding='UTF-8')).hexdigest()
    version = DBHelper.get_version_from_db(md5, "TWO_FOUR_ANSWER")
    if version is None:
        parse_and_insert(response.text)
        DBHelper.insert_version_to_db(md5, "TWO_FOUR_ANSWER")

def __challenge_answer_update__():
    response = requests.get(Config.CHALLENGE_ANSWER)
    md5 = hashlib.md5(response.text.encode(encoding='UTF-8')).hexdigest()
    version = DBHelper.get_version_from_db(md5, "CHALLENGE_ANSWER")
    if version is None:
        challenge_answer_json = response.json()
        for question, answer in challenge_answer_json.items():
            question= question.replace("\xa0","")
            exist = DBHelper.get_challenge_question_from_db(question)
            if(exist is None):
                DBHelper.insert_challenge_question_to_db(question,answer)
        DBHelper.insert_version_to_db(md5, "CHALLENGE_ANSWER")

def update():
    __two_four_answer_update__()
    __challenge_answer_update__()

