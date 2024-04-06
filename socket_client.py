from server_client.utils import parameters as sk_params, send_msg, recv_msg, socket
from camera.utils import parameters as cam_params
from camera.camera import Camera
from sound_player.sound_player import *
from xfyun_api.utils import parameters as xf_params, plot_image_with_rectangles
from xfyun_api.xfyun_model import OcrModel, ImageUSModel
import cv2
import threading


camera = Camera(1)
soundPlayer = SoundPlayer()
ocrModel = OcrModel()
imageUSModel = ImageUSModel()
VIDEO_WIN = 'Video'
RES_WIN = 'Result'
WIN_FLAG = 0
res_frame = None
message = None

def msg_receiver(socket, func):
    global message
    message = None
    message = recv_msg(socket, logging=True)
    func()
    send_msg(socket, sk_params['orders']['end'], logging=True)

def async_run_msg_receiver(socket):
    def func_after_recv_msg():
        global res_frame
        orders = sk_params['orders']
        if message == orders['ocr']:
            image_path = camera.save_frame_to_local()
            whole_text, recs = ocrModel.get_result_from_request(image_path)
            print(f'ocr result: {whole_text}')
            res_frame = cv2.imread(image_path)
            res_frame = plot_image_with_rectangles(res_frame, recs)
            whole_text = whole_text.replace('\n', ' ')
            soundPlayer.play_sound(f'识别结果是：{whole_text}' if whole_text != '' else '未识别到文字。')

        elif message == orders['image_understanding']:
            image_path = camera.save_frame_to_local()
            imageUSModel.init_dialogue_by_image(image_path)
            res_frame = cv2.imread(image_path)
            print(f'image_understanding result: {imageUSModel.answer}')
            soundPlayer.play_sound(imageUSModel.answer, False)

        elif message == orders['speed_up']:
            soundPlayer.speed_up()

        elif message == orders['speed_down']:
            soundPlayer.speed_down()

        elif message == orders['on_finger_recog']:
            camera.switch_finger_recog(True)

        elif message == orders['off_finger_recog']:
            camera.switch_finger_recog(False)
            
    t = threading.Thread(target=msg_receiver, args=[socket, func_after_recv_msg])
    t.start()
    return t

def socket_client():
    global message
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((sk_params['host'], sk_params['port']))
        s.listen()
        conn, addr = s.accept()
        cv2.namedWindow(VIDEO_WIN, WIN_FLAG)
        cv2.namedWindow(RES_WIN, WIN_FLAG)
        msg_receiver_thread = None
        with conn:
            print('connecting with: ', addr)
            while camera.is_opened():
                ret, frame = camera.read_frame()
                if not ret: raise Exception('Camera open failed!')

                if msg_receiver_thread is None or \
                        message is not None and not msg_receiver_thread.is_alive():
                    msg_receiver_thread = async_run_msg_receiver(conn)

                if camera.is_on_finger_recog:
                    frame = camera.read_drawn_frame()

                cv2.imshow(VIDEO_WIN, frame)
                if res_frame is not None:
                    cv2.imshow(RES_WIN, res_frame)
            
                if cv2.waitKey(10) & 0xFF == 27:  # Esc to quit
                    break

    print('Socket client closed.')
    camera.release_cap()
    cv2.destroyAllWindows()


if __name__ =='__main__':
    socket_client()