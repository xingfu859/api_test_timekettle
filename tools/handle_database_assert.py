"""

封装函数的步骤：
第一步： 功能代码写出来 --done
第二步： def封装
第三步： 参数化： 如果有一些变化的数据/不确定的数据 设置为形参
第四步： 设置返回值： 这个函数是否有数据要给调动的人使用；
 - 不需要 断言不需要返回值

一个函数封装完了 ，函数优化：
1、加上日志： 方便进行问题定位和排查: 但凡确实结果的位置都可以加上日志【print的地方】
2、判空： 有些数据没有这提取字段 读取出来结果None，不需要做断言操作。
3、断言： 还需做一个异常捕获



"""
# 第一步： 从excel里读取这个数据库断言的表达式
import json
from tools.handle_mysql import HandleMysql
from data.setting import my_db
from tools.handle_replace import replace_mark_fun
from loguru import logger


def database_assert_fun(assert_expre):
    if assert_expre is None:
        return
    logger.info("======================数据库断言开始！============================")
    assert_expre = json.loads(assert_expre)
    logger.info(f"断言的表达式：{assert_expre}")
    for k,v in assert_expre.items():
        k = replace_mark_fun(k)
        logger.info(f"数据库断言的SQL语句：{k}")
        sql_result = HandleMysql(**my_db).query_sql(k)
        for i in sql_result.values(): # i就是获取数据库结果里的values
            logger.info(f"数据库的查询的实际结果是：{i}")
            logger.info(f"数据库的查询的预期结果是：{v}")
            try:
                assert str(i) == v
                logger.info("数据库断言成功！")
            except AssertionError as e:
                logger.error("数据库断言失败！")
                raise e


