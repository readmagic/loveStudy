# coding: utf-8
import Config
import requests
import base64
import difflib
import string
from urllib.parse import quote
import traceback
import DBHelper
def ocr(file_path):
    def fetch_token():
        params = {'grant_type': 'client_credentials',
                  'client_id': Config.API_KEY,
                  'client_secret': Config.SECRET_KEY}
        response = requests.post(Config.TOKEN_URL, params)
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
    image_url = Config.OCR_URL + "?access_token=" + token

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
            if words.startswith('A.') or \
                    words.startswith('B.') or \
                    words.startswith('C.') or \
                    words.startswith('D.') or \
                    words.startswith('E.') or \
                    words.startswith('F.'):
                options.append(words.split(".")[1])
        return question, options
    except:
        traceback.print_exc()
        print("ocr识别失败")
        return None
def query_answer(question, options=None):
    if ("词形" in question or "读音" in question):
        keywords = options
    else:
        keywords = __get_keywords__(question)
    if options is None:
        options = []
    answer = DBHelper.get_challenge_answer_from_db(question, options)
    if answer is None:
        answer = __query_from_syiban__(question, keywords, options)
    return answer
def search_answer(content, options):
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
        _, i = Config.INST.choice(counts)
        print(f'搜索结果全0，随机一个 {i}')
    print(f'根据搜索结果: {i} 很可能是正确答案')
    return options[i]


# 从问题中分割出连续的语句作为关键词
def __get_keywords__(question):
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

def __query_from_syiban__(question, keywords, options):
    def str_similar(answer, options):
        result = options[0]
        x = 0
        for option in options:
            y = difflib.SequenceMatcher(None, answer, option).quick_ratio()
            if y > x:
                y = x
            result = option
        return result

    for keyword in keywords:
        response = Config.SESSION.get("http://www.syiban.com/search/index/init.html?modelid=1&q=" + keyword)
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








