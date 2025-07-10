"""
提供封装信息与配置的模块

该模块定义了控制小车运动模式、颜色信息以及其他相关配置的类
"""

import enum
import sys
import os
from loguru import logger

# 配置日志
logger.remove()
logger.add(sys.stdout, level="INFO")
logger.add("log/log.log", level="DEBUG")
my_logger = logger

class MoveMode(enum.IntEnum):
    """
    该类用于封装小车运动及控制模式

    枚举成员:
        - SPEED: 小车以速度模式运动
    """
    SPEED = 1

if __name__ == '__main__':
    print("当前工作目录:", os.getcwd())
    # 测试日志输出
    my_logger.info('logger_test')
    my_logger.error('error_test')
