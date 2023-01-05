from api.fofa import FoFa
from api.hunter import Hunter


class Search:
    def __init__(self, type, query, limit):
        self.query = query
        self.limit = limit
        if type == 'fofa':
            self.data_list = self.fofaSearch()
        elif type == 'hunter':
            self.data_list = self.hunterSearch()
        else:
            self.data_list = self.mergeSearch()

    def fofaSearch(self):
        fofa = FoFa()
        fofa_data = fofa.search(self.query)
        return fofa_data

    def hunterSearch(self):
        hunter = Hunter()
        hunter_data = hunter.search(self.query, self.limit)
        return hunter_data

    def mergeSearch(self):
        all_data_list = []
        index_list = []
        hunter_data = self.hunterSearch()
        fofa_data = self.fofaSearch()
        # 首先根据hunter数据建立索引列表，用于存放IP和端口判断数据是否重复，格式为ip:port
        if hunter_data:
            for data in hunter_data:
                ip_port = "{}:{}".format(data[1], data[2])
                if ip_port not in index_list:
                    index_list.append(ip_port)
                    all_data_list.append(data)
        if fofa_data:
            # 遍历fofa数据，如果不存在该条数据，则插入到列表中，并更新索引列表
            for data in fofa_data:
                ip_port = "{}:{}".format(data[1], data[2])
                if ip_port not in index_list:
                    index_list.append(ip_port)
                    all_data_list.append(data)
        return all_data_list
