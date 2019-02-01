from datetime import datetime

from django.shortcuts import reverse, render, HttpResponse, get_object_or_404, get_list_or_404, redirect
from django.views.generic.base import View
from django.db import transaction

from trade.models import ShoppingCart, OrderInfo, OrderGoods
from goods.models import Goods, GoodsCategory
from tools.alipay import AliPay
from binshop.settings import ali_pub_key_path, private_key_path
from users.models import UserAddress


class AddShoppingCartView(View):
    """ 加入购物车 """

    def post(self, request):
        # 判断用户是否登陆
        if not request.user.is_authenticated:
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')

        # 获取参数，商品id和数量
        good_id = request.POST.get('good_id', '')
        nums = int(request.POST.get('nums', 1))

        # # 检查参数 商品是否存在 nums是否为int
        if not all([good_id, nums]):
            return HttpResponse('{"status": "fail", "msg": "信息有错"}', content_type='application/json')

        good = get_object_or_404(Goods, id=good_id)

        try:
            # 先查是否有这条购物车记录，更新数量
            cart = ShoppingCart.objects.get(user=request.user, goods_id=good_id)
            if request.POST.get('type') == 'update':
                cart.nums = nums
            else:
                cart.nums += nums
            if cart.nums > good.goods_num:
                return HttpResponse('{"status": "fail", "msg": "商品库存不足"}', content_type='application/json')
            cart.save()

        except ShoppingCart.DoesNotExist:
            cart = ShoppingCart()
            cart.user = request.user
            cart.goods = good
            cart.nums = nums
            if cart.nums > good.goods_num:
                return HttpResponse('{"status": "fail", "msg": "商品库存不足"}', content_type='application/json')
            cart.save()

        return HttpResponse('{"status": "success", "msg": "购物车添加成功"}', content_type='application/json')


class ShoppingCartView(View):
    """ 购物车页面和删除购物车记录 """

    def get(self, request):
        """ 购物车页面 """
        user = request.user
        if not user.is_authenticated:
            return redirect('login')

        cart = ShoppingCart.objects.filter(user=user)
        # cart = get_list_or_404(ShoppingCart, user=user)

        total_nums = 0
        total_price = 0

        for cart_ in cart:
            total_nums += cart_.nums
            total_price += cart_.nums * cart_.goods.shop_price

        # 顶部导航栏
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

        return render(request, 'cart.html', {
            'cart': cart,
            'is_active': 'cart',
            'total_nums': total_nums,
            'total_price': total_price,
            'five_categories': five_categories,
            'all_categories': all_categories,
        })

    def post(self, request):
        """ 删除购物车单条记录 感觉可以用delete """
        # 判断用户是否登陆
        user = request.user
        if not user.is_authenticated:
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')

        cart = get_object_or_404(ShoppingCart, user=user, goods_id=request.POST.get('good_id'))
        cart.delete()
        return HttpResponse('{"status": "success", "msg": "删除购物车记录成功"}', content_type='application/json')


class OrderView(View):
    """ post去结算提交订单 订单页 """

    def get(self, request):
        return redirect(reverse('cart'))

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))

        # 获取参数，购物车内商品id
        good_ids = request.POST.getlist('good_ids')

        if len(good_ids) == 0:
            return redirect(reverse('cart'))

        # 顶部导航栏
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

        # 获取收货地址
        default_address = UserAddress.objects.get(is_default=True)
        address = UserAddress.objects.filter(is_default=False)

        goods = []
        total_nums = 0
        total_price = 0

        for good_id in good_ids:
            good = ShoppingCart.objects.get(user=request.user, goods_id=good_id)
            total_nums += good.nums
            total_price += good.nums * good.goods.shop_price
            goods.append(good)

        return render(request, 'order.html', {
            'goods': goods,
            'total_nums': total_nums,
            'total_price': total_price,
            'five_categories': five_categories,
            'all_categories': all_categories,
            'is_active': 'cart',
            'default_address': default_address,
            'address': address
        })


