from datetime import datetime
import os
from django.db import models
from django.contrib.auth.models import AbstractUser


# 自定义商品图片上传的路径
def get_image_name(model, filename):
    ext = os.path.splitext(filename)[-1]
    name = os.path.splitext(filename)[-2]
    # 存放在 media/users/images/用户名-文件名.后缀
    return 'users/images/{0}-{1}{2}'.format(model.username, name, ext)


class UserProfile(AbstractUser):
    """ 扩展原有的auth_user表 """
    nickname = models.CharField(verbose_name='昵称', max_length=50, default='')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(verbose_name='性别', max_length=6, choices=(('male', u'男'), ('female', u'女 ')),
                              default='female')
    address = models.CharField(verbose_name='地址', max_length=100, default='')
    mobile = models.CharField(verbose_name='电话', max_length=11, null=True, blank=True)
    image = models.ImageField(verbose_name='头像', max_length=100, null=True, blank=True, upload_to=get_image_name,
                              default=u'image/default.jpg')

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyCode(models.Model):
    """ 邮箱验证码 """
    code = models.CharField(verbose_name='验证码', max_length=20)
    email = models.EmailField(verbose_name='邮箱', max_length=50)
    type = models.CharField(verbose_name='类型', max_length=20,
                            choices=(('register', '注册'), ('forget', '忘记密码'), ('change', '修改邮箱')))
    is_used = models.BooleanField(verbose_name='是否激活', default=False)
    add_time = models.DateTimeField(verbose_name='发送时间', default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


# TODO 短信验证码


class UserAddress(models.Model):
    """ 用户收货地址 """
    user = models.ForeignKey(UserProfile, verbose_name='用户id', on_delete=models.CASCADE)
    signer = models.CharField(verbose_name='收件人', max_length=20)
    signer_mobile = models.CharField(max_length=11, default="", verbose_name="电话")
    address = models.CharField(max_length=100, default="", verbose_name="详细地址")
    is_default = models.BooleanField(default=False, verbose_name='是否默认')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.nickname + self.address
