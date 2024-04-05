from pocketsphinx import LiveSpeech

parameters = {
    'model': {
        'en': 'keyword_recognition/model/en-us/en-us',
        'zh': 'keyword_recognition/model/zh-cn/zh-cn'
    },
    'keyword_en': {
        'lm': 'keyword_recognition/keyword_en/7980.lm',
        'dic': 'keyword_recognition/keyword_en/7980.dic'
    },
    'keyword_zh': {
        'keywords': {
            '文字识别': 'ocr', 
            '图片理解': 'image_understanding',
            '开启手势识别': 'on_finger_recog',
            '关闭手势识别': 'off_finger_recog',
            '语速加快': 'speed_up',
            '语速减慢': 'speed_down'
        },
        'lm': 'keyword_recognition\\keyword_zh/3746.lm',
        'dic': 'keyword_recognition\\keyword_zh/3746.dic'
    },
}
