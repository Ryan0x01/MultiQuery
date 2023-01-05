def file_reader(filename):
    """
    从文件中读取数据，进行批量查询
    :param filename:
    """
    lines = []
    with open(filename, 'r', encoding='utf8') as f:
        for line in f:
            lines.append(line.strip())
    return lines


def save_to_excel(filename, data_list):
    """
    将数据保存到Excel表中
    :param filename: Excel文件名
    :param data_list: 待写入文件的数据集
    """
