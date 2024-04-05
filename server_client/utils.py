import socket
 
parameters = {
    'host': '127.0.0.1',  # 监听的IP地址
    'port': 65432,  # 监听的端口号
    'orders': {  # 自定义指令
        'ocr': '1',
        'image_understanding': '2',
        'speed_up': '3',
        'speed_down': '4',
        'on_finger_recog': '5',
        'off_finger_recog': '6',
        'end': '7',
        'unknown': '8'
    }
}

def send_msg(socket, msg, logging=False):
    data = msg
    if isinstance(msg, str):
        data = msg.encode()
    socket.sendall(data)
    if logging: print(f'send data: {msg}')

def recv_msg(socket, bufsize=1024, logging=False):
    data = socket.recv(bufsize)
    if not data: return None
    msg = data.decode()
    if logging: print(f'receive data: {msg}')
    return msg