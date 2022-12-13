# coding: utf-8
def get_question_text(views):
    for view in views:
        text = view.info['text']
        if len(text) > 5 and \
                '填空题' not in text and \
                '多选题' not in text and \
                '单选题' not in text:
            return text


def get_question_type(views):
    for view in views:
        text = view.info['text']
        if '填空题' in text:
            return '填空题'
        if '多选题' in text:
            return '多选题'
        if '单选题' in text:
            return '单选题'


def get_answer_option(views):
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
