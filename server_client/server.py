from utils import *

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # 创建socket对象
    s.connect((parameters['host'], parameters['port']))  # 连接到接收端

    while True:
        message = input("请输入指令：")
        if not message:
            break
        
        send_msg(s, message)
        resp = recv_msg(s)
        print(f'reponse: {resp}')
