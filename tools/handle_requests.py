"""
封装发送请求方法之后，思考优化：
1、看不到过程，不方便定位问题： 日志
    - 请求四大要素
    - 响应消息体

# 域名部分: 接口测试的时候需要跟这个域名和端口  拼接一个完整的接口地址
base_url = {'test':'http://shop.lemonban.com:8107',
       'dev':'http://dev.mall.lemonban.com:3344',
       'pre':'http://pre.mall.lemonban.com:3344'}

"""
import json
from tools.handle_path import pic_path
import requests
from loguru import logger
from tools.handle_replace import replace_mark_fun
from tools.handle_extract import extrac_response
from tools.handle_presql import pre_sql_fun
from data.setting import base_url


# 这是一个函数 ： 函数可以直接调用夹具么？ -- 夹具可以调夹具 用例可以调夹具 函数不可以直接调用夹具
def request_api(case,get_env,token=None): # get_env的值 pre test dev
    # 发送接口请求
    method = case["请求方法"]
    url = base_url[get_env] + case["接口地址"]  # env参数的值域名+/login
    param = case["请求参数"]  # {"filename":"lemon.png"}
    header = case["请求头"]
    presql = case["前置SQL"] # 前置sql的表达式
    # 在执行前置sql之前 替换前置SQL占位符
    presql = replace_mark_fun(presql)
    # 在发送请求之前并是在完成替换之前 执行sql  把数据库结果存到环境变量里去： 才能给后面完成替换操作
    pre_sql_fun(presql)

    # 发送接口之前要完成参数 头部等替换操作 并且替换函数参数一定是字符串 ： 发送请求并且在我反序列化之前
    url = replace_mark_fun(url) # 替换地址
    param = replace_mark_fun(param)  #得到返回值： 替换完成后的字符串 赋值给这个参数
    header = replace_mark_fun(header) #得到返回值： 替换完成后的字符串 赋值给这头部

    # 对可能会为None的头部和参数进行判空处理  --如果不为空 再反序列化转化为字典
    if header is not None:
        header = json.loads(header)  # 字典
        if token is not None:  # 如果token不为空 那么token替换掉Authorization的值
            header["Authorization"] = token # 如果有Authorization -- 替换value； 如果没有Authorization -新增
    if param is not None:
        param = json.loads(param)

    # 日志记录请求消息的四大要素
    logger.info("=====================请求消息=======================")
    logger.info(f"请求方法是：{method}")
    logger.info(f"请求地址是：{url}")
    logger.info(f"请求头是：：{header}")
    logger.info(f"请求参数是：{param}")

    req = None  # 返回结果的变量初始化
    # 第一层： 先根据method判断
    if method.lower() == "get":
        req = requests.request(method, url, headers=header, params=param)
    if method.lower() == "post":
        # 第二次: 如果method是post的话再根据content-type判断
        if header["Content-Type"] == "application/json":
            req = requests.request(method, url, headers=header, json=param)
        elif header["Content-Type"] == "application/x-www-form-urlencoded":
            req = requests.request(method, url, headers=header, data=param)
        elif header["Content-Type"] == "multipart/form-data":
            header.pop("Content-Type")  # 因为上传接口不能接受content-type头部 会报错 删除
            filename = param["filename"]
            file_param = {"file": (filename, open(pic_path / filename, mode="rb"))}
            logger.info(f"文件参数：{file_param}")
            logger.info(f"文件上传的头部：{header}")
            req = requests.request(method, url, headers=header, files=file_param)
    if method.lower() == "put":
        req = requests.request(method, url, headers=header, json=param)
    # 日志记录相应结果：
    logger.info("===============响应消息=====================")
    logger.info(f"响应状态码：{req.status_code}")
    logger.info(f"响应消息体：{req.text}")
    # 在得到了接口的响应解雇哦之后再提取响应字段 -在这里调用提取的函数  设置提取的值到环境变量里去
    extrac_response(req,case["提取响应字段"])

    return req  # 返回接口的响应结果对象 ： 很多分支，可能在某个分支里没定义req变量