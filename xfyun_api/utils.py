import cv2


parameters = {
    'appid': '81ad0733',
    'apisecret': 'NWY2NjU0ZTM1NzY1ZWNkMzk4NmYyNjkx',
    'apikey': '575a56c98e20a0c70c3b6f310fdac451',
    'urls': {
        'ocr': 'http://api.xf-yun.com/v1/private/hh_ocr_recognize_doc',
        'image_understading': 'wss://spark-api.cn-huabei-1.xf-yun.com/v2.1/image',
    },
}

def plot_image_with_rectangles(img, 
                                recs: list, 
                                rec_color=(0, 255, 0)):
    ploted_img = img.copy()
    for rec in recs:
        ploted_img = cv2.rectangle(ploted_img, (rec[0], rec[1]), (rec[2], rec[3]), rec_color, 1)
    return ploted_img
