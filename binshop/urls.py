from django.urls import path, include, re_path
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve  # 处理图片静态文件
import xadmin
# from users.views import login_1  # 函数式调用
from users.views import IndexView, LoginView, LogoutView, RegisterView, ActiveView, ForgetView, ResetView
from goods.views import CategoryView, GoodDetailView, CartView
from trade.views import AddShoppingCartView, ShoppingCartView, OrderView, OrderCommitView
from users.views import UserInfoView
from trade.views import AlipayView
# from binshop.settings import STATIC_ROOT,MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),

    path('', IndexView.as_view(), name='index'),
    path('users/', include('users.urls')),

    # path('login/', login_1, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    re_path('active/(?P<active_code>.*)/', ActiveView.as_view(), name='active'),
    # path('active/<str:code>', RegisterView.as_view(), name='register'),

    path('forget/', ForgetView.as_view(), name='forget_pwd'),
    path('reset/', ResetView.as_view(), name='reset_pwd'),

    path('captcha/', include('captcha.urls')),

    path('goods/', include('goods.urls')),
    path('goods/<int:id>/', GoodDetailView.as_view(), name='good_detail'),
    path('category/<int:id>/', CategoryView.as_view(), name='category'),

    path('cart/', ShoppingCartView.as_view(), name='cart'),
    path('order/', include('trade.urls')),
    path('alipay/return/', AlipayView.as_view(), name='alipay'),

    # re_path('static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT}),
    # re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 404和500
handler404 = 'user_operation.views.page_not_found'
handler500 = 'user_operation.views.page_error'
