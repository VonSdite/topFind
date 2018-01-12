# -*- coding: utf-8 -*-
# @Author   : Sdite
# @DateTime : 2018-01-11 13:40:41

import json
import time
import requests
import threading
from selenium import webdriver

# 用百度进行搜索
search_url = 'https://www.baidu.com/'

# 题目的来源url
source_url = 'http://htpmsg.jiecaojingxuan.com/msg/current'

# 浏览器的搜索框和搜索按钮
webTextEdit = None
button = None

# 问题集合
questions = []

# 选项集合
options = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


# 打开百度
def openWeb():
    global webTextEdit, button
    driver = webdriver.Chrome()         # 浏览器
    driver.get(search_url)
    webTextEdit = driver.find_element_by_xpath('//*[@id="kw"]')
    button = driver.find_element_by_xpath('//*[@id="su"]')


# 搜索函数
def searchAnswer(query):
    '''
    Args: 
        query:   搜索的题目字符串

    Returns: 
        None
    '''
    global webTextEdit, button
    try:
        query = query[query.find('.') + 1: query.find('?')]
        webTextEdit.clear()
        webTextEdit.send_keys(query)
        button.click()
    except:
        print('本次自动搜索出错，请复制粘贴搜索。')


def savePrefix():
    # 写入保存文件的时间前缀
    with open('record.txt', 'a', encoding='utf-8') as f:
        f.write('=======================================\n')
        f.write(time.strftime('%F %X') + '\n')
        f.write('=======================================\n')


def save(question, option, answer):
    with open('record.txt', 'a', encoding='utf-8') as f:
        f.write(question + '\n')
        f.write(' '.join(option))
        f.write('\n答案: %s\n' % str(answer))


# 获取题目 选项和最终答案
def getInfo():
    '''
    Args: 
        None

    Returns: 
        None
    '''
    try:
        resp = requests.get(url=source_url, headers=headers, timeout=4).text
        try:
            resp_dict = json.loads(resp)    # 解析json
            if resp_dict['msg'] != 'no data':
                # 获取题目
                question = resp_dict['data']['event'].get('desc', None)

                # 获取选项
                option = resp_dict['data']['event'].get('options', None)

                # 获取正确选项
                correct_option = resp_dict['data'][
                    'event'].get('correctOption', None)

                # 题目
                if question not in questions:
                    questions.append(question)
                    print(question)              # 显示题目
                    print("选项: ")
                    print(" ".join(option))      # 显示选项

                    # 开线程去自动搜索
                    threading.Thread(target=searchAnswer,
                                     args=(question, )).start()

                # 答案, 这是题目之后才会抓到的答案包, 不能提前得知
                if correct_option != None:
                    correct_answer = option[correct_option]

                    if option not in options:
                        options.append(option)
                        print('正确答案: ' + str(correct_answer))

                        threading.Thread(target=save, args=(
                            question, option, correct_option)).start()  # 保存到文件

                        print('\nWaiting for new question')

        except:
            pass
    except:
        pass


def init():
    # 线程打开网页
    threading.Thread(target=openWeb).start()

    # 在保存的文件中写入时间
    savePrefix()

    print('Waiting for question')


def main():
    init()  # 初始化

    while True:
        getInfo()

        try:
            if questions[-1].find('12.') != -1 and len(questions) == len(options):
                print('本次直播结束')
                break
        except:
            pass


if __name__ == '__main__':
    main()
 