'''
    @description: 滑块轨迹工具类
    @params: 
    @author: MR.阿辉
    @datetime: 2024-01-15 22:51:02
    @return: 
'''
import math
import random
import numpy as np

'''
    @description: 极验3代滑动轨迹生成
    @params: distance 缺口滑动距离
    @params: grain 粒度，值越高，轨迹粒度越细。
    @author: MR.阿辉
    @datetime: 2024-01-15 22:51:25
    @return: 
'''
def geetest_slidev3(distance,grain:int=30):
    def __ease_out_expo(sep):
        if sep == 1:
            return 1
        else:
            return 1 - pow(2, -10 * sep)

    def get_slide_track(distance):
        """
        根据滑动距离生成滑动轨迹
        :param distance: 需要滑动的距离
        :return: 滑动轨迹<type 'list'>: [[x,y,t], ...]
            x: 已滑动的横向距离
            y: 已滑动的纵向距离, 除起点外, 均为0
            t: 滑动过程消耗的时间, 单位: 毫秒
        """
        if not isinstance(distance, int) or distance < 0:
            raise ValueError(f"distance类型必须是大于等于0的整数: distance: {distance}, type: {type(distance)}")
        # 初始化轨迹列表
        slide_track = [
            [random.randint(-50, -10), random.randint(-50, -10), 0],
            [0, 0, 0],
        ]
        # 共记录count次滑块位置信息
        count = 30 + int(distance / 2)
        # 初始化滑动时间
        t = random.randint(50, 100)
        # 记录上一次滑动的距离
        _x = 0
        _y = 0
        for i in range(count):
            # 已滑动的横向距离
            x = round(__ease_out_expo(i / count) * distance)
            # 滑动过程消耗的时间
            t += random.randint(10, 20)
            if x == _x:
                continue
            slide_track.append([x, _y, t])
            _x = x
        slide_track.append([distance, 0, t])

        return slide_track, t


    return get_slide_track(distance)


'''
    @description: 极验4代滑动轨迹生成
    @params: distance 缺口滑动距离
    @params: grain 粒度，值越高，轨迹粒度越细。
    @author: MR.阿辉
    @datetime: 2024-01-15 22:51:25
    @return: 
'''
def geetest_slidev4(distance,grain:int=30):
    def __ease_out_expo(x):
        if x == 1:
            return 1
        else:
            return 1 - pow(2, -10 * x)

    def __ease_out_quart(x):
        return 1 - pow(1 - x, 4)


    def get_slide_track(distance):
        """
        根据滑动距离生成滑动轨迹
        :param distance: 需要滑动的距离
        :return: 滑动轨迹<type 'list'>: [[x,y,t], ...]
            x: 已滑动的横向距离
            y: 已滑动的纵向距离, 除起点外, 均为0
            t: 滑动过程消耗的时间, 单位: 毫秒
        """
        ttt = 0
        if not isinstance(distance, int) or distance < 0:
            raise ValueError(f"distance类型必须是大于等于0的整数: distance: {distance}, type: {type(distance)}")
        # 初始化轨迹列表
        slide_track = [
            [random.randint(20, 60), random.randint(10, 40), 0]
        ]
        # 共记录count次滑块位置信息
        count = grain + int(distance / 2)
        # 初始化滑动时间
        t = random.randint(50, 100)
        # 记录上一次滑动的距离
        _x = 0
        _y = 0
        for i in range(count):
            # 已滑动的横向距离
            x = round(__ease_out_expo(i / count) * distance)
            # 滑动过程消耗的时间
            t = random.randint(10, 20)
            if x == _x:
                continue
            slide_track.append([x - _x, _y, t])
            _x = x
            ttt += t
        slide_track.append([0, 0, random.randint(200, 300)])
        return slide_track, ttt
    return get_slide_track(distance)


'''
    @description: 数美滑动轨迹生产
    @params: distance 缺口滑动距离
    @author: MR.阿辉
    @datetime: 2024-01-23 15:55:23
    @return: 
'''
def ishumei_slide(distance):
    tracks = []

    y,v,t = 0,0,1
    current = 0
    mid = distance * 3 / 4
    exceed = 20
    z = t

    tracks.append([0, 0, 1])

    while current < (distance + exceed):
        if current < mid / 2:
            a = 15
        elif current < mid:
            a = 20
        else:
            a = -30
        a /= 2
        v0 = v
        s = v0 * t + 0.5 * a * (t * t)
        current += int(s)
        v = v0 + a * t

        y += random.randint(-5, 5)
        z += 100 + random.randint(0, 10)

        tracks.append([min(current, (distance + exceed)), y, z])

    while exceed > 0:
        exceed -= random.randint(0, 5)
        y += random.randint(-5, 5)
        z += 100 + random.randint(0, 10)
        tracks.append([min(current, (distance + exceed)), y, z])

    return tracks

if __name__ == "__main__" :
    
    # 极验4代滑块
    #print(geetest_slidev4(147,100))
    
    # 数美滑块
    print(ishumei_slide(123))
