import os
import re
import sys
import time
import json
import pickle
import execjs
import datetime
import requests
from enum import Enum
from lxml import etree
from functools import wraps
from diskcache import Cache
from typing_extensions import Self
import requests.models as requests_models
from urllib.parse import urlparse,parse_qs
from typing import List,Union,Optional,cast
import requests.sessions as  requests_sessions
import requests.structures as requests_structures
from execjs._external_runtime import ExternalRuntime
from .config import Logger,Utils

# TODO: 请求方式
class RequestModule(Enum):
    GET = 'get'
    POST = 'post'
    OPTIONS = 'options'
    
# TODO：数据类型
class DataType(Enum):
    TEXT = 1 # 字符串
    BYTE = 2 # 字节
    DICT = 3 # 字典
    
# TODO: 文件类型
class FileType(Enum):
    # 文本文件格式
    TXT = 'txt'
    CSV = 'csv'
    JS = 'js'
    XLSX = 'xlsx'
    JSON = 'json'
    HTML = 'html'
    PDF = 'PDF'
    LOG = 'log'
    
    # 图片文本格式
    PNG = 'png'
    JPG = 'jpg'
    WEBP = 'webp'
    
    # 视频音频文本格式
    M4A = 'm4a'
    MP3 = 'mp3'
    MP4 = 'mp4'
    M3U8 = 'm3u8'
    
    # 特殊文本格式
    TS = 'ts'
    PICKLE = 'pickle'
    KEY='key'

# TODO: 操作系统对应的请求头
class DeviceHeaders(Enum):
    PC_MAC = 'PC-Mac'
    PC_WINDOWS = 'PC_Windows'
    MP_ANDROID = 'MP-Android'
    MP_IPHONE = 'MP-iPhone'

