#! /usr/bin/python3
# copyright 2024, CHUA某人版权所有。
# TruePigLatin ——可能是史上运行速度最快、最准（doge）的Pig Latin翻译器
# 用法：import truepiglatin [as tpl];pl = tpl[truepiglatin].translate("这是个示例。This is a EXAMPLE.");print(pl)


def translate(msg, dash=False):
    """
    输入：str，输出：str
    参数：dash，控制Pig Latin流派
    """
    vowels = ('a', 'e', 'i', 'o', 'u', 'y')
    pig_latin = []

    for word in msg.split():
        # 分离单词前端的非英文字符
        prefix_non_letters = ''
        while len(word) > 0 and not word[0].isalpha():
            prefix_non_letters += word[0]
            word = word[1:]
        if len(word) == 0:
            pig_latin.append(prefix_non_letters)
            continue

        # 分离单词后端的非英文字符
        suffix_non_letters = ''
        while not word[-1].isalpha():
            suffix_non_letters += word[-1]
            word = word[:-1]

        # 识别并保存单词是全大写还是首字母大写
        was_upper = word.isupper()
        was_title = word.istitle()

        word = word.lower()  # 为方便处理，将单词转换为小写

        # 分离并识别单词首字母是否为辅音字母
        prefix_consonants = ''
        while len(word) > 0 and word not in vowels:
            prefix_consonants += word[0]
            word = word[1:]

        # 添加Pig Latin式结尾
        if prefix_consonants != '':
            if dash is False:
                word += prefix_consonants + 'ay'
            else:
                word += '-' + prefix_consonants + 'ay'
        else:
            if dash is False:
                word += 'yay'
            else:
                word += '-yay'

        # 恢复单词原状
        if was_title:
            word = word.title()
        if was_upper:
            word = word.upper()

        # 拼接单词
        pig_latin.append(prefix_non_letters + word + suffix_non_letters)

    # 连词成句并返回
    return ' '.join(pig_latin)
