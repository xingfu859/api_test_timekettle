"""
文件上传的接口：
1、调用接口发送请求方法是ok
2、接口本身是需要接口鉴权的： 先登录接口  提取token 得到token
  --登录接口先执行，上传接口的前置操作 是登录

方案： pytest的夹具 fixture功能 前置操作
 - conftest文件实现夹具共享： 测试用例共享  并且返回值token
 - 在pytest测试用例里调用这个夹具
 - 优化了一下requests_api方法 -接受token更新头部

上传接口是通过requets_api方法发送请求： token传到reqesuts_api方法
- 通过参数的形式传入进去  必须先给这个requests_api方法定义形参

"""
import json

import pytest
import requests
from tools.handle_excel import read_excel
from tools.handle_path import case_path
from tools.handle_resp_assert import response_assert
from tools.handle_requests import request_api
from tools.handle_database_assert import database_assert_fun


# 第二步：会使用excel读取封装函数 读取数据  [{},{},{}]
case_all = read_excel(case_path,"注册接口-数据库断言")

# 第三步：pytest的数据驱动 ： 用例方法 执行所有数据，得到每条测试结果
@pytest.mark.parametrize("case",case_all)  # case是字典
def test_logincase(case,get_env):
    expected_result = case["预期结果"]
    db_assert_data = case["数据库断言"]
    req = request_api(case,get_env)
    response_assert(req,expected_result)
    database_assert_fun(db_assert_data)