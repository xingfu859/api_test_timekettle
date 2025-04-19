"""
因为可能需要多个生成数据的方法 可以统一类里面封装管理 -- 实例方法

- 自己去优化一下 - 把faker初始化实例属性 init方法   --不写也没关系
"""
from faker import Faker
from tools.handle_mysql import HandleMysql
from data.setting import my_db


class GenData:
    def gen_unregister_phone(self):
        fk = Faker(locale='zh_CN')
        while True:
            # 第一步： 生成随机手机号码
            phone = fk.phone_number()  # 手机号码
            # 第二步： 执行数据库查询操作
            sql = f'select * from tz_user where user_mobile = "{phone}"'
            # 调用数据库查询的方法
            result = HandleMysql(**my_db).query_sql(sql)
            # 数据库查询有结果-返回字典；如果没有查询结果的话返回是None
            if result is not None:
                continue  # 继续生成新的号码 然后再查询
            else:
                return phone  # 使用这个号码

    # 生成用户名方法
    def gen_unregister_name(self):
        fk = Faker(locale='zh_CN')
        while True:
            # 第一步： 生成随机手机号码
            uname = fk.user_name()  # 手机号码
            # 第二步： 执行数据库查询操作
            sql = f'select * from tz_user where nick_name = "{uname}"'
            # 调用数据库查询的方法
            result = HandleMysql(**my_db).query_sql(sql)
            # 数据库查询有结果-返回字典；如果没有查询结果的话返回是None
            if result is not None:
                continue  # 继续生成新的号码 然后再查询
            else:
                return uname  # 使用这个号码

if __name__ == '__main__':
    # print(GenData().gen_unregister_name())
    # print(GenData().gen_unregister_phone())
    #
    print(eval('GenData().gen_unregister_name()'))