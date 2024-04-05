import os
import ssl
from .utils import *
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import json
import requests
import _thread as thread
import websocket

class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg

class Url:
    def __init__(this, host, path, schema):
        this.host = host
        this.path = path
        this.schema = schema
        pass

class XFYunApi:
    def __init__(self) -> None:
        self.appid = parameters['appid']
        self.apisecret = parameters['apisecret']
        self.apikey = parameters['apikey']
        self.url = None

    def __parse_url(self, requset_url):
        stidx = requset_url.index("://")
        host = requset_url[stidx + 3:]
        schema = requset_url[:stidx + 3]
        edidx = host.index("/")
        if edidx <= 0:
            raise AssembleHeaderException("invalid request url:" + requset_url)
        path = host[edidx:]
        host = host[:edidx]
        u = Url(host, path, schema)
        return u
    
    def assemble_ws_auth_url(self, method="GET") -> str:  # 鉴权认证
        if self.url is None: raise AssembleHeaderException('url is not initialized')
        u = self.__parse_url(self.url)
        host = u.host
        path = u.path
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
        signature_sha = hmac.new(
            self.apisecret.encode('utf-8'), 
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
        print("signature:", signature_sha)
        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.apikey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        print("authorization:", authorization)
        values = {
            "host": host,
            "date": date,
            "authorization": authorization
        }
        return self.url + "?" + urlencode(values)
  
class OcrModel(XFYunApi):
    def __init__(self) -> None:
        super().__init__()
        self.url = parameters['urls']['ocr']

    def __get_request_data_from_path(self, image_path):
        image_ext = image_path.split('.')[-1]
        # print(f'image encoding: {file_ext}')
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        body = {
            "header": {
                "app_id": self.appid,
                "status": 3
            },
            "parameter": {
                "hh_ocr_recognize_doc": {
                    "recognizeDocumentRes": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json"
                    }
                }
            },
            "payload": {
                "image": {
                    "encoding": image_ext,
                    "image": str(base64.b64encode(image_bytes), 'utf-8'),
                    "status": 3
                }
            }
        }
        return json.dumps(body)
    
    def send_request(self, image_path):
        """向指定url发送post请求，并获取json格式的text内容"""
        if not os.path.exists(image_path): raise AssembleHeaderException('image file not exist!')
        request_url = self.assemble_ws_auth_url('POST')
        request_data = self.__get_request_data_from_path(image_path)
        headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'appid': 'APPID'}
        response = requests.post(request_url, data=request_data, headers=headers)
        res_json = json.loads(response.content.decode())
        text_json = json.loads(base64.b64decode(res_json['payload']['recognizeDocumentRes']['text']).decode())
        return text_json

    def __get_rentangles_from_json(self, text_json):
        recs = []
        for line in text_json['lines']:
            pos = line['position']
            rec = [pos[0], pos[1], pos[4], pos[5]]
            recs.append(rec)
        return recs
    
    def get_result_from_request(self, image_path):
        text_json = self.send_request(image_path)
        whole_text = text_json['whole_text']
        recs = self.__get_rentangles_from_json(text_json)
        return whole_text, recs

class ImageUSModel(XFYunApi):
    def __init__(self) -> None:
        super().__init__()
        self.url = parameters['urls']['image_understading']
        self.finished = None
        self.answer = ''

    def __on_message(self, ws, msg):
        data = json.loads(msg)
        code = data['header']['code']
        if code != 0:
            print(f'error request: {code}, {data}')
            self.ws.close()
        else:
            choices = data["payload"]["choices"]
            status = choices["status"]
            content = choices["text"][0]["content"]
            # print(f'{content}', end="")
            self.answer += content
            if status == 2:
                self.ws.close()
    def __on_error(self, *args): 
        pass
    def __on_close(self, *args): 
        self.finished = True
    def __on_open(self, *args):
        self.finished = False
        data = json.dumps(self.__get_params(self.__checklen(self.dialogue)))
        self.ws.send(data)

    def __get_params(self, text):
        data = {
            "header": {
                "app_id": self.appid
            },
            "parameter": {
                "chat": {
                    "domain": "image",
                    "temperature": 0.5,
                    "top_k": 4,
                    "max_tokens": 2028,
                    "auditing": "default"
                }
            },
            "payload": {
                "message": {
                    "text": text
                }
            }
        }
        return data

    def __getlength(self, text):
        length = 0
        for content in text:
            temp = content["content"]
            leng = len(temp)
            length += leng
        return length
    
    def __checklen(self, text):
        while (self.__getlength(text[1:])> 8000):
            del text[1]
        return text
    
    def init_dialogue_by_image(self, image_path):
        with open(image_path, 'rb') as f:
            image_data = f.read()
        self.dialogue = [
            {
                "role": "user", 
                "content": str(base64.b64encode(image_data), 'utf-8'), 
                "content_type": "image"
             },
             {
                "role": "user",
                "content": "这张图片是什么内容",
                "content_type": "text"
            }
        ]
        self.ws = websocket.WebSocketApp(
            url=self.assemble_ws_auth_url(),
            on_open=self.__on_open,
            on_message=self.__on_message,
            on_error=self.__on_error,
            on_close=self.__on_close
        )
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def get_request_data(self, role, content):
        # TODO: 开发连续对话功能
        jsoncon = {
            'role': role,
            'content': content
        }
        self.dialogue.append(jsoncon)
