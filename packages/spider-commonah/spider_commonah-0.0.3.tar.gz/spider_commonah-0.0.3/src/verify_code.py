'''
    @description: 基于 ddddocr 实现的各种场景下的图片识别
    @params: 
    @author: MR.阿辉
    @datetime: 2023-12-31 09:12:48
    @return: 
'''
import re
import os
import sys
import cv2
import json
import math
import time
import base64
import ddddocr
import requests
import numpy as np
from io import BytesIO
from typing import Optional, Union,Tuple
from PIL import Image
from request_session import Request

class Utils():
    
    '''
        @description: 判断字符串是否为 base64字符串
        @params: text 文本内容
        @author: MR.阿辉
        @datetime: 2023-12-31 09:50:19
        @return: bool
    '''
    def is_base64(self,text):
        try:
            # 剔除换行符
            text = re.sub('(\r|\n)','',text)
            
            # 将字符串解码为二进制数据
            decoded_data = base64.b64decode(text)
            
            # 将二进制数据编码为字符串
            encoded_data = base64.b64encode(decoded_data)
            
            
            if len(text) % 4 == 0 and encoded_data == text.encode():
                return True
            else:
                return False
        
        except Exception as e:
            print("Error occur red while checking string:", str(e))
            return False
    
    '''
        @description: 判断图片是否为 url 地址
        @params: test 文本
        @author: MR.阿辉
        @datetime: 2024-01-20 09:40:35
        @return: 返回判定结果，True or False
    '''
    def is_url(self,text:str) -> bool:
        pattern = r'^https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$'
        return re.match(pattern, text)
    
    
    '''
        @description: 请求图片的url将图片流转换成base64
        @params: url 图片的网络地址
        @author: MR.阿辉
        @datetime: 2024-01-20 09:44:52
        @return: base64 字符串
    '''
    def url2base64(self,url) -> Optional[bytes]:
        
        with Request(os.path.abspath(__file__)) as request:
            def callback(resp):
                if resp.status_code == 200:
                    # 打开图像文件
                    image = Image.open(BytesIO(resp.content))
                    buffered = BytesIO()
                    # 转换成 RGB 避免产生 OSError: cannot write mode RGBA as JPEG 异常
                    # 原因如下：这是因为RGBA意思是红色，绿色，蓝色，Alpha的色彩空间，Alpha指透明度。而JPG不支持透明度，所以要么舍弃Alpha透明度，要么保存为.png文件。
                    image = image.convert('RGB')
                    image.save(buffered,format='JPEG')
                    return base64.b64encode(buffered.getvalue())
                else:
                    return None
            return request.send(url=url)(callback)
    
    '''
        @description: 图片地址转 base64
        @params: image 可以是base64 字符串或文件路径。如果是文件则需要转换成 base64
        @author: MR.阿辉
        @datetime: 2023-12-12 12:59:53
        @return: 
    '''
    def image_b64(self,image:Union[str,bytes]) -> str:
        
        # 判断是否是否为字节，如果为字节则将字节转换成base64字符串
        if isinstance(image,bytes):
            return base64.b64encode(image).decode('utf-8')
        # 判断 image 是否为网络地址
        if self.is_url(image):
            # 将网络IO转换成Base64
            return self.url2base64(image)
        
        # 获取图片的base64，data:image/png;base64,我们得舍去
        m = re.match('data:.*;base64,(.*)',image)
        if m:
            return m.group(1)
        
        # 将图片文件转换成 base64
        if os.path.isfile(image):
            with open(image,'rb') as f:
                image_bytes = f.read()
                image_base64 = base64.b64encode(image_bytes).decode('utf8')
                return image_base64
        
        # 判断是否为 base64，如果是直接返回
        if self.is_base64(image):
            return image
    
    '''
        @description: 将base64 转换成 byte
        @params: image_base64 base64 字符串
        @author: MR.阿辉
        @datetime: 2023-12-31 09:32:57
        @return: 
    '''
    def base64_to_bytes(self,image_base64):
        image_bytes = base64.b64decode(image_base64)
        return image_bytes
    
    '''
        @description:图鉴
        @params: 
        @author: MR.阿辉
        @datetime: 2024-01-17 15:46:58
        @return: 
    '''
    def ttshitu(self,img, typeid):
        data = {"username": 'ahuidaren', "password": 'V8YH5jyTiB', "typeid": typeid, "image": self.image_b64(img)}
        result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
        if result['success']:
            return result["data"]["result"]
        else:
            #！！！！！！！注意：返回 人工不足等 错误情况 请加逻辑处理防止脚本卡死 继续重新 识别
            return result["message"]
    
    '''
        @description: 裁剪图片
        @params: image cv2 图像
        @params: x 裁剪 x 坐标
        @params: y 裁剪 y 坐标
        @params: w 裁剪图片宽度
        @params: h 裁剪图片高度
        @author: MR.阿辉
        @datetime: 2024-01-28 10:43:59
        @return: 
    '''
    def crop_image(self,image,x,y,w,h):
        #cropped_image = image.crop((x,y,x+w,y+h))
        # 起始点y坐标:结束点y坐标,起始点x坐标:结束点x坐标
        cropped_image = image[y:y+int(round(h,0)), x:x+int(round(w,0))]
        return cropped_image
        # # 展示图片
        # # cropped_image.show()
        #buffered = BytesIO()
        #cropped_image.save(buffered,format="JPEG")
        #return base64.b64encode(buffered.getvalue())
    
    '''
        @description: 图像重置大小，
        @params: image cv2 图像
        @params: resize int 数据类型， 正数，同比例扩大，负数，同比例缩小
        @author: MR.阿辉
        @datetime: 2024-01-28 10:45:45
        @return: 
    '''
    def resized_image(self,image,resize):        
        # 图片原始大小
        height, width = image.shape[:2]
        if resize > 0:
            target_width = width * resize
            target_height = height * resize
        elif resize < 0:
            target_width = width / abs(resize)
            target_height = height / abs(resize)
        return cv2.resize(image, (int(target_width), int(target_height)))

    