'''
    @description: 装饰器工具类
    @author: MR.阿辉
    @datetime: 2024-01-22 13:47:57
'''
class DecoratorTools():
    # TODO: 日志文件
    INIT_FILE_HANDLER = False
    
    def __init__(self,project_file) -> None:
        self.project_name,self.project_dir,self.source_dir = Utils.get_project_info(project_file)
        
    
    @staticmethod
    def __initfile_handler():
        if DecoratorTools.INIT_FILE_HANDLER is False:
            DecoratorTools.INIT_FILE_HANDLER = True
    
    '''
        @description: 装饰器-函数异常重试
        @params: max_retry_count 最大重试次数 默认3次
        @params: time_interval 每次重试的时间间隔
        @author: MR.阿辉
        @datetime: 2023-12-17 21:27:30
        @return: 
    '''
    @staticmethod
    def task_retry(max_retry_count:int=3,time_interval:int=3):
        def dector(func):
            @wraps(func)
            def wrapper(*args,**kwargs):
                logger = Logger(f'{args[0].source_dir}/log/request',args[0].project_name,'request')
                
                # 运行开始时间
                start_time = time.time()
                
                # 函数循环重试
                for ranking in range(max_retry_count):
                    try:
                        # 函数执行
                        resut = func(*args,**kwargs)
                        logger.logger.info(f'函数「{func.__name__}」；总共运行时长:「{Utils.format_seconds(time.time()-start_time)}」，重试次数「{ranking}」次。')
                        return resut
                    except Exception as e:
                        logger.logger.exception(f"请求异常:\n{e}")
                        logger.logger.warning(f'函数({func.__name__}): 「{time_interval}」秒之后，准备进行第「{ranking+1}」次重试；')
                        time.sleep(time_interval)
            return wrapper
        return dector
    
    
    '''
        @description: 发送请求日志记录
        @params: log_dir 日志保存目录
        @author: MR.阿辉
        @datetime: 2024-01-22 11:44:35
        @return: 
    '''
    @staticmethod
    def log(logmsg:str=None): # type: ignore
        
        def dector(func):
            # 所执行的函数名称
            function_name = func.__name__
            
            def send_logging(logger,*args,**kwargs):
                # 请求地址
                url = kwargs.get('url')
                # 请求方式
                module = RequestModule.GET.value if kwargs.get('module') is None else kwargs.get('module')
                # 请求参数
                params = {} if kwargs.get('params') is None else kwargs.get('params')
                # 请求头
                headers = {} if kwargs.get('headers') is None else kwargs.get('headers')
                
                logger.info('================ start send request ================ ')
                
                logger.info(f'请求地址: {url}')
                logger.info(f'请求方式: {module}')
                logger.info(f'请求参数: {json.dumps(params,ensure_ascii=False)}')
                logger.info(f'请求头: {json.dumps(headers,ensure_ascii=False)}')
                
                # 运行开始时间
                start_time = time.time()
                # 开始发送请求
                resut = func(*args,**kwargs)
                logger.info(f'此次请求总计耗时: 「{Utils.format_seconds(time.time()-start_time)}」')
                logger.info('================ end send request ================ ')
                logger.info('\n')
                return resut
            
            def session_cookies_logging(logger,*args,**kwargs):
                
                k = args[1] if len(args) > 1 else None
                v = args[2] if len(args) > 2 else None
                
                result  = func(*args,**kwargs)
                
                if k is None and v is None:
                    logger.info('从 request session 中获取所有的cookie信息: ')
                    logger.info(result)
                elif k is not None and v is None:
                    logger.info(f'从 request session 中获取key 为: {k} 的cookie信息: ')
                    logger.info(f'cookie 值为: {v}')
                else:
                    logger.info(f'向 request session key 为: {k} 的cookie信息: ')
                    logger.info(f'cookie 值为: {v}')
                
                return result
            
            def deserialize_session_logging(logger,*args,**kwargs):
                logger.info('正在进行request session 反序列化...')
                result  = func(*args,**kwargs)
                if result:
                    logger.info('反序列化完成...')
                else:
                    logger.info('文件已失效，需要重新进行序列化...')
                return result
            
            @wraps(func)
            def wrapper(*args,**kwargs):
                logger = Logger(f'{args[0].source_dir}/log/request',args[0].project_name,'request')
            
                DecoratorTools.__initfile_handler()

                if logmsg is not None:
                    logger.logger.info(logmsg)
                
                # 记录发送请求日志
                if  function_name == 'send':
                    return send_logging(logger.logger,*args,**kwargs)
                elif function_name == 'execjs':
                    logger.logger.info('js 文件调用')
                    logger.logger.info(kwargs)
                    logger.logger.info(args)
                elif function_name == 'response_cookie':
                    result  = func(*args,**kwargs)
                    logger.logger.info(f'从 response 中获取 cookie 为: {args[1]} 的value: {result} ...')
                    return result
                elif function_name == 'session_cookies':
                    return session_cookies_logging(logger.logger,*args,**kwargs)
                elif function_name == 'deserialize_session':
                    return deserialize_session_logging(logger.logger,*args,**kwargs)
                elif function_name == 'serialize_session':
                    logger.logger.info('准备对 request ession 进行持久化...')
                    logger.logger.info(f'序列化时长 {kwargs}')
                else:
                    logger.logger.info(f'执行函数 {function_name} ...')
                    logger.logger.info(args)
                    logger.logger.info(kwargs)
                    logger.logger.info('\n')
                
                return func(*args,**kwargs)
            return wrapper
        return dector
    
