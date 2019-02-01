import random

from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import get_object_or_404
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Goods, GoodsCategory


class CartView(View):
    def get(self, request):
        return render(request, 'cart.html')


class OrderView(View):
    def get(self, request):
        return render(request, 'order.html')


class GoodDetailView(View):
    """ 商品详情页 """

    def get(self, request, id):
        good = get_object_or_404(Goods, id=id)
        good.click_num += 1
        good.save()

        # 顶部导航栏 全部分类数据
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
        # 顶部导航栏End

        # 新品推荐
        new_goods = Goods.objects.all().order_by('add_time')[:3]

        # 相似商品。这里不会于是才用了，读取当前类别下的商品，随机取三条
        like_goods = []
        category_goods = Goods.objects.filter(Q(category_id=good.category_id)).all()

        s = []
        while len(s) < 3:
            x = random.randint(0, category_goods.__len__()-1)
            if x not in s:
                s.append(x)

        for i in s:
            like_goods.append(category_goods[i])

        return render(request, 'goods/good-detail.html', {
            'good': good,
            'five_categories': five_categories,
            'all_categories': all_categories,
            'new_goods': new_goods,
            'like_goods': like_goods
        })


class GoodsListView(View):
    """ 精选商品列表 """

    def get(self, request):
        # 顶部导航栏 全部分类数据
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

        goods = Goods.objects.all()
        keyword = request.GET.get('keyword', '')
        if keyword:
            goods = goods.filter(Q(name__icontains=keyword) | Q(category__name__icontains=keyword) | Q(
                goods_brief__icontains=keyword) | Q(goods_desc__icontains=keyword))

        sort = request.GET.get('sort', 'add_time')
        if sort not in ['add_time', 'sold_num', 'click_num']:
            sort = 'add_time'

        goods = goods.order_by('-sold_num', '-click_num', '-add_time').order_by('-' + sort)
        hot_goods = goods.order_by('-add_time')[:5]

        try:
            page = request.GET.get('page', 1)
            p = Paginator(goods, 12, request=request)
            goods = p.page(page)
        except (PageNotAnInteger, EmptyPage):
            page = 1
            p = Paginator(goods, 12, request=request)
            goods = p.page(page)

        return render(request, 'goods/hot-goods-list.html', {
            'goods': goods,
            'hot_goods': hot_goods,
            'five_categories': five_categories,
            'all_categories': all_categories,
            'is_acitve': 'hot',
            'sort': sort,
            'keyword': keyword or '',
        })


class CategoryView(View):
    """ 各个分类的列表 """

    def get(self, request, id):
        category = get_object_or_404(GoodsCategory, id=id)

        # 面包屑小导航 二级分类和三级分类Q(parent_category_id=category.parent_category.parent_category_id) |
        # sub_category = GoodsCategory.objects.all().filter(Q(parent_category_id=category.parent_category_id) | Q(parent_category_id=id), category_type=2)
        # sub_sub_category = GoodsCategory.objects.all().filter(Q(parent_category__parent_category_id=id) | Q(parent_category_id=id), category_type=3)

        if category.category_type == 1:
            sub_category = category.sub_cat.all()
            sub_sub_category = GoodsCategory.objects.filter(Q(parent_category__parent_category_id=id), category_type=3)
        elif category.category_type == 2:
            sub_category = GoodsCategory.objects.get(id=category.parent_category_id).sub_cat.all()
            sub_sub_category = category.sub_cat.all()
        elif category.category_type == 3:
            sub_category = GoodsCategory.objects.get(id=category.parent_category.parent_category_id).sub_cat.all()
            sub_sub_category = GoodsCategory.objects.get(id=category.parent_category_id).sub_cat.all()

        # 顶部导航栏 全部分类数据
        categories = GoodsCategory.objects.filter(category_type=1)
        five_categories = categories[:5]
        all_categories = []

        # category一级分类 sub_cats二级分类 sub_sub_cats三级分类
        for cat in categories:
            sub_cats = cat.sub_cat.all()
            all_sub_category = []

            for sub_cat in sub_cats:  # sub_cats 二级类集合
                sub_sub_cats = sub_cat.sub_cat.all()
                all_sub_sub_category = []

                for sub_sub_cat in sub_sub_cats:  # sub_sub_cats 三级类集合
                    all_sub_sub_category.append({'id': sub_sub_cat.id, 'name': sub_sub_cat.name})

                all_sub_category.append({'id': sub_cat.id, 'name': sub_cat.name, 'sub_cat': all_sub_sub_category})

            all_categories.append({'id': cat.id, 'name': cat.name, 'sub_cat': all_sub_category})

        sort = request.GET.get('sort', 'add_time')
        if sort not in ['add_time', 'sold_num', 'click_num']:
            sort = 'add_time'

        # 获取某个大类下的所有商品
        goods = Goods.objects.all().filter(Q(category_id=id) | Q(category__parent_category_id=id) | Q(
            category__parent_category__parent_category_id=id)).order_by('-' + sort)

        # 热门商品
        hot_goods = goods.order_by('-click_num')[:3]

        try:
            page = request.GET.get('page', 1)
            p = Paginator(goods, 12, request=request)
            goods = p.page(page)
        except (PageNotAnInteger, EmptyPage):
            page = 1
            p = Paginator(goods, 12, request=request)
            goods = p.page(page)

        return render(request, 'goods/goods-list.html', {
            'five_categories': five_categories,
            'all_categories': all_categories,
            'goods': goods,
            'hot_goods': hot_goods,
            'sub_category': sub_category,
            'sub_sub_category': sub_sub_category,
            'this_category': category,
            'sort': sort,
        })
