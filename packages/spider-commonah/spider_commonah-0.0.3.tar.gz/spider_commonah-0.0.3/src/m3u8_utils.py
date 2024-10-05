from ast import Index
import os
import re
import shutil
import asyncio
import aiohttp
import aiofiles
from tqdm import tqdm
from aiohttp import TCPConnector
from request_session import DataType, Request
from request_session import Request,FileType,DataType


class M3U8Utils:
    
    FFMPEG_HOME:str = '/Users/zhangzhonghui/Documents/plug/ffmpeg'
    
    def __init__(self,request:Request,restart=False):
        self.request = request
        self.restart = restart
        self.ts_urls = []
        # 标记是否合并成功
        self.merge_success = False
        # 并发控制
        self.semaphore = asyncio.Semaphore(10)

    '''
        @description: 从 web_url 中解析 出 m3u8 url
        @params: web_url 网站地址
        @params: callback 回调函数
        @author: MR.阿辉
        @datetime: 2024-09-12 22:18:26
        @return: 
    '''
    def build_m3u8_url(self,
                web_url:str,callback):
        # TODO: Implement function to get m3u8 file from url
        self.m3u8_url:str = self.request.send(url=web_url)(callback)
        return self
    
    '''
        @description: 保存 m3u8 文件
        @params: file_path 保存 m3u8 文件的路径
        @params: file_name m3u8 文件的名称
        @author: MR.阿辉
        @datetime: 2024-09-12 22:24:07
        @return: 
    '''
    def save_m3u8_file(self,file_path:str,file_name:str='data'):
        self.source_file_path = file_path
        
        # TODO: Implement function to save m3u8 file
        self.request.send(url=self.m3u8_url)
        
        # 生成一个 data.m3u8 文件路径
        self.m3u8_file_path = self.request.sink2file(
            file_path=file_path,
            file_name=file_name,
            file_type=FileType.M3U8,
            data_type=DataType.TEXT)
        
        return self
    

    '''
        @description: 解析 m3u8 文件
        @params: parse_key_callback 解析 key 的回调函数
        @params: parse_ts_callback 解析 ts 的回调函数
        @author: MR.阿辉
        @datetime: 2024-09-12 22:48:29
        @return: 
    '''
    def parse_m3u8_file(self,
            parse_key_callback,
            parse_ts_callback):
        
        # TODO: Implement function to parse m3u8 file
        
        with open(self.m3u8_file_path, 'r') as f:
            for index,line in enumerate(f.readlines()):
                key_result = parse_key_callback(self.m3u8_url,line)
                if key_result is not None:
                    self.key_url = (index+1,key_result)
                ts_result:str = parse_ts_callback(self.m3u8_url,line)
                if ts_result is not None:
                    ts_url:str = ts_result.strip().replace('\n','')
                    self.ts_urls.append((index+1,ts_url)) 
        return self
    
    '''
        @description: 使用协程下载 ts 文件
        @params: 
        @author: MR.阿辉
        @datetime: 2024-09-13 13:42:03
        @return: 
    '''
    async def __download_ts(self,file_path:str,ts_index:int,ts_url:str,pbar,retry_num:int=0):
        retry_num = retry_num + 1
        for _ in range(10):
            try:
                # 并发控制
                async with self.semaphore:
                    headers = self.request.get_session().headers
                    
                    # 下载
                    async with aiohttp.ClientSession(
                        headers=headers,connector=TCPConnector(ssl=False)) as session: # type: ignore
                        async with session.get(url=ts_url,headers=headers) as resp:
                            if resp.status >= 200 and resp.status < 300:
                                async with aiofiles.open(file_path,mode='wb') as f:
                                    await f.write(await resp.read())
                                    # 更新进度条
                                    pbar.update(1)
                                    
                            else:
                                print(ts_url, f"下载失败!, 准备第 {retry_num} 次重试 ")
                                # 暂停 n 秒后继续
                                await asyncio.sleep(3)
                                return await self.__download_ts(file_path,ts_index,ts_url,pbar,retry_num)
            
            except Exception as e:
                print(e)
                print(ts_url, f"下载失败!, 准备第 {retry_num} 次重试 ")
                # 暂停 n 秒后继续
                await asyncio.sleep(3)
                return await self.__download_ts(file_path,ts_index,ts_url,pbar,retry_num)
    
    '''
        @description: 构建 下载任务
        @params: 
        @author: MR.阿辉
        @datetime: 2024-09-13 13:42:39
        @return: 
    '''
    async def __build_tasks(self):
        
        # 设置 ts 文件保存路径
        ts_dir = os.path.dirname(self.m3u8_file_path)
        
        task_list = []
        with tqdm(total=len(self.ts_urls),ascii=True,desc='downloading ts file') as pbar:
            for index,ts_url in self.ts_urls:
                
                ts_file_path =  os.path.join(ts_dir,f'{index}.ts')
                # 检查 ts 文件是否存在，避免重复下载,并且不需要标识为重新下载
                if not os.path.exists(ts_file_path) or self.restart:
                    task = self.__download_ts(ts_file_path,index,ts_url,pbar)
                    task_list.append(task)
            if len(task_list) > 0:
                return await asyncio.wait(task_list)


    '''
        @description: 合并 ts 文件
        @params: mp4_file_name mp4 文件名(全路径)
        @author: MR.阿辉
        @datetime: 2024-09-13 13:47:37
        @return: 
    '''
    def __merge_ts(self,mp4_file_name):
        ts_dir = os.path.dirname(self.m3u8_file_path)
        
        # 获取目录下所有的文件 过滤 key.m3u8
        ts_list:list = list(filter(lambda x:len(re.findall('.ts',x))>0,os.listdir(ts_dir)))
        ts_map:dict = {int(re.findall('\d+',file_name)[0]):file_name for file_name in ts_list}
        
        # 生成 index.m3u8
        file_path = os.path.join(ts_dir,'index.m3u8')
        with open(file_path,mode='w') as f:
            with open(self.m3u8_file_path,mode='r') as m3u8_file:            
                for index,line in enumerate(m3u8_file.readlines()):
                    serial:int = index+1
                    # 定义 key的位置
                    if self.key_url is not None and self.key_url[0] == serial:
                        # 正则替换
                        key_path:str = os.path.join(ts_dir,'key.key')
                        new_key = f'URI="{key_path}"'
                        new_line:str = re.sub('URI="(.*/key.key)"',new_key,line)
                        f.write(new_line)
                    elif serial in ts_map:
                        ts_file_name:str = ts_map.get(serial) # type: ignore
                        f.write(f"{ts_file_name}\n")
                    else:
                        f.write(line)
        
        try:
            # 使用 ffmpeg 对文件进行合并
            md = f'{M3U8Utils.FFMPEG_HOME} -allowed_extensions ALL -protocol_whitelist "file,http,crypto,tcp" -i {file_path} -c copy {mp4_file_name}'

            print('ffmpeg 合并命令:',md)
            os.system(md)
            self.merge_success = True
        except Exception as e:
            print(e)
            print("合并失败!")


    '''
        @description: 下载视频
        @params: 
        @author: MR.阿辉
        @datetime: 2024-09-13 13:45:52
        @return: 
    '''
    def download(self,
            mp4_save_path:str,
            mp4_file_name:str):
        # 下载 key 文件
        if self.key_url is not None:
            # 下载 key.key 加密文件到本地
            self.request.send(url=self.key_url[1])
            self.request.sink2file(file_path=self.source_file_path,
                file_name='key.key',
                data_type=DataType.BYTE)
        
        # 创建事件循环
        loop = asyncio.get_event_loop()
        try:
            
            #将协程对象加入到消息循环
            loop.run_until_complete(self.__build_tasks())
        finally:
            print('closing event loop')
            loop.close()
        
        # 生成 mp4 文件 
        mp4_file = self.request.save_path(
            file_path=mp4_save_path,
            file_name=mp4_file_name,
            file_type=FileType.MP4)
        
        self.__merge_ts(mp4_file)

    
    def __del__(self):
        if self.merge_success:
            # 清理下载历史文件
            shutil.rmtree(os.path.dirname(self.m3u8_file_path))