'''
    @description: 自定义数据请求类
    @author: MR.阿辉
    @datetime: 2023-12-06 19:03:49
'''
class Request(Logger):
        
    '''
        @description: 构造器，实例化一个新的Request对象
        @params: project_file 项目地址，创建 Request 对象是指定为 os.path.abspath(__file__) 即可
        @params: device 设备，默认为 pc mac。
        @params: print_banner 是否打印 banner图
        @params: send_mail 是否发送邮件告警？默认为False
        @author: MR.阿辉
        @datetime: 2024-01-22 16:17:53
        @return: 
    '''
    def __init__(self,
                project_file:Optional[str],
                device:DeviceHeaders=DeviceHeaders.PC_MAC,
                print_banner:bool=True,
                send_mail:bool=False) -> None:
        self.device = device
        self.banner(print_banner)
        self.project_file=project_file
        self.project_name,self.project_dir,self.source_dir = Utils.get_project_info(project_file)
        super().__init__(f'{self.source_dir}/log/request',self.project_name,'request')

        self.send_mail = send_mail
        
    '''
        @description: 进入上下文管理器
        @params: 
        @author: MR.阿辉
        @datetime: 2024-03-21 22:18:31
        @return: 
    '''
    def __enter__(self) -> Self:
        self.start_time:float = time.time()
        # 初始化 session
        self.session = self.__init_session(self.device)
        return self
    
    '''
        @description: 生成 banner 图
        banner 图片在线网站；https://www.bootschool.net/ascii-art 
        print 颜色码 https://blog.csdn.net/cui_yonghua/article/details/129751013
        @params: 
        @author: MR.阿辉
        @datetime: 2024-02-05 12:37:13
        @return: 
    '''
    def banner(self,print_banner):
        # TODO: 读取本地 banner 图，需要保证common/source目录下，有个banner.txt文件
        common_dir = os.path.abspath(__file__).split('src')[0]
        banner_file = f'{common_dir}source/banner.txt'
        if print_banner and os.path.exists(banner_file):
            current_time =datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(banner_file,mode='r') as f:
                text = re.sub('(\d{4}.*\d{2})',f'\033[1;32m{current_time}\033[0m' ,f.read())
                text = re.sub('(作者名称)','\033[1;35m阿辉大人\033[0m',text)
                print(f"\033[1;33m{text}\033[0m")
    
    '''
        @description: 初始化 session
        @params: 电脑 device 信息
        @author: MR.阿辉
        @datetime: 2024-01-22 16:18:36
        @return: 
    '''
    @DecoratorTools.log('初始化 RequestSession ...')
    def __init_session(self,device:DeviceHeaders) -> requests_sessions.Session:
        session = requests.session()
        
        # 设置请求头
        session.headers = Utils.get_headers(device.value)
            
        # TODO：配置请求连接池
        adapter = requests.adapters.HTTPAdapter(  # type: ignore
            pool_connections = 10,
            pool_maxsize = 50,
            max_retries = 3,
            pool_block=False)
        
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    
    '''
        @description: 获取当前项目的source目录地址
        @params: 
        @author: MR.阿辉
        @datetime: 2023-12-18 09:43:07
        @return: 
    '''
    @DecoratorTools.log('获取项目的source目录地址 ...')
    def get_source_dir(self):
        return self.source_dir
    
    '''
        @description: 解析 js 文件
        @params: jsname js 文件名，可以不带 .js，会从当前项目中查找 该js文件，如果不存在则取 common 项目中查找，如果都不存在则报错。
        @params: project js 所属项目，有些时候我们需要引入其他项目的js文件。
                project表示需要引入js的所属项目名称。如果为空则引入当前项目或common项目的js
        @author: MR.阿辉
        @datetime: 2023-12-06 18:35:50
        @return: js 对象
    '''
    @DecoratorTools.log('准备执行js文件 ...')
    def execjs(self,jsname:str,project:Optional[str]=None) -> ExternalRuntime.Context: 
        
        def build_jspath(source_dir):
            return os.path.join(source_dir,f'js/{jsname}') if jsname.endswith('.js') else os.path.join(source_dir,f'js/{jsname}.js')
        
        if project is None:
            # 判断是否以.js结尾
            js_path = build_jspath(self.source_dir)
        else:
            js_path = build_jspath(os.path.join(os.path.abspath(project),'source'))
        
        # 判断文件是否存在，如果不存在则从从 common 模块查找。
        if not os.path.exists(js_path):
            common_dir = os.path.abspath(__file__).split('src')[0]
            source_dir = f'{common_dir}source/'
            js_path = build_jspath(source_dir)        
        
        with open(js_path,mode='r') as f:
            return execjs.compile(f.read())

    '''
        @description: 发送请求
        @params: url 请求地址
        @params: module 请求方式
        @params: params 请求参数,
        @params: allow_redirects 开启重定向
        @params: renew_session 开启session缓存之后，发送请求之后是否更新cookie
        @params: proxies 代理
        @params: delay 延迟请求时长，单位秒，如果小于 1 则不延迟
        @author: MR.阿辉
        @datetime: 2023-12-06 18:34:05
        @return: 返回 then 进行数据回调
    '''
    @DecoratorTools.task_retry()
    @DecoratorTools.log('准备发送请求...')
    def send(self,
            url:str,
            module:RequestModule=RequestModule.GET,
            params=None,
            allow_redirects=True,
            headers:dict={},
            proxies:dict={},
            delay:int=0
        ):
        
        if len(headers.keys())<1:
            headers = Utils.get_headers('PC-Mac')
        
        
        # 延迟执行
        if delay > 0:
            time.sleep(delay)
        
        # 发送请求
        if module == RequestModule.GET:
            self.response:requests_models.Response = self.session.get(url,verify=False,params=params,headers=headers,proxies=proxies,allow_redirects=allow_redirects)
        elif module == RequestModule.OPTIONS:
            self.response:requests_models.Response = self.session.options(url,verify=False,params=params,headers=headers,proxies=proxies,allow_redirects=allow_redirects)
        elif module == RequestModule.POST:
            # 默认格式为 'application/x-www-form-urlencoded'
            post_params = params
            
            # 检查是否为 application/json
            content_type = headers.get('Content-Type')
            if re.search('application/json',str(content_type)) and isinstance(params , dict):
                #  application/json格式的请求头是指用来告诉服务端post过去的消息主体是序列化后的 JSON 字符串。
                post_params = json.dumps(params,separators=(',', ':'))                
                # 区别：请求头格式为application/x-www-form-urlencoded与application/json的主要差别在于请求主体的构造格式（前者是键值对，后者是JSON串）,前者直接用字典传入，后者用json.dumps()函数将字典转为JSON串即可。
            elif re.search('application/x-www-form-urlencoded',str(content_type)):
                # 除了传统的application/x-www-form-urlencoded表单，我们另一个经常用到的是上传文件用的表单，这种表单的类型为multipart/form-data，
                # multipart/form-data主要用于文件上传，当我们使用它时，必须让 form表单的enctype 等于 multipart/form-data
                pass
            
            
            # 发送 post 请求
            self.response:requests_models.Response = self.session.post(url,
                    verify=False,
                    data=post_params,
                    headers=headers,
                    proxies=proxies,
                    allow_redirects=allow_redirects)

        
        return self.then
    
    '''
        @description: 获取请求 session
        @params: 
        @author: MR.阿辉
        @datetime: 2023-12-06 18:33:41
        @return: session 对象
    '''
    @DecoratorTools.log('获取当前 RequestSession 信息...')
    def get_session(self):
        return self.session
    
    '''
        @description:  获取 session cookie 属性
        @params: key，可以为空，返回所有响应头信息 ，否则返回该key的请求头信息
        @params: value, 如何 key 和 value 都不为空，则向 headers 添加数据，并返回 value。
        @author: MR.阿辉
        @datetime: 2023-12-06 18:32:26
        @return: 返回 key 所对应的内容，或所有的 cookie信息
    '''
    @DecoratorTools.log('session cookies 设置/获取...')
    def session_cookies(self,key:Optional[str]=None,value:Optional[str]=None):
        if key is not None and value is not None:
            self.session.cookies[key] = value
            return  value
        elif  key is not None:
            return self.session.cookies.get(key)
        return self.session.cookies
    
    '''
        @description: 获取 response 响应头 信息
        @params: key，可以为空，返回所有响应头信息 ，否则返回该key的请求头信息
        @params: value, 如何 key 和 value 都不为空，则向 headers 添加数据，并返回 value。
        @author: MR.阿辉
        @datetime: 2023-12-06 18:30:17
        @return: key 所对应的值或响应头所有的数据，以字典的形式返回。
    '''
    @DecoratorTools.log('response 请求头 设置/获取...')
    def response_headers(self,key:Optional[str]=None,value:Optional[str]=None) -> Union[str,requests_structures.CaseInsensitiveDict,None]:
        if key is not None and value is not None:
            self.response.headers[key] = value
            return  value
        if  key is not None:
            return self.response.headers.get(key)
        return self.response.headers

    '''
        @description: 获取 response 中 Set-Cookie 值
        @params: key
        @author: MR.阿辉
        @datetime: 2023-12-09 23:42:08
        @return: return value
    '''
    @DecoratorTools.log('从 response 中 获取 cookie ...')
    def response_cookie(self,key:str) -> Optional[str]:
        # set_cookie = resp.headers['Set-Cookie']
        # session.cookies["_zap"] = re.findall('_zap=(.*?);',set_cookie)[0]
        set_cookie = self.response_headers('Set-Cookie')
        if set_cookie == None:
            return set_cookie
        values = re.findall(f'{key}=(.*?);',set_cookie) # type: ignore
        return values[0] if len(values) > 0 else ''
    
    '''
        @description: 解析 html
        @params: xpath_str xpath 语法格式
        @author: MR.阿辉
        @datetime: 2023-12-06 18:31:49
        @return:  xpath 对象
        @DecoratorTools.log('xpath 解析...')
    '''
    def xpath(self,xpath_str) -> list:
        if self.response.status_code == requests.codes.ok:
            html = etree.HTML(self.response.text,parser=None)
            return html.xpath(xpath_str)
        return []
    
    '''
        @description: 解析url 上的参数
        @params: url web url
        @params: key key 如果为 None，返回url上所有的参数，
        @author: MR.阿辉
        @datetime: 2023-12-06 18:28:08
        @return:  如果指定了 key 返回 key 所对应的值，如果key为空则返回所有url所有的参数，以字典的形式返回。
    '''
    def get_url_params(self,url,key:Optional[str]=None):
        
        url_parse = urlparse(url)
        query_parmas = url_parse.query
        if query_parmas is None or query_parmas == '':
            query_parmas = urlparse(url_parse.fragment).query
        
        
        params = parse_qs(query_parmas)
        if key is not None:
            return  ''.join(params.get(key)) # type: ignore
        
        return params
    
    '''
        @description: 检查文件是否存在，不存在则创建该文件所属目录，并返回该文件完整地址。
        @params: file_path 文件路径
        @params: file_type 文件类型，定义成字典
        @params: file_name 文件名称
        @author: MR.阿辉
        @datetime: 2024-02-06 14:08:06
        @return: 新创建或已存在的文件全路径
    '''
    def save_path(self,
                file_path:str,
                file_type:FileType=FileType.TXT,
                file_name:Optional[str]=None
            ) -> str:
        # 如果 file_path 没有指定，则使用 url path 生成。
        def build_file_path(file_path):
            # 如果 file_path 是 / 开头的，需要剔除/         
            if file_path.startswith('/') and file_path.__len__() >0:
                file_path  = file_path[1:]
            
            if file_path.__len__() == 0:
                file_path =file_type.value
            return file_path
        
        # 检查文件夹是否存在，不存在则创建
        save_dir = os.path.join(self.source_dir,build_file_path(file_path))
        # 如果 file_path 是一个 目录则生成一个新的文件名
        if file_name is None:
            # 通过日期生成文件名
            file_name = f'{datetime.datetime.now().strftime("%Y%m%d")}.{file_type.value}'
        
        if file_name.split('.').__len__() == 1:
            file_name = f'{file_name}.{file_type.value}'
        
        return Utils.mkdirs(save_dir,file_name)
    
    '''
        @description: 将数据保存到文件中
        @params: data_type 数据类型， 默认为字符串，可以改为 byte
        @params: fill_list 填充，字符串列表，只有保存文本文件时有用
        @params: file_type 文件类型
        @params: file_path 文件保存地址，可以为空，会根据 请求的url进行生成，不为空则保存到当前项目的 source 目录下。 例如 输入 a/b 或 /a/b 全路径就是 xxx/source/a/b
        @params: file_name 文件名称，如果指定文件后缀，则根据数据类型来
        @author: MR.阿辉
        @datetime: 2023-12-06 18:26:45
        @return: 文件地址
    '''
    def sink2file(self,
            data_type:DataType=DataType.TEXT,
            fill_list:Optional[list]=None,
            file_type:FileType=FileType.TXT,
            file_path:Optional[str]=None,
            file_name:Optional[str]=None) -> str:
        
        self.logger.info('================ start sink file ================ ')
        # 请求url
        request_url:str = cast(str,self.response.request.url)
        
        if file_path is None:
                file_path = urlparse(request_url).path
        
        save_path:str = self.save_path(file_path,file_type,file_name)
        
        
        if data_type == DataType.BYTE:
            with open(save_path,mode='wb') as f:
                f.write(self.response.content)
        
        elif data_type == DataType.TEXT:
            # 保存文件
            with open(save_path,mode='w') as f:
                # 追加内容
                if fill_list is not None:
                    f.writelines(fill_list)
                
                if file_type == FileType.JSON:
                    f.write(json.dumps(self.response.json(),ensure_ascii=False))
                else:
                    # 写入文件
                    f.write(self.response.text)
            
        return save_path
    
    '''
        @description: 这个功能挺常用的，专门用于下载图片
        @params: url 图片地址
        @params: file_name 文件名称
        @params: file_path 文件保存地址
        @author: MR.阿辉
        @datetime: 2024-01-14 13:56:06
        @return: 图片地址
    '''
    def sink2picture(self,url:str,file_name:str,file_path:str,file_type:FileType=FileType.WEBP) -> str:
        self.send(url)
        return self.sink2file(
            file_name=file_name,
            file_path=file_path,
            file_type=file_type,
            data_type=DataType.BYTE)
    
    '''
        @description: 解析 jsonp 
        @params: jsonpstr 字符串
        @author: MR.阿辉
        @datetime: 2023-12-06 18:39:54
        @return: 以字典的形式返回
    '''
    def parse_jsonp(self,jsonpstr:str)-> dict:
        #r"\((?P<code_str>.*)\)"
        result = re.match("^[^(]*?\((.*)\)[^)]*$",jsonpstr,re.S)
        if result is not None:
            return json.loads(result.group(1))
        return {}
    
    '''
        @description: 该功能比较常见，用于从javascript 中提取内容，
        @params: regex 正则表达式。
        @params: out_type 响应数据类型
        @params: flags
        @author: MR.阿辉
        @datetime: 2024-02-06 14:34:07
        @return: 
    '''
    @DecoratorTools.log('解析javascript...')
    def javascript_extract(self,regex:str,out_type:DataType=DataType.TEXT,flags:int=re.S) -> Union[dict,str]:
        html_str = self.response.text
        self.logger.info('javascript_extract')
        self.logger.info(html_str)
        
        result = re.search(regex,html_str,flags)
        if result:
            if out_type == DataType.DICT:
                return execjs.eval('(function(t){return t})('+result.group(1)+')')    
            elif out_type == DataType.TEXT:
                return result.group(1)
        return ''
    '''
        @description:  响应回调
        @params: callback 回调函数
        @author: MR.阿辉
        @datetime: 2024-01-11 16:04:15
        @return: 
    '''
    def then(self,callback):
        return callback(self.response)

    '''
        @description: 序列化session
        @params: expire 缓存过期时长，可根据网站实际时间进行设置
        @params: unit 时长单位; sec 秒、min 分、 hour 小时、day 天 默认为 min
        @params: params 持久化 request session 时保存的一些额外参数信息，
            params 主要用于登录之后返回一些额外信息的场景；例如tooken，这种信息很难从session中获取到，所以需要额外保存。
            具体使用场景可以参考 海南免税
        @author: MR.阿辉
        @datetime: 2024-01-11 16:03:52
        @return:  无任何返回
    '''
    @DecoratorTools.log('request session 序列化...')
    def serialize_session(self,expire:int=60,unit:str='min',params:Optional[dict]=None) -> None:
        unit_to_seconds = {
            'sec': 1,
            'min': 60,
            'hour': 3600,
            'day': 216000
        }
        
        # session 持久化时长
        expire = expire * unit_to_seconds[unit]
        
        # 指定 session 缓存所在目录
        session_cache = Cache(os.path.join(self.source_dir,'cache/session/'))
        session_cache.set(self.project_file,pickle.dumps(self.session),expire=expire)
        
        # 持久化参数
        if params is not None:
            params_cache = Cache(os.path.join(self.source_dir,'cache/params/'))
            params_cache.set(self.project_file,pickle.dumps(params),expire=expire)
        
    
    '''
        @description: 反序列化session
        @params: url 用于验证session是否失效问题。
        @author: MR.阿辉
        @datetime: 2024-01-11 16:32:29
        @return:  返回 dict 类型，
            result: 表示 sesion 序列化结果，True 表示反序列化成功。False表示失败或没有
            params: 持久化时所保存的参数，
    '''
    @DecoratorTools.log('request session 反序列化...')
    def deserialize_session(self,url:Optional[str]=None) -> dict:
        # 指定 session 缓存所在目录
        session_cache = Cache(os.path.join(self.source_dir,'cache/session/'))
        session_result = session_cache.get(self.project_file)
        #  如果数据为 None，返回 False，告知用户缓存已经失效需要重新进行缓存。
        if session_result is None:
            return {
                'result':False,
                'params':None
            }
        # 使用 pickle 反序列化 session 对象
        self.session = pickle.loads(session_result)  # type: ignore
        if url is not  None:
            resp  = self.session.get(url=url,verify=False)
            
            # cookie_header = resp.headers.get('Set-Cookie')
            # # sesion 已经过期
            # if cookie_header is  None:
            #     return {
            #         'result':False,
            #         'params':None
            #     }
                
            # # 查看session过期时间
            # expires = ''.join(re.findall('expires=(.*?);',cookie_header,flags=re.IGNORECASE))

            # t = datetime.datetime.strptime(expires, '%a, %d-%b-%Y %H:%M:%S GMT')
            
        
        # 反序列化参数
        params_cache = Cache(os.path.join(self.source_dir,'cache/params/'))
        params_result = params_cache.get(self.project_file)
        
        return {
            'result': True,
            'params': {} if params_result is None else  pickle.loads(params_result)  # type: ignore
        }
    
    '''
        @description: 退出上下文管理器
        @params: 
        @author: MR.阿辉
        @datetime: 2024-03-21 22:18:07
        @return: 
    '''
    def __exit__(self,exc_type,exc_value,exc_traceback):
        self.session.close()
        self.logger.info(f'此次任务总计耗时: {Utils.format_seconds(time.time() - self.start_time)}')