"""
这个算法的操作是固定的 所以可以直接封装  后续直接调用。

"""
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


def encrypt_with_rsa(data,ras_pulic_key):
    data_bytes = data.encode("UTF8")  #转化为二进制数据
    # 第一步：读取公钥信息内容
    with open(ras_pulic_key) as f:
        public_key_str = f.read()
        # 第二步：通过RSA导入公钥信息，并返回公钥对象
        public_key = RSA.importKey(public_key_str)
        # 第三步： 基于公钥创建RSA加密器对象
        pk = PKCS1_v1_5.new(public_key)
        # 第四步：通过RSA加密器对象进行加密（加密前数据转换为二进制格式）
        rsa_data = pk.encrypt(data_bytes)  # 这个是二进制的数据
        # 第五步：需要先进行base64编码，才可以转化为字符串可用文本
        base64_data = base64.b64encode(rsa_data)
        # 第六步： 将二进制数据转化为文本
        return base64_data.decode("UTF8")  # 密文返回