'''
    @description: 爬虫逆向，验证码识别工具类
    @params: 
    @author: MR.阿辉
    @datetime: 2 024-01-29 09:14:16
    @return: 
'''
class Verisy(Utils):
    
    '''
        @description: 
        @params: bg_image 背景图， 文件地址或base64图片（注意不含：data:image/jpg;base64,直接图片base64编码）。
        @params: slider_image 滑块图 可选，文件地址或base64图片（注意不含：data:image/jpg;base64,直接图片base64编码）。
        @author: MR.阿辉
        @datetime: 2023-12-31 09:14:50
        @return: 
    '''
    def __init__(self,bg_image:Union[str,bytes],slider_image:Union[str,bytes,None]=None) -> None:
        # 背景图
        self.bg_image = super().image_b64(bg_image)
        # 滑块图
        self.slider_image =  super().image_b64(slider_image) if slider_image is not None else None

    '''
        @description: 手动识别点选验证码，满足绝大部分点选场景；
            1. 注意网页点选验证码的尺寸，确定是否需要裁剪和缩小扩大。
            2. 点选坐标是从验证码左上脚到点选的位置，逆向过程中可能坐标计算是从浏览器左上角开始计算。
        @params: crop_size 裁剪比例： (x,y)
        @params: resize int 数据类型， 正数，同比例扩大，负数，同比例缩小
        @author: MR.阿辉
        @datetime: 2023-12-31 09:16:32
        @return: 例如 [(x,y),(x,y),(x,y)]
    '''
    def simple_click(self,crop_size:Tuple[int,int]=(-1,-1),resize:int=0):
        
        # 直接读取base64字节
        image = cv2.imdecode(np.asarray(bytearray(base64.b64decode(self.bg_image)), dtype=np.uint8),cv2.IMREAD_UNCHANGED)
        
        # TODO： 图片裁剪
        w,h= crop_size
        if w > -1 and h > -1 :
            image = super().crop_image(image,0,0,w,h)
        
        # TODO： 图片缩放/扩大
        if resize != 0:
            image =  super().resized_image(image,resize)
        
        # 记录每一次的点击坐标
        position_list = []
        
        def lbuttondown(x,y,image):
            # 收集鼠标点击后的坐标
            t = int(time.time()*1000)
            print((x,y,t))
            
            position_list.append((x,y,t))
            # 圆的半径
            r = 15
            
            # 控制点击坐标点为9个
            if (len(position_list) > 9 ):
                return
            
            if len(position_list) > 1:
                start_clear = False
                for p in position_list:
                    # 判断是否在另一个坐标的范围内
                    if not start_clear:
                        start_clear = r*r >= (math.pow(x-p[0],2) + math.pow(y-p[1],2))
                        continue
                    if start_clear:
                        position_list.remove(p) 
            
            # 在图像上绘制圆,图片、中心点、半径，颜色，圆轮廓粗细、线类型
            cv2.circle(image, (x, y), r, (0, 255, 0),2,-1)
            
            # 在图像上添加坐标文本，将数字画到边框中间位置。根据测试，x-10 y+10即可
            # （图像，文本内容，坐标点，字体类型，字体大小，颜色，字体粗细）
            cv2.putText(image, f'{len(position_list)}', (x-10, y+10),cv2.FONT_HERSHEY_SIMPLEX, 1, (240,255,255), 2)
            
            # 获取指定像素点的颜色
            # pixel_color = image[x, y]
            
            # 时间设置为1，表示只保留1秒钟，既不会影响该有的功能也不会有 while True 的性能影响。关键只需要关闭一次。
            cv2.imshow(win_name,image)
            
            cv2.waitKey(1)
        
        # 回调函数：鼠标点击输出点击的坐标
        # （事件（鼠标移动、左键、右键），横坐标，纵坐标，组合键，setMouseCallback的userdata用于传参
        def mouse_callback(event, x, y, flags, image):
            # 如果鼠标左键点击，则输出横坐标和纵坐标
            if event == cv2.EVENT_LBUTTONDOWN:
                lbuttondown(x,y,image)
                
        
        def zh_ch(s):
            return s.encode("gbk").decode('utf-8',errors='ignore')

        win_name = u'请依次点击[蕴、历、玉、社]'

        # 创建窗口
        cv2.namedWindow(win_name,cv2.WINDOW_AUTOSIZE)
        cv2.moveWindow(win_name, 434,205)


        # 将回调函数绑定到窗口
        cv2.setMouseCallback(win_name, mouse_callback,image)

        # 显示图像 原来的方案
        # while True:
        #     cv2.imshow(win_name, image)
        #     k = cv2.waitKey(1) & 0xFF
        #     # 按esc键退出
        #     if k == 27:
        #         break
        
        # 最优方案
        # 记录当前的图像
        cv2.imshow(win_name, image)
        k = cv2.waitKey(0) & 0xFF
        # 按esc键退出
        if k == 27:
            cv2.destroyAllWindows()
            return position_list
        
    '''
        @description: 字符识别，提取图片中的所有字符串
        @params: 
        @author: MR.阿辉
        @datetime: 2024-01-10 19:00:41
        @return: 
    '''
    def simple_identify(self):
        response = super().base64_to_bytes(self.bg_image)
        ocr = ddddocr.DdddOcr(show_ad=False)
        return ocr.classification(response)
    '''
        @description: 基于 ddddocr 实现滑块验证，识别缺口坐标，需要两张图，带缺口的背景图以及滑块图
        @params: 
        @author: MR.阿辉
        @datetime: 2024-01-15 23:09:26
        @return: {'target_y': 0, 'target': [169, 14, 229, 74]}
    '''
    def simple_slide(self):
        det = ddddocr.DdddOcr(det=False,ocr=False,show_ad=False)
        return det.slide_match(
            super().base64_to_bytes(self.slider_image),
            super().base64_to_bytes(self.bg_image),
            simple_target=True)

    def get_distance(self):
        # 滑块图
        bg_img = cv2.imdecode(np.asarray(bytearray(base64.b64decode(self.bg_image)), dtype=np.uint8), 0)
        # 背景图
        slider_img = cv2.imdecode(np.asarray(bytearray(base64.b64decode(self.slider_image)), dtype=np.uint8), 0)
        
        # 3. 使用matchTemplate方法进行模板匹配，返回背景图中与滑块的位置匹配值数组
        result = cv2.matchTemplate(slider_img, bg_img, cv2.TM_CCORR_NORMED)
        # 4. 使用numpy中的unravel_index函数获取result中位置匹配值最大的索引位置，既是滑动的距离
        _, distance = np.unravel_index(result.argmax(), result.shape)
        return distance


    '''
        @description: 图片预览
        @params: 
        @author: MR.阿辉
        @datetime: 2024-01-19 15:14:34
        @return: 
    '''
    def preview(self,b64:str):
        img_bytes = super().base64_to_bytes(b64)
        # 创建BytesIO对象，并从Bytes对象中加载图像数据
        image = Image.open(BytesIO(img_bytes))
        # 展示图像
        image.show()
    
