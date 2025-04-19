"""
"""
from openpyxl import load_workbook


def read_excel(excel, sheet):
    """
    :param excel: excel文件路径
    :param sheet: 读取数据的表单
    :return: 读取后的所有数据，保存为列表嵌套字典格式
    """
    wb = load_workbook(excel)
    sh = wb[sheet]

    # 读取当前表单全部数据
    cases = list(sh.values)  # 得到列表嵌套元组的数据
    # 每条用例数据都要跟表头元组压缩，先取出来表头
    heading = cases[0]
    list_case = []  # 定义空列表，用来存放压缩后的字典数据
    # 依次拿到后面的每一行的数据-遍历，分别与表头行zip压缩
    for i in cases[1:]:
        data = dict(zip(heading, i))  # zip压缩后转成字典
        list_case.append(data)
    return list_case


if __name__ == '__main__':
    from tools.handle_path import excel_path
    result_data = read_excel(excel_path, "login")
    print(result_data)
