import base64
import json
import math
import time

import requests

from config.config import config


class Hunter:
    def __init__(self):
        self.index = 0  # 当前使用的是第几个账号
        self.account = config['hunter']['account']
        self.nums = len(self.account)  # 共有几个账号
        self.username = self.account[0]['username']
        self.key = self.account[0]['key']
        self.page = 1
        self.size = config['hunter']['page_size']
        self.is_web = 0

    def refresh_params(self, search):
        params = {
            "username": self.username,
            "api-key": self.key,
            "page": self.page,
            "page_size": self.size,
            "is_web": self.is_web,
            "search": search
        }
        return params

    def search(self, text, limit):
        url = "https://hunter.qianxin.com/openApi/search"
        base64_text = base64.b64encode(text.encode('utf-8')).decode("utf-8")
        params = self.refresh_params(base64_text)
        try:
            page_nums = 1
            data_list = []
            page_print = False  # 是否位于分页查询部分，用于打印积分输出
            show_totals = True  # 用于第一次查询时显示查询结果总数
            while params['page'] <= page_nums:
                rest = requests.get(url=url, params=params)
                rest.json()
                data = json.loads(rest.text)
                # 积分用完，切换账号继续请求
                while data['code'] == 40204:
                    self.changeAccount()
                    params = self.refresh_params(base64_text)
                    rest = requests.get(url=url, params=params)
                    rest.json()
                    data = json.loads(rest.text)
                # 响应内容提示请求过多
                while data['code'] == 429:
                    time.sleep(1)
                    rest = requests.get(url=url, params=params)
                    rest.json()
                    data = json.loads(rest.text)
                # 令牌缺失
                if data['code'] == 401:
                    raise ValueError('Hunter令牌缺失，请检查账号配置！')
                # 系统维护
                elif data['code'] == 40301:
                    raise ValueError('Hunter系统维护中，无法进行数据请求，请稍后再试')
                # 请求数据成功
                elif data['code'] == 200 or data['code'] == 40205:
                    total = data['data']['total']
                    page_nums = math.ceil(total / self.size)
                    if show_totals:
                        print("Hunter发现数据：{}, ".format(total), end="")
                        show_totals = False
                    if limit != 0 and total > limit:
                        # raise ValueError("Hunter发现数据：{}，可能存在泛解析机制，结束分页查询".format(total))
                        print("可能存在泛解析机制，中止分页查询。", end="")
                        page_nums = 1
                    if not page_print:
                        print(data['data']['rest_quota'])  # 打印今日剩余积分
                    if not data['data']['arr']:
                        raise ValueError("Hunter未发现相关数据")
                    # 展示分页数据
                    data_length = len(data['data']['arr'])
                    if page_nums > 1:
                        print("第{}页发现数据：{}, ".format(params['page'], data_length), end="")
                        print(data['data']['rest_quota'])  # 打印今日剩余积分
                        page_print = True
                        params['page'] += 1
                        time.sleep(2)
                    else:
                        # 用于跳出循环
                        page_nums -= 1
                    # 对数据进行筛选，只获取部分数据，将所有筛选的数据放到一个列表中返回
                    for i in range(data_length):
                        # 获取指定数据
                        protocol = data['data']['arr'][i]['protocol']
                        ip = data['data']['arr'][i]['ip']
                        port = data['data']['arr'][i]['port']
                        domain = data['data']['arr'][i]['domain']
                        # 将中间件信息处理为字符串，格式：中间件/版本
                        component = ""
                        if component != "":
                            for cmp in data['data']['arr'][i]['component']:
                                component += "{}".format(cmp['name'])
                                if cmp['version']:
                                    component += "/{}, ".format(cmp['version'])
                                else:
                                    component += ", "
                            component = component.strip(", ")
                        web_title = data['data']['arr'][i]['web_title']
                        icp = data['data']['arr'][i]['number']
                        # 将筛选数据插入列表
                        data_list.append([protocol, ip, port, domain, component, web_title, icp])
                else:
                    raise ValueError("Hunter请求错误，请检查请求参数后再尝试！")
            return data_list
        except ValueError as e:
            print('{}'.format(e))
            return []

    def changeAccount(self):
        if self.index < self.nums:
            self.index += 1
            self.username = self.account[self.index]['username']
            self.key = self.account[self.index]['key']
            print("Hunter积分不足已更换账号，当前账号为: {}".format(self.username))
        else:
            print("积分不足，所有账号积分均已用完，Hunter数据查询失败")
