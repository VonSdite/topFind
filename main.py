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

# 三个浏览器的搜索框和搜索按钮
webTextEdit1 = None
button1 = None

webTextEdit2 = None
button2 = None

webTextEdit3 = None
button3 = None

# 问题集合
questions = []

# 选项集合
options = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


# 打开百度
def openWeb():
    global webTextEdit1, button1, webTextEdit2, button2, webTextEdit3, button3
    driver1 = webdriver.Chrome()         # 浏览器
    driver1.get(search_url)
    webTextEdit1 = driver1.find_element_by_xpath('//*[@id="kw"]')
    button1 = driver1.find_element_by_xpath('//*[@id="su"]')

    driver2 = webdriver.Chrome()         # 浏览器
    driver2.get(search_url)
    webTextEdit2 = driver2.find_element_by_xpath('//*[@id="kw"]')
    button2 = driver2.find_element_by_xpath('//*[@id="su"]')

    driver3 = webdriver.Chrome()         # 浏览器
    driver3.get(search_url)
    webTextEdit3 = driver3.find_element_by_xpath('//*[@id="kw"]')
    button3 = driver3.find_element_by_xpath('//*[@id="su"]')


# 搜索函数
def searchAnswer(query, postfix):
    '''
    Args: 
        query:   搜索的题目字符串
        postfix: 后缀, 选项的list表

    Returns: 
        None
    '''
    global webTextEdit1, button1, webTextEdit2, button2, webTextEdit3, button3
    try:
        query = query[query.find('.') + 1: query.find('?')]
        # 搜索题目+第1个选项
        webTextEdit1.clear()
        webTextEdit1.send_keys(query + ' ' + postfix[0])
        button1.click()

        # 搜索题目+第2个选项
        webTextEdit2.clear()
        webTextEdit2.send_keys(query + ' ' + postfix[1])
        button2.click()

        # 搜索题目+第3个选项
        webTextEdit3.clear()
        webTextEdit3.send_keys(query + ' ' + postfix[2])
        button3.click()
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
                    print(question)     # 显示题目
                    print(*option)      # 显示选项

                    # 开线程去自动搜索
                    threading.Thread(target=searchAnswer,
                                     args=(question, option)).start()

                # 答案, 这是题目之后才会抓到的答案包, 不能提前得知
                if correct_option != None:
                    correct_answer = option[correct_option]

                    if option not in options:
                        options.append(option)
                        print('正确答案: ' + str(correct_answer))

                        save(question, option, correct_option)  # 保存到文件

                        print('\nWaiting for new question')

        except:
            print('￣□￣｜｜突然发生点小错误')
    except:
        return '网络异常!!!!'


def init():
    # 线程打开三个网页
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
