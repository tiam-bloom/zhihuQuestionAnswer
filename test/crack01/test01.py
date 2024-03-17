# _*_ coding : UTF-8 _*_
# @Time : 2024/3/15 23:29
# @Auther : Tiam
# @File : test01.py
# @Project : 20240315-python知乎回答评论抓取
# @Desc : https://www.2177.com.cn/a/112.html


import urllib
import requests
from py_mini_racer import MiniRacer
import hashlib
import execjs
import json
import time
from urllib.parse import urlparse

d_co = 'AJDWnZsqnxWPThsPHCtfo2a8YYdYSZ-bLv0=|1664238731'
version = '101_3_3.0'
path = '/remix/well/1419263074604343296/catalog?offset=10&limit=13&order_by=global_idx&is_new_column=true'
cookies = {
    'd_c0': d_co,
}


def get_x_zse_96(val):
    m = hashlib.md5()

    m.update(val.encode('utf-8'))

    with open('../../zhihuvmp.js', 'r') as s:
        ctx1 = execjs.compile(s.read(), cwd=r'/usr/local/lib/node_modules')
    encrypt_str = ctx1.call('get_zse_96', m.hexdigest())
    return encrypt_str

    # js_code = open('zhihuvmp.js', encoding='utf-8').read()
    # ctx = MiniRacer()
    # ctx.eval(js_code)
    # result = ctx.call('get_zse_96', m.hexdigest())
    # return result


def get_page_list(url):
    val = f'{version}+{path}+{d_co}'
    headers = {
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,fr;q=0.7,zh-TW;q=0.6,ja;q=0.5",
        "origin": "https://www.zhihu.com",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "x-zse-93": version,
        "x-zse-96": get_x_zse_96(val),
    }
    url = "https://api.zhihu.com/remix/well/1419263074604343296/catalog"

    params = {
        "offset": 10,
        "limit": 13,
        "order_by": "global_idx",
        "is_new_column": "true"
    }

    pid = '1419263074604343296'
    response = requests.get(url, params=params, cookies=cookies, headers=headers)
    with open(f'{pid}-2.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(response.json()))

    print(response.json())
    return response.json()


def parse_json(_url):
    paid = '1419263074604343296'
    with open(f'{paid}-2.txt', "r") as f:
        json_data = json.load(f)

    # json_data = json.loads(data)
    # print(json.dumps(json_data, indent=2))  # 将JSON代码格式化输出

    # app_context = json_data.get('appContext')
    # print(json.dumps(app_context, indent=2))

    catalog_data = json_data.get('data')
    seq = 1
    column_id = 2
    if catalog_data:
        for section in catalog_data:  # 迭代catalogData中的每个元素
            section_title = section['title']  # 获取每个元素的标题
            section_chapter = section['index']['serial_number_txt']
            title = section_chapter + section_title
            seid = section['id']
            file_path = f"/{paid}/{seid}.txt"
            createtime = int(time.time())
            # print(f"章节标题：{title} {section_title},url:")
            # print(f"https://www.zhihu.com/market/paid_column/{paid}/section/{seid}")
            # query = "INSERT INTO fa_novel_section (column_id, paid, seid, seq, title, file_path, createtime) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            query = f"INSERT INTO fa_novel_section (column_id, paid, seid, seq, title, file_path, createtime) VALUES ({column_id}, '{paid}', '{seid}', {seq}, '{title}', '{file_path}', {createtime})"
            print(query)
            seq += 1


    else:
        print("未找到name属性")


if __name__ == '__main__':
    url = 'https://www.zhihu.com/xen/market/remix/paid_column/1609560969377628160?is_share_data=true'
    # get_page_list(url)

    parse_json(url)


def parse_pid(_url):
    parsed_url = urlparse(_url)
    path = parsed_url.path
    column_id = path.rsplit('/', 1)[-1]
    return column_id
