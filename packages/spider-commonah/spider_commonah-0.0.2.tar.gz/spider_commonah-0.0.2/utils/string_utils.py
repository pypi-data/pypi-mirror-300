'''
    @description: 字符串工具类
    @params: 
    @author: MR.阿辉
    @datetime: 2024-10-05 07:01:22
    @return: 
'''
import re

'''
    @description: 判断字符串是否为url
    @params: url 字符串地址
    @author: MR.阿辉
    @datetime: 2024-03-12 14:40:38
    @return: 
'''
def is_url(url:str) -> bool:
    pattern = r'^https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$'
    return bool(re.match(pattern, url))

'''
    @description: 判断字符串是否为数值
    @params: s 字符串
    @author: MR.阿辉
    @datetime: 2024-09-19 22:02:00
    @return: 
'''
def is_number(s:str):
    # 正则表达式匹配正整数或负整数
    pattern = r'^-?\d+(\.\d+)?$'
    return bool(re.match(pattern, s))