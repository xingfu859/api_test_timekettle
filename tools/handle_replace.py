"""
目前支持变量替换  所以加上一个分支 支持函数的替换
 -#gen_unregister_phone()#：mark如果包含（） | 以（）结尾的话 那么就是做函数的调用
 - #gen_unregister_phone#  ： 占位符里是变量名 直接环境变量取值替换
对mark变量进行if判断：
 - 如果有括号：执行这个函数  得到生成数据
    - 1） 生成的数据存到环境变量里
        - setattr(类，属性名，属性值)： 属性名应该是函数名字去掉括号 函数名字就是mark，mark.strip("()")-属性名字
    - 2） 用生成的数据 完成函数占位符的替换
 - 否则替换变量

"""
# 为了验证结果 我们在这里预设换一个环境变量
# class EnviData:
#     orderNumbers = '1904520669115453440'


import re
from loguru import logger
from data.envr_data import EnviData
from tools.handle_gendata import GenData

def replace_mark_fun(str_data):
    if str_data is None:
        logger.info("数据为空，不需要替换！")
        return
    result = re.findall("#(.*?)#",str_data) # ['token_type', 'access_token']
    if result: # 空列表-- 正则没有匹配到任何结果 就不会进入分支； 非空列表--有匹配结果就会执行下面的分支
        logger.info("===================开始替换数据=========================")
        logger.info(f"原始字符串是：{str_data}")
        logger.info(f"需要替换的占位符有：{result}")
        for mark in result:
            # 加一个判断分支  是否有括号
            if mark.endswith("()"):  #函数的调用- mark是 字符串的类型 'gen_unregister_phone()'
                # gen_data是接受生成的数据 -- 函数的返回值
                gen_data = eval(f'GenData().{mark}')  # 'GenData().gen_unregister_phone()' -- eval函数执行引号里Python表示式
                #1） 生成的数据存到环境变量里： mark这个字符串去掉后面（） strip("()") 得到属性名字
                setattr(EnviData,mark.strip("()"),gen_data)
                # 2） 用生成的数据 完成函数占位符的替换 并得到替换完成后的字符串
                str_data = str_data.replace(f"#{mark}#",str(gen_data))
            else:  #否则就是变量的替换
                if hasattr(EnviData,mark): # 判断环境变量里是否有这个属性名 : 有-替换
                    # 如果有这个属性 那么获取这个属性的值
                    value = getattr(EnviData,mark) #  "6124107c-bcf5-4601-b2e5-ccff1d1b09e0" 替换的内容
                    # 执行替换操作： 在str_data字符串里替换 #token_type# --> value
                    str_data = str_data.replace(f"#{mark}#",str(value)) # 字符串的替换操作是生成新的字符串 不是替换原字符串
    else:
        logger.info(f"要替换的占位符为空：{result},不需要做替换操作！")
    logger.info(f"替换完成之后的字符串是：{str_data}")
    return str_data

