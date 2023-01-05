import base64
import json

import requests

from config.config import config


class FoFa:
    def __init__(self):
        self.email = config['fofa']['email']
        self.key = config['fofa']['key']
        self.size = config['fofa']['size']
        self.fields = "protocol,ip,port,domain,server,title,icp"

    def search(self, text):
        url = "https://fofa.info/api/v1/search/all"
        base64_text = base64.b64encode(text.encode('utf-8')).decode("utf-8")
        params = {
            "email": self.email,
            "key": self.key,
            "size": self.size,
            "fields": self.fields,
            "qbase64": base64_text
        }
        try:
            rest = requests.get(url=url, params=params)
            rest.json()
            data = json.loads(rest.text)
            if data['error']:
                if data['errmsg'] == "[-700] Account Invalid":
                    raise ValueError("FoFa账号配置错误，请检查账号配置！")
            elif not data:
                raise ValueError("FoFa请求错误，请检查请求参数后再尝试！")
            else:
                total = data['size']
                print("FoFa数据获取成功，发现{}条数据".format(total))
            return data['results']
        except Exception as e:
            print('{}'.format(e))
            return []
