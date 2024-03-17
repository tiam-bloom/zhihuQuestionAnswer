# _*_ coding : UTF-8 _*_
# @Time : 2024/3/16 12:42
# @Auther : Tiam
# @File : get_ip
# @Project : 20240315-python知乎回答评论抓取
# @Desc :
import requests
from lxml import html, etree


def get_author_ip(people_url):
    response = requests.get('https://www.zhihu.com/people/jia-yu-bu-shi-gui-74')

    # 解析HTML文档
    element = etree.HTML(response.content)
    # 构建XPath表达式来查找<h1>标签
    xpath_expression = '//div[@class="ProfileHeader-userCover"]//span/text()'

    # 使用find()方法获取单个节点
    ip_text = element.xpath(xpath_expression)[0]

    # print(ip_text)
    return ip_text


get_author_ip()
