
import json
from tools.handle_mysql import HandleMysql
from data.setting import my_db
from data.envr_data import EnviData
from loguru import logger

def pre_sql_fun(sql_data):
    if sql_data is None:
        return
    logger.info("================前置SQL处理开始执行=======================")
    sql_data = json.loads(sql_data)
    logger.info(f"前置sql的提取表达式是：{sql_data}")
    for k,v in sql_data.items():
        sql_result = HandleMysql(**my_db).query_sql(v)  # 查询的结果是字典： {'mobile_code': '534419'}
        for i,j in sql_result.items():  # 不要写死这个数据库的字段的名字  是变化  for循环动态获取真实的值
            setattr(EnviData,k,j)  #存到环境变量里 k是属性名  j是属性值
    logger.info (f"结果设置家为环境变量后的属性为：{EnviData.__dict__}")

if __name__ == '__main__':
    sql_data = '''{"mobile_code":
    "select mobile_code  from tz_sms_log where user_phone='15312121214' order by rec_date desc limit 1;"}'''
    pre_sql(sql_data)