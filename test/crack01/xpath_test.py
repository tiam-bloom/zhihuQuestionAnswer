# _*_ coding : UTF-8 _*_
# @Time : 2024/3/16 13:11
# @Auther : Tiam
# @File : xpath_test
# @Project : 20240315-python知乎回答评论抓取
# @Desc :
from lxml import html

# 提供的HTML字符串
html_string = ('<span class="css-1xfvezd"><style data-emotion-css="1qkvt8e">.css-1qkvt8e{margin-right:2px;}</style><svg width="16px" height="16px" viewbox="0 0 24 24" class="ZDI ZDI--LocationFill24 css-1qkvt8e" '
               'fill="currentColor"><path fill-rule="evenodd" d="M6.311 4.888a8.046 8.046 0 0 1 13.735 5.69c0 1.682-.615 3.4-1.448 4.968-.836 1.575-1.924 3.055-2.939 4.276-1.933 2.326-5.385 2.326-7.318 0-1.015-'
               '1.22-2.102-2.7-2.939-4.276-.832-1.567-1.447-3.286-1.447-4.969 0-2.134.847-4.18 2.356-5.689ZM12 13.5a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" clip-rule="evenodd"/></svg>IP 地址</span>')

# 解析HTML字符串
tree = html.fromstring(html_string)

# 构建XPath表达式来查找包含特定文本的<span>标签
# 这里我们使用contains()函数来匹配文本"IP 地址"
xpath_expression = './/span[contains(text(), "IP 地址")]'

# 使用find()方法获取单个节点
span_node = tree.xpath(xpath_expression)

# 获取节点的文本内容
text_content = span_node[0].text_content() if span_node else None
print(text_content)  # 输出: "IP 地址"