from django.urls import path
from django.conf.urls import url

from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, SiteView, \
    SiteDetailView, OrderListView, OrderDetailView

app_name = 'users'
urlpatterns = [
    # 个人中心用户信息
    path('info/', UserInfoView.as_view(), name='user_info'),

    # 个人中心用户上传头像
    path('image/upload/', UploadImageView.as_view(), name='image_upload'),

    # 个人中心用户修改密码
    path('update/pwd/', UpdatePwdView.as_view(), name='update_pwd'),

    # 个人中心修改邮箱验证码，发送验证码
    path('sendemail_code/', SendEmailCodeView.as_view(), name='sendemail_code'),

    # 个人中心修改邮箱
    path('update_email/', UpdateEmailView.as_view(), name='update_email'),

    # 个人中心 收货地址
    path('site/list/', SiteView.as_view(), name='site_list'),

    # 个人中心 修改收货地址
    path('site/<int:id>/', SiteDetailView.as_view(), name='site_detail'),

    # 个人中心 订单列表
    path('order/', OrderListView.as_view(), name='user_order'),

    # 个人中心 订单详情
    path('order/<int:order_id>/', OrderDetailView.as_view(), name='order_detail')

]
