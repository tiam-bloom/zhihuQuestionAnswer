# _*_ coding : UTF-8 _*_
# @Time : 2024/3/15 22:32
# @Auther : Tiam
# @File : signature
# @Project : 20240315-python知乎回答评论抓取
# @Desc :
import hashlib
import os

import execjs

d_c0 = 'AMAW7Hf1ahaPTt3aKjIujKEgJpOWE1mpaZk=|1677915009'
version = '101_3_3.0'


def get_x_zse_96(path):
    signature = {
        'x-zse-93': version,
        'path': path,
        'd_c0': d_c0
    }
    val = '+'.join(signature.values())

    m = hashlib.md5()
    m.update(val.encode('utf-8'))

    # os.path.join()
    with open('zhihuvmp.js', 'r') as s:
        ctx1 = execjs.compile(s.read())
    encrypt_str = ctx1.call('get_zse_96', m.hexdigest())
    return encrypt_str


if __name__ == '__main__':
    print(get_x_zse_96('/api/v4/comment_v5/answers/2997437272/root_comment?limit=10&offset=568157402_10538825519_0&order_by=score'))
