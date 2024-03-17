# _*_ coding : UTF-8 _*_
# @Time : 2024/3/16 16:14
# @Auther : Tiam
# @File : get_comment
# @Project : 20240315-python知乎回答评论抓取
# @Desc :
import json
import os
import random
import time
from datetime import datetime

import requests
import signature


def to_item(x):
    return {
        'comment_id': x.get('id'),
        '评论内容': x.get('content'),
        '创建时间': datetime.fromtimestamp(x.get('created_time')).strftime('%Y-%m-%d %H:%M:%S'),
        '点赞数': x.get('like_count'),
        '作者名': x.get('author').get('name'),
        'IP': x.get('comment_tag')[0].get('text'),
        'child_comment_count': x.get('child_comment_count'),
        'child_comments': list(map(to_item, x.get('child_comments'))) if x.get('child_comment_count') != 0 else [],
        '回复对象': x.get('reply_to_author').get('name') if x.get('reply_to_author') else '',
    }


def get_child_comment_page(url):
    #
    cookies = {
        'd_c0': 'AMAW7Hf1ahaPTt3aKjIujKEgJpOWE1mpaZk=|1677915009',
    }

    headers = {
        'cookie': '; '.join([f'{k}={v}' for k, v in cookies.items()]),
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()


def get_child_comment_list(comment_id):
    print('comment_id: ', comment_id)
    url = f'https://www.zhihu.com/api/v4/comment_v5/comment/{comment_id}/child_comment?limit=20&offset='
    is_end = False
    total_child_comment_list = []
    page = 0
    while not is_end:
        try:
            json_data = get_child_comment_page(url)
            if json_data is not None:
                page += 1
                child_comment_list = list(map(to_item, json_data.get('data')))
                total_child_comment_list.extend(child_comment_list)

                print(page, '当前总评论数: ', len(total_child_comment_list))

                paging = json_data.get('paging')
                is_end = paging.get('is_end')
                url = paging.get('next')
        except:
            print('请求失败', url)
            pass

    return total_child_comment_list


def get_root_comment_page(url):
    # 提取url中的path
    path = url.split('zhihu.com')[1]
    cookies = {
        'd_c0': 'AMAW7Hf1ahaPTt3aKjIujKEgJpOWE1mpaZk=|1677915009',
    }

    headers = {
        'cookie': '; '.join([f'{k}={v}' for k, v in cookies.items()]),
        'x-zse-93': '101_3_3.0',
        'x-zse-96': signature.get_x_zse_96(path)
    }

    response = requests.get(
        url,
        cookies=cookies,
        headers=headers,
    )
    if response.status_code == 200:
        return response.json()
    else:
        print('请求失败')


def get_root_comment_list(answer_id):
    print('answer_id: ', answer_id)
    url = f'https://www.zhihu.com/api/v4/comment_v5/answers/{answer_id}/root_comment?order_by=score&limit=20&offset='
    is_end = False
    total_comment_list = []
    count = 0
    while not is_end:
        json_data = get_root_comment_page(url)
        if json_data is None:
            continue

        count += 1
        comment_list = list(map(to_item, json_data.get('data')))

        for comment in comment_list:
            child_comment_count = comment.get('child_comment_count')
            # 默认子评论有两条, 大于2条需要重新 请求全部的回复
            if child_comment_count > 2:
                time.sleep(random.random())
                comment['child_comments'] = get_child_comment_list(comment.get('comment_id'))
            # 不保存子评论的层级关系
            if child_comment_count > 0:
                for c in comment['child_comments']:
                    del c['child_comments']
                total_comment_list.extend(comment['child_comments'])
            comment.pop('child_comments')

        total_comment_list.extend(comment_list)

        print(count, '当前总评论数: ', len(total_comment_list))

        paging = json_data.get('paging')
        is_end = paging.get('is_end')
        url = paging.get('next')
        # break
        if count % 5 == 0:
            time.sleep(random.randint(1, 2))
        # time.sleep(random.randint(0, 1))

    return total_comment_list
    # with open(f'comment/comment_{answer_id}.json', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(total_comment_list, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    # 指定要遍历的目录
    directory = './data/'
    # 使用os.walk()遍历目录
    for dir_path, dir_names, filenames in os.walk(directory):
        # 处理每个目录下的文件
        for filename in filenames:
            if '601307254' in filename or '597272501' in filename:
                continue
            print('filename: ', filename)
            # 拼接完整的文件路径
            file_path = os.path.join(dir_path, filename)
            # 读取JSON文件
            with open(file_path, 'r', encoding='utf-8') as f:
                total_answer_comment_list = []
                json_data = json.load(f)
                for data in json_data:
                    answer_comment_list = get_root_comment_list(data.get('answer_id'))
                    total_answer_comment_list.extend(answer_comment_list)
                with open(f'comment/comment_{filename}.json', 'w', encoding='utf-8') as fc:
                    fc.write(json.dumps(total_answer_comment_list, ensure_ascii=False, indent=2))
    # 测试

    # 一个回答下的评论
    # get_root_comment_list('2997437272')  # answer_id
    # get_root_comment_list('3000598929')

    # total_child_comment_list = get_child_comment_list('10538499010')
    # print(json.dumps(total_child_comment_list, ensure_ascii=False, indent=2))
