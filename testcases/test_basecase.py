"""
购物车模块
# 第二步：会使用excel读取封装函数 读取数据  [{},{},{}]
case_all = read_excel(case_path,"登录")

# 第三步：pytest的数据驱动 ： 用例方法 执行所有数据，得到每条测试结果
@pytest.mark.parametrize("case",case_all)  # case是字典
def test_logincase(case,get_env):  #调用环境的夹具 再传给函数的参数 test dev
    expected_result = case["预期结果"]
    #调用了reqests_api方法  得到响应结果对象
    req = request_api(case,get_env)
    # 调用断言的函数
    response_assert(req,expected_result)

# 第二步：会使用excel读取封装函数 读取数据  [{},{},{}]
case_all = read_excel(case_path,"上传-关联")

# 第三步：pytest的数据驱动 ： 用例方法 执行所有数据，得到每条测试结果
@pytest.mark.parametrize("case",case_all)  # case是字典
def test_logincase(case,get_env):
    expected_result = case["预期结果"]
    req = request_api(case,get_env)
    response_assert(req,expected_result)
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
case_all = read_excel(case_path,"APP端通测用例")

# 第三步：pytest的数据驱动 ： 用例方法 执行所有数据，得到每条测试结果
@pytest.mark.parametrize("case",case_all)  # case是字典
def test_base_case(case):
    expected_result = case["预期结果"]
    db_assert_data = case["数据库断言"]
    req = request_api(case,"pre")
    # 响应结果
    response_assert(req,expected_result)
    # 数据库断言
    database_assert_fun(db_assert_data)