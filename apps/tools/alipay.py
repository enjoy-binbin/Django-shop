# -*- coding: utf-8 -*-

# pip install pycryptodome
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
from urllib.parse import quote_plus
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
from base64 import decodebytes, encodebytes

import json


class AliPay(object):
    """
    支付宝支付接口  -- 使用的是沙箱环境
    alipay.trade.page.pay 电脑网站支付 文档:
    https://docs.open.alipay.com/270/alipay.trade.page.pay/
    """

    def __init__(self, appid, app_notify_url, app_private_key_path,
                 alipay_public_key_path, return_url, debug=False):
        self.appid = appid  # 蚂蚁金服开发者平台 沙箱环境 appid
        self.app_notify_url = app_notify_url  # 支付成功后支付宝会 POST异步url
        self.return_url = return_url  # 支付成功后GET同步url

        self.app_private_key_path = app_private_key_path  # 私钥路径
        with open(self.app_private_key_path) as fp:
            self.app_private_key = RSA.importKey(fp.read())  # 私钥

        self.alipay_public_key_path = alipay_public_key_path  # 公约路径
        with open(self.alipay_public_key_path) as fp:
            self.alipay_public_key = RSA.import_key(fp.read())  # 公钥

        if debug is True:  # 沙箱环境
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        else:  # 正式环境，需要企业资格认证
            self.__gateway = "https://openapi.alipay.com/gateway.do"

    # 构建请求参数　　跟订单相关的
    def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):
        # 请求参数，跟订单相关的
        biz_content = {
            "subject": subject,  # 订单标题
            "out_trade_no": out_trade_no,  # 商品订单号
            "total_amount": total_amount,  # 订单总金额
            "product_code": "FAST_INSTANT_TRADE_PAY",  # 销售产品码
            # "qr_pay_mode":4
        }

        biz_content.update(kwargs)  # 如果有额外的参数，可以通过update加进来
        data = self.build_body("alipay.trade.page.pay", biz_content, self.return_url)
        return self.sign_data(data)

    # 构建参数body method为默认值为请求的接口方法：alipay.trade.page.pay
    def build_body(self, method, biz_content, return_url=None):
        data = {
            "app_id": self.appid,
            "method": method,
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "biz_content": biz_content
        }

        if return_url is not None:
            data["notify_url"] = self.app_notify_url
            data["return_url"] = self.return_url

        return data

    # 签名单数的 格式化
    def sign_data(self, data):
        data.pop("sign", None)  # 签名的时候不能有sign字段，所以先pop出来
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        sign = self.sign(unsigned_string.encode("utf-8"))
        # ordered_items = self.ordered_data(data)
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in unsigned_items)

        # 获得最终的订单信息字符串
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    # 根据文档 要求对参数进行排序
    def ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    # 数据签名
    def sign(self, unsigned_string):
        key = self.app_private_key
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA256.new(unsigned_string))
        # base64 编码，转换为unicode表示并移除回车
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        return sign

    def _verify(self, raw_content, signature):
        # 开始计算签名
        key = self.alipay_public_key
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(raw_content.encode("utf8"))
        if signer.verify(digest, decodebytes(signature.encode("utf8"))):
            return True
        return False

    # 验证支付宝的return_url的合法性
    def verify(self, data, signature):
        if "sign_type" in data:
            sign_type = data.pop("sign_type")
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
        return self._verify(message, signature)


if __name__ == "__main__":
    # 反过来测试 return_url是否合法，取消掉下面的注释，注释最后面的代码
    # return_url = ''
    # o = urlparse(return_url)
    # query = parse_qs(o.query)  # 值会全部放在list里
    # processed_query = {}
    # ali_sign = query.pop("sign")[0]  # list取出第一个元素

    # alipay = AliPay(
    #     appid="2016091400506109",
    #     app_notify_url="http://119.29.27.194:8005/alipay/return/",  # POST异步请求url
    #     app_private_key_path="../trade/keys/private_2048.txt",  # 私钥
    #     alipay_public_key_path="../trade/keys/alipay_2048.txt",  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
    #     debug=True,  # 默认False, True为调用沙箱url
    #     return_url="http://119.29.27.194:8005/alipay/return/"  # GET同步请求url
    # )
    # for key, value in query.items():
    #     processed_query[key] = value[0]
    # print (alipay.verify(processed_query, ali_sign))

    alipay = AliPay(
        appid="2016091400506109",
        app_notify_url="http://119.29.27.194:8005/alipay/return/",  # POST异步请求url
        app_private_key_path="../trade/keys/private_2048.txt",  # 私钥
        alipay_public_key_path="../trade/keys/alipay_2048.txt",  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        debug=True,  # 默认False, True为调用沙箱url
        return_url="http://119.29.27.194:8005/alipay/return/"  # GET同步请求url
    )

    url = alipay.direct_pay(
        subject="iphone X 256G",  # 订单标题
        out_trade_no="20180146623999",  # 自己创建的不重复的订单号，测试时需要修改
        total_amount=1,  # 价格总计
        return_url="http://119.29.27.194:8005/alipay/return/"  # GET同步url
    )
    re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

    print(re_url)
