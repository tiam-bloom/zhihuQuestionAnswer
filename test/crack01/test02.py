# _*_ coding : UTF-8 _*_
# @Time : 2024/3/16 10:00
# @Auther : Tiam
# @File : test02
# @Project : 20240315-python知乎回答评论抓取
# @Desc :
import hashlib
import json
import random
import time
from datetime import datetime
from urllib.parse import urlencode

import execjs
import requests

zhihu = 'https://www.zhihu.com'
d_c0 = 'AMAW7Hf1ahaPTt3aKjIujKEgJpOWE1mpaZk=|1677915009'


def get_signature_param(path):
    signature = {
        'x-zse-93': '101_3_3.0',
        'path': path,
        'd_c0': d_c0
    }
    return '+'.join(signature.values())


def get_x_zse_96(val):
    m = hashlib.md5()
    m.update(val.encode('utf-8'))

    with open('../../zhihuvmp.js', 'r') as s:
        ctx1 = execjs.compile(s.read())
    encrypt_str = ctx1.call('get_zse_96', m.hexdigest())
    return encrypt_str


def question_feeds(question_id):
    # 当前时间戳
    timestamp = int(time.time() * 1000)
    cookies = {
        '_xsrf': 'dffd11af-96c7-4e64-a5bd-87f0236e6cdf',
        '_zap': 'de483e18-f5a6-4944-88b9-deb889f044f4',
        'd_c0': d_c0,
        'YD00517437729195%3AWM_TID': 'yIl0kbDqFKhEVRQRRVeFOc8MDFFmX%2BLp',
        'YD00517437729195%3AWM_NI': '9X%2BrFmVsfYWtacM0JWY2mFTeC6ZO3n31MNGaIfjSVvIKiB%2FT95g0v5QQhNgqPgNHyZH7OmSX%2FLTpDkqY5cuR3UWyUNpOJredW7pyrzc%2B1vvHC1fGWPTncw%2FBasC0kUJSa2Q%3D',
        'YD00517437729195%3AWM_NIKE': '9ca17ae2e6ffcda170e2e6ee8bf07eede8ad90f47b96a88ba6c44e939a8f82c16ef497f88ad85985afa691d72af0fea7c3b92afb88e593c56796adaabad680a3bd83d1c95d9beea3a7d76f81ea96b0b266f1ef83afc66b8bbaa6b4d57e8b95a7a3ae60fbeba9d1f53f938fa8afe67b94b982a9fc528ce9818ed254ed949c91c761b387fb84f85af18b999ad846b4918693e87095e9c09af172a1f5ff97f54481efaaa8d65c98b2ad98ae4aa3ad8dd1ea5f8a8dafd3d437e2a3',
        'q_c1': 'e6dda5fd70234573a66d021b9007c6bc|1699596026000|1699596026000',
        'z_c0': '2|1:0|10:1710128054|4:z_c0|80:MS4xeHVMTkJ3QUFBQUFtQUFBQVlBSlZUVi02eldiZWU1TTlGZmZYQnUtLVV1bnRxd3VsU3V3c1lRPT0=|48e1c3a23f0be5fa53ab7a5fbb5463278eeb696c4454083f4fd4edd3badd8c33',
        'KLBRSID': f'b5ffb4aa1a842930a6f64d0a8f93e9bf|{timestamp}|1710554918',
    }
    cookie = '; '.join([f'{k}={v}' for k, v in cookies.items()])
    print('cookie: ', cookie)

    # 生成32位随机字符串
    # cursor = ''.join([random.choice('0123456789abcdef') for _ in range(32)])
    params = (
        ('cursor', '89d7c53c679d06e99e7037f75df0f02d'),  # 32位
        ('include',
         'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,reaction_instruction,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[*].author.follower_count,vip_info,badge[*].topics;data[*].settings.table_of_content.enabled'),
        ('limit', '5'),
        ('offset', '2'),
        ('session_id', '1710560488120236566'),  # 盲猜登录凭证
    )
    query_string = urlencode(params)
    path = f'/api/v4/questions/{question_id}/feeds?{query_string}'
    url = zhihu + path
    print('url', url)
    # 构建签名
    signature_param = get_signature_param(path)
    x_zse_96 = get_x_zse_96(signature_param)
    print('x_zse_96: ', x_zse_96)
    headers = {
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'x-zse-96': x_zse_96,  # '2.0_xVbQ+ZpK6kYfFT5UxsRmcKuyhXYOfO+4pVXZerDMcDnFRlRNQ/6H9DKGO0ei7XVq'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_data = response.json()

        def to_item(x):
            x = x.get('target')
            return {
                'answer_id': x.get('id'),
                '作者名': x.get('author').get('name'),
                '创建时间': datetime.fromtimestamp(x.get('created_time')).strftime('%Y-%m-%d %H:%M:%S'),
                '赞同数': x.get('voteup_count'),
                '回答内容': x.get('content'),
            }

        answer_list = list(map(to_item, json_data.get('data')))
        print(json.dumps(answer_list, indent=2, ensure_ascii=False))

        # 写入
        with open(f'{question_id}-2.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(response.json(), ensure_ascii=False, indent=2))
    else:
        print(response.text)


def main():
    # 597272501, 606309719
    question_feeds(606309719)


if __name__ == '__main__':
    main()
