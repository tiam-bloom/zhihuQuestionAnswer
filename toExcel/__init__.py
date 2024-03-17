# _*_ coding : UTF-8 _*_
# @Time : 2024/3/16 18:23
# @Auther : Tiam
# @File : __init__.py
# @Project : 20240315-python知乎回答评论抓取
# @Desc :

import json
import pandas as pd
import os

import pandas as pd
import json


def json_file_to_excel(json_file_path, excel_file_path):
    """
    将JSON文件转换为Excel文件。

    参数:
    json_file_path (str): JSON文件的路径。
    excel_file_path (str): 要保存的Excel文件的路径。
    """
    # 读取JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # 检查JSON数据是否为字典或列表
    if isinstance(json_data, dict):
        # 如果是字典，将其转换为列表（包含单个元素）
        json_data = [json_data]
    elif not isinstance(json_data, list):
        raise ValueError("JSON data must be a dictionary or a list.")

    # 将数据转换为DataFrame
    df = pd.DataFrame(json_data)

    # 将DataFrame写入Excel文件
    df.to_excel(excel_file_path, index=False, engine='openpyxl')


def main():
    # 遍历data文件夹中的文件

    # 指定要遍历的目录
    directory = '../comment/'

    # 使用os.walk()遍历目录
    for dir_path, dir_names, filenames in os.walk(directory):
        # 处理每个目录下的文件
        for filename in filenames:
            # 拼接完整的文件路径
            file_path = os.path.join(dir_path, filename)
            # 这里可以添加你的处理代码
            json_file_to_excel(file_path, f'../excel/{filename}.xlsx')


if __name__ == '__main__':
    main()
