import pymysql

from config.config import config


class Database:
    def __init__(self):
        # 数据库配置读取
        self.host = config['database']['host']
        self.port = config['database']['port']
        self.user = config['database']['user']
        self.passwd = config['database']['password']
        self.db = config['database']['db_name']
        self.table = config['database']['table']
        # 数据库连接初始化
        self.conn = self.connect()
        self.cursor = self.conn.cursor()

    def connect(self):
        try:
            conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.passwd,
                                   charset="utf8mb4", autocommit=True, cursorclass=pymysql.cursors.DictCursor)
            return conn
        except Exception:
            raise Exception("MySQL数据库连接失败，请检查配置是否正确")

    def initDatabase(self):
        try:
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS {};".format(self.db))
            self.conn.select_db(self.db)
        except Exception:
            raise Exception("数据库初始化失败")

    def createTable(self):
        try:
            # conn.cursor().execute("DROP TABLE IF EXISTS {};".format(self.table))
            self.cursor.execute("CREATE TABLE IF NOT EXISTS {}("
                                  "`id` int primary key auto_increment comment '序号',"
                                  "`protocol` varchar(100) comment '协议',"
                                  "`ip` varchar(100) comment 'IP',"
                                  "`port` int comment '端口',"
                                  "`domain` varchar(255) comment '域名',"
                                  "`component` varchar(255) comment '组件/版本',"
                                  "`title` varchar(500) comment '站点标题',"
                                  "`icp` varchar(255) comment '备案号');".format(self.table))
            print("数据表创建成功！")
        except Exception as e:
            print("数据表创建失败！")
            raise Exception(e)

    def insertIntoTable(self, data_list):
        try:
            sql_value = ""
            for data in data_list:
                sql_value += "'{}',".format(data)
            self.cursor.execute("insert into {}(protocol,ip,port,domain,component,title,icp) values({});"
                                .format(self.table, sql_value.strip(',')))
        except Exception as e:
            print("{}数据插入失败！".format(data_list[0]))
            raise Exception(e)

    def __del__(self):
        self.cursor.close()
        self.conn.close()
