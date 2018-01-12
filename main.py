# -*- coding: utf-8 -*-
# @Author   : Sdite
# @DateTime : 2018-01-11 13:40:41

import json
import requests
from selenium import webdriver
import time
import threading

questions = []
answers_set = []

url = 'https://www.baidu.com/'

webTextEdit1 = None
button1 = None

webTextEdit2 = None
button2 = None

webTextEdit3 = None
button3 = None

# 打开百度
def openWeb():
    global webTextEdit1, button1, webTextEdit2, button2, webTextEdit3, button3 
    driver1 = webdriver.Chrome()         # 浏览器
    driver1.get(url)
    webTextEdit1 = driver1.find_element_by_xpath('//*[@id="kw"]')
    button1 = driver1.find_element_by_xpath('//*[@id="su"]')

    driver2 = webdriver.Chrome()         # 浏览器
    driver2.get(url)
    webTextEdit2 = driver2.find_element_by_xpath('//*[@id="kw"]')
    button2 = driver2.find_element_by_xpath('//*[@id="su"]')

    driver3 = webdriver.Chrome()         # 浏览器
    driver3.get(url)
    webTextEdit3 = driver3.find_element_by_xpath('//*[@id="kw"]')
    button3 = driver3.find_element_by_xpath('//*[@id="su"]')
        
def search_answer(query, postfix):
    global webTextEdit1, button1, webTextEdit2, button2, webTextEdit3, button3  
    # try:
    webTextEdit1.clear()
    webTextEdit1.send_keys(query + ' ' + postfix[0])
    button1.click()

    webTextEdit2.clear()
    webTextEdit2.send_keys(query + ' ' + postfix[1])
    button2.click()

    webTextEdit3.clear()
    webTextEdit3.send_keys(query + ' ' + postfix[2])
    button3.click()
    # except:
    #     print('本次自动搜索出错，请复制粘贴搜索。')

def get_answer():
    try:
        resp = requests.get('http://htpmsg.jiecaojingxuan.com/msg/current',timeout=4).text
        try:
            resp_dict = json.loads(resp)
            if resp_dict['msg'] == 'no data':
                return None
            else:
                resp_dict = eval(str(resp))
                question = resp_dict['data']['event']['desc']
                question = question[question.find('.') + 1:question.find('?')]
                correct_option = resp_dict['data']['event'].get('correctOption', None)
                if question not in questions:
                    questions.append(question)
                    print('问题: ')
                    print(question)
                    answers = eval(resp_dict['data']['event']['options'])
                    print(*answers)
                    threading.Thread(target=search_answer, args=(question, answers)).start()
                    return None
                elif correct_option != None:
                    correct_answer = eval(resp_dict['data']['event']['options'])[correct_option]
                    if correct_answer not in answers_set:
                        answers_set.append(correct_answer)
                        print('正确答案: ')
                        print(correct_answer)
                        print('\n\nWaiting for new question...\n\n')
                    return None
                else:
                    return None
        except:
            return None
    except:
        return '网络异常!!!!'


def main():
    print('Waiting for question...\n\n')
    while True:
        answer = get_answer()
        if answer != None:
            print(answer)

        if len(questions) == 12 and len(answers_set) == 12:
            with open('record.txt', 'a', encoding='utf-8') as f:
                f.write('=======================================\n')
                f.write(time.strftime('%F %X') + '\n')
                f.write('=======================================\n')

                for index in range(0, 12):
                    f.write(str(index) 
                        + '.' 
                        + questions[index] 
                        + ' ' 
                        + answers_set[index] 
                        + '\n')  
        break                  
            

if __name__ == '__main__':
    # 开线程来打开三个网页
    threading.Thread(target=openWeb).start()

    main()
     
        

  