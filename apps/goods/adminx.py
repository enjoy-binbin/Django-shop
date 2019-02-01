# -*- coding: utf-8 -*-
import xadmin

from .models import Goods, GoodsCategory, Banner


class GoodsAdmin(object):
    ordering = ['id']
    # goods_desc内容不显示
    list_display = ["name", "click_num", "sold_num", "fav_num", "goods_num", "market_price",
                    "shop_price", "goods_brief", "is_new", "is_hot", "add_time"]
    search_fields = ['name', ]
    list_editable = ["is_hot", ]
    list_filter = ["name", "click_num", "sold_num", "fav_num", "goods_num", "market_price",
                   "shop_price", "is_new", "is_hot", "add_time", "category__name"]
    # style_fields = {"goods_desc": "ueditor"}


class GoodsCategoryAdmin(object):
    list_display = ["name", "category_type", "parent_category", "add_time"]
    list_filter = ["category_type", "parent_category", "name"]
    search_fields = ['name', ]
    ordering = ['category_type']


class BannerAdmin(object):
    list_display = ["goods", "image", "index", "add_time"]
    list_filter = ["goods", "image", "index", "add_time"]
    search_fields = ["goods", "image", "index", "add_time"]


xadmin.site.register(Goods, GoodsAdmin)
xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)
xadmin.site.register(Banner, BannerAdmin)
