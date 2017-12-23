import time
import random
import requests
import socket
import re
import http.client
import sys

URL = 'https://m.10010.com/NumApp/NumberCenter/qryNum?callback=jsonp_queryMoreNums&provinceCode=76&cityCode=760&monthFeeLimit=0&groupKey=41242783&searchCategory=3&net=01&amounts=200&codeTypeCode=&searchValue=&qryType=02&goodsNet=4&_=1513948237449'


def get_content(url):
    '''获取url内容'''
    #request header信息
    header = {
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    #超时时间
    timeout = random.choice(range(80,180))
    while True:
        try:
            #请求url获取返回的response对象
            rep = requests.get(url, headers=header, timeout=timeout)
            # rep = requests.get(url)
            rep.encoding = 'utf-8'
            break
        except:
            #出错后延迟一段你时间重试
            time.sleep(random.choice(range(5, 20)))

    return rep.text

def grade(phone):
    '''给手机号打分'''
    if phone[3:7] == phone[7:]:#1--abcdabcd
        return 100
    elif phone[3:5] == phone[7:9] and phone[5:7] == phone[9:]: #1--aabbaabb
        return 95
    elif phone[3:7] == phone[7::-1]: #1--abcddcba
        return 90
    elif phone[7:9] == phone[9:]: #尾号aabb
        return 80
    elif phone[7:9] == phone[9::-1]: #尾号abba
        return 70
    elif phone[3:5] == phone[7:9]: #1--ab--ab--
        return 50
    else:
        return 0
    #可以在加一些其他的判定条件

def save_resule(result):
    '''把结果保存到result.txt文件'''
    if len(result) > 0:
        with open('result.txt', 'a') as f:
            for x in result:
                f.write(x + '\n')

#循环查询次数
loop = 5
#结果集合
result = []

if len(sys.argv) == 2:
    loop = int(sys.argv[1])

for i in range(1, loop+1):
    # now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # print('{}  第{}次查询'.format(now, i))
    html = get_content(URL) #请求url，获取json内容
    # print(html)
    regex_str = r'1\d{10}'
    #提取手机号
    phones = re.findall(regex_str, html)
    for x in phones:
        level = grade(x)
        if level > 0 and x not in result:
            result.append(x)
            print(level, '-', x)
    time.sleep(random.choice(range(1, 5)))#不要请求的太频繁
save_resule(result)#循环结束保存到result.txt文件






