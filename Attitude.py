"""
提供串口初始化与通信、解算GPS、解算IMU模块的功能

主要功能包括:
- 串口初始化与通信
- 解算GPS模块数据（经纬度）
- 解算IMU模块数据（航向角）
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

class Attitude:
    """"
    用于解算无人车姿态的类
    用到的传感器为维特智能WTGAHRS1
    该类提供了串口初始化，解算姿态数据等功能
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
    
    def read_GPS(self):
        """
        读取GPS数据（经纬度）

        Returns:
            tuple: (经度, 纬度)，单位为度（float）
        """
        while True:
            # 查找包头
            head1 = self._serial.read(1)
            if head1 == b'\x55':
                head2 = self._serial.read(1)
                if head2 == b'\x57':
                    # 读取8字节数据（经度4字节+纬度4字节）
                    data = self._serial.read(8)
                    if len(data) != 8:
                        continue
                    lon_bytes = data[0:4]
                    lat_bytes = data[4:8]
                    # 读取校验和
                    sum_byte = self._serial.read(1)
                    # 校验和计算
                    sum_calc = 0x55 + 0x57 + sum(lon_bytes) + sum(lat_bytes)
                    if (sum_calc & 0xFF) != sum_byte[0]:
                        my_logger.warning("GPS数据校验和错误，丢弃该帧")
                        continue
                    # 解析经度和纬度（4字节，低字节在前，补码，单位1e-7度）
                    lon = int.from_bytes(lon_bytes, byteorder='little', signed=True)
                    lat = int.from_bytes(lat_bytes, byteorder='little', signed=True)
                    # 转换为NMEA0183格式的ddmm.mmmmmm（协议说明）
                    lon_deg = lon // 10000000
                    lon_min = (lon % 10000000) / 100000
                    lon_val = abs(lon_deg) + lon_min / 60.0

                    lat_deg = lat // 10000000
                    lat_min = (lat % 10000000) / 100000
                    lat_val = abs(lat_deg) + lat_min / 60.0

                    return lon_val, lat_val # 返回经度和纬度，单位为度（float），正负表示东西南北
    
    def read_IMU(self):
        """
        读取IMU数据（航向角Yaw，单位：度）

        Returns:
            float: 航向角（Yaw，单位：度）
        """
        while True:
            head1 = self._serial.read(1)
            if head1 == b'\x55':
                head2 = self._serial.read(1)
                if head2 == b'\x53':
                    data = self._serial.read(8)  # RollL, RollH, PitchL, PitchH, YawL, YawH, VL, VH
                    if len(data) != 8:
                        continue
                    sum_byte = self._serial.read(1)
                    # 校验和计算
                    sum_calc = 0x55 + 0x53 + sum(data)
                    if (sum_calc & 0xFF) != sum_byte[0]:
                        my_logger.warning("IMU数据校验和错误，丢弃该帧")
                        continue
                    # 提取Yaw
                    yaw_bytes = bytes([data[4], data[5]])
                    yaw_raw = int.from_bytes(yaw_bytes, byteorder='little', signed=True)
                    # 转换为角度
                    yaw = yaw_raw / 32768 * 180
                    return yaw  # 返回航向角（Yaw，单位：度），范围[-180, 180] 0°代表正北
                
if __name__ == '__main__':
    available_ports = list_available_ports()
    if not available_ports:
        print("没有可用的串口设备，程序退出。")
        exit(1)

    # 提示用户选择一个具体的串口
    print("请选择姿态传感器的串口：")
    for idx, port_info in enumerate(available_ports, start=1):
        print(f"{idx}. 端口: {port_info['port']}, 描述: {port_info['description']}")

    try:
        choice = int(input("请输入对应的序号: "))
        if 1 <= choice <= len(available_ports):
            sensor_port = available_ports[choice - 1]['port']
        else:
            print("无效的选择，程序退出。")
            exit(1)
    except ValueError:
        print("输入无效，程序退出。")
        exit(1)

    sensor_baudrate = 115200

    try:
        attitude = Attitude(port=sensor_port, baudrate=sensor_baudrate)
    except RuntimeError as e:
        my_logger.error(f"串口初始化失败: {e}")
        exit(1)

    while True:
        start_time = time.time()

        # 读取GPS数据
        gps_data = attitude.read_GPS()
        if gps_data:
            lon, lat = gps_data
            print(f"经度: {lon}, 纬度: {lat}")

        # 读取IMU数据
        imu_data = attitude.read_IMU()
        if imu_data:
            print(f"航向角: {imu_data}")

        # 控制循环频率为100Hz（即每10ms循环一次）
        elapsed = time.time() - start_time
        sleep_time = max(0, 0.009 - elapsed)
        time.sleep(sleep_time)
