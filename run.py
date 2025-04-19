"""
入口文件：
1、记录日志文件
2、pytest.main -- 收集测试用例 执行测试用例 生成报告

"""
import pytest
from loguru import logger
from tools.handle_path import log_path,report_path
import sys

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

# 收集和执行测试用例
pytest.main(["-v","-s",f"--alluredir={report_path}","--clean-alluredir",f"--env={param}"])

