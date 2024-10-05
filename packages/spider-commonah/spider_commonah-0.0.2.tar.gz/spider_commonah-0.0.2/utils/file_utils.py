'''
    @description: 文件工具类
    @params: 
    @author: MR.阿辉
    @datetime: 2024-10-05 07:02:45
    @return: 
'''
import os

'''
    @description: 判断字符串是否为文件地址
    @params: path 文件地址字符串
    @author: MR.阿辉
    @datetime: 2024-03-12 14:41:30
    @return: 
'''
def is_file_path(path:str) -> bool:
    try:
        if  not isinstance(path, str):
            return False
        # os.path.exists(0) 返回为 True ，绝了
        return os.path.exists(path) and os.path.isfile(path)
    except Exception as _:
        return False

'''
    @description: mkdir 创建文件
    @params: file_dir 文件目录地址
    @params: file_name 文件名称
    @author: MR.阿辉
    @datetime: 2024-03-12 14:50:39
    @return: 
'''
def mkdirs(file_dir:str,file_name:str,) -> str:
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    return os.path.join(file_dir,file_name) 