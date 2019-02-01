from django.urls import path

from .views import OrderView, OrderCommitView, AddShoppingCartView, ImmediatelyCreateOrder

app_name = 'trade'
urlpatterns = [
    path('', OrderView.as_view(), name='order'),  # 订单页

    path('commit/', OrderCommitView.as_view(), name='order_commit'),  # 提交订单

    path('cart/add/', AddShoppingCartView.as_view(), name='add_cart'),  # 添加购物车

    path('immediately_buy', ImmediatelyCreateOrder.as_view(), name='immediately_buy'),  # 立即购买
]