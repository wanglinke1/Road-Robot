"""
提供串口初始化与通信以及控制小车运动功能的模块

主要功能包括:
- 串口初始化与通信
- 控制小车运动模式
"""


import time
import serial
import serial.tools.list_ports
from Coordinate import Coordinate

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
        # 数据包格式：         包头、模式、 高八、低八、 旋转角、空、  空、  空、   空、   空、 包尾
        # x坐标移动            0xFF 0x01 x_high x_low  0x00  0x00  0x00  0x00  0x00  0x00  0xFE
        # y坐标移动            0xFF 0x02 y_high y_low  0x00  0x00  0x00  0x00  0x00  0x00  0xFE
        # 旋转运动             0xFF 0x03   0x00  0x00 angle  0x00  0x00  0x00  0x00  0x00  0xFE
        # 给定坐标运动         0xFF  0x04  pre_x pre_x pre_y pre_y tar_x tar_x tar_y tar_y 0xFE
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

    def wait_for_start_cmd(self) -> None:
        """
        等待下位机的开启指令，指令设置为[0xFF, 0x10, 0xFE]

        Returns:
            None: 函数结束代表受到了指令
        """
        while True:
            head = ord(self._serial.read(1))
            if head == 0xFF:
                data = ord(self._serial.read(1))
                if data == 0x10:
                    self._serial.read(1)
                    self._serial.reset_input_buffer()
                    my_logger.info(f"接收到了下位机的启动消息！")
                    break

    def __send_serial_msg(self, mode: MoveMode, distance: float = None, rotation_angle: int = None, pre_x: int = None, pre_y: int = None, tar_x: int = None, tar_y: int = None) -> None:
        """
        发送串口指令给下位机，在被调用时会先对输入的数据进行检查；发送完指令后调用self.__wait_for_action_done()等待下位机反馈

        Args:
            mode (MoveMode): 运动模式，详情见Config.py
            distance (float): 运动距离，单位为cm
            rotation_angle (int): 旋转角度，单位为度
        Returns:
            None: 函数结束代表发送成功并且收到了下位机的执行结束消息
        """
        buffer = []
        log_msg = f''

        # 对输入数据进行检查
        if mode in [MoveMode.X_move, MoveMode.Y_move]:
            if distance is None:
                raise ValueError
            if -327.68 <= distance <= 327.67:
                pass
            else:
                my_logger.warning(f"距离设置范围过大，目前支持[-327.68, 327.67] m。截取距离的低十六位")

        elif mode in [MoveMode.rotate]:
            if rotation_angle is None:
                raise ValueError

        elif mode in [MoveMode.coordinate]:
            if pre_x is None:
                raise ValueError

        else:
            my_logger.error(f"无法识别的Move模式：{mode}")

        # 进行数据处理
        if mode in [MoveMode.X_move, MoveMode.Y_move]:

            dis_cm = int(distance * 100)
            high_byte: int = (dis_cm & 0xFF00) >> 8
            low_byte = dis_cm & 0x00FF

            buffer = [0xFF, mode.value, high_byte, low_byte, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFE]

            log_msg = f'动作模式为{mode.name}，使用米作为单位，原始移动距离为{distance}m。'

        elif mode in [MoveMode.rotate]:
            rotation_angle_ = int(rotation_angle & 0xFF)
            buffer = [0xFF, mode.value, 0x00, 0x00, rotation_angle_, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFE]
            log_msg = f'动作模式为旋转，使用度作为单位，原始输入为{rotation_angle_}度'

        elif mode in [MoveMode.coordinate]:
            pre_x_ = int(pre_x & 0xFFFF)
            pre_y_ = int(pre_y & 0xFFFF)
            tar_x_ = int(tar_x & 0xFFFF)
            tar_y_ = int(tar_y & 0xFFFF)

            buffer = [0xFF, mode.value,
                      (pre_x_ & 0xFF00) >> 8, pre_x_ & 0x00FF,
                      (pre_y_ & 0xFF00) >> 8, pre_y_ & 0x00FF,
                      (tar_x_ & 0xFF00) >> 8, tar_x_ & 0x00FF,
                      (tar_y_ & 0xFF00) >> 8, tar_y_ & 0x00FF,
                      0xFE]

            log_msg = f'动作模式为坐标移动，原始输入坐标为({pre_x}, {pre_y})到({tar_x}, {tar_y})'

        else:
            raise ValueError(f'无法识别的模式{mode}')

        if mode:
            send_num = self._serial.write(bytes(buffer))
            my_logger.debug(f"向下位机发送了{send_num}个字节的数据，数据内容为{buffer}。" + log_msg)
            self.__wait_for_action_done()
            my_logger.info(f"接收到串口消息，下位机动作执行完毕")

    def move_X(self, distance: float) -> None:
        """
        控制小车前后方向上的移动

        Args:
            distance: 移动距离，单位为米，范围为[-327, 327]m
        Returns:
            None: 延时程序，函数返回时代表动作完成
        """
        self.__send_serial_msg(mode=MoveMode.X_move, distance=distance)
        if distance >= 0:
            my_logger.info(f"向前{distance}m")
        else:
            my_logger.info(f"后退{distance}m")
        

    def move_Y(self, distance: float) -> None:
        """
        控制小车左右方向上的移动

        Args:
            distance: 移动距离，单位为米，范围为[-327, 327]m
        Returns:
            None: 延时程序，函数返回时代表动作完成
        """
        self.__send_serial_msg(mode=MoveMode.Y_move, distance=distance)
        if distance >= 0:
            my_logger.info(f"向左{distance}m")
        else:
            my_logger.info(f"向右{distance}m")

    def rotate(self, angle: int) -> None:
        """
        控制小车底盘旋转

        Args:
            angle (int): 角度值，单位为度，范围为[-360, 360]，逆时针方向为正
        Returns:
            None: 延时程序，函数返回时代表动作完成
        """
        self.__send_serial_msg(mode=MoveMode.rotate, rotation_angle=angle)
        if angle >= 0:
            my_logger.info(f"向左转{angle}°")
        else:
            my_logger.info(f"向右转 {angle}°")

    def coordinate(self, pre_x, pre_y, tar_x, tar_y) -> None:
        """
        控制到指定坐标点

        pre_x:
            当前小车x坐标,单位为mm
        pre_y:
            当前小车y坐标,单位为mm
        tar_x:
            目标小车x坐标,单位为mm
        tar_y:
            目标小车y坐标,单位为mm
        """
        self.__send_serial_msg(mode=MoveMode.coordinate, pre_x=pre_x, pre_y=pre_y, tar_x=tar_x, tar_y=tar_y)
        my_logger.info(f"当前x坐标为:{pre_x}mm")
        my_logger.info(f"当前y坐标为:{pre_y}mm")
        my_logger.info(f"目标x坐标为:{tar_x}mm")
        my_logger.info(f"目标y坐标为:{tar_y}mm")

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
        choose = input('请选择模式(M[move]/E[exit]): ').strip().lower()
        if choose == 'm':
            while True:
                choose = input('请选择模式(X[x_move]/Y[y_move]/R[rotate]/C[coordinate]/E[exit]): ').strip().lower()
                if choose == 'x':
                    try:
                        distance = float(input('请输入距离(m): '))
                        control.move_X(distance=distance)
                    except ValueError:
                        print("请输入有效的数字")
                elif choose == 'y':
                    try:
                        distance = float(input('请输入距离(m): '))
                        control.move_Y(distance=distance)
                    except ValueError:
                        print("请输入有效的数字")
                elif choose == 'r':
                    try:
                        angle = int(input('请输入角度°: '))
                        control.rotate(angle=angle)
                    except ValueError:
                        print("请输入有效的整数")
                elif choose == 'c':
                    available_ports = list_available_ports()
                    if not available_ports:
                        print("没有可用的串口设备，程序退出。")
                        exit(1)

                    # 提示用户选择一个具体的串口
                    print("请选择一个UWB串口：")
                    for idx, port_info in enumerate(available_ports, start=1):
                        print(f"{idx}. 端口: {port_info['port']}, 描述: {port_info['description']}")

                    try:
                        choice = int(input("请输入对应的序号: "))
                        if 1 <= choice <= len(available_ports):
                            uwb_port = available_ports[choice - 1]['port']
                        else:
                            print("无效的选择，程序退出。")
                            exit(1)
                    except ValueError:
                        print("输入无效，程序退出。")
                        exit(1)

                    uwb_baudrate = 115200

                    try:
                        coordinate = Coordinate(port=uwb_port, baudrate=uwb_baudrate)
                    except RuntimeError as e:
                        my_logger.error(f"串口初始化失败: {e}")
                        exit(1)

                    # 设置基站坐标和目标物体高度
                    coordinate.set_base_stations()
                    coordinate.set_z_target()
                    
                    # 读取串口数据
                    distance = coordinate.read_serial_data()
                    
                    # 检查是否成功读取到数据
                    if distance:
                        print("基站0-2的距离为：")
                        print(f"基站0: {distance[0]} mm")
                        print(f"基站1: {distance[1]} mm")
                        print(f"基站2: {distance[2]} mm")
                        print("正在计算坐标...")
                        coordinates = coordinate.solve_coordinates()
                        print(f"计算得到的坐标为：x={coordinates[0]} mm, y={coordinates[1]} mm")
                        # 清空缓存区
                        pre_x = int(coordinates[0])
                        pre_y = int(coordinates[1])
                        tar_x = int(input('请输入目标x坐标: '))
                        tar_y = int(input('请输入目标y坐标: '))
                        control.coordinate(pre_x=pre_x, pre_y=pre_y, tar_x=tar_x, tar_y=tar_y)
                elif choose == 'e':
                    print('已退出运动选择模式')
                    break
                else:
                    print('请正确选择模式')
        elif choose == 'e':
            print('已退出')
            break
        else:
            print('请正确选择模式')