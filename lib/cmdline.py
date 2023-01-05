import argparse
import textwrap
import time


def cmdline():
    banner = """
███╗   ███╗██╗   ██╗██╗  ████████╗██╗ ██████╗ ██╗   ██╗███████╗██████╗ ██╗   ██╗
████╗ ████║██║   ██║██║  ╚══██╔══╝██║██╔═══██╗██║   ██║██╔════╝██╔══██╗╚██╗ ██╔╝
██╔████╔██║██║   ██║██║     ██║   ██║██║   ██║██║   ██║█████╗  ██████╔╝ ╚████╔╝ 
██║╚██╔╝██║██║   ██║██║     ██║   ██║██║▄▄ ██║██║   ██║██╔══╝  ██╔══██╗  ╚██╔╝  
██║ ╚═╝ ██║╚██████╔╝███████╗██║   ██║╚██████╔╝╚██████╔╝███████╗██║  ██║   ██║   
╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝    
                                                                  by OssianSong"""
    parser = argparse.ArgumentParser(
        prog="python MultiQuery.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(banner),
        exit_on_error=False,
        add_help=False)
    # 进行聚合查询相关参数
    target = parser.add_argument_group('target')
    target.add_argument("-q", metavar="QUERY", type=str, help="输入查询语法进行查询")
    target.add_argument("-t", metavar="TYPE", type=str, choices=['fofa', 'hunter']
                        , help="指定查询平台，可选：fofa、hunter，参数为空则进行所有平台聚合查询")
    target.add_argument("-f", metavar="FILENAME", type=str, help="从指定的txt文件中读取查询语法进行批量查询")
    # 保存结果相关参数
    output = parser.add_argument_group('output')
    output.add_argument("-o", metavar="FILENAME", nargs='?', const=time.strftime('%Y%m%d%H%M%S', time.localtime()),
                        help="指定文件名将数据保存到Excel中,参数为空时使用时间戳作为默认文件名")
    output.add_argument("-d", "--db", action="store_true", default=False, help="将结果保存到数据库中")
    options = parser.add_argument_group('options')
    options.add_argument("-l", metavar="LIMIT", type=int, nargs='?', const=200,
                         help="是否进行Hunter查询数量限制，但返回结果数超过指定数目时中止分页查询")
    options.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help='查看程序使用帮助')
    return parser
