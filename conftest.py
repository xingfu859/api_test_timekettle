"""
conftest： pytest7.4+版本， 根目录下不能发现的
- pytest 版本 7.3.1 版本
- 如果版本不一样 可以conftest文件放在testcases目录

在这个夹具里先实现登录的操作
 - 发送登录请求
 - 得到响应结果提取token
 - 再返回这个token： 那么在测试用例里调用这个夹具 直接得到夹具的返回值

"""

import pytest

# 定义夹具——执行登录接口
import requests
from jsonpath import jsonpath
from loguru import logger


@pytest.fixture()
def login_fixture():
    param = {"principal": "lemon_py", "credentials": "12345678", "appType": 3, "loginType": 0}
    url = 'http://mall.lemonban.com:8107/login'
    res = requests.request("post", url, json=param)
    # 提取token
    access_token = jsonpath(res.json(), '$..access_token')[0]
    token_type = jsonpath(res.json(), '$..token_type')[0]
    token =  token_type + access_token
    yield token #返回值

# 定义一个钩子函数: 如果要定义多个自定义的参数 那么在同一个钩子函数里 定义多条参数
def pytest_addoption(parser):
    # 注册自定义参数命令行参数
    parser.addoption("--env", default="test", choices=['dev', 'test', 'pre', 'prod'],
                     help="命令行参数 '--env' 设置测试环境切换")



# 定义一个夹具： 目的是为了接收pytest参数传进来的值 --这个夹具的名字可以自己随便取
@pytest.fixture()
def get_env(request):
    # option变量名就可以存储 --env的参数的值： test  dev pro
    env_value = request.config.getoption("--env")
    logger.info(f"--env的参数的值是{env_value}")
    # 设置返回值 把拿到的数据返回
    yield env_value