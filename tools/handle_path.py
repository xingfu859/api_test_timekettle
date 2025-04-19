"""
文件路径处理 -- 日志文件路径、用例excel文件，图片数据文件等等 -- 公共函数/方法/类 代码要做修改，比较方便的-- 封装在tools == 基于代码分层管理。

当前文件是做路径处理的公共方法
"""
from pathlib import Path

# 日志文件的路径处理
log_path = Path(__file__).absolute().parent.parent/"logs"/"lmall_api.log"

# excel文件的路径处理
excel_path = Path(__file__).absolute().parent.parent/"data"/"testcase73_1.xlsx"

# mall测试用例的excel文件
case_path = Path(__file__).absolute().parent.parent/"data"/"testcase_mall.xlsx"

# 上传图片路径
pic_path = Path(__file__).absolute().parent.parent/"data"

# 报告路径
report_path = Path(__file__).absolute().parent.parent/"allure_reports"

# 公钥路径
pub_key_path = Path(__file__).absolute().parent.parent/"data"/"rsa_public_key.pem"

if __name__ == '__main__':
    print(log_path)
    # D:\Pycharm_workspace\python73_class\day08_异常捕获和日志处理\logs\py73.log
