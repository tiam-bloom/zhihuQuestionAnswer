# _*_ coding : UTF-8 _*_
# @Time : 2024/3/16 14:30
# @Auther : Tiam
# @File : test04
# @Project : 20240315-python知乎回答评论抓取
# @Desc :


import requests

headers = {
    'cookie': 'd_c0=1; ',
}

response = requests.get('https://www.zhihu.com/api/v4/questions/610276483/feeds', headers=headers)

print(response.json())