from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Goods

# from users.models import UserProfile
# 当开发第三方应用，不知道别人设计的model
# 可以这样获取到settings里设置的user.model
User = get_user_model()


class ShoppingCart(models.Model):
    """ 购物车 """
    user = models.ForeignKey(User, verbose_name="用户id", on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name="商品id", on_delete=models.CASCADE)
    nums = models.IntegerField(default=0, verbose_name="商品购买数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")

    def __str__(self):
        return "%s(%d)".format(self.goods.name, self.nums)


class OrderInfo(models.Model):
    """ 订单详情 """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED", "交易结束"),
        ("paying", "待支付"),
    )

    PAY_METHOD = (
        (1, '支付宝'),
        (2, '微信支付'),
        (3, '货到付款'),
        (4, '银联支付')
    )

    order_sn = models.CharField(verbose_name="订单号", max_length=30, null=True, blank=True, unique=True)
    trade_sn = models.CharField(verbose_name="交易号", max_length=100, unique=True, null=True, blank=True)

    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    signer = models.CharField(verbose_name="收件人", max_length=10, null=True, blank=True)
    signer_mobile = models.CharField(verbose_name="收件手机号", max_length=11, null=True, blank=True)
    address = models.CharField(verbose_name="收货地址", max_length=50, null=True, blank=True)
    # address = models.ForeignKey('users.UserAddress', verbose_name='收获地址', on_delete=models.CASCADE)

    pay_method = models.SmallIntegerField(verbose_name='支付方式', choices=PAY_METHOD, default=1)
    pay_status = models.CharField(verbose_name="订单状态", choices=ORDER_STATUS, default="paying", max_length=30)

    post_message = models.CharField(verbose_name="订单留言", max_length=200)
    order_mount = models.FloatField(verbose_name="订单金额", default=0.0)
    pay_time = models.DateTimeField(verbose_name="支付时间", null=True, blank=True)

    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "订单信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(models.Model):
    """ 订单里的商品详情 , 订单一对多个商品的关系"""
    order = models.ForeignKey(OrderInfo, verbose_name="订单信息", related_name="goods", on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE)
    goods_num = models.IntegerField(default=0, verbose_name="商品数量")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)

    # 大猪蹄子  生日快乐  2019/1/10
