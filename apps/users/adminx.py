# -*- coding: utf-8 -*-
import xadmin
from xadmin import views

from .models import EmailVerifyCode, UserAddress, UserProfile


class BaseSetting(object):
    """ 基本adminView配置 """
    enable_themes = True  # 启动主题
    use_bootswatch = True  # 主题列表


class CommSetting(object):
    """ commonView配置 """
    site_title = '彬彬商场后台管理系统'  # 后台标题
    site_footer = 'Binbin Mall'  # 后台脚注
    # menu_style = "accordion"  # 可以收缩app的菜单栏
    # global_search_models = [model1, ...]  # 后台顶部搜索框


class EmailVerifyCodeAdmin(object):
    """邮箱验证码"""
    list_display = ['email', 'id', 'code', 'type', 'add_time']  # 列表页显示的字段
    search_fields = ['code', 'email', 'type']  # 可以用来搜索的字段
    list_filter = ['code', 'email', 'type', 'add_time']  # 过滤器能过滤的字段


class AddressAdmin(object):
    list_display = ['user', 'signer', 'signer_mobile', 'address']
    search_fields = ['user', 'signer', 'signer_mobile', 'address']
    list_filter = ['user', 'signer', 'signer_mobile', 'address']


# 注册xadmin全局设置
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, CommSetting)

# 注册app
xadmin.site.register(EmailVerifyCode, EmailVerifyCodeAdmin)
xadmin.site.register(UserAddress, AddressAdmin)
