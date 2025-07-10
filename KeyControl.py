import time
import serial
import serial.tools.list_ports
import curses
import threading

from MoveControl import MoveControl
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

class KeyControl(MoveControl):
    def __init__(self, stm_port, stm_baudrate):
        super().__init__(port=stm_port, baudrate=stm_baudrate)
        self.speed_step = 1000  # 每次按键速度变化步长
        self.max_speed = 32767
        self.min_speed = -32767
        self.motor_speeds = [0, 0, 0, 0]  # [m1, m2, m3, m4]
        self.lock = threading.Lock()

    def update_speed(self, key_set):
        with self.lock:
            # 基础速度变化
            delta = [0, 0, 0, 0]
            if 'w' in key_set:
                delta = [self.speed_step] * 4
            if 's' in key_set:
                delta = [d - self.speed_step for d in delta]
            if 'a' in key_set:
                delta = [d - self.speed_step if i in [0,2] else d + self.speed_step for i, d in enumerate(delta)]
            if 'd' in key_set:
                delta = [d + self.speed_step if i in [0,2] else d - self.speed_step for i, d in enumerate(delta)]
            if 'q' in key_set:
                self.motor_speeds = [0, 0, 0, 0]
            else:
                # 线性叠加
                self.motor_speeds = [
                    max(self.min_speed, min(self.max_speed, self.motor_speeds[i] + delta[i]))
                    for i in range(4)
                ]
            # 发送速度
            self.SPEED(*self.motor_speeds)
            my_logger.info(f"当前电机速度: {self.motor_speeds}")

    def key_control_loop(self):
        import curses
        stdscr = curses.initscr()
        curses.cbreak()
        stdscr.keypad(True)
        stdscr.nodelay(True)
        try:
            key_set = set()
            while True:
                c = stdscr.getch()
                if c != -1:
                    key = chr(c).lower()
                    if key in ['w', 'a', 's', 'd', 'q']:
                        key_set.add(key)
                        self.update_speed(key_set)
                        if key == 'q':
                            key_set.clear()
                    elif c == 27:  # ESC退出
                        break
                else:
                    # 松开按键时清空key_set
                    key_set.clear()
                time.sleep(0.05)
        finally:
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()

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
        keycontrol = KeyControl(port=stm_port, baudrate=stm_baudrate)
    except RuntimeError as e:
        my_logger.error(f"串口初始化失败: {e}")
        exit(1)

    keycontrol.key_control_loop()