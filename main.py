from slacker import Slacker
import time
from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup
import os
import sys
import re
from apscheduler.schedulers.blocking import BlockingScheduler
import random
from config import *
sched = BlockingScheduler()

token =''
slack = Slacker(token)

DONE_PROBLEMS = open("problems.txt",'r').readlines()


def checker():
    current_problem = open("problems.txt", 'r').readlines()[-1]
    
    


def algoPick():
    done = False
    ctime = time.strftime('%y/%m/%d', time.localtime(time.time()))
    
    while done == False:
        
        page_select = random.choice(range(1,MAX_PAGE))
        hdr = {'User-Agent': 'Mozilla/5.0', 'referer' : 'http://m.naver.com'}
        pre_url = 'https://www.acmicpc.net/problemset/' + str(page_select)

        url = urllib.request.Request(pre_url, headers=hdr)
        my_url = urlopen(url)
        soup = BeautifulSoup(my_url,'html.parser')
        table = soup.find_all(id="problemset")
        problems = table[0].find_all("tr")
        problems = problems[1:]

        select = random.choice(range(1,100))
        try:
            p = problems[select]
            
            p_num = p.find_all("td")[0].text
            
            if p_num in DONE_PROBLEMS:
                continue
            
            hard = p.find_all("td")[-1].text
            other = p.find_all("td")[-3].text
            name = p.find(class_="click-this").text
            dum = "https://www.acmicpc.net"
            link = dum + p.find(class_="click-this").a['href']
        
            if float(hard[:-1]) < HARD or int(other) < OTHERS:
                print("so hard")
            else:
                done = True
                with open("problems.txt",'a') as f:
                    f.write(p_num + '\n')
                print(hard,name,link,other)
    
        except:
            continue

    
    attachments_dict = dict()
    attachments_dict['pretext'] = ctime
    attachments_dict['title'] = name
    attachments_dict['title_link'] = link
    attachments_dict['fallback'] = "새로운 알고리즘을 가져왔어요!!"
    attachments_dict['text'] = random.choice(["이것도 풀 수 있을까?", "한번 도전해보시지~", "이거 풀면 인정해줄게!", "파이썬킹이 되거라!"])
    #attachments_dict['mrkdwn_in'] = ["text", "pretext"]  # 마크다운을 적용시킬 인자들을 선택합니다.
    attachments = [attachments_dict]
    
    
    slack.chat.post_message(channel='#python-algo',text=None,attachments=attachments)
    
if __name__ == "__main__":
    algoPick()