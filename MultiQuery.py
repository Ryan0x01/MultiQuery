import sys

from lib.cmdline import cmdline
from lib.options import Options
from lib.search import Search
from lib.output import Output

"""
需求：
    1. 在底部固定打印进度条
    2. 添加多个查询结果，待添加：zoomeye、quake、shadon
    3. 可单独进行FoFa或Hunter查询，也可以进行统一查询
    4. 将结果保存为excel，或存入数据库
    5. 纯净模式，将结果保存为[协议://ip:port]格式，保存到txt
    6. 可以进行单一语法查询，也可以通过读取文件批量查询
    7. 添加数据过滤，过滤Hunter和FoFa被污染的数据源或关键字
    8. 是否开启子域名泛解析或端口泛解析过滤模式
优化：
    1. 连接数据库时，先创建表，然后再在遍历中插入，不重复执行创建表的操作
    2. 每次都要重新连接数据库然后关闭
    3. 每读取一条文件数据，都需要重新实例化FoFa和Hunter类，可以在读取之间就实例化完，重复利用同一实例化的类
"""


if __name__ == '__main__':
    all_data = []
    # 参数初始化
    args = Options(cmdline())
    # 读文件批量查询
    data = []
    if args.file is not None:
        count = 1
        with open(args.file, 'r') as f:
            for line in f:
                print('======= 正在查询第{}条数据 ======='.format(count))
                query = line.strip()
                search = Search(args.type, query, args.limit)
                if len(search.data_list) != 0:
                    data.extend(search.data_list)
                count += 1
    else:
        search = Search(args.type, args.query, args.limit)
        data = search.data_list
    # 对数据进行输出或存储
    if len(data) == 0:
        print('查询完毕，未查询到相关数据')
    else:
        Output(data, args.out, args.out_file)



