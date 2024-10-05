# coding=utf-8
import os
import re
import json
class JsonTree:
    
    '''
        @description: 
        @params: e  json文件路径 或 其他（字典、字符串、数值等）
        @author: MR.阿辉
        @datetime: 2024-01-03 10:58:26
        @return: 
    '''
    def __init__(self,e) -> None:
        # 判断是否为文件
        if self.is_path(e):
            with open(e,mode='r') as f:
                self.json_data = json.load(f)
        else:
            self.json_data=e
    
    '''
        @description: 验证传入进来的 json_data 是否为json文件
        @params: json文件地址或 字典
        @author: MR.阿辉
        @datetime: 2024-01-03 10:03:16
        @return: 返回 True or False
    '''
    def is_path(self,path):
        try:
            if  not isinstance(path, str):
                return False
            # os.path.exists(0) 返回为 True ，绝了
            return os.path.exists(path) and os.path.isfile(path)
        except Exception as _:
            return False        
    
    '''
        @description: 自定义json xpath语法，按照自己的业务需求来定义json解析规则
        @params: query 自定义的jsonxpath语法规则
        @author: MR.阿辉
        @datetime: 2024-01-03 10:04:51
        @return:  返回一个新的 JsonTree 对象
    '''
    def xpath(self,query):
        
        if  isinstance(self.json_data, list):
            return self.__xpath_list(query)
        elif isinstance(self.json_data,dict):
            return self.__xpath_dict(query)
        else:
            return JsonTree(self.json_data)
    
    '''
        @description: 解析单个
        @params: 
        @author: MR.阿辉
        @datetime: 2024-01-03 10:15:51
        @return: 
    '''
    def __p(self,p):
        # 获取表达式
        b = re.findall('\[(.*)\]',p)
        
        if len(b) > 0:
            return (re.findall('(.*?)\[',p)[0],b[0])
        return (p,None)
    
    '''
        @description:  解析 query 语法规则
        @params: 
        @author: MR.阿辉
        @datetime: 2024-01-03 10:10:18
        @return: 
    '''
    def __query_analysis(self,query):
        pipeline = []
        f,t=0,True
        for i,e in enumerate(query):
            if e == '.' and t ==True:
                pipeline.append(query[f:i])
                f=i+1
            elif e == '[':
                t = False
            elif e == ']':
                t = True
                pipeline.append(query[f:i+1])
                f=i+1
        if f < len(query):
            pipeline.append(query[f:])
        return pipeline
    
    def __xpath_dict(self,query):
        
        pipeline = self.__query_analysis(query)
        if len(pipeline) == 0 :
            return JsonTree(None)
        
        p = self.__p(pipeline.pop(0))
        
        if p[0] == '_':
            for k,v in self.json_data.items():
                element = v
                break
        else:
            element =  self.json_data.get(p[0])
        
        if len(pipeline) == 0:
            if  isinstance(element, list):
                # 判断是否为过滤表达式
                if p[1] is not None and p[1].strip().startswith('?'):
                    #match = re.search(r'\?(\w+)([!=><]+)(.*)', p[1].replace(' ',''))
                    pass
                
                return [JsonTree(e) for e in  element]
            elif isinstance(element,dict):
                return JsonTree(element)
            else:
                return JsonTree(element)
        
        self.json_data = element
        return self.xpath('.'.join(pipeline))
    
    '''
        @description: 解析 数组型的字典
        @params: 
        @author: MR.阿辉
        @datetime: 2024-01-03 10:06:52
        @return: 返回一组新的JsonTree对象
    '''
    def __xpath_list(self,query):
        return list(filter(lambda x: x.get() is not None,[JsonTree(e).xpath(query) for e in self.json_data]))
    
    '''
        @description: 如果为列表 弹出 self.json_data 第一个元素，否则直接返回 self.json_data
        @params: fields 需要过滤的字段
        @author: MR.阿辉
        @datetime: 2023-12-29 17:26:18
        @return: 
    '''
    def take(self,fields:list=None):
        if  isinstance(self.json_data, list):
            data = self.json_data.pop(0)
        else:
            data = self.json_data
        
        if fields is not None and isinstance(fields,list):
            return {field: JsonTree(data).xpath(field).get() for field in fields}
        elif fields is not None and isinstance(fields,str):
            return JsonTree(data).xpath(fields).get()
        else:
            return data
        
    def get(self):
        return self.json_data
    
    def __del__(self):
        self.json_data = None


if __name__ == "__main__" :

    json_tree = JsonTree('/Users/zhangzhonghui/Documents/project/python/spider/information/source/json/zhihu/you-ran-27-70.json')

    for e in  json_tree.xpath('data.target'):
        print(e.take('question.title'))# 标题