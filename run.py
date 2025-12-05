"""
入口文件：
1、记录日志文件
2、pytest.main -- 收集测试用例 执行测试用例 生成报告
'''
'''
allure使用：pytest.main()加参数
1、运行用例的时候会自动生成结果文件： 使用pytest运行的参数：加一个参数：--alluredir=reports  相对于run.py所在工作目录下的目录
 - 在相对于run.py所在工作目录下就会生成reports文件夹下的allure结果文件。-json文件给allure看的 我们不需要看 看不懂。
 -这些只是结果文件，还没有生成报告，接下来要allure来解析这些结果文件，生成allure的报告 --HTML页面给人看懂的

2、使用allure命令生成报告：
cmd里或者terminal里，跳转到rootdir目录；==cd 切换目录
运行命令： allure serve reports=== serve后面跟的是自己定义的结果文件的目录，相对于rootdir的目录；

3、"--clean-alluredir"  清除历史执行json'文件记录。 --一般都会加上。
"""
import pytest
from loguru import logger
from tools.handle_path import log_path,report_path
import sys
#写入日志文件
logger.add(sink=log_path,
           level="INFO",
           rotation="1 day",
           retention="20 days",
           encoding="UTF8")

# 接受命令行执行参数
try:
    param = sys.argv[1]
except Exception as e:
    param = "test"

# pytest.main -- 收集测试用例 执行测试用例 生成报告
pytest.main(["-v","-s",f"--alluredir={report_path}","--clean-alluredir",f"--env={param}"])

