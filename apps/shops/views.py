from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Shops, CityDict


class ShopListView(View):
    """ 店铺列表View """
    def get(self, request):
        shops = Shops.objects.all()
        shops_count = shops.count()
        cities = CityDict.objects.all()

        city_id = request.GET.get('city_id', '')
        if city_id:
            shops = shops.filter(city_id=int(city_id))

        try:
            page = request.GET.get('page', 1)
            p = Paginator(shops, 5, request=request)
            shops = p.page(page)
        except (PageNotAnInteger, EmptyPage):
            page = 1
            p = Paginator(shops, 5, request=request)
            shops = p.page(page)

        return render(request, 'shops/shops-list.html', {
            'shops': shops,
            'shops_count': shops_count,
            'cities': cities,
            'city_id': city_id,
        })

