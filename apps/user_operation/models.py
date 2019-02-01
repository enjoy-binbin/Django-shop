from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from goods.models import Goods

User = get_user_model()

class UserFav(models.Model):
    """ 用户收藏 """
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name="商品", help_text="商品id", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")  # 两个字段作为联合唯一索引

    def __str__(self):
        return self.user.username