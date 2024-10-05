from enum import Enum
from openpyxl.styles import Alignment

'''
    @description: TODO：CELL 数据类型 枚举定义
    @params: 
    @author: MR.阿辉
    @datetime: 2024-10-05 06:42:37
    @return: 
'''
class CellDataType(Enum):
    TEXT = 1 # 字符串
    PIC = 2 # 图片
    NUMBER = 3 # 数值
    DATETIME = 4 # 日期

'''
    @description: 对齐方式
        水平对齐方式常见的有
            两端对齐（justify）、
            填满对齐（fill）、
            左对齐（left）、
            一般对齐（general）、
            右对齐（right）、
            居中对齐（center）、
            分散对齐（distributed）
        垂直对齐常见的有
            靠下对齐（bottom），
            居中对齐（center），
            分散对齐（distributed），
            靠上对齐（top），
            两端对齐（justify）
    @params: 
    @author: MR.阿辉
    @datetime: 2024-09-20 09:14:54
    @return: 
'''
class CellPositionType(Enum):
    # 创建一个居中对齐的对象
    # horizontal='center' 水平居中
    # vertical='center' 垂直居中、vertical='center' 垂直居中、 
    # wrap_text=True 自动换行
    # indent 缩进
    
    # 水平、垂直居中，自动换行
    POSITION_CENTER = Alignment(horizontal='center', vertical='center',wrap_text=True)
    # 左对齐
    POSITION_LEFT = Alignment(horizontal='left', vertical='center',wrap_text=True,indent=1)
    # 右对齐
    POSITION_RIGHT = Alignment(horizontal='right', vertical='center',wrap_text=True)
    # 垂直居中、水平分散对齐
    POSITION_DISTRIBUTED = Alignment(horizontal='distributed', vertical='center',wrap_text=True,indent=1)