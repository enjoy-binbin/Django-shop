import hashlib
import json

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect

from .models import UserProfile, EmailVerifyCode, UserAddress
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm, UserInfoForm, UploadImageForm, AddressForm
from goods.models import GoodsCategory, Banner, Goods
from tools.send_email import send_email
from tools.mixin_utils import LoginRequiredMixin
from trade.models import OrderInfo, OrderGoods
from tools.alipay import AliPay
from binshop.settings import private_key_path, ali_pub_key_path


class CustomBackend(ModelBackend):
    """
        settings里配置AUTHENTICATION_BACKENDS
        这里将email和username和nickname都当作username进行Q并起来
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(nickname=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UploadImageView(LoginRequiredMixin, View):
    """ 个人中心 上传头像 """

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()

            # 因为image_form使用了 modelForm，所以这里可以传入一个ins和使用save方法
            image_form.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail"}', content_type='application/json')


class UpdatePwdView(View):
    """ 在个人中心修改密码 """

    def post(self, request):
        update_form = ResetPwdForm(request.POST)
        if update_form.is_valid():
            pwd1 = request.POST.get('password', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status": "fail", "msg": "两次密码不一致" }', content_type='application/json')

            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse('{"status": "success", "msg": "修改密码成功" }', content_type='application/json')
        else:
            return HttpResponse(json.dumps(update_form.errors), content_type='application/json')


class IndexView(View):
    """ 首页的VIew """

    def get(self, request):
        categories = GoodsCategory.objects.filter(category_type=1)
        five_categories = categories[:5]
        all_categories = []

        # category一级分类 sub_cats二级分类 sub_sub_cats三级分类
        for category in categories:
            sub_cats = category.sub_cat.all()
            all_sub_category = []

            for sub_cat in sub_cats:
                sub_sub_cats = sub_cat.sub_cat.all()
                all_sub_sub_category = []

                for sub_sub_cat in sub_sub_cats:
                    all_sub_sub_category.append({'id': sub_sub_cat.id, 'name': sub_sub_cat.name})

                all_sub_category.append({'id': sub_cat.id, 'name': sub_cat.name, 'sub_cat': all_sub_sub_category})

            all_categories.append({'id': category.id, 'name': category.name, 'sub_cat': all_sub_category})

        # 首页轮播的商品
        banners = Banner.objects.all().order_by('index')[:5]

        # 热卖商品
        hot_goods = Goods.objects.all().order_by('-sold_num', '-click_num', '-add_time')[:6]

        # 新品上新
        new_goods = Goods.objects.all().order_by('-add_time')[:10]

        return render(request, 'index.html', {
            # 'categories': categories,
            'five_categories': five_categories,
            'all_categories': all_categories,
            'is_acitve': 'index',
            'banners': banners,
            'hot_goods': hot_goods,
            'new_goods': new_goods
        })


class RegisterView(View):
    """ 用户注册View """

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'users/register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('email', '')
            # 判断邮箱是否存在
            if UserProfile.objects.filter(email=username):
                return render(request, 'users/register.html', {'register_form': register_form, 'msg': '邮箱已存在'})

            # from django.contrib.auth.models import User
            # user = User.object.create_user('bin', 'binloveplay1314@qq.com', 'password')
            # user.save()
            # 创建新用户
            user = UserProfile()
            user.username = username
            user.email = user.username
            user.password = make_password(request.POST.get('password', ''))  # 对密码进行加密
            user.is_active = False  # 新用户是未激活的

            # 发送激活邮件
            if (send_email(username, 'register')):
                user.save()
                return render(request, 'users/login.html', {'msg': '请前往邮箱进行邮箱认证'})

            return render(request, 'users/login.html', {'msg': '激活邮件发送失败'})
        else:
            return render(request, 'users/register.html', {'register_form': register_form})


class LoginView(View):
    """ 用户登陆View """

    def get(self, request):
        return render(request, 'users/login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    return render(request, 'users/login.html', {'login_form': login_form, 'msg': '邮箱未激活'})
            else:
                # TODO: 账号错误 或 密码错误
                return render(request, 'users/login.html', {'login_form': login_form, 'msg': '账号或密码错误'})
        else:
            return render(request, 'users/login.html', {'login_form': login_form})


class LogoutView(View):
    """ 用户登出 """

    def get(self, request):
        logout(request)
        return redirect(reverse('index'))


class ActiveView(View):
    """ 用户激活邮箱 """

    def get(self, request, active_code):
        all_codes = EmailVerifyCode.objects.filter(code=active_code)
        if all_codes:
            for code in all_codes:
                if not code.is_used:
                    email = code.email
                    code.is_used = True
                    code.save()
                    user = UserProfile.objects.get(email=email)
                    user.is_active = True
                    user.save()
                    return render(request, 'users/login.html', {'msg': '激活成功'})
                else:
                    return render(request, 'users/login.html', {'msg': '用户已激活'})
        else:
            return render(request, 'users/register.html', {'msg': '激活连接不合法'})


class ForgetView(View):
    """ 用户忘记密码View """

    def get(self, request):
        forget_pwd_form = ForgetPwdForm()
        return render(request, 'users/forgetpwd.html', {'forget_pwd_form': forget_pwd_form})

    def post(self, request):
        forget_pwd_form = ForgetPwdForm(request.POST)
        if forget_pwd_form.is_valid():
            email = request.POST.get('email', '')
            user = UserProfile.objects.filter(email=email)
            if user:
                if (send_email(email, 'forget')):  # send_email发送成功会返回 1
                    return render(request, 'users/forgetpwd.html', {'msg': '邮件发送成功，请到邮箱确认'})
                else:
                    return render(request, 'users/forgetpwd.html', {'msg': '邮件发送失败，请重试'})
            else:
                return render(request, 'users/forgetpwd.html', {'forget_pwd_form': forget_pwd_form, 'msg': '邮箱不存在'})
        else:
            return render(request, 'users/forgetpwd.html', {'forget_pwd_form': forget_pwd_form})


class ResetView(View):
    """ 重置密码View, 在get中判断链接是否合法 """

    def get(self, request):
        timestamp = request.GET.get('timestamp', '')
        hash_str = request.GET.get('hash', '')
        email = request.GET.get('email', '')

        # if not timestamp or not hash_str or not email:
        if not all([timestamp, hash_str, email]):
            return render(request, 'users/login.html', {'msg': '重置链接不合法-缺少参数'})

        all_codes = EmailVerifyCode.objects.filter(email=email, is_used=False, type='forget').order_by('-add_time')
        if all_codes:
            code_obj = all_codes[0]
            code = code_obj.code
        else:
            return render(request, 'users/login.html', {'msg': '重置链接不合法-无记录'})

        md5 = hashlib.md5()
        md5_str = md5.update((code + email + str(timestamp)).encode('utf8'))
        if hash_str == md5.hexdigest():
            code_obj.is_used = True
            code_obj.save()
            return render(request, 'users/password_reset.html', {'email': email})
        else:
            return render(request, 'users/login.html', {'msg': '重置链接不合法'})

    def post(self, request):
        reset_form = ResetPwdForm(request.POST)
        email = request.POST.get('email', '')
        if reset_form.is_valid():
            password = request.POST.get('password', '')
            password2 = request.POST.get('password2', '')
            if password != password2:
                return render(request, 'users/password_reset.html',
                              {'email': email, 'msg': '两次密码不一致,请重试', 'reset_form': reset_form})
            else:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(password)
                user.save()
                return render(request, 'users/login.html')
        else:
            return render(request, 'users/password_reset.html',
                          {'email': email, 'reset_form': reset_form})


class UserInfoView(LoginRequiredMixin, View):
    """ 用户个人信息 """

    def get(self, request):
        # 个人信息在前台那 request.user.xxx 获取 {{ request.user.email }}
        return render(request, 'users/usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """ 发送邮箱验证码 """

    def get(self, request):
        email = request.GET.get('email', '')
        # 判断邮箱是否存在
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email": "邮箱已被注册"}', content_type='application/json')

        if send_email(email, 'change'):
            return HttpResponse('{"status": "success", "msg": "验证码发送成功"}', content_type='application/json')

        return HttpResponse('{"msg": "验证码发送失败"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """  个人中心修改邮箱 """

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        email_code = EmailVerifyCode.objects.filter(email=email, code=code, type='change', is_used=False)
        if email_code:
            email_code[0].is_used = True
            email_code[0].save()
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"code": "验证码有错"}', content_type='application/json')


class SiteView(LoginRequiredMixin, View):
    """ get方法为收获地址的列表 site/list/, POST方法为收获地址的添加 """

    def get(self, request):
        user = request.user
        address = UserAddress.objects.filter(user=user, is_default=False)
        default_address = UserAddress.objects.filter(is_default=True)
        if default_address:
            default_address = default_address[0]

        return render(request, 'users/usercenter-site.html', {
            "address": address,
            'default_address': default_address
        })

    def post(self, request):
        address_form = AddressForm(request.POST)
        default_address = UserAddress.objects.filter(is_default=True)
        if default_address:
            default_address = default_address[0]

        if address_form.is_valid():
            signer = request.POST.get('signer', '')
            address = request.POST.get('address', '')
            signer_mobile = request.POST.get('signer_mobile', '')
            is_default = request.POST.get('is_default', False)

            user_address = UserAddress()
            user_address.signer = signer
            user_address.signer_mobile = signer_mobile
            user_address.address = address
            user_address.is_default = is_default
            user_address.user = request.user
            user_address.save()

            if is_default:
                default_address = user_address
                if default_address:
                    default_address.is_default = False
                    default_address.save()

            address = UserAddress.objects.filter(user=request.user)
            error = '添加成功'
        else:
            error = '全都要填写或手机号填写有误'
            address = ''

        return render(request, 'users/usercenter-site.html', {
            'error': error,
            'address': address,
            'default_address': default_address
        })


class SiteDetailView(LoginRequiredMixin, View):
    """ get方法为单个收获地址的展示，POST方法为单个收货地址的修改 """

    def get(self, request, id):
        address = get_object_or_404(UserAddress, id=id)
        default_address = UserAddress.objects.get(is_default=True)

        return render(request, 'users/usercenter-site-detail.html', {
            "address": address,
            'default_address': default_address
        })

    def post(self, request, id):
        address_form = AddressForm(request.POST)
        address = get_object_or_404(UserAddress, id=id)

        if address_form.is_valid():
            error = ''
            is_delete = request.POST.get('is_delete', False)
            if is_delete and not address.is_default:
                address.delete()
                return redirect('users:site_list')
            else:
                error += '默认地址不允许删除　　　'

            address.signer = request.POST.get('signer', '')
            address.signer_mobile = request.POST.get('signer_mobile', '')
            address.address = request.POST.get('address', '')

            is_default = request.POST.get('is_default', False)
            if is_default:
                default_address = get_object_or_404(UserAddress, is_default=True)
                default_address.is_default = False
                default_address.save()
                address.is_default = True

            address.save()
            error += '修改成功'
        else:
            error = '全都要填写或手机号填写有误'

        return render(request, 'users/usercenter-site-detail.html', {
            "address": address,
            "error": error
        })


class OrderListView(LoginRequiredMixin, View):
    """ 个人中心订单列表 """

    def get(self, request):
        order_info = OrderInfo.objects.filter(user=request.user).order_by('-add_time')
        return render(request, 'users/usercenter-order.html', {
            'order_info': order_info
        })


class OrderDetailView(LoginRequiredMixin, View):
    """ 个人中心订单详情，根据订单id """

    def get(self, request, order_id):
        order_info = get_object_or_404(OrderInfo, id=order_id, user=request.user)

        order_goods = get_list_or_404(OrderGoods, order_id=order_id)

        alipay_url = self.get_AliPay_url(subject=order_info.order_sn, out_trade_no=order_info.order_sn,
                                         total_amount=order_info.order_mount)

        return render(request, 'users/usercenter-order-detail.html', {
            'order_info': order_info,
            'order_goods': order_goods,
            'alipay_url': alipay_url
        })

    def get_AliPay_url(self, subject, out_trade_no, total_amount):
        alipay = AliPay(
            appid="2016091400506109",
            app_notify_url="http://119.29.27.194:8005/alipay/return/",  # POST异步请求url
            app_private_key_path=private_key_path,  # 私钥
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
            debug=True,  # 默认False, True为调用沙箱url, False为生产环境
            return_url="http://119.29.27.194:8005/alipay/return/"  # GET同步请求url
        )

        url = alipay.direct_pay(
            subject=subject,  # 订单标题
            out_trade_no=out_trade_no,  # 自己创建的不重复的订单号，测试时需要修改
            total_amount=total_amount,  # 价格总计
            return_url="http://119.29.27.194:8005/alipay/return/"  # GET同步url
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url


# step one， step two上面都是基于类的用法
def login_1(request):
    """ 基于函数的用法 """
    if request.method == 'GET':
        return render(request, 'users/login.html', {})
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'index.html', {})
        else:
            return render(request, 'users/login.html', {'msg': '用户名或密码错误', 'username': username, 'password': password})