class ImmediatelyCreateOrder(View):
    """ 商品详情页立即创建订单 """

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))

        # 获取参数，商品id 和 购买数量
        good_id = request.POST.get('good_id', '')
        buynum = int(request.POST.get('buynum', 0))
        if not all([good_id, buynum]):
            return redirect(reverse('index'))

        # 顶部导航栏
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

        # 获取收货地址
        default_address = UserAddress.objects.get(is_default=True)
        address = UserAddress.objects.filter(is_default=False)

        goods = []  # 拼接模板里循环的数据
        good = get_object_or_404(Goods, id=good_id)
        good.nums = buynum
        good.goods = {'id': good.id, 'name': good.name, 'goods_front_image': good.goods_front_image,
                      'shop_price': good.shop_price}
        goods.append(good)

        total_nums = buynum
        total_price = buynum * good.shop_price

        return render(request, 'order.html', {
            'goods': goods,
            'total_nums': total_nums,
            'total_price': total_price,
            'five_categories': five_categories,
            'all_categories': all_categories,
            'is_active': 'cart',
            'default_address': default_address,
            'address': address
        })


# 创建订单
class OrderCommitView(View):
    @transaction.atomic
    def post(self, request):
        """ post提交订单 """

        # 接受参数
        user = request.user
        address_id = request.POST.get('params[address_id]')
        address = UserAddress.objects.get(id=address_id, user=user)
        pay_method = request.POST.get('params[pay_method]')
        goods_id = request.POST.getlist('params[goods_id][]')
        post_message = request.POST.get('params[post_message]', '')
        nums = int(request.POST.get('params[nums]', '1'))

        # 参数检验
        if not all([address_id, pay_method, goods_id]):
            return HttpResponse('{"status": "fail", "msg": "参数有错或购物车为空"}', content_type='application/json')

        # 事务保存点
        sid = transaction.savepoint()

        order_info = OrderInfo()
        order_info.user = user
        order_info.signer = address.signer
        order_info.signer_mobile = address.signer_mobile
        order_info.address = address.address

        order_info.order_sn = datetime.now().strftime("%Y%m%d%H%M%S") + str(user.id)
        order_info.pay_method = pay_method
        order_info.post_message = post_message
        order_info.save()

        order_mount = 0  # 总价格
        for good_id in goods_id:
            try:  # 购物车里创建的订单
                cart_good = ShoppingCart.objects.get(goods_id=good_id)
                cart_good_nums = cart_good.nums
            except:  # 这个是 用户立即购买创建的订单
                cart_good_nums = nums

            good = Goods.objects.get(id=good_id)
            if cart_good_nums > good.goods_num:
                # 回滚事务
                transaction.savepoint_rollback(sid)
                return HttpResponse('{"status": "fail", "msg": "商品库存不足"}', content_type='application/json')
            else:
                order_good = OrderGoods()
                order_good.goods = good
                order_good.goods_num = cart_good_nums
                order_good.order = order_info
                order_good.save()

                order_mount += good.shop_price * cart_good_nums
                good.goods_num -= cart_good_nums  # 减少库存
                try:
                    cart_good.delete()
                except:
                    pass
                good.save()

        # 订单信息
        order_info.order_mount = order_mount
        order_info.save()

        return HttpResponse('{"status": "success", "msg": "订单创建成功"}', content_type='application/json')


class AlipayView(View):
    def get(self, request):
        # 处理支付宝的 return_url
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value

        # 将sign pop出来做验证（根据文档）
        sign = processed_dict.pop('sign', None)

        alipay = AliPay(
            appid="2016091400506109",
            app_notify_url="http://119.29.27.194:8005/alipay/return/",  # POST异步请求url
            app_private_key_path=private_key_path,  # 私钥路径
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥路径，验证支付宝回传消息使用，不是你自己的公钥
            debug=True,  # 默认False, True为调用沙箱url
            return_url="http://119.29.27.194:8005/alipay/return/"  # GET同步请求url
        )
        verify_res = alipay.verify(processed_dict, sign)

        if verify_res:  # 验证通过
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            # trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                # 更新订单信息，将支付宝返回的一些信息更新进数据库
                # existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()
            # return Response('success')  # 返回一个success给支付宝

            response = redirect('index')  # 跳转到 vue的首页
            # 设置 cookie, 在vue那接收到后进行下一个url的跳转
            response.set_cookie('nextPath', 'pay', max_age=2)
            return response
        else:
            response = redirect('index')
            return response

    def post(self, request):
        pass
