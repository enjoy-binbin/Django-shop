from datetime import datetime

from django.db import models


class CityDict(models.Model):
    """ 店铺所在城市 """
    name = models.CharField(verbose_name='城市', max_length=20)
    desc = models.CharField(verbose_name='描述', max_length=100)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '店铺城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Shops(models.Model):
    """ 店铺信息 """
    name = models.CharField(verbose_name='店铺名称', max_length=20, default='')
    desc = models.TextField(verbose_name='店铺描述', default='')
    # tag = models.CharField(verbose_name='店铺标签', max_length=20, default='个人商')
    image = models.ImageField(verbose_name='logo', upload_to='shops/%Y/%m', max_length=50)
    address = models.CharField(verbose_name='店铺地址', max_length=50)
    city = models.ForeignKey(CityDict, verbose_name='所在城市', on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '店铺信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

