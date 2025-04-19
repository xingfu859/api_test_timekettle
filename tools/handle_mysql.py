import pymysql
from pymysql import cursors
from loguru import logger


class HandleMysql:
    def __init__(self, user, password, database, port, host):
        # 实例属性 -- 数据库连接
        self.conn = pymysql.connect(
            user=user,
            password=password,
            database=database,
            port=port,
            host=host,
            charset="utf8mb4",  # 支持包含中文在内的各种字符集 语法记住即可
            cursorclass=cursors.DictCursor  # # 在数据库连接时，设置参数cursorclass为字典游标，fetch返回数据为字典格式
        )
        # 实例属性 - 数据库游标
        self.cur = self.conn.cursor()

    # 实例方法 - 查询方法
    def query_sql(self, sql, fetch_num=1, size=None):
        """
        :param sql: 查询的sql语句
        :param fetch_num: 获取查询结果的条数，默认值为1。传入1获取1条数据，传入2获取多条数据，传入3获取所有数据
        :param size: 当传入fetch_num为2的时候，再传入size控制具体几条数据，size默认为None
        :return: 返回查询的具体结果集
        """
        try:
            result = self.cur.execute(sql)
            logger.info(f"数据库查询结果的条数为：{result}")
            if result > 0:  # 判断是否有查询结果，再去进行详细的数据获取
                if fetch_num == 1:
                    data = self.cur.fetchone()
                    logger.info(f"数据库的查询结果为：{data}")
                    return data
                elif fetch_num == 2:
                    data = self.cur.fetchmany(size=size)
                    logger.info(f"数据库的查询结果为：{data}")
                    return data
                elif fetch_num == 3:
                    data = self.cur.fetchall()
                    logger.info(f"数据库的查询结果为：{data}")
                    return data
            else:
                logger.info("数据库没有查询到数据！")
        except Exception as err:
            logger.error(f"数据库查询异常！{err}")
        finally:
            self.cur.close()
            self.conn.close()

if __name__ == '__main__':
    from data.setting import my_db
    sql = """select mobile_code,user_phone from tz_sms_log where user_phone = "15312121212" ORDER BY rec_date limit 1;"""
    result = HandleMysql(**my_db).query_sql(sql)
    print(result)  # 如果没有查询结果默认返回的 返回是None