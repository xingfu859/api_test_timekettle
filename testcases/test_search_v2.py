"""
使用pytest测试框架执行登录测试用例：
pytest测试框架去测试接口： 对应用测试用例。【登录，搜索，购物车等】
* 第一步：针对每个模块设计测试用例 + 测试数据==  正常测试数据+ 异常测试数据，放在excel表格管理。
* 第二步：会使用excel读取封装函数 读取数据 == 列表嵌套字典的格式数据 [{},{},{}....]
* 第三步：pytest的数据驱动 ： 用例方法 执行所有数据，得到每条测试结果

导包的原则： 从根目录下的第一个文件夹开始导包。

登录用例： [{},{},{}]
{'用例编号': 'login_001', '用例标题': '登录成功',
 '优先级': 'p1',
 '请求方法': 'post',
 '接口地址': 'http://shop.lemonban.com:8107/login',
 '请求头': '{"Content-Type":"application/json","Accept-Language":"zh"}',
 '请求参数': '{"principal": "lemon_py", "credentials": "12345678", "appType": 3, "loginType":0}',
 '预期结果': None}

发送请求发现了一个问题：
1、报错：headers = '{"Content-Type":"application/json","Accept-Language":"zh"}'
  信息：    AttributeError: 'str' object has no attribute 'items'
  -原因： requests库的头部 和参数等都要是字典格式传输的。
  - debug调试看下数据类型： header和param 都是str类型 所以不能直接用于接口参数的传递
解决方案：
1、eval() 函数： 脱引号的  str  --  dict
  - 问题： 数据里有非法Python格式数据： false --False  ，null, true
2、替代的方案： json反序列化。 --了解json数据。


"""
import json

import pytest
import requests
from tools.handle_excel import read_excel
from tools.handle_path import case_path
from tools.handle_resp_assert import response_assert
from tools.handle_requests import request_api


# 第二步：会使用excel读取封装函数 读取数据  [{},{},{}]
case_all = read_excel(case_path,"搜索")

# 第三步：pytest的数据驱动 ： 用例方法 执行所有数据，得到每条测试结果
@pytest.mark.parametrize("case",case_all)  # case是字典
def test_logincase(case,get_env):
    expected_result = case["预期结果"]
    req = request_api(case,get_env)
    response_assert(req,expected_result)