if __name__ == "__main__" :
    
    # ================ 极验点选 ================
    # verisy = Verisy(
    #     bg_image='https://static.geetest.com/captcha_v3/batch/v3/59315/2024-01-20T10/word/ce000b4f13114ef98be263827c2c06f9.jpg?challenge=5ee09e2a982c10b1cda6ae2551f0b508'
    # )
    
    # result = verisy.simple_click(crop_size=(333.375,384))
    # for e in result:
    #     x,y,t = e
    #     # 结果值 1008/306
    #     # 1021/905 434/152
    #     print(x+905,y+152,t)
    
    # # '4681_855,1172_4455,7291_5685'
    # ================ 数美 滑块 ================
    # verisy = Verisy(
    #     bg_image='https://castatic.fengkongcloud.cn/crb/set-000006/v2/0133892a8965e33f3ba85b17f45b6268_bg.jpg',
    #     slider_image='https://castatic.fengkongcloud.cn/crb/set-000006/v2/0133892a8965e33f3ba85b17f45b6268_fg.png'
    # )
    # result = verisy.simple_slide_recognition(resize=-2)
    # print(result)
    
    # ================ 数美 点选 ================
    #verisy = Verisy(bg_image='https://castatic.fengkongcloud.cn/crb/select-set-000008-1.0.1-r1/v2/7807cbd17f5b17d9b61206fbd23a428c.jpg')
    
    # result =verisy.simple_click(crop_size=(600,300),resize=-2)
    # for r in result:
    #     x,y = r
    #     mouse_event = {
    #         'clientX': x+972,
    #         'clientY': y+609,
    #         'offsetX':x,
    #         'offsetY':y,
    #         'x': x+972,
    #         'y': y+609,
    #         'offsetX':x,
    #         'offsetY':y+1,
    #         'pageX': x + 972,
    #         'pageY': y + 666,
    #         'screenX': x + 2412,
    #         'screenY': y + 730
    #     }
    #     print(mouse_event)
    
    # 海南免税
    # verisy = Verisy(bg_image='/Users/zhangzhonghui/Documents/project/python/spider/common/source/code/hnms-bg.jpg',
    #     slider_image='/Users/zhangzhonghui/Documents/project/python/spider/common/source/code/hnms-slider.jpg')
    
    # v = verisy.simple_slide()
    # print(v)
    
    # verisy =Verisy(
    #     bg_image='https://castatic.fengkongcloud.cn/crb/spatial_select/spatial_select-1.0.0-set-000001/v1/6328673feda18302e7c2467604a88a05.jpg',
    # )
    
    # # v =verisy.simple_slide()
    # # print(v)
    # verisy.simple_click(resize=-2)
    
    verisy = Verisy(
        bg_image='/Users/zhangzhonghui/Documents/project/python/spider/common/source/code/dx.jpg'
    )
    for ret in verisy.simple_click():
        print(ret)