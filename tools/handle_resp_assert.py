"""
封装函数的步骤：
第一步： 功能代码写出来 --done
第二步： def封装
第三步： 参数化： 如果有一些变化的数据/不确定的数据 设置为形参
第四步： 设置返回值： 这个函数是否有数据要给调动的人使用；断言函数不需要返回的。

一个函数封装完了 ，思考几个补充：
1、加上日志： 方便进行问题定位和排查: 但凡确实结果的位置都可以加上日志【print的地方】
2、断言可能会失败记得加上异常捕获： 记录日志  + 抛出错误 【try 】
3、判空： 有些数据没有这个断言字典 读取出来结果None，不需要做断言操作。

"""

import json

# 登录响应结果: req.json() 得到字典的结果  因为jsonpath提取需要字典的结果
from jsonpath import jsonpath
from loguru import logger
from tools.handle_replace import replace_mark_fun


def response_assert(response,expected_result):
    """
    这是一个响应结果断言的函数：对接口进行响应断言；支持接口的结果是json格式和文本格式。
    :param response: 接口响应结果消息对象
    :param expected_result: 从excel里读取出来的断言表达式
    :return: 没有返回值
    """
    logger.info("================开始做响应结果断言=============================")
    if expected_result is None:
        logger.info("这条用例不需要做断言！")
        return  # 如果响应断言是None  不需要做断言 直接返回
    #在反序列化转化为字典之前  完成断言表达式的替换操作
    expected_result = replace_mark_fun(expected_result)

    expected_result = json.loads(expected_result)   #字典
    logger.info(f"期望结果表达式：{expected_result}")
    for k,v in expected_result.items():
        if k.startswith("$"):
            actual_result = jsonpath(response.json(),k)[0]
            logger.info(f"执行结果是{actual_result}")
            logger.info(f"预期结果是{v}")
            try:
                assert actual_result == v
                logger.info("断言通过！")
            except AssertionError as e:
                logger.error("断言失败！")
                raise e
        elif k == "text":
            actual_result = response.text
            logger.info(f"执行结果是{actual_result}")
            logger.info(f"预期结果是{v}")
            try:
                assert actual_result == v
                logger.info("断言通过！")
            except AssertionError as e:
                logger.error("断言失败！")
                raise e