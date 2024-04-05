from server_client.utils import socket, send_msg, recv_msg,\
                                 parameters as sk_params
from keyword_recognition.utils import LiveSpeech, parameters as kw_params


def socket_server():
    """keyword recognition in the loop, when triggered then send message by socket_server"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:  # 创建socket对象
        server.connect((sk_params['host'], sk_params['port']))  # 连接到接收端

        speech = LiveSpeech(
            verbose=False,
            sampling_rate=16000,
            buffer_size=2048,
            no_search=False,
            full_utt=False,
            hmm=kw_params['model']['zh'],
            lm=kw_params['keyword_zh']['lm'],
            dic=kw_params['keyword_zh']['dic']
        )

        for phrase in speech:
            phrase = str(phrase)
            keywords_m = kw_params['keyword_zh']['keywords']
            if phrase in keywords_m.keys():
                print(f"keyword: {phrase}")
                send_msg(server, sk_params['orders'][keywords_m[phrase]], logging=True)
                resp = recv_msg(server, logging=True)

if __name__ =='__main__':
    socket_server()