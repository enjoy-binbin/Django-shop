import xadmin

from .models import ShoppingCart, OrderInfo, OrderGoods


class ShoppingCartAdmin(object):
    """ 购物车管理器 """
    list_display = ['user', 'nums', 'add_time']
    search_fields = ['user', 'nums', 'add_time']
    list_filter = ['user', 'nums', 'add_time']


class OrderInfoAdmin(object):
    """ 订单信息管理器 """
    list_display = ['order_sn', 'user', 'signer', 'signer_mobile', 'pay_method', 'pay_status', 'order_mount', 'pay_time',
                    'add_time']
    search_fields = ['order_sn', 'user', 'signer', 'signer_mobile', 'pay_method', 'pay_status', 'order_mount', 'pay_time',
                     'add_time']
    list_filter = ['order_sn', 'user', 'signer', 'signer_mobile', 'pay_method', 'pay_status', 'order_mount', 'pay_time',
                   'add_time']

    show_detail_fields = ['order_sn']
    refresh_times = (3, 5)
    list_export = ('xls', 'xml', 'json')


class OrderGoodsAdmin(object):
    """ 订单商品管理器 """
    list_display = ['order', 'goods', 'goods_num', 'add_time']
    search_fields = ['order', 'goods', 'goods_num', 'add_time']
    list_filter = ['order', 'goods', 'goods_num', 'add_time']


xadmin.site.register(ShoppingCart, ShoppingCartAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)
xadmin.site.register(OrderGoods, OrderGoodsAdmin)
