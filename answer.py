# _*_ coding : UTF-8 _*_
# @Time : 2024/3/15 20:17
# @Auther : Tiam
# @File : answer
# @Project : 20240315-python知乎回答评论抓取
# @Desc :  回答抓取
import json
import random
import time
import urllib
from datetime import datetime
from urllib.parse import urlencode

import requests
from lxml import etree


def get_author_ip(url_token):
    try:
        people_url_prefix = 'https://www.zhihu.com/people/'
        response = requests.get(people_url_prefix + url_token)

        # 解析HTML文档
        element = etree.HTML(response.content)
        # 构建XPath表达式来查找<h1>标签
        xpath_expression = '//div[@class="ProfileHeader-userCover"]//span/text()'

        # 使用find()方法获取单个节点
        ip_text = element.xpath(xpath_expression)[0]
    except Exception as e:
        ip_text = '暂无IP'
    # print(ip_text)
    return ip_text


def to_item(x):
    x = x.get('target')
    return {
        'answer_id': x.get('id'),
        '作者名': x.get('author').get('name'),
        '作者ID': x.get('author').get('id'),
        'url_token': x.get('author').get('url_token'),
        '作者IP': get_author_ip(x.get('author').get('url_token')),
        '创建时间': datetime.fromtimestamp(x.get('created_time')).strftime('%Y-%m-%d %H:%M:%S'),
        '更新时间': datetime.fromtimestamp(x.get('updated_time')).strftime('%Y-%m-%d %H:%M:%S'),
        '赞同数': x.get('voteup_count'),
        '回答内容': x.get('content'),
        '评论数': x.get('comment_count'),
        '评论内容': '待定',
    }


def get_comment_list(answer_id):
    pass


def questions_feeds(url):
    cookies = {
        '_xsrf': 'dffd11af-96c7-4e64-a5bd-87f0236e6cdf',
        '_zap': 'de483e18-f5a6-4944-88b9-deb889f044f4',
        'd_c0': 'AMAW7Hf1ahaPTt3aKjIujKEgJpOWE1mpaZk=|1677915009',
        'YD00517437729195%3AWM_TID': 'yIl0kbDqFKhEVRQRRVeFOc8MDFFmX%2BLp',
        'YD00517437729195%3AWM_NI': '9X%2BrFmVsfYWtacM0JWY2mFTeC6ZO3n31MNGaIfjSVvIKiB%2FT95g0v5QQhNgqPgNHyZH7OmSX%2FLTpDkqY5cuR3UWyUNpOJredW7pyrzc%2B1vvHC1fGWPTncw%2FBasC0kUJSa2Q%3D',
        'YD00517437729195%3AWM_NIKE': '9ca17ae2e6ffcda170e2e6ee8bf07eede8ad90f47b96a88ba6c44e939a8f82c16ef497f88ad85985afa691d72af0fea7c3b92afb88e593c56796adaabad680a3bd83d1c95d9beea3a7d76f81ea96b0b266f1ef83afc66b8bbaa6b4d57e8b95a7a3ae60fbeba9d1f53f938fa8afe67b94b982a9fc528ce9818ed254ed949c91c761b387fb84f85af18b999ad846b4918693e87095e9c09af172a1f5ff97f54481efaaa8d65c98b2ad98ae4aa3ad8dd1ea5f8a8dafd3d437e2a3',
        'q_c1': 'e6dda5fd70234573a66d021b9007c6bc|1699596026000|1699596026000',
        'z_c0': '2|1:0|10:1710128054|4:z_c0|80:MS4xeHVMTkJ3QUFBQUFtQUFBQVlBSlZUVi02eldiZWU1TTlGZmZYQnUtLVV1bnRxd3VsU3V3c1lRPT0=|48e1c3a23f0be5fa53ab7a5fbb5463278eeb696c4454083f4fd4edd3badd8c33',
        'KLBRSID': 'b5ffb4aa1a842930a6f64d0a8f93e9bf|1710560488|1710554918',
        '_xsrf': 'UtZxQ4MUgkFWFeSvwLzMuwk7D6TxQrBG',
        'KLBRSID': '4efa8d1879cb42f8c5b48fe9f8d37c16|1710568946|1710568946',
        '_xsrf': 'UtZxQ4MUgkFWFeSvwLzMuwk7D6TxQrBG',
        'KLBRSID': 'f48cb29c5180c5b0d91ded2e70103232|1710569502|1710569502',
    }
    headers = {
        'cookie': '; '.join([f'{k}={v}' for k, v in cookies.items()]),
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_data = response.json()

        res_data = {
            'answer_list': list(map(to_item, json_data.get('data'))),
            'paging': json_data.get('paging')
        }

        # print(json.dumps(res_data, indent=2, ensure_ascii=False))

        return res_data
    else:
        print('请求失败')


def question(question_id):
    print('开始抓取问题: ', question_id)
    params = {
        'include': 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,reaction_instruction,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[*].author.follower_count,vip_info,badge[*].topics;data[*].settings.table_of_content.enabled',
        'order': 'updated',
        'limit': 20
    }
    query_string = urlencode(params)
    url = f'https://www.zhihu.com/api/v4/questions/{question_id}/feeds?{query_string}'

    total_answer_list = []
    is_end = False
    counts = 0
    try:
        while not is_end:
            counts += 1
            res_data = questions_feeds(url)
            total_answer_list.extend(res_data['answer_list'])
            print('第几次请求: ', counts, '当前页码: ', res_data['paging']['page'], ', 当前回答数: ', len(total_answer_list), '是否结束: ', res_data['paging']['is_end'])
            # 更新下次
            is_end = res_data['paging']['is_end']
            url = res_data['paging']['next']
            # if counts > 0:
            #     break
            # 随机休眠
            time.sleep(random.random())
    except Exception as e:
        print('异常: ', e)
    print('总回答数: ', len(total_answer_list))
    # 写入json文件
    with open(f'data/question_{question_id}.json', 'w', encoding='utf-8') as f:
        json.dump(total_answer_list, f, ensure_ascii=False, indent=2)
    print('写入成功')


if __name__ == '__main__':
    # 问题ID列表
    question_id_list = ['597272501', '601307254', '605656495', '606309719', '609890590', '610276483', '610276645', '610276645', '610393993', '610963260', '614881513', '623287280', '646529705', '647322856']
    # question_id_list = ['601307254', '606309719']  # 测试

    for question_id in question_id_list:
        question(question_id)
        # break
