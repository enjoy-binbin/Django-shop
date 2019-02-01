# -*- coding: utf-8 -*-
import xadmin

from .models import CityDict, Shops


class CityDictAdmin(object):
    """ 城市管理器 """
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc', 'add_time']
    list_filter = ['name', 'desc', 'add_time']


class ShopAdmin(object):
    """ 店铺管理器 """
    list_display = ['name', 'image', 'city', 'add_time']  # 列表页显示的字段
    search_fields = ['name', 'image', 'city', 'add_time']  # 可以用来搜索的字段
    list_filter = ['name', 'image', 'city', 'add_time']  # 过滤器能过滤的字段


# 注册app
# xadmin.site.register(CityDict, CityDictAdmin)
# xadmin.site.register(Shops, ShopAdmin)
