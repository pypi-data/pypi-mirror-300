import json
import random


'''
    @description: 随机读取一个请求头配置
    @params: device 浏览器驱动 PC-Mac
    @author: MR.阿辉
    @datetime: 2024-03-12 17:20:37
    @return: 
'''
def get_headers(device:str) -> dict:
    # TODO：读取 请求头的 json 配置文件
    
    headers_config_file = "./source/json/headers.json"
    with open(headers_config_file, "r", encoding="utf-8") as f:
        terminal,system = device.split('-')
        headers_data = json.load(f)
        headers_list = headers_data[terminal][system]
        # 随机取一个请求头
        return random.choice(headers_list)