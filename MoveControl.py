"""
提供串口初始化与通信以及控制小车运动功能的模块

主要功能包括:
- 串口初始化与通信
- 控制小车运动模式
"""


import time
import serial
import serial.tools.list_ports

from Config import my_logger, MoveMode

def list_available_ports():
    """
    搜索并列出当前连接的串口设备

    Returns:
        list: 可用串口的列表，每个元素是一个字典，包含端口号和描述信息
    """
    ports = serial.tools.list_ports.comports()
    available_ports = []

    for port in ports:
        available_ports.append({
            "port": port.device,
            "description": port.description
        })

    if available_ports:
        print("可用的串口设备如下：")
        for idx, port_info in enumerate(available_ports, start=1):
            print(f"{idx}. 端口: {port_info['port']}, 描述: {port_info['description']}")
    else:
        print("未检测到可用的串口设备。")

    return available_ports

class MoveControl:
    """
    用于串口通信及小车运动控制的类

    这个类提供了串口初始化，控制小车运动及控制舵机模式等功能

    方法:
        __init__: 进行串口初始化
        __wait_for_action_done: 等待下位机完成动作
        wait_for_start_cmd: 等待下位机发送启动指令
        __send_serial_msg: 向下位机发送各模式指令

        move_X: 控制小车前后运动
        move_Y: 控制小车左右运动

        rotate: 控制小车旋转

        clear_buffer: 清空缓存区
    """

    def __init__(self, port: str, baudrate: int) -> None:
        """
        串口初始化

        Args:
            port(str): 设备端口号
            baudrate(int): 波特率

        Returns:
            None
        """
        my_logger.info(f'正在初始化串口')
        try:
            self._serial = serial.Serial(port, baudrate)
        except serial.SerialException as e:
            my_logger.error(e)

        if self._serial.is_open:
            my_logger.info("串口成功初始化")
        else:
            raise RuntimeError("串口未能成功初始化")

        self.buffer_format = [0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFE]
        # 数据包格式：         包头、模式、 高八、低八、 高八、 低八、 高八、低八、高八、 低八、 包尾
        # SPEED移动          0xFF 0x01 1_high 1_low 2_high 2_low 3_high 3_low 4_high 4_low 0xFE
    def __wait_for_action_done(self) -> None:
        """
        上位机向下位机发送动作指令后，下位机应该在动作执行结束后向上位机反馈动作结束的命令
        此方法用于等待下位机的结束指令[0xFF, 0x01, 0xFE]

        Returns:
            None
        """
        while True:
            head = ord(self._serial.read(1))
            if head == 0xFF:
                data = ord(self._serial.read(1))
                if data == 0x01:
                    self._serial.read(1)
                    self._serial.reset_input_buffer()
                    break
    
    def __send_serial_msg(self, mode: MoveMode, moter_1: int = None, moter_2: int = None, moter_3: int = None, moter_4: int = None) -> None:
        """
        发送串口指令给下位机，在被调用时会先对输入的数据进行检查

        Args:
            mode (MoveMode): 运动模式，详情见Config.py
            moter_1, moter_2, moter_3, moter_4: 电机速度，范围[-32768, 32767]
        Returns:
            None: 函数结束代表发送成功
        """
        buffer = []
        log_msg = f''

        # 对输入数据进行检查
        if mode == MoveMode.SPEED:
            # 检查电机参数
            for idx, moter in enumerate([moter_1, moter_2, moter_3, moter_4], start=1):
                if moter is None:
                    raise ValueError(f"电机{idx}速度未指定")
                if not (-32768 <= moter <= 32767):
                    my_logger.warning(f"电机{idx}速度{moter}超出范围[-32768, 32767]，将截取低16位")

            moter_1 = int(moter_1 & 0xFFFF)
            moter_2 = int(moter_2 & 0xFFFF)
            moter_3 = int(moter_3 & 0xFFFF)
            moter_4 = int(moter_4 & 0xFFFF)

            buffer = [0xFF, mode.value,
                      (moter_1 & 0xFF00) >> 8, moter_1 & 0x00FF,
                      (moter_2 & 0xFF00) >> 8, moter_2 & 0x00FF,
                      (moter_3 & 0xFF00) >> 8, moter_3 & 0x00FF,
                      (moter_4 & 0xFF00) >> 8, moter_4 & 0x00FF,
                      0xFE]
            log_msg = f'动作模式为{mode.name}，电机速度分别为: {moter_1}, {moter_2}, {moter_3}, {moter_4}'
        else:
            my_logger.error(f"无法识别的Move模式：{mode}")
            raise ValueError(f'无法识别的模式{mode}')

        send_num = self._serial.write(bytes(buffer))
        my_logger.info(f"向下位机发送了{send_num}个字节的数据，数据内容为{buffer}。" + log_msg)


    def SPEED(self, moter_1: int, moter_2: int, moter_3: int, moter_4: int) -> None:
        """
        控制小车的速度

        Args:
            moter_1: 电机1的速度，范围[-32768, 32767]
            moter_2: 电机2的速度，范围[-32768, 32767]
            moter_3: 电机3的速度，范围[-32768, 32767]
            moter_4: 电机4的速度，范围[-32768, 32767]
        """
        self.__send_serial_msg(mode=MoveMode.SPEED, moter_1=moter_1, moter_2=moter_2, moter_3=moter_3, moter_4=moter_4)

    def clear_buffer(self) -> None:
        """
        清空缓存区

        Returns:
            None
        """
        self._serial.reset_input_buffer()
        self._serial.reset_output_buffer()

if __name__ == '__main__':
    available_ports = list_available_ports()
    if not available_ports:
        print("没有可用的串口设备，程序退出。")
        exit(1)

    # 提示用户选择一个具体的串口
    print("请选择单片机的串口：")
    for idx, port_info in enumerate(available_ports, start=1):
        print(f"{idx}. 端口: {port_info['port']}, 描述: {port_info['description']}")

    try:
        choice = int(input("请输入对应的序号: "))
        if 1 <= choice <= len(available_ports):
            stm_port = available_ports[choice - 1]['port']
        else:
            print("无效的选择，程序退出。")
            exit(1)
    except ValueError:
        print("输入无效，程序退出。")
        exit(1)

    stm_baudrate = 115200

    try:
        control = MoveControl(port=stm_port, baudrate=stm_baudrate)
    except RuntimeError as e:
        my_logger.error(f"串口初始化失败: {e}")
        exit(1)

    while True:
        try:
            moter_1 = int(input("请输入电机1的速度 (-32768 ~ 32767): "))
            moter_2 = int(input("请输入电机2的速度 (-32768 ~ 32767): "))
            moter_3 = int(input("请输入电机3的速度 (-32768 ~ 32767): "))
            moter_4 = int(input("请输入电机4的速度 (-32768 ~ 32767): "))
            control.SPEED(moter_1, moter_2, moter_3, moter_4)
        except ValueError as e:
            my_logger.error(f"输入错误: {e}")
        except Exception as e:
            my_logger.error(f"发生错误: {e}")