"""
提取表达式： {"check_code":"text"}
 - k : 变量名
 - v :text 文本

之前的; {"prodId":"$..prodId"}
   - k : 变量名
   - v :jsonpath表达式

完善的思路：
1、在循环取值后 对v进行分支判断：
  - 如果是=="text"
  - 如果是以“$”开头 做jsonpath的提取

"""


import json
from jsonpath import jsonpath
from data.envr_data import EnviData
from loguru import logger


def extrac_response(response,extract_expre):
    """
    这是一个提取响应结果数据的函数
    :param response: 接口响应消息对象
    :param extract_expre: 从excel里读取的提取响应消息的表达式
    :return: 没有返回值
    """
    if extract_expre is None:
        logger.info("这条用例没有需要提取响应的数据！")
        return
    logger.info("===================开始提取响应数据=========================")
    extract_expre = json.loads(extract_expre) # 字典
    logger.info(f"提取响应结果的表达式是：{extract_expre}")
    for k,v in extract_expre.items():  # k 是变量名  v是jsonpath提取表达式
        value = None  # value初始化
        if v.startswith("$"):
            value = jsonpath(response.json(),v)[0]
        elif v == "text":
            value = response.text  # 直接获取响应消息的文本
        logger.info(f"提取的数据值是：{value}")
        setattr(EnviData,k,value) # 属性名字-k，属性值-提取的value
    logger.info(f"提取并存储到环境变量的类属性：{EnviData.__dict__}")  # 查看这个类的所有属性 确认是否存到环境变量里去了

if __name__ == '__main__':
    response = {'access_token': '6124107c-bcf5-4601-b2e5-ccff1d1b09e0', 'token_type': 'bearer',
                'refresh_token': '96c52b4e-7eac-4bfc-b656-401b032f6276', 'expires_in': 1295999,
                'pic': 'http://shop.lemonban.com:8108/2025/03/903f6ed2174d4f07ab64dd8620e2aa7b.png',
                'userId': '1f6c1b09905e4d52865907a8dbea0ba6', 'nickName': 'lemon_py', 'enabled': True}

    extract_expre = '{"access_token":"$..access_token","token_type":"$..token_type"}'
    extrac_response(response,extract_expre)