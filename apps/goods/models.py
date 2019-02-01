import os
from datetime import datetime

from django.db import models

from DjangoUeditor.models import UEditorField
from shops.models import Shops


class GoodsCategory(models.Model):
    """ 商品分类 """
    CATEGORY_TYPE = (
        (1, '一级分类'),
        (2, '二级分类'),
        (3, '三级分类'),
    )
    name = models.CharField(verbose_name='类别名', max_length=30, default='', help_text='类别名')
    code = models.CharField(verbose_name='类别编号', max_length=30, default='', help_text='类别编号')
    desc = models.TextField(verbose_name='类别描述', default='', help_text='类别描述')
    category_type = models.IntegerField(verbose_name='分类级别', choices=CATEGORY_TYPE, help_text='分类级别')
    # 父类级别, self指向自己, related_name后面查询时使用
    parent_category = models.ForeignKey('self', verbose_name='父类', on_delete=models.CASCADE, help_text='父类级别',
                                        related_name='sub_cat', blank=True, null=True)
    is_tab = models.BooleanField(verbose_name='是否导航', default=False, help_text='是否导航')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 自定义商品图片上传的路径
def get_image_name(model, filename):
    ext = os.path.splitext(filename)[-1]
    return 'goods/images/{0}{1}'.format(model.name, ext)


class Goods(models.Model):
    """ 商品信息 """
    category = models.ForeignKey(GoodsCategory, verbose_name='商品类目', on_delete=models.CASCADE)
    # shop = models.ForeignKey(Shops, verbose_name='店铺信息', on_delete=models.CASCADE)
    goods_sn = models.CharField(verbose_name="商品唯一货号", max_length=50, default="")
    name = models.CharField(verbose_name="商品名", max_length=100)
    click_num = models.IntegerField(verbose_name="点击数", default=0)
    sold_num = models.IntegerField(verbose_name="商品销售量", default=0)
    fav_num = models.IntegerField(verbose_name="收藏数", default=0)
    goods_num = models.IntegerField(verbose_name="库存数", default=0)
    market_price = models.FloatField(verbose_name="市场价格", default=0)
    shop_price = models.FloatField(verbose_name="本店价格", default=0)
    goods_desc = UEditorField(verbose_name="商品描述", imagePath="goods/images/", width=1000, height=300,
                              filePath="goods/files/", default='')
    goods_brief = models.TextField(max_length=500, verbose_name="商品简短描述")
    ship_free = models.BooleanField(default=True, verbose_name="是否承担运费")
    goods_front_image = models.ImageField(verbose_name="封面图", upload_to=get_image_name, null=True, blank=True,
                                          default='goods/images/default.png')
    is_new = models.BooleanField(verbose_name="是否新品", default=False)
    is_hot = models.BooleanField(verbose_name="是否热销", default=False)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    """
    商品详情页里的轮播图
    """
    goods = models.ForeignKey(Goods, verbose_name="商品", related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="", verbose_name="图片", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    """ 首页轮播的商品 """
    goods = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner', verbose_name="轮播图片", null=True, blank=True)
    index = models.IntegerField(default=0, verbose_name="轮播顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '首页轮播'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name
