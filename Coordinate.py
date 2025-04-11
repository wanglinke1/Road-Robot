import numpy as np
import serial
import serial.tools.list_ports
import time

from Config import my_logger

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

class Coordinate:
    """
    用于串口通信及小车坐标结算的类

    这个类提供了串口初始化，解算小车坐标的功能
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

        # 初始化坐标相关变量
        self.base_stations = []  # 基站坐标
        self.z_target = 0        # 目标物体高度
        self.distances = []      # 目标物体到基站的距离
        self.buffer_format = [  0x43, 0x6d, 0x64, 0x4d, 0x3a, 0x34, # 包头
                                0x5b, # 长度
                                0x00, 0x00, 0x00, 0x00, # 标签测距时间
                                0x00, 0x00, # 标签地址
                                0x00, 0x00, # 基站地址
                                0x00, # 标签测距序列号
                                0x00, # 标签测距有效位
                                0x00, 0x00, 0x00, 0x00, # 目标物体到基站0的欧式距离
                                0x00, 0x00, 0x00, 0x00, # 目标物体到基站1的欧式距离
                                0x00, 0x00, 0x00, 0x00, # 目标物体到基站2的欧式距离
                                0x00, 0x00, 0x00, 0x00, # 目标物体到基站3的欧式距离
                                0x00, 0x00, 0x00, 0x00, # 目标物体到基站4的欧式距离
                                0x00, 0x00, 0x00, 0x00, # 目标物体到基站5的欧式距离
                                0x00, 0x00, 0x00, 0x00, # 目标物体到基站6的欧式距离
                                0x00, 0x00, 0x00, 0x00, # 目标物体到基站7的欧式距离
                                0x00, # 卡尔曼滤波是否开启
                                0x00, 0x00, 0x00, 0x00, # 目标物体到基站0的卡尔曼滤波欧式距离
                                0x00, 0x00, 0x00, 0x00, # 目标物体到基站1的卡尔曼滤波欧式距离
                                0x00, 0x00, 0x00, 0x00, # 目标物体到基站2的卡尔曼滤波欧式距离
                                0x00, 0x00, 0x00, 0x00, # 目标物体到基站3的卡尔曼滤波欧式距离
                                0x00, 0x00, 0x00, 0x00, # 目标物体到基站4的卡尔曼滤波欧式距离
                                0x00, 0x00, 0x00, 0x00, # 目标物体到基站5的卡尔曼滤波欧式距离
                                0x00, 0x00, 0x00, 0x00, # 目标物体到基站6的卡尔曼滤波欧式距离
                                0x00, 0x00, 0x00, 0x00, # 目标物体到基站7的卡尔曼滤波欧式距离
                                0x00, # 是否开启硬件定位标志位
                                0x00, # 开启硬件定位，定位维度
                                0x00, # 硬件定位，基站有效位
                                0x00, # 标签定位结果
                                0x00, 0x00, 0x00, 0x00, # 标签定位结果x
                                0x00, 0x00, 0x00, 0x00, # 标签定位结果y
                                0x00, 0x00, 0x00, 0x00, # 标签定位结果z
                                0x00, # 检验位
                                0x0d, 0x0a] # 包尾 # 解析目标物体到基站0-2的欧式距离

    def set_base_stations(self):
        """
        设置三个基站的坐标
        """
        print("请输入三个基站的坐标 (单位：mm)：")
        try:
            self.base_stations = []
            for i in range(3):
                x = float(input(f"请输入基站{i}的x坐标:(单位：mm) "))
                y = float(input(f"请输入基站{i}的y坐标:(单位：mm) "))
                z = float(input(f"请输入基站{i}的z坐标:(单位：mm) "))
                self.base_stations.append((x, y, z))
        except ValueError:
            print("输入无效，程序退出。")
            exit(1)

    def set_z_target(self):
        """
        设置目标物体的高度
        """
        try:
            self.z_target = float(input("请输入目标物体的高度 (z坐标，单位：mm): "))
        except ValueError:
            print("输入无效，程序退出。")
            exit(1)

    def read_serial_data(self):
        """
        从串口读取数据包并解析目标物体到基站0-2的欧式距离

        Returns:
            list: 目标物体到基站0-2的欧式距离(单位:mm)
        """
        try:
            while True:
                # 读取包头
                header = self._serial.read(6)
                if header != b'CmdM:4':  # 检查包头是否正确
                    continue

                # 读取长度字段
                length = self._serial.read(1)
                length = int.from_bytes(length, byteorder='little')

                # 读取数据体
                data = self._serial.read(length)

                # 读取校验位和包尾
                checksum = self._serial.read(1)
                footer = self._serial.read(2)
                if footer != b'\r\n':  # 检查包尾是否正确
                    continue

                # 解析目标物体到基站0-2的欧式距离
                self.distances = [
                    int.from_bytes(data[10:14], byteorder='little'),  # 基站0距离
                    int.from_bytes(data[14:18], byteorder='little'),  # 基站1距离
                    int.from_bytes(data[18:22], byteorder='little')   # 基站2距离
                ]

                return self.distances

        except Exception as e:
            print(f"读取串口数据时发生错误: {e}")
            return None

    def clear_buffer(self) -> None:
        """
        清空缓存区

        Returns:
            None
        """
        self._serial.reset_input_buffer()
        self._serial.reset_output_buffer()

    def solve_coordinates(self):
        """
        解算目标物体的 xy 坐标
        :单位为mm
        :param distances: 目标物体到三个基站的欧式距离，格式为 [d0, d1, d2]
        :return: 目标物体的 (x, y) 坐标
        """
        # 提取基站坐标
        x0, y0, z0 = self.base_stations[0]
        x1, y1, z1 = self.base_stations[1]
        x2, y2, z2 = self.base_stations[2]

        # 提取距离
        d0, d1, d2 = self.distances

        # 构建方程组
        A = np.array([
            [2 * (x1 - x0), 2 * (y1 - y0)],
            [2 * (x2 - x0), 2 * (y2 - y0)]
        ])
        b = np.array([
            d0**2 - d1**2 - x0**2 + x1**2 - y0**2 + y1**2 - (self.z_target - z0)**2 + (self.z_target - z1)**2,
            d0**2 - d2**2 - x0**2 + x2**2 - y0**2 + y2**2 - (self.z_target - z0)**2 + (self.z_target - z2)**2
        ])

        # 解方程组
        xy = np.linalg.solve(A, b)
        return xy[0], xy[1]


if __name__ == '__main__':
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

    while True:
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
            coordinate.clear_buffer()
        else:
            print("未读取到有效数据，等待下一次读取...")
        time.sleep(1)