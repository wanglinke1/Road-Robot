from flask import Flask, request, jsonify, send_from_directory
from MoveControl import MoveControl
from Config import MoveMode
import serial.tools.list_ports  # 用于列出串口

# 启动后端后，在浏览器中输入如下网址，即可访问前端页面
# http://127.0.0.1:5000/

app = Flask(__name__)

# 初始化 MoveControl 实例
control = None  # 全局变量，用于存储 MoveControl 实例

# 设置静态文件目录
@app.route('/')
def serve_index():
    return send_from_directory('.', 'Makers.html')

@app.route('/list_ports', methods=['GET'])
def list_ports():
    ports = serial.tools.list_ports.comports()
    print("检测到的串口:", ports)  # 添加调试日志
    available_ports = [{"index": idx + 1, "port": port.device, "description": port.description} for idx, port in enumerate(ports)]
    return jsonify(available_ports)

@app.route('/init', methods=['POST'])
def init_control():
    """
    初始化 MoveControl 实例
    """
    global control
    data = request.json
    port_index = data.get('port_index')  # 前端传递的串口序号
    baudrate = data.get('baudrate', 115200)

    try:
        # 获取所有可用串口
        ports = serial.tools.list_ports.comports()
        if port_index < 1 or port_index > len(ports):
            return jsonify({'error': '无效的串口序号'}), 400

        # 根据序号选择串口
        port = ports[port_index - 1].device
        control = MoveControl(port=port, baudrate=baudrate)
        return jsonify({'message': f'MoveControl 初始化成功，使用端口 {port}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/send', methods=['POST'])
def send_command():
    """
    接收前端发送的命令并执行
    """
    global control
    if control is None:
        return jsonify({'error': 'MoveControl 未初始化'}), 400

    data = request.json
    command = data.get('command')

    try:
        if command == 'forward':
            control.move_X(distance=0.1)
        elif command == 'backward':
            control.move_X(distance=-0.1)
        elif command == 'left':
            control.move_Y( distance=-0.1)
        elif command == 'right':
            control.move_Y(distance=0.1)
        elif command == 'rotate_left':
            control.rotate(angle=-72)
        elif command == 'rotate_right':
            control.rotate(angle=72)
        else:
            return jsonify({'error': '未知命令'}), 400

        return jsonify({'message': f'{command} 执行成功'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)