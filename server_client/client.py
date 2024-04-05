from utils import *

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((parameters['host'], parameters['port']))  # 绑定主机和端口
    s.listen()  # 开始监听
    conn, addr = s.accept()  # 接受连接
    with conn:
        print('连接来自：', addr)
        while True:
            # 接收数据
            msg = recv_msg(conn, logging=True)
            if msg is None:
                break

            if msg == 'order1':
                send_msg(conn, 'finished', logging=True)
                
                # 这里可以写执行操作1的代码

            elif msg == 'order2':
                send_msg(conn, 'finished', logging=True)

                # 这里可以写执行操作2的代码

            else:
                send_msg(conn, 'unkown order', logging=